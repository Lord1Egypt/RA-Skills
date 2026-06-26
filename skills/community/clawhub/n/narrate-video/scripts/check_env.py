#!/usr/bin/env python3
"""Check that required Azure Speech environment variables are configured.

Only checks existence — never reads or displays key values.
"""

import os

ENV_FILE = os.path.expanduser("~/.narrate_video.env")
REQUIRED_VARS = ["AZURE_SPEECH_KEY", "AZURE_SPEECH_REGION"]


def check_env():
    found = {}
    if os.path.isfile(ENV_FILE):
        with open(ENV_FILE) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    name = line.split("=", 1)[0].strip()
                    value = line.split("=", 1)[1].strip()
                    if name in REQUIRED_VARS and value:
                        found[name] = True
    else:
        print(f"MISSING: {ENV_FILE} not found")
        print(f"  Create it with:")
        print(f"  AZURE_SPEECH_KEY=your-key-here")
        print(f"  AZURE_SPEECH_REGION=your-region-here")
        return False

    ok = True
    for var in REQUIRED_VARS:
        if var in found:
            print(f"OK: {var} is set")
        else:
            print(f"MISSING: {var}")
            ok = False

    if not ok:
        print(f"\n  Add missing vars to {ENV_FILE}")
    return ok


if __name__ == "__main__":
    exit(0 if check_env() else 1)
