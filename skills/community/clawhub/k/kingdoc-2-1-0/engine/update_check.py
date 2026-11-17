"""KingDoc 更新检查模块"""
import json
import sys
import argparse
from pathlib import Path
from datetime import datetime

try:
    import requests
except ImportError:
    requests = None

# SkillHub API endpoint for checking updates
SKILLHUB_UPDATE_URL = "https://api.skillhub.cn/api/v1/skills/check_update"
SKILLHUB_SKILL_SLUG = "kingdoc"


def check_update(current_version: str) -> dict:
    """Check if a newer version of KingDoc is available
    
    Returns:
        dict with keys: latest (str), release_note (str), instruction (str), has_update (bool)
    """
    if requests is None:
        return {"error": "requests library not installed", "has_update": False}
    
    try:
        resp = requests.get(
            SKILLHUB_UPDATE_URL,
            params={"slug": SKILLHUB_SKILL_SLUG, "version": current_version},
            timeout=10
        )
        if resp.status_code == 200:
            data = resp.json()
            latest = data.get("latest", current_version)
            has_update = _version_compare(latest, current_version) > 0
            return {
                "latest": latest,
                "release_note": data.get("release_note", ""),
                "instruction": data.get("instruction", ""),
                "has_update": has_update
            }
    except Exception as e:
        return {"error": str(e), "has_update": False}
    
    return {"has_update": False}


def _version_compare(v1: str, v2: str) -> int:
    """Compare two version strings. Returns >0 if v1 > v2, <0 if v1 < v2, 0 if equal."""
    parts1 = [int(x) for x in v1.split(".")]
    parts2 = [int(x) for x in v2.split(".")]
    for a, b in zip(parts1, parts2):
        if a != b:
            return a - b
    return len(parts1) - len(parts2)


def main():
    parser = argparse.ArgumentParser(description="KingDoc Update Checker")
    parser.add_argument("--version", required=True, help="Current version (e.g. 2.1.0)")
    args = parser.parse_args()
    
    print(f"KingDoc Update Checker")
    print(f"Current version: {args.version}")
    print(f"Checking for updates...")
    
    result = check_update(args.version)
    
    if result.get("error"):
        print(f"[WARN] Could not check for updates: {result['error']}")
        sys.exit(0)
    
    if result.get("has_update"):
        print(f"\n🆕 New version available: v{result['latest']}")
        if result.get("release_note"):
            print(f"\nRelease notes:\n{result['release_note']}")
        if result.get("instruction"):
            print(f"\nUpdate instruction:\n{result['instruction']}")
        print(f"\nTo update, run: skillhub install kingdoc --version {result['latest']}")
    else:
        print(f"[OK] You are using the latest version (v{args.version})")
    
    sys.exit(0)


if __name__ == "__main__":
    main()
