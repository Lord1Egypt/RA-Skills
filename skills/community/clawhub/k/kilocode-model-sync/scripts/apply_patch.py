#!/usr/bin/env python3
"""
apply_patch.py — Apply a kilocode model patch to openclaw.json, then restart gateway.

Usage:
    python3 apply_patch.py <patch_file.patch.json>

Output (stdout): JSON result object
Exit 0: success
Exit 1: error
"""

import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

OPENCLAW_JSON = Path.home() / ".openclaw" / "openclaw.json"
OPENCLAW_BIN  = Path.home() / ".nvm" / "versions" / "node" / "v24.12.0" / "bin" / "openclaw"


def find_openclaw() -> str:
    """Find the openclaw binary."""
    if OPENCLAW_BIN.exists():
        return str(OPENCLAW_BIN)
    # Try PATH
    result = shutil.which("openclaw")
    if result:
        return result
    raise RuntimeError("openclaw binary not found")


def backup_config() -> Path:
    """Create a timestamped backup of openclaw.json."""
    ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    backup = OPENCLAW_JSON.parent / f"openclaw.json.bak.{ts}"
    shutil.copy2(OPENCLAW_JSON, backup)
    return backup


def apply_models_patch(config: dict, new_models: list) -> dict:
    """Replace models.providers.kilocode.models in config dict."""
    if "models" not in config:
        config["models"] = {}
    if "providers" not in config["models"]:
        config["models"]["providers"] = {}
    if "kilocode" not in config["models"]["providers"]:
        config["models"]["providers"]["kilocode"] = {}
    config["models"]["providers"]["kilocode"]["models"] = new_models
    return config


def restart_gateway(openclaw: str) -> dict:
    """Restart the OpenClaw gateway and wait for it to come back up."""
    # Send restart
    result = subprocess.run(
        [openclaw, "gateway", "restart"],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        return {"ok": False, "error": result.stderr.strip() or "restart failed"}

    # Wait for gateway to come back (poll up to 30s)
    for attempt in range(10):
        time.sleep(3)
        probe = subprocess.run(
            [openclaw, "gateway", "status"],
            capture_output=True, text=True, timeout=10
        )
        if probe.returncode == 0 and "RPC probe: ok" in probe.stdout:
            return {"ok": True, "attempts": attempt + 1}

    return {"ok": False, "error": "Gateway did not come back online within 30s"}


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "error": "Usage: apply_patch.py <patch_file>"}))
        sys.exit(1)

    patch_path = Path(sys.argv[1])
    if not patch_path.exists():
        print(json.dumps({"status": "error", "error": f"Patch file not found: {patch_path}"}))
        sys.exit(1)

    # 1. Load patch
    try:
        patch = json.loads(patch_path.read_text())
    except Exception as e:
        print(json.dumps({"status": "error", "error": f"Invalid patch JSON: {e}"}))
        sys.exit(1)

    if patch.get("applied"):
        print(json.dumps({"status": "error", "error": "Patch already applied"}))
        sys.exit(1)

    new_models = patch.get("models")
    if not new_models:
        print(json.dumps({"status": "error", "error": "Patch has no models list"}))
        sys.exit(1)

    # 2. Load openclaw.json
    if not OPENCLAW_JSON.exists():
        print(json.dumps({"status": "error", "error": f"openclaw.json not found: {OPENCLAW_JSON}"}))
        sys.exit(1)

    try:
        config = json.loads(OPENCLAW_JSON.read_text())
    except Exception as e:
        print(json.dumps({"status": "error", "error": f"Failed to parse openclaw.json: {e}"}))
        sys.exit(1)

    # 3. Backup
    backup_path = backup_config()

    # 4. Apply patch
    try:
        updated_config = apply_models_patch(config, new_models)
        OPENCLAW_JSON.write_text(json.dumps(updated_config, indent=2))
    except Exception as e:
        # Restore backup on failure
        shutil.copy2(backup_path, OPENCLAW_JSON)
        print(json.dumps({"status": "error", "error": f"Failed to write config: {e}", "restored": True}))
        sys.exit(1)

    # 5. Mark patch as applied
    patch["applied"] = True
    patch["applied_at"] = datetime.now(timezone.utc).isoformat()
    patch_path.write_text(json.dumps(patch, indent=2))

    # 6. Restart gateway
    try:
        openclaw_bin = find_openclaw()
        restart_result = restart_gateway(openclaw_bin)
    except Exception as e:
        restart_result = {"ok": False, "error": str(e)}

    result = {
        "status":       "ok" if restart_result["ok"] else "applied_restart_failed",
        "backup_path":  str(backup_path),
        "patch_path":   str(patch_path),
        "models_count": len(new_models),
        "gateway":      restart_result,
    }

    print(json.dumps(result, indent=2))
    sys.exit(0 if restart_result["ok"] else 1)


if __name__ == "__main__":
    main()
