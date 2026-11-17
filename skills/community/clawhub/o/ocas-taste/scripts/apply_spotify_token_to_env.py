#!/usr/bin/env python3
"""
Bridge script: after the operator completes the Spotify OAuth Authorization Code
flow (which writes the refresh token to
  commons/data/ocas-taste/music/spotify_token.json
via spotify_auth_helper.py), copy that refresh token into
  ~/.hermes/profiles/indigo/.env
as SPOTIFY_REFRESH_TOKEN, which is exactly what the cron puller
(spotify_history_puller.py, invoked by rr_taste_sync_spotify.sh) reads.

Without this bridge the cron stays DEGRADED even after OAuth, because the
auth helper writes to a file while the puller expects an env var.

Usage:
  python3 apply_spotify_token_to_env.py
"""
import sys
if __name__ == "__main__" and ("--help" in sys.argv or "-h" in sys.argv):
    print('Apply Spotify OAuth token into the environment/env file.')
    print("Usage: apply_spotify_token_to_env.py [options]")
    print("Run with no arguments for default behavior; see SKILL.md for flags.")
    print("  -h, --help  Show this help message")
    sys.exit(0)
import json
import re
import os
import sys
from pathlib import Path

HERMES_HOME = Path(os.environ.get("HERMES_HOME") or os.environ.get("HERMES_HOME", os.path.join(os.path.expanduser("~"), ".hermes", "profiles", "indigo")))
TOKEN_FILE = HERMES_HOME / "commons/data/ocas-taste/music/spotify_token.json"
ENV_FILE = HERMES_HOME / ".env"


def main():
    if not TOKEN_FILE.exists():
        print(f"ERROR: token file not found: {TOKEN_FILE}")
        print("Complete the Spotify OAuth flow first (see spotify_oauth_fix.md).")
        return 1
    try:
        data = json.loads(TOKEN_FILE.read_text())
    except Exception as e:
        print(f"ERROR: could not parse {TOKEN_FILE}: {e}")
        return 1
    rt = data.get("refresh_token")
    if not rt:
        print("ERROR: no refresh_token in token file (authorization may have expired).")
        return 1

    env = ENV_FILE.read_text() if ENV_FILE.exists() else ""
    kept = [l for l in env.splitlines()
            if not re.match(r"^\s*SPOTIFY_REFRESH_TOKEN\s*=", l)]
    kept.append(f"SPOTIFY_REFRESH_TOKEN={rt}")
    ENV_FILE.write_text("\n".join(kept).rstrip("\n") + "\n")
    print(f"OK: wrote SPOTIFY_REFRESH_TOKEN to {ENV_FILE}")
    print("Next: confirm with `hermes cron run e0a126b6c9f7` (or wait for next scheduled run).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
