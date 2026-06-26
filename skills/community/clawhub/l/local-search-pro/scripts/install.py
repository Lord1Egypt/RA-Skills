#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "searxng"
SETTINGS_FILE = CONFIG_DIR / "settings.yml"


def run(cmd):
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        sys.exit(result.returncode)


def docker_exists():
    return subprocess.call("docker --version > /dev/null 2>&1", shell=True) == 0


def write_settings(dev_mode=False):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    if dev_mode:
        safe_search = 0
        limiter = "false"
        print("⚠ Running in DEV mode (limiter OFF, safe_search OFF)")
    else:
        safe_search = 1
        limiter = "true"
        print("✅ Running in PRODUCTION mode (secure defaults)")

    SETTINGS_FILE.write_text(f"""
use_default_settings: true

server:
  bind_address: 0.0.0.0
  port: 8080
  secret_key: local_search_pro_secure_2026

search:
  safe_search: {safe_search}
  formats:
    - html
    - json

limiter:
  enabled: {limiter}
""")


def main():
    dev_mode = "--dev" in sys.argv

    if not docker_exists():
        print("Docker not found. Please install Docker first.")
        sys.exit(1)

    write_settings(dev_mode)

    run("docker rm -f searxng-local > /dev/null 2>&1 || true")

    run(
        "docker run -d --name searxng-local "
        "-p 127.0.0.1:8080:8080 "
        f"-v {SETTINGS_FILE}:/etc/searxng/settings.yml "
        "--restart unless-stopped "
        "searxng/searxng"
    )

    print("✅ SearXNG deployed on 127.0.0.1:8080")


if __name__ == "__main__":
    main()
