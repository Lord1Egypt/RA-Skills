#!/usr/bin/env python3
import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Apply the recommended OpenClaw gateway config for Tailscale Serve."
    )
    parser.add_argument("--config", required=True, help="Path to openclaw.json")
    parser.add_argument("--ts-hostname", required=True, help="MagicDNS hostname")
    parser.add_argument("--token", required=True, help="Gateway token")
    parser.add_argument("--port", type=int, default=18789, help="Gateway port")
    return parser.parse_args()


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        print(f"[ERROR] Invalid JSON in {path}: {exc}", file=sys.stderr)
        sys.exit(1)
    if not isinstance(data, dict):
        print(f"[ERROR] Top-level JSON in {path} must be an object", file=sys.stderr)
        sys.exit(1)
    return data


def dedupe(items):
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def main() -> int:
    args = parse_args()
    config_path = Path(args.config).expanduser()
    config_path.parent.mkdir(parents=True, exist_ok=True)

    data = load_json(config_path)
    gateway = data.get("gateway")
    if not isinstance(gateway, dict):
        gateway = {}

    control_ui = gateway.get("controlUi")
    if not isinstance(control_ui, dict):
        control_ui = {}

    auth = gateway.get("auth")
    if not isinstance(auth, dict):
        auth = {}

    tailscale = gateway.get("tailscale")
    if not isinstance(tailscale, dict):
        tailscale = {}

    existing_origins = control_ui.get("allowedOrigins", [])
    if not isinstance(existing_origins, list):
        existing_origins = []

    required_origins = [
        f"http://localhost:{args.port}",
        f"http://127.0.0.1:{args.port}",
        f"https://{args.ts_hostname}",
    ]

    control_ui["allowedOrigins"] = dedupe(
        required_origins + [origin for origin in existing_origins if isinstance(origin, str)]
    )

    auth["mode"] = "token"
    auth["token"] = args.token
    auth["allowTailscale"] = True

    tailscale["mode"] = "serve"
    tailscale["resetOnExit"] = False

    gateway["port"] = args.port
    gateway["mode"] = "local"
    gateway["bind"] = "loopback"
    gateway["controlUi"] = control_ui
    gateway["auth"] = auth
    gateway["tailscale"] = tailscale
    data["gateway"] = gateway

    backup_path = None
    if config_path.exists():
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = config_path.with_suffix(config_path.suffix + f".bak.{stamp}")
        shutil.copy2(config_path, backup_path)

    config_path.write_text(json.dumps(data, indent=2) + "\n")

    print(f"[OK] Wrote {config_path}")
    if backup_path:
        print(f"[OK] Backup saved to {backup_path}")
    print(f"[OK] Allowed origin added: https://{args.ts_hostname}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
