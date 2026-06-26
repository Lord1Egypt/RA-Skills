"""Auth dispatcher — per-component auth, no hardcoded Google dependency."""

from __future__ import annotations

import os


def bootstrap_for_component(component_name: str, auth_config: dict) -> dict:
    """Run auth bootstrap for one component based on its auth config.

    Returns {"ok": True} or {"ok": False, "error": "..."}
    """
    kind = auth_config.get("kind", "none")

    if kind == "none":
        return {"ok": True, "kind": "none", "message": "No auth needed"}

    if kind == "google":
        from importlib import import_module
        try:
            mod = import_module(f"glancely.examples.{component_name}.scripts.google_oauth")
            return mod.bootstrap_interactive()
        except ImportError:
            return {
                "ok": False,
                "error": f"google_oauth.py not found for {component_name}"
            }

    if kind == "env":
        env_vars = auth_config.get("required_env", [])
        missing = [v for v in env_vars if not os.environ.get(v)]
        if missing:
            return {
                "ok": False,
                "error": f"Missing env vars: {', '.join(missing)}"
            }
        return {"ok": True, "kind": "env"}

    return {"ok": False, "error": f"Unknown auth kind: {kind}"}
