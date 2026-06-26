#!/usr/bin/env python3
"""
lsp_client.py — Persistent LSP client for OpenClaw agent.

Supports two modes:
  1. Daemon mode (recommended): start once, query many times via HTTP
     python3 lsp_client.py daemon --lang typescript --root <dir> [--port <n>]
  2. One-shot mode: start server, query, shutdown
     python3 lsp_client.py goto --lang typescript --root <dir> --file <f> --line <n> --col <n>

Usage (one-shot):
  lsp_client.py goto    --lang ts --root <dir> --file <path> --line <n> --col <n>
  lsp_client.py refs    --lang ts --root <dir> --file <path> --line <n> --col <n>
  lsp_client.py hover   --lang ts --root <dir> --file <path> --line <n> --col <n>
  lsp_client.py diag    --lang ts --root <dir> --file <path>
  lsp_client.py symbols --lang ts --root <dir> [--query <text>]

Usage (daemon):
  lsp_client.py daemon --lang ts --root <dir> [--port 9876]
  curl -s http://127.0.0.1:9876/goto    -d '{"file":"src/main.ts","line":10,"col":5}'
  curl -s http://127.0.0.1:9876/refs    -d '{"file":"src/main.ts","line":10,"col":5}'
  curl -s http://127.0.0.1:9876/hover   -d '{"file":"src/main.ts","line":10,"col":5}'
  curl -s http://127.0.0.1:9876/diag    -d '{"file":"src/main.ts"}'
  curl -s http://127.0.0.1:9876/symbols -d '{"query":"UserService"}'
  curl -s http://127.0.0.1:9876/shutdown
  curl -s http://127.0.0.1:9876/ping
"""

import argparse
import json
import os
import subprocess
import sys
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

# LSP SymbolKind enum (for human-readable output)
SYMBOL_KINDS = {
    1: "File", 2: "Module", 3: "Namespace", 4: "Package", 5: "Class",
    6: "Method", 7: "Property", 8: "Field", 9: "Constructor", 10: "Enum",
    11: "Interface", 12: "Function", 13: "Variable", 14: "Constant",
    15: "String", 16: "Number", 17: "Boolean", 18: "Array", 19: "Object",
    20: "Key", 21: "Null", 22: "EnumMember", 23: "Struct", 24: "Event",
    25: "Operator", 26: "TypeParameter",
}

# LSP DiagnosticSeverity
DIAG_SEVERITIES = {1: "ERROR", 2: "WARNING", 3: "INFO", 4: "HINT"}

# Language server configs
SERVERS = {
    "typescript": {
        "cmd": ["typescript-language-server", "--stdio"],
        "filetypes": [".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"],
    },
    "python": {
        "cmd": ["pyright-langserver", "--stdio"],
        "filetypes": [".py"],
    },
}


def file_uri(path: str) -> str:
    return f"file://{os.path.abspath(path)}"


def uri_to_path(uri: str) -> str:
    return uri[7:] if uri.startswith("file://") else uri


