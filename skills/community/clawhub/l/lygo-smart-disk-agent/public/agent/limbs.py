"""OpenClaw-shaped limbs for Smart Disk (core subset)."""
from __future__ import annotations

import platform
import shutil
import webbrowser
from pathlib import Path
from typing import Any, Callable


def build_limbs(ctx: dict[str, Any]) -> dict[str, Callable[..., dict[str, Any]]]:
    root: Path = ctx["root"]
    ollama = ctx["ollama"]
    cfg = ctx["cfg"]
    seal = ctx["seal"]
    memory = ctx["memory"]

    def help_limb(args: list[str] | None = None) -> dict[str, Any]:
        return {
            "ok": True,
            "limbs": sorted(
                [
                    "help",
                    "status",
                    "health",
                    "chat",
                    "lattice",
                    "memory",
                    "open-url",
                    "army-sentinel",
                ]
            ),
            "note": "LYGO SMART DISK AGENT core limbs (OpenClaw-shaped, LYGO soul)",
        }

    def status_limb(args: list[str] | None = None) -> dict[str, Any]:
        tags = ollama.tags()
        return {
            "ok": True,
            "agent": "LYGO_SMART_DISK_AGENT",
            "root": str(root),
            "platform": platform.platform(),
            "ollama_base": cfg.get("ollama_base"),
            "models_seen": tags,
            "primary": cfg.get("models", {}).get("primary"),
            "seal_policy": (seal.get("policy") or {}),
        }

    def health_limb(args: list[str] | None = None) -> dict[str, Any]:
        tags = ollama.tags()
        primary = cfg.get("models", {}).get("primary", "qwen2.5:3b")
        fallbacks = cfg.get("models", {}).get("fallbacks") or []
        picked = ollama.pick_model(primary, fallbacks)
        free = shutil.disk_usage(str(root)).free
        auth = ctx.get("auth")
        auth_info = auth.public_info() if auth is not None else {
            "password_gate": False,
            "local_token": False,
            "auth_required": False,
        }
        return {
            "ok": True,
            "brain": "warm" if picked else ("cold" if ollama._ping() else "missing"),
            "model": picked,
            "models": tags,
            "disk_free_bytes": free,
            "bind": f"{cfg.get('bind')}:{cfg.get('port')}",
            "password_gate": False,  # not a remote/vendor password wall
            "local_token": bool(auth_info.get("local_token")),
            "auth_required": bool(auth_info.get("auth_required")),
            "firmware_signature": seal.get("signature"),
        }

    def lattice_limb(args: list[str] | None = None) -> dict[str, Any]:
        return {
            "ok": True,
            "lattice": "SDA-LOCAL",
            "p0": "active",
            "p1": "mycelium",
            "ethical_chip_ref": seal.get("ethical_chip_ref"),
            "guardian_ref": seal.get("guardian_ref"),
            "stack_pointer": "I:\\E Drive\\lygo-protocol-stack (optional host)",
            "usb_lineage": seal.get("usb_lineage"),
        }

    def memory_limb(args: list[str] | None = None) -> dict[str, Any]:
        """Local/CLI recall only. HTTP API blocks this limb (see smart_disk_agent handler)."""
        n = 10
        if args and args[0].isdigit():
            n = min(50, int(args[0]))
        # Only metadata-style rows should be present (chat text not stored)
        recent = memory.list_recent(n)
        safe = []
        for row in recent:
            b = dict(row.get("bundle") or {})
            # Defense in depth: never return message/reply text keys if present
            for k in list(b.keys()):
                if k in ("message", "reply", "result") or "content" in k.lower():
                    b.pop(k, None)
            safe.append({"id": row.get("id"), "ts": row.get("ts"), "bundle": b})
        return {"ok": True, "recent": safe, "http_export": False}

    def open_url_limb(args: list[str] | None = None) -> dict[str, Any]:
        """CLI-only host open. Allowlist loopback + documented LYGO public sites."""
        args = args or []
        if not args:
            return {"ok": False, "error": "url_required"}
        url = args[0].strip()
        allowed_prefixes = (
            "http://localhost",
            "https://localhost",
            "http://127.0.0.1",  # loopback literal still allowed at CLI
            "https://deepseekoracle.github.io/",
            "https://github.com/DeepSeekOracle/",
            "https://clawhub.ai/deepseekoracle/",
            "https://excavationpro.ca/",
            "https://huggingface.co/spaces/DeepSeekOracle/",
        )
        if not any(url.startswith(p) for p in allowed_prefixes):
            return {
                "ok": False,
                "error": "url_not_allowlisted",
                "note": "Only localhost / DeepSeekOracle public HTTPS prefixes",
            }
        webbrowser.open(url)
        return {"ok": True, "opened": url}

    def army_limb(args: list[str] | None = None) -> dict[str, Any]:
        return {
            "ok": True,
            "ollama_ping": ollama._ping(),
            "models": ollama.tags(),
            "note": "Full army lives on USB CLAW; SDA reports brain sentinel only",
        }

    def chat_limb(args: list[str] | None = None) -> dict[str, Any]:
        msg = " ".join(args or []).strip()
        if not msg:
            return {"ok": False, "error": "message_required"}
        return ctx["chat_fn"](msg)

    return {
        "help": help_limb,
        "status": status_limb,
        "health": health_limb,
        "lattice": lattice_limb,
        "memory": memory_limb,
        "open-url": open_url_limb,
        "army-sentinel": army_limb,
        "chat": chat_limb,
    }
