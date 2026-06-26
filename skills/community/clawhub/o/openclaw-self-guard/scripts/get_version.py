#!/usr/bin/env python3
"""
OpenClaw Self Guard - Get Local Version
Detects the installed OpenClaw version
"""

import subprocess
import json
import re
import sys
import os

def get_openclaw_version():
    """Get the installed OpenClaw version"""
    try:
        # Try openclaw --version
        result = subprocess.run(
            ["openclaw", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            # Extract version number
            match = re.search(r'(\d+\.\d+(?:\.\d+)?)', version)
            if match:
                return match.group(1), version
    except Exception:
        pass
    
    # Try reading from package.json
    try:
        paths = [
            "/home/raspi/.npm-global/lib/node_modules/openclaw/package.json",
            "/usr/local/lib/node_modules/openclaw/package.json",
            os.path.expanduser("~/.npm-global/lib/node_modules/openclaw/package.json")
        ]
        for path in paths:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    data = json.load(f)
                    version = data.get('version', 'unknown')
                    return version, f"OpenClaw v{version}"
    except Exception:
        pass
    
    return None, "Could not detect version"


def get_version_info():
    """Get all version info as JSON"""
    version, display = get_openclaw_version()
    return {
        "version": version,
        "display": display,
        "success": version is not None
    }


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        print(json.dumps(get_version_info()))
    else:
        version, display = get_openclaw_version()
        if version:
            print(f"OpenClaw version: {display}")
        else:
            print("Could not detect OpenClaw version")
            sys.exit(1)
