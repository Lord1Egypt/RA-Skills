#!/usr/bin/env python3
"""A2A Task Listener for OpenClaw - receives tasks routed from the A2A API Gateway.

When a task arrives, it invokes the local OpenClaw instance to produce a real
response instead of returning a mock echo. Invocation method is configurable
via env vars (A2A_OPENCLAW_COMMAND or A2A_OPENCLAW_URL)."""

import json
import os
import shutil
import subprocess
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timezone
from pathlib import Path


def _detect_local_ip() -> str:
    """Auto-detect Tailscale IP or first network interface for local bind."""
    try:
        result = subprocess.run(
            ["tailscale", "ip", "-4"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    try:
        result = subprocess.run(
            ["hostname", "-I"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip().split()[0]
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return "0.0.0.0"


def _detect_slug() -> str:
    """Auto-generate agent slug from hostname."""
    try:
        result = subprocess.run(
            ["hostname", "-s"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip().lower()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return "openclaw"


def _load_conf() -> dict:
    """Load a2a.conf from the skill directory or shared a2a-client directory."""
    conf = {}
    # Check local skill dir first, then shared a2a-client dir
    paths = [
        Path(__file__).parent / "a2a.conf",
        Path(__file__).parent.parent / "a2a-client" / "a2a.conf",
    ]
    for path in paths:
        if path.exists():
            for line in path.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    conf[key] = value
            break  # Use first found
    return conf


# ── Load configuration with priority: env vars > a2a.conf > auto-detected defaults ──

_conf = _load_conf()
_auto_ip = _detect_local_ip()
_auto_slug = _detect_slug()

PORT = int(
    os.environ.get("LISTENER_PORT", "")
    or os.environ.get("PORT", "")
    or _conf.get("LISTENER_PORT", "8100")
)
BIND_ADDR = (
    os.environ.get("BIND_ADDR", "")
    or _conf.get("BIND_ADDR", "")
    or _auto_ip  # Default: auto-detect local IP for binding
)
API_KEY = (
    os.environ.get("A2A_GATEWAY_API_KEY", "")
    or os.environ.get("A2A_API_KEY", "")
    or _conf.get("A2A_GATEWAY_API_KEY", "")
    # If empty: auth checks are disabled (with warning)
)
AGENT_SLUG = (
    os.environ.get("AGENT_SLUG", "")
    or _conf.get("AGENT_SLUG", "")
    or _auto_slug  # Default: auto-detect from hostname
)
AGENT_NAME = (
    os.environ.get("AGENT_NAME", "")
    or _conf.get("AGENT_NAME", "")
    or AGENT_SLUG.capitalize()
)
AGENT_URL = (
    os.environ.get("AGENT_URL", "")
    or _conf.get("AGENT_URL", "")
    or f"http://{BIND_ADDR}:{PORT}"  # Default: construct from bind addr + port
)
AGENT_CAPABILITIES = (
    os.environ.get("AGENT_CAPABILITIES", "")
    or _conf.get("AGENT_CAPABILITIES", "chat,code,research")
)
AGENT_AUTH_TYPE = (
    os.environ.get("AGENT_AUTH_TYPE", "")
    or _conf.get("AGENT_AUTH_TYPE", "bearer")
)

AGENT_CARD = {
    "slug": AGENT_SLUG,
    "name": AGENT_NAME,
    "description": f"{AGENT_NAME} agent instance for A2A task processing",
    "url": AGENT_URL,
    "capabilities": AGENT_CAPABILITIES.split(",") if isinstance(AGENT_CAPABILITIES, str) else AGENT_CAPABILITIES,
    "auth_type": AGENT_AUTH_TYPE,
}


def log(msg: str):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    print(f"[{ts}] {msg}", flush=True)


class A2AHandler(BaseHTTPRequestHandler):
    """HTTP handler for A2A protocol endpoints."""

    def log_message(self, format, *args):
        log(format % args)

    def _send_json(self, code: int, body: dict):
        payload = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _send_error(self, code: int, message: str):
        self._send_json(code, {"error": message})

    def _check_auth(self) -> bool:
        """Validate Bearer token against configured API key."""
        if not API_KEY:
            # No API key configured — allow all requests
            return True
        auth = self.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return False
        token = auth[7:]
        return token == API_KEY

    # ── GET routes ──

    def do_GET(self):
        path = self.path.rstrip("/") if self.path != "/" else self.path

        # Health check
        if path == "/health":
            self._send_json(200, {"status": "ok", "agent": AGENT_SLUG})
            return

        # Agent card by slug
        if path == f"/v1/a2a/agents/{AGENT_SLUG}":
            self._send_json(200, AGENT_CARD)
            return

        # Agent card by any slug (flexible)
        if path.startswith("/v1/a2a/agents/"):
            slug = path.split("/v1/a2a/agents/")[-1]
            if slug:
                card = {**AGENT_CARD, "slug": slug}
                self._send_json(200, card)
                return

        self._send_error(404, "Not found")

    # ── POST routes ──

    def do_POST(self):
        path = self.path.rstrip("/") if self.path != "/" else self.path

        if path == "/v1/a2a/tasks/send":
            self._handle_task_send()
            return

        self._send_error(404, "Not found")

    def _handle_task_send(self):
        """Handle incoming A2A task via POST /v1/a2a/tasks/send."""
        # Auth check
        if not self._check_auth():
            log("AUTH FAILED: invalid or missing Bearer token")
            self._send_error(401, "Unauthorized")
            return

        # Read body
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            self._send_error(400, "Missing request body")
            return

        raw = self.rfile.read(content_length)
        try:
            task = json.loads(raw)
        except json.JSONDecodeError as e:
            self._send_error(400, f"Invalid JSON: {e}")
            return

        # Extract task details
        task_id = task.get("id", "unknown")
        session_id = task.get("sessionId", "unknown")
        message_obj = task.get("message", {})
        content = message_obj.get("content", "")
        role = message_obj.get("role", "user")
        metadata = task.get("metadata", {})

        log(f"TASK RECEIVED: id={task_id} session={session_id} role={role} content={content[:200]}")
        if metadata:
            log(f"  metadata: {json.dumps(metadata)[:300]}")

        # Invoke OpenClaw to get a real response
        result_text, result_status = self._invoke_openclaw(task_id, session_id, content)

        # Build A2A SendTaskResponse
        response = {
            "id": task_id,
            "status": result_status,
            "result": {
                "kind": "text",
                "content": result_text,
            },
        }

        self._send_json(200 if result_status == "completed" else 500, response)
        log(f"TASK {result_status.upper()}: id={task_id}")

    def _invoke_openclaw(self, task_id: str, session_id: str, content: str) -> tuple:
        """Invoke OpenClaw to process the incoming message.

        Returns (response_text, status) where status is 'completed' or 'failed'.

        Invocation priority:
          1. A2A_OPENCLAW_COMMAND — shell command template (use {message} placeholder)
          2. A2A_OPENCLAW_URL — HTTP API URL (POST with JSON body)
          3. Auto-detect: use 'openclaw agent' CLI if available
          4. Error: no invocation method configured
        """
        openclaw_cmd = (
            os.environ.get("A2A_OPENCLAW_COMMAND", "")
            or _conf.get("A2A_OPENCLAW_COMMAND", "")
        )
        openclaw_url = (
            os.environ.get("A2A_OPENCLAW_URL", "")
            or _conf.get("A2A_OPENCLAW_URL", "")
        )
        timeout_secs = int(
            os.environ.get("A2A_OPENCLAW_TIMEOUT", "")
            or _conf.get("A2A_OPENCLAW_TIMEOUT", "60")
        )

        # ── Method 1: Custom command ──
        if openclaw_cmd:
            return self._invoke_via_command(openclaw_cmd, task_id, session_id, content, timeout_secs)

        # ── Method 2: HTTP URL ──
        if openclaw_url:
            return self._invoke_via_url(openclaw_url, task_id, session_id, content, timeout_secs)

        # ── Method 3: Auto-detect 'openclaw agent' CLI ──
        openclaw_bin = shutil.which("openclaw")
        if openclaw_bin:
            return self._invoke_via_openclaw_cli(openclaw_bin, task_id, session_id, content, timeout_secs)

        # ── No method available ──
        err = (
            "No OpenClaw invocation method configured. "
            "Set A2A_OPENCLAW_COMMAND (shell command template), "
            "A2A_OPENCLAW_URL (HTTP API URL), or ensure 'openclaw' CLI is on PATH. "
            "See a2a-server SKILL.md for details."
        )
        log(f"INVOCATION ERROR: {err}")
        return (err, "failed")

    def _invoke_via_command(self, cmd_template: str, task_id: str, session_id: str, content: str, timeout_secs: int) -> tuple:
        """Run a custom shell command with {message} and {session_id} placeholders."""
        cmd = cmd_template.replace("{message}", content.replace('"', '\\"'))
        cmd = cmd.replace("{session_id}", session_id.replace('"', '\\"'))
        log(f"INVOKING COMMAND: {cmd[:300]}")
        try:
            result = subprocess.run(
                cmd, shell=True, capture_output=True, text=True, timeout=timeout_secs
            )
            if result.returncode != 0:
                err = result.stderr.strip() or f"Command exited with code {result.returncode}"
                log(f"COMMAND FAILED: {err[:500]}")
                return (err, "failed")
            output = result.stdout.strip()
            # Try to parse as JSON (openclaw agent --json returns JSON)
            try:
                parsed = json.loads(output)
                text = self._extract_text_from_openclaw_json(parsed)
                if text:
                    return (text, "completed")
            except json.JSONDecodeError:
                pass
            return (output, "completed")
        except subprocess.TimeoutExpired:
            err = f"OpenClaw command timed out after {timeout_secs}s"
            log(f"COMMAND TIMEOUT: {err}")
            return (err, "failed")
        except Exception as e:
            err = f"Command execution error: {e}"
            log(f"COMMAND ERROR: {err}")
            return (err, "failed")

    def _invoke_via_url(self, url: str, task_id: str, session_id: str, content: str, timeout_secs: int) -> tuple:
        """POST the message to an HTTP API endpoint."""
        import urllib.request
        import urllib.error

        payload = json.dumps({
            "id": task_id,
            "sessionId": session_id,
            "message": {"role": "user", "content": content},
        }).encode()
        log(f"INVOKING URL: POST {url}")
        try:
            req = urllib.request.Request(
                url, data=payload, headers={"Content-Type": "application/json"}
            )
            # Forward any configured API key
            url_api_key = (
                os.environ.get("A2A_OPENCLAW_URL_API_KEY", "")
                or _conf.get("A2A_OPENCLAW_URL_API_KEY", "")
            )
            if url_api_key:
                req.add_header("Authorization", f"Bearer {url_api_key}")
            with urllib.request.urlopen(req, timeout=timeout_secs) as resp:
                body = resp.read().decode()
                try:
                    parsed = json.loads(body)
                    text = self._extract_text_from_openclaw_json(parsed)
                    if text:
                        return (text, "completed")
                    # Fallback: return raw body
                    return (body.strip(), "completed")
                except json.JSONDecodeError:
                    return (body.strip(), "completed")
        except urllib.error.HTTPError as e:
            err_body = e.read().decode()[:500] if e.fp else ""
            err = f"HTTP {e.code}: {err_body}"
            log(f"URL ERROR: {err}")
            return (err, "failed")
        except urllib.error.URLError as e:
            err = f"URL error: {e.reason}"
            log(f"URL ERROR: {err}")
            return (err, "failed")
        except Exception as e:
            err = f"URL request error: {e}"
            log(f"URL ERROR: {err}")
            return (err, "failed")

    def _invoke_via_openclaw_cli(self, openclaw_bin: str, task_id: str, session_id: str, content: str, timeout_secs: int) -> tuple:
        """Invoke OpenClaw via the 'agent' subcommand with --json output."""
        # Use session_id for continuity, or generate one from task_id
        safe_session = session_id if session_id != "unknown" else f"a2a-{task_id}"
        cmd = [
            openclaw_bin, "agent",
            "-m", content,
            "--session-id", safe_session,
            "--json",
        ]
        log(f"INVOKING OPENCLAW CLI: {' '.join(cmd[:6])}")
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout_secs
            )
            if result.returncode != 0:
                err = result.stderr.strip() or f"openclaw agent exited with code {result.returncode}"
                # CLI sometimes puts real errors in stdout with returncode 1
                if not err and result.stdout.strip():
                    err = result.stdout.strip()[:500]
                log(f"OPENCLAW CLI FAILED: {err[:500]}")
                return (err, "failed")
            output = result.stdout.strip()
            if not output:
                return ("(empty response from OpenClaw)", "completed")
            # Parse JSON output
            try:
                parsed = json.loads(output)
                text = self._extract_text_from_openclaw_json(parsed)
                return (text or output, "completed")
            except json.JSONDecodeError:
                # Not JSON — return raw text
                return (output, "completed")
        except subprocess.TimeoutExpired:
            err = f"OpenClaw agent timed out after {timeout_secs}s"
            log(f"OPENCLAW CLI TIMEOUT: {err}")
            return (err, "failed")
        except Exception as e:
            err = f"OpenClaw CLI execution error: {e}"
            log(f"OPENCLAW CLI ERROR: {err}")
            return (err, "failed")

    @staticmethod
    def _extract_text_from_openclaw_json(data: dict) -> str:
        """Extract the text response from OpenClaw JSON output.

        Handles the format produced by 'openclaw agent --json':
          result.payloads[0].text
        """
        try:
            payloads = data.get("result", {}).get("payloads", [])
            if payloads and isinstance(payloads, list):
                texts = []
                for p in payloads:
                    t = p.get("text", "")
                    if t:
                        texts.append(t)
                if texts:
                    return "\n".join(texts)
        except (AttributeError, TypeError, IndexError):
            pass

        # Fallback: look for content/message at top level
        for key in ("content", "message", "text", "response"):
            val = data.get(key, "")
            if isinstance(val, str) and val.strip():
                return val.strip()

        return ""


def main():
    server = HTTPServer((BIND_ADDR, PORT), A2AHandler)
    log(f"A2A Listener starting on {BIND_ADDR}:{PORT} (agent={AGENT_SLUG})")
    if not API_KEY:
        log("⚠ No API key configured — auth checks disabled (set A2A_GATEWAY_API_KEY)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log("Shutting down...")
        server.server_close()
        sys.exit(0)


if __name__ == "__main__":
    main()