class LSPClient:
    """LSP client: supports both one-shot and persistent daemon queries."""

    def __init__(self, server_cmd: list[str], root_uri: str, root_path: str):
        self.server_cmd = server_cmd
        self.root_uri = root_uri
        self.root_path = os.path.abspath(root_path)
        self.process = None
        self.request_id = 0
        self.responses = {}
        self._diagnostics = {}
        self._lock = threading.Lock()        # protects request_id, responses, _diagnostics
        self._send_lock = threading.Lock()    # serializes writes to stdin (LSP not concurrent-safe)
        self._opened_files: set[str] = set()  # track didOpen to avoid duplicates
        self._reader = None
        self._alive = False

    def start(self):
        """Start language server and keep it running (daemon mode)."""
        self.process = subprocess.Popen(
            self.server_cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self._alive = True
        self._reader = threading.Thread(target=self._read_loop, daemon=True)
        self._reader.start()
        # Drain stderr in background for diagnostics
        self._stderr_buf = []
        def drain_stderr():
            while self.process and self.process.poll() is None:
                line = self.process.stderr.readline()  # type: ignore[union-attr]
                if line:
                    self._stderr_buf.append(line.decode(errors="replace").strip())
        threading.Thread(target=drain_stderr, daemon=True).start()
        if not self._initialize():
            err = "; ".join(self._stderr_buf[-5:]) if self._stderr_buf else "no stderr"
            raise RuntimeError(f"Failed to initialize LSP server: {err}")
        return True

    def stop(self):
        """Shutdown language server."""
        self._alive = False
        if self.process:
            try:
                self._send_request_sync("shutdown", {})
                self._send_notification("exit", {})
                self.process.wait(timeout=5)
            except Exception:
                self.process.kill()
            self.process = None

    def is_alive(self) -> bool:
        return self._alive and self.process is not None and self.process.poll() is None

    def run_query(self, query_fn):
        """One-shot: start server, run query, shutdown."""
        try:
            self.process = subprocess.Popen(
                self.server_cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self._alive = True
            self._stderr_buf = []
            reader = threading.Thread(target=self._read_loop, daemon=True)
            reader.start()
            def drain_stderr():
                while self.process and self.process.poll() is None:
                    line = self.process.stderr.readline()  # type: ignore[union-attr]
                    if line:
                        self._stderr_buf.append(line.decode(errors="replace").strip())
            threading.Thread(target=drain_stderr, daemon=True).start()

            if not self._initialize():
                err = "; ".join(self._stderr_buf[-5:]) if self._stderr_buf else "no stderr"
                return {"error": f"Failed to initialize LSP server: {err}"}

            result = query_fn()
            return result
        except ValueError as e:
            return {"error": str(e)}
        finally:
            self.stop()

    # --- Query methods ---

    def query_goto(self, filepath: str, line: int, col: int) -> list[dict]:
        self._open_file(filepath)
        resp = self._send_request_sync("textDocument/definition", {
            "textDocument": {"uri": file_uri(filepath)},
            "position": {"line": line - 1, "character": col},
        })
        if not resp or "result" not in resp:
            return []
        result = resp["result"]
        if isinstance(result, dict):
            result = [result]
        return [{"file": uri_to_path(loc.get("uri", "")), "line": loc["range"]["start"]["line"] + 1,
                 "col": loc["range"]["start"]["character"]} for loc in result]

    def query_refs(self, filepath: str, line: int, col: int) -> list[dict]:
        self._open_file(filepath)
        resp = self._send_request_sync("textDocument/references", {
            "textDocument": {"uri": file_uri(filepath)},
            "position": {"line": line - 1, "character": col},
            "context": {"includeDeclaration": True},
        })
        if not resp or "result" not in resp:
            return []
        return [{"file": uri_to_path(loc.get("uri", "")), "line": loc["range"]["start"]["line"] + 1,
                 "col": loc["range"]["start"]["character"]} for loc in resp["result"]]

    def query_hover(self, filepath: str, line: int, col: int) -> str | None:
        self._open_file(filepath)
        resp = self._send_request_sync("textDocument/hover", {
            "textDocument": {"uri": file_uri(filepath)},
            "position": {"line": line - 1, "character": col},
        })
        if not resp or "result" not in resp or resp["result"] is None:
            return None
        contents = resp["result"].get("contents", {})
        if isinstance(contents, str):
            return contents
        if isinstance(contents, dict):
            return contents.get("value", "")
        if isinstance(contents, list):
            parts = []
            for item in contents:
                if isinstance(item, str):
                    parts.append(item)
                elif isinstance(item, dict):
                    parts.append(item.get("value", ""))
            return "\n".join(parts)
        return None

    def query_diag(self, filepath: str) -> list[dict]:
        self._open_file(filepath)
        uri = file_uri(filepath)
        # Clear stale diagnostics, then wait for fresh publishDiagnostics
        with self._lock:
            self._diagnostics.pop(uri, None)
        deadline = time.time() + 10
        while time.time() < deadline:
            if not self.is_alive():
                return [{"severity": "ERROR", "line": 0, "message": "Language server crashed"}]
            with self._lock:
                if uri in self._diagnostics:
                    diags = self._diagnostics.pop(uri)
                    return [{"severity": DIAG_SEVERITIES.get(d.get("severity", 0), "?"),
                             "line": d["range"]["start"]["line"] + 1,
                             "message": d.get("message", "")} for d in diags]
            time.sleep(0.1)
        return []

    def query_symbols(self, query: str = "") -> list[dict]:
        resp = self._send_request_sync("workspace/symbol", {"query": query})
        if not resp or "result" not in resp:
            return []
        results = []
        for sym in resp["result"]:
            loc = sym.get("location", {})
            kind = sym.get("kind", 0)
            results.append({
                "name": sym.get("name", ""),
                "kind": kind,
                "kind_name": SYMBOL_KINDS.get(kind, f"Unknown({kind})"),
                "file": uri_to_path(loc.get("uri", "")),
                "line": loc.get("range", {}).get("start", {}).get("line", 0) + 1,
                "container": sym.get("containerName", ""),
            })
        return results

    # --- Internal ---

    def _send_request_sync(self, method: str, params: dict, timeout: float = 15.0) -> dict | None:
        req_id = self._send_request(method, params)
        deadline = time.time() + timeout
        while time.time() < deadline:
            if not self.is_alive():
                return None
            with self._lock:
                if req_id in self.responses:
                    return self.responses.pop(req_id)
            time.sleep(0.02)
        return None

    def _next_id(self) -> int:
        with self._lock:
            self.request_id += 1
            return self.request_id

    def _send_message(self, msg: dict):
        body = json.dumps(msg, ensure_ascii=False).encode("utf-8")
        header = f"Content-Length: {len(body)}\r\n\r\n".encode("ascii")
        with self._send_lock:
            if self.process and self.process.stdin:
                try:
                    self.process.stdin.write(header + body)
                    self.process.stdin.flush()
                except BrokenPipeError:
                    self._alive = False

    def _send_request(self, method: str, params: dict) -> int:
        req_id = self._next_id()
        self._send_message({"jsonrpc": "2.0", "id": req_id, "method": method, "params": params})
        return req_id

    def _send_notification(self, method: str, params: dict):
        self._send_message({"jsonrpc": "2.0", "method": method, "params": params})

    def _read_loop(self):
        """Read LSP messages from server stdout using buffered reads."""
        import io
        stdout = self.process.stdout  # type: ignore[assignment]
        buf = b""
        while self._alive and self.process and self.process.poll() is None:
            try:
                # Read one byte at a time to find headers reliably,
                # but batch body reads for efficiency
                # First: read until we have a complete header
                while b"\r\n\r\n" not in buf:
                    ch = stdout.read(1)
                    if not ch:
                        return
                    buf += ch

                # Parse header to get Content-Length
                header_end = buf.find(b"\r\n\r\n")
                header = buf[:header_end].decode("ascii", errors="ignore")
                length = 0
                for line in header.split("\r\n"):
                    if line.startswith("Content-Length:"):
                        length = int(line.split(":")[1].strip())
                        break

                if length == 0:
                    buf = buf[header_end + 4:]
                    continue

                # Read body (may need multiple reads)
                body_start = header_end + 4
                while len(buf) < body_start + length:
                    remaining = body_start + length - len(buf)
                    chunk = stdout.read(min(remaining, 8192))
                    if not chunk:
                        return
                    buf += chunk

                # Extract and parse body
                body = buf[body_start:body_start + length]
                buf = buf[body_start + length:]

                try:
                    msg = json.loads(body.decode("utf-8"))
                    self._handle_message(msg)
                except json.JSONDecodeError:
                    pass
            except Exception:
                continue

    def _parse_message(self, buf: bytes) -> tuple[dict | None, int]:
        """Parse a single LSP message from buffer. Returns (msg, bytes_consumed)."""
        # Find end of header
        header_end = buf.find(b"\r\n\r\n")
        if header_end == -1:
            return None, 0

        header = buf[:header_end].decode("ascii", errors="ignore")
        length = 0
        for line in header.split("\r\n"):
            if line.startswith("Content-Length:"):
                length = int(line.split(":")[1].strip())
                break
        if length == 0:
            # Malformed header, skip past it
            return None, header_end + 4

        body_start = header_end + 4
        body_end = body_start + length
        if len(buf) < body_end:
            return None, 0  # Incomplete body, wait for more data

        body = buf[body_start:body_end]
        try:
            msg = json.loads(body.decode("utf-8"))
            return msg, body_end
        except json.JSONDecodeError:
            return None, body_end

    def _handle_message(self, msg: dict):
        """Route a parsed LSP message to the right handler."""
        if "id" in msg and "method" not in msg:
            with self._lock:
                self.responses[msg["id"]] = msg
        if msg.get("method") == "textDocument/publishDiagnostics":
            with self._lock:
                self._diagnostics[msg["params"]["uri"]] = msg["params"].get("diagnostics", [])

    def _initialize(self) -> bool:
        params = {
            "processId": os.getpid(),
            "rootUri": self.root_uri,
            "capabilities": {
                "textDocument": {
                    "definition": {"dynamicRegistration": False},
                    "references": {"dynamicRegistration": False},
                    "hover": {"dynamicRegistration": False, "contentFormat": ["markdown", "plaintext"]},
                    "publishDiagnostics": {"relatedInformation": True},
                },
                "workspace": {
                    "symbol": {"dynamicRegistration": False},
                },
            },
        }
        resp = self._send_request_sync("initialize", params, timeout=30.0)
        if resp and "result" in resp:
            self._send_notification("initialized", {})
            return True
        return False

    def _open_file(self, filepath: str):
        path = Path(filepath).resolve()
        path_str = str(path)

        # Skip if already opened (daemon mode optimization)
        if path_str in self._opened_files:
            return

        # Security: only open files under project root
        try:
            common = os.path.commonpath([path_str, self.root_path])
            if common != self.root_path:
                raise ValueError(f"File outside project root: {path}")
        except ValueError:
            raise ValueError(f"File outside project root: {path}")

        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            content = ""
        ext = path.suffix.lower()
        lang_id = {".ts": "typescript", ".tsx": "typescript", ".js": "javascript",
                   ".jsx": "javascript", ".py": "python"}.get(ext, "plaintext")
        self._send_notification("textDocument/didOpen", {
            "textDocument": {"uri": file_uri(path_str), "languageId": lang_id, "version": 1, "text": content}
        })
        self._opened_files.add(path_str)


# --- Daemon HTTP Server ---

class DaemonHandler(BaseHTTPRequestHandler):
    """HTTP handler that proxies requests to a persistent LSP server."""

    def log_message(self, format, *args):
        pass  # Suppress HTTP logs

    def _check_auth(self) -> bool:
        """Validate Bearer token if daemon was started with --token."""
        expected = getattr(self.server, "auth_token", None)
        if expected is None:
            return True  # No token required
        header = self.headers.get("Authorization", "")
        if header == f"Bearer {expected}":
            return True
        self._respond({"error": "unauthorized"}, 401)
        return False

    def _read_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        return json.loads(self.rfile.read(length))

    def _respond(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if not self._check_auth():
            return
        if self.path == "/ping":
            client = self.server.lsp_client  # type: ignore
            self._respond({"status": "ok", "alive": client.is_alive()})
        else:
            self._respond({"error": "not found"}, 404)

    def do_POST(self):
        if not self._check_auth():
            return

        client = self.server.lsp_client  # type: ignore

        if not client.is_alive():
            self._respond({"error": "Language server is not running"}, 503)
            return

        try:
            body = self._read_body()
        except Exception:
            self._respond({"error": "invalid JSON body"}, 400)
            return

        try:
            if self.path == "/goto":
                result = client.query_goto(body["file"], body["line"], body["col"])
                self._respond({"result": result})
            elif self.path == "/refs":
                result = client.query_refs(body["file"], body["line"], body["col"])
                self._respond({"result": result})
            elif self.path == "/hover":
                result = client.query_hover(body["file"], body["line"], body["col"])
                self._respond({"result": result})
            elif self.path == "/diag":
                result = client.query_diag(body["file"])
                self._respond({"result": result})
            elif self.path == "/symbols":
                query = body.get("query", "")
                result = client.query_symbols(query)
                self._respond({"result": result})
            elif self.path == "/shutdown":
                self._respond({"status": "shutting down"})
                threading.Thread(target=lambda: (time.sleep(0.5), os._exit(0)), daemon=True).start()
            else:
                self._respond({"error": f"unknown endpoint: {self.path}"}, 404)
        except Exception as e:
            self._respond({"error": str(e)}, 500)


def run_daemon(lang: str, root: str, port: int, token: str | None = None):
    config = SERVERS.get(lang)
    if not config:
        print(f"Unsupported language: {lang}", file=sys.stderr)
        sys.exit(1)

    print(f"Starting {lang} language server for {root}...", file=sys.stderr)
    client = LSPClient(config["cmd"], file_uri(root), root)
    try:
        client.start()
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    server = HTTPServer(("127.0.0.1", port), DaemonHandler)
    server.lsp_client = client  # type: ignore
    server.auth_token = token  # type: ignore
    print(f"LSP daemon ready on http://127.0.0.1:{port}", file=sys.stderr)
    if token:
        print(f"  Auth: Bearer token required", file=sys.stderr)
        print(f'  Example: curl -H "Authorization: Bearer {token}" http://127.0.0.1:{port}/ping', file=sys.stderr)
    print('  POST /goto    -d \'{"file":"...","line":N,"col":N}\'', file=sys.stderr)
    print('  POST /refs    -d \'{"file":"...","line":N,"col":N}\'', file=sys.stderr)
    print('  POST /hover   -d \'{"file":"...","line":N,"col":N}\'', file=sys.stderr)
    print('  POST /diag    -d \'{"file":"..."}\'', file=sys.stderr)
    print('  POST /symbols -d \'{"query":"..."}\'', file=sys.stderr)
    print('  POST /shutdown', file=sys.stderr)
    print('  GET  /ping    (includes alive status)', file=sys.stderr)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        client.stop()
        server.server_close()


# --- One-shot commands ---

def cmd_goto(lang, root, filepath, line, col):
    config = SERVERS.get(lang)
    if not config:
        print(f"Unsupported: {lang}", file=sys.stderr); sys.exit(1)
    client = LSPClient(config["cmd"], file_uri(root), root)
    result = client.run_query(lambda: client.query_goto(filepath, line, col))
    print(json.dumps(result, ensure_ascii=False))


def cmd_refs(lang, root, filepath, line, col):
    config = SERVERS.get(lang)
    if not config:
        print(f"Unsupported: {lang}", file=sys.stderr); sys.exit(1)
    client = LSPClient(config["cmd"], file_uri(root), root)
    result = client.run_query(lambda: client.query_refs(filepath, line, col))
    print(json.dumps(result, ensure_ascii=False))


def cmd_hover(lang, root, filepath, line, col):
    config = SERVERS.get(lang)
    if not config:
        print(f"Unsupported: {lang}", file=sys.stderr); sys.exit(1)
    client = LSPClient(config["cmd"], file_uri(root), root)
    result = client.run_query(lambda: client.query_hover(filepath, line, col))
    print(json.dumps(result, ensure_ascii=False))


def cmd_diag(lang, root, filepath):
    config = SERVERS.get(lang)
    if not config:
        print(f"Unsupported: {lang}", file=sys.stderr); sys.exit(1)
    client = LSPClient(config["cmd"], file_uri(root), root)
    result = client.run_query(lambda: client.query_diag(filepath))
    print(json.dumps(result, ensure_ascii=False))


def cmd_symbols(lang, root, query=""):
    config = SERVERS.get(lang)
    if not config:
        print(f"Unsupported: {lang}", file=sys.stderr); sys.exit(1)
    client = LSPClient(config["cmd"], file_uri(root), root)
    result = client.run_query(lambda: client.query_symbols(query))
    print(json.dumps(result, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="LSP client for OpenClaw agent")
    sub = parser.add_subparsers(dest="command")

    # Shared args for all subcommands
    def add_common(p):
        p.add_argument("--lang", required=True, choices=list(SERVERS.keys()))
        p.add_argument("--root", required=True, help="Project root directory")
        return p

    g = add_common(sub.add_parser("goto"))
    g.add_argument("--file", required=True)
    g.add_argument("--line", required=True, type=int)
    g.add_argument("--col", required=True, type=int)

    r = add_common(sub.add_parser("refs"))
    r.add_argument("--file", required=True)
    r.add_argument("--line", required=True, type=int)
    r.add_argument("--col", required=True, type=int)

    h = add_common(sub.add_parser("hover"))
    h.add_argument("--file", required=True)
    h.add_argument("--line", required=True, type=int)
    h.add_argument("--col", required=True, type=int)

    d = add_common(sub.add_parser("diag"))
    d.add_argument("--file", required=True)

    s = add_common(sub.add_parser("symbols"))
    s.add_argument("--query", default="", help="Symbol name filter (empty = all)")

    dm = add_common(sub.add_parser("daemon"))
    dm.add_argument("--port", type=int, default=9876, help="HTTP port (default: 9876)")
    dm.add_argument("--token", default=None, help="Auth token for Bearer authentication (optional)")

    args = parser.parse_args()

    if args.command == "goto":
        cmd_goto(args.lang, args.root, args.file, args.line, args.col)
    elif args.command == "refs":
        cmd_refs(args.lang, args.root, args.file, args.line, args.col)
    elif args.command == "hover":
        cmd_hover(args.lang, args.root, args.file, args.line, args.col)
    elif args.command == "diag":
        cmd_diag(args.lang, args.root, args.file)
    elif args.command == "symbols":
        cmd_symbols(args.lang, args.root, args.query)
    elif args.command == "daemon":
        run_daemon(args.lang, args.root, args.port, args.token)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
