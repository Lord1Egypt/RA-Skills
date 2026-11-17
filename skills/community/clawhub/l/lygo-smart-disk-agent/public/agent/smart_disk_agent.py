#!/usr/bin/env python3
"""LYGO SMART DISK AGENT — lean supervisor + local portal API."""
from __future__ import annotations

import hashlib
import json
import os
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agent.auth import LocalTokenAuth  # noqa: E402
from agent.limbs import build_limbs  # noqa: E402
from agent.ollama_client import OllamaClient  # noqa: E402
from kernel import P0Gate, P1Memory, P3Consensus, P5Identity  # noqa: E402

SIGNATURE = "Δ9Φ963-LYGO-SMART-DISK-AGENT-v1.1.0"

# HTTP limbs allowed after local token auth
HTTP_LIMBS_OK = frozenset({"help", "status", "health", "lattice", "army-sentinel"})
HTTP_LIMBS_BLOCKED = {
    "open-url": "CLI-only; prevent unauth host browser opens",
    "memory": "CLI-only; chat memory not exported over HTTP",
    "chat": "use POST /api/chat",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


class SmartDiskAgent:
    def __init__(self, root: Path | None = None):
        self.root = root or ROOT
        self.cfg = load_json(self.root / "config" / "smart_disk.json")
        self.seal = load_json(self.root / "firmware" / "seal.json")
        self.seal_hash = hashlib.sha256(
            (self.root / "firmware" / "seal.json").read_bytes()
        ).hexdigest()
        self.auth = LocalTokenAuth(self.root, self.cfg)
        self.gate = P0Gate()
        self.memory = P1Memory(self.root / "data")
        self.consensus = P3Consensus()
        self.identity = P5Identity()
        self.ollama = OllamaClient(self.cfg.get("ollama_base", "http://localhost:11434"))
        self.limbs = build_limbs(
            {
                "root": self.root,
                "ollama": self.ollama,
                "cfg": self.cfg,
                "seal": self.seal,
                "memory": self.memory,
                "chat_fn": self.chat,
                "auth": self.auth,
            }
        )

    def chat(self, message: str) -> dict[str, Any]:
        node = self.identity.create_node("chat", [message[:80]])
        v = self.gate.validate(message)
        if v.get("verdict") == "QUARANTINE":
            return {
                "ok": False,
                "verdict": "QUARANTINE",
                "reason": v.get("reason"),
                "light_code": node["light_code"],
                "reply": "P0 gate quarantined that request.",
            }
        primary = self.cfg.get("models", {}).get("primary", "qwen2.5:3b")
        fallbacks = self.cfg.get("models", {}).get("fallbacks") or []
        model = self.ollama.pick_model(primary, fallbacks)
        if not model:
            out = {
                "ok": False,
                "verdict": v.get("verdict"),
                "light_code": node["light_code"],
                "reply": "Brain cold: no Ollama model found on localhost:11434. Install Ollama and pull qwen2.5:3b or llama3.2:1b.",
                "brain": "missing",
            }
            self.memory.store({"kind": "chat_fail", "ok": False})
            return out
        chat_cfg = self.cfg.get("chat") or {}
        result = self.ollama.chat(
            model,
            chat_cfg.get("system") or "You are LYGO SMART DISK AGENT.",
            message,
            temperature=float(chat_cfg.get("temperature", 0.35)),
            num_predict=int(chat_cfg.get("num_predict", 384)),
        )
        bundle = {
            "kind": "chat",
            "model": model,
            "message_sha256": hashlib.sha256(
                message.encode("utf-8", errors="ignore")
            ).hexdigest()[:16],
            "message_len": len(message),
            "reply_len": len((result.get("reply") or "") if result.get("ok") else ""),
            "ok": bool(result.get("ok")),
            "light_code": node["light_code"],
            "verdict": v.get("verdict"),
            "consensus": self.consensus.achieve({"command": "chat"}),
        }
        mid = self.memory.store(bundle)
        if not result.get("ok"):
            return {
                "ok": False,
                "verdict": v.get("verdict"),
                "light_code": node["light_code"],
                "model": model,
                "reply": f"Ollama error: {result.get('error')}",
                "memory_id": mid,
            }
        return {
            "ok": True,
            "verdict": v.get("verdict"),
            "light_code": node["light_code"],
            "model": model,
            "reply": result.get("reply") or "",
            "memory_id": mid,
            "signature": SIGNATURE,
        }

    def run_limb(self, name: str, args: list[str] | None = None) -> dict[str, Any]:
        args = args or []
        node = self.identity.create_node(name, args)
        v = self.gate.validate(name + " " + " ".join(args))
        if v.get("verdict") == "QUARANTINE":
            return {"ok": False, "verdict": "QUARANTINE", "reason": v.get("reason")}
        fn = self.limbs.get(name)
        if not fn:
            return {"ok": False, "error": "unknown_limb", "limb": name}
        result = fn(args)
        mid = self.memory.store(
            {
                "kind": "limb",
                "limb": name,
                "args_len": len(args),
                "ok": bool((result or {}).get("ok", True)),
                "light_code": node["light_code"],
            }
        )
        result = dict(result)
        result["memory_id"] = mid
        result["light_code"] = node["light_code"]
        result["verdict"] = v.get("verdict")
        return result


def make_handler(agent: SmartDiskAgent):
    portal = agent.root / "portal"

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt: str, *args) -> None:
            pass

        def _send(self, code: int, body: bytes, ctype: str = "application/json") -> None:
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("X-Frame-Options", "DENY")
            self.end_headers()
            self.wfile.write(body)

        def _json(self, code: int, obj: Any) -> None:
            self._send(code, json.dumps(obj, ensure_ascii=False).encode("utf-8"))

        def _authorized(self) -> bool:
            parsed = urlparse(self.path)
            tok = agent.auth.extract(self.headers, parsed.query)
            return agent.auth.ok(tok)

        def _require_auth(self) -> bool:
            """Return True if request may proceed."""
            if not agent.auth.required:
                return True
            if self._authorized():
                return True
            self._json(
                401,
                {
                    "ok": False,
                    "error": "unauthorized",
                    "auth_required": True,
                    "header": agent.auth.header_name,
                    "note": "Local operator token required. See data/.sda_local_token or boot console.",
                },
            )
            return False

        def do_OPTIONS(self) -> None:  # noqa: N802
            self.send_response(204)
            self.end_headers()

        def do_GET(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            path = parsed.path

            if path in ("/", "/index.html"):
                f = portal / "index.html"
                self._send(200, f.read_bytes(), "text/html; charset=utf-8")
                return
            if path.startswith("/static/"):
                f = portal / path[len("/static/") :]
                if f.is_file() and portal in f.resolve().parents:
                    ctype = (
                        "text/css"
                        if f.suffix == ".css"
                        else "application/javascript"
                        if f.suffix == ".js"
                        else "application/octet-stream"
                    )
                    self._send(200, f.read_bytes(), ctype)
                    return

            # Public: health + auth probe (no secrets)
            if path == "/api/health":
                h = agent.run_limb("health")
                h.update(agent.auth.public_info())
                h["seal_sha256"] = agent.seal_hash
                h["signature"] = SIGNATURE
                h["authenticated"] = self._authorized()
                self._json(200, h)
                return
            if path == "/api/auth":
                self._json(
                    200,
                    {
                        **agent.auth.public_info(),
                        "authenticated": self._authorized(),
                        "ok": True,
                    },
                )
                return

            # Protected GETs
            if not self._require_auth():
                return
            if path == "/api/status":
                st = dict(agent.run_limb("status"))
                st.pop("root", None)
                st["root_redacted"] = True
                self._json(200, st)
                return
            if path == "/api/memory":
                self._json(
                    403,
                    {
                        "ok": False,
                        "error": "memory_not_available_over_http",
                        "note": "CLI: python agent/smart_disk_agent.py limb memory",
                    },
                )
                return
            if path == "/api/help":
                self._json(200, agent.run_limb("help"))
                return
            self._json(404, {"error": "not_found", "path": path})

        def do_POST(self) -> None:  # noqa: N802
            path = urlparse(self.path).path
            n = int(self.headers.get("Content-Length") or 0)
            if n < 0 or n > 65536:
                self._json(413, {"error": "body_too_large", "max": 65536})
                return
            raw = self.rfile.read(n) if n else b"{}"
            try:
                data = json.loads(raw.decode("utf-8") or "{}")
            except json.JSONDecodeError:
                self._json(400, {"error": "bad_json"})
                return

            # Auth: header / query, or JSON body token field
            if agent.auth.required:
                tok = agent.auth.extract(self.headers, urlparse(self.path).query)
                if not agent.auth.ok(tok):
                    body_tok = data.get("token") or data.get("sda_token")
                    if not agent.auth.ok(str(body_tok) if body_tok else None):
                        self._json(
                            401,
                            {
                                "ok": False,
                                "error": "unauthorized",
                                "auth_required": True,
                                "header": agent.auth.header_name,
                            },
                        )
                        return

            if path == "/api/chat":
                msg = (data.get("message") or "").strip()
                self._json(200, agent.chat(msg))
                return
            if path == "/api/limb":
                limb = (data.get("limb") or "").strip()
                if limb in HTTP_LIMBS_BLOCKED:
                    self._json(
                        403,
                        {
                            "ok": False,
                            "error": "limb_disabled_over_http",
                            "limb": limb,
                            "note": HTTP_LIMBS_BLOCKED[limb],
                        },
                    )
                    return
                if limb not in HTTP_LIMBS_OK:
                    self._json(403, {"ok": False, "error": "limb_not_allowed", "limb": limb})
                    return
                args = data.get("args") or []
                if not isinstance(args, list):
                    args = [str(args)]
                out = agent.run_limb(limb, [str(a) for a in args])
                if limb == "status" and isinstance(out, dict):
                    out = dict(out)
                    out.pop("root", None)
                    out["root_redacted"] = True
                self._json(200, out)
                return
            self._json(404, {"error": "not_found"})

    return Handler


def serve(open_browser: bool | None = None) -> None:
    agent = SmartDiskAgent()
    bind = str(agent.cfg.get("bind", "localhost")).strip() or "localhost"
    if bind in ("0.0.0.0", "::", "[::]"):
        if os.environ.get("LYGO_SDA_ALLOW_LAN") != "1":
            print("[SDA] refusing non-loopback bind; set LYGO_SDA_ALLOW_LAN=1 to override")
            bind = "localhost"
    port = int(agent.cfg.get("port", 9631))
    httpd = ThreadingHTTPServer((bind, port), make_handler(agent))
    base = f"http://{bind}:{port}/"
    if agent.auth.required and agent.auth.token:
        url = f"{base}?t={agent.auth.token}"
        print(f"[{SIGNATURE}] listening {base}")
        print(f"  Ollama: {agent.cfg.get('ollama_base')}  seal={agent.seal_hash[:16]}…")
        print(f"  Auth: LOCAL TOKEN required (header {agent.auth.header_name})")
        print(f"  Token file: {agent.auth.path}")
        print(f"  Token: {agent.auth.token}")
        print("  (one-shot browser URL includes token; not a cloud password gate)")
    else:
        url = base
        print(f"[{SIGNATURE}] listening {base}")
        print("  Auth: open loopback (auth.required=false)")
    if open_browser is None:
        open_browser = bool(agent.cfg.get("open_browser_on_boot", True))
    if open_browser:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[SDA] stop")
        httpd.shutdown()


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    if not argv or argv[0] in ("serve", "boot"):
        serve()
        return 0
    if argv[0] == "token":
        a = SmartDiskAgent()
        print(a.auth.token or "(auth disabled)")
        return 0
    if argv[0] == "health":
        a = SmartDiskAgent()
        h = a.run_limb("health")
        h.update(a.auth.public_info())
        print(json.dumps(h, indent=2))
        return 0
    if argv[0] == "chat" and len(argv) > 1:
        print(json.dumps(SmartDiskAgent().chat(" ".join(argv[1:])), indent=2))
        return 0
    if argv[0] == "limb" and len(argv) > 1:
        print(json.dumps(SmartDiskAgent().run_limb(argv[1], argv[2:]), indent=2))
        return 0
    print("Usage: smart_disk_agent.py [serve|token|health|chat <msg>|limb <name> ...]")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
