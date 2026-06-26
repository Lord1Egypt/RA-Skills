#!/usr/bin/env python3
"""
Update OpenClaw config with selected models.
Usage: python3 update_config.py --primary <id> --enabled <id1,id2,...> --fallbacks <id1,id2,...>
Outputs JSON: {"success": true, "hot_reloaded": true}
"""
import json
import sys
import subprocess
import argparse

def patch_config(patch_obj):
    patch_json = json.dumps(patch_obj)
    result = subprocess.run(
        ["openclaw", "config", "patch", "--stdin"],
        input=patch_json,
        capture_output=True,
        text=True
    )
    return result.returncode == 0, result.stdout + result.stderr

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--primary", required=True, help="Primary model ID")
    parser.add_argument("--enabled", required=True, help="Comma-separated enabled model IDs")
    parser.add_argument("--fallbacks", default="", help="Comma-separated fallback model IDs (ordered)")
    args = parser.parse_args()

    def to_config_id(mid):
        """Ensure ID has openrouter/ prefix for config storage."""
        if not mid: return mid
        if mid.startswith('openrouter/'): return mid
        return 'openrouter/' + mid

    enabled_ids = [to_config_id(x.strip()) for x in args.enabled.split(",") if x.strip()]
    fallback_ids = [to_config_id(x.strip()) for x in args.fallbacks.split(",") if x.strip()]
    primary_id = to_config_id(args.primary)

    # Build models dict (preserve existing, add new)
    models_dict = {}
    for mid in enabled_ids:
        # Keep entry minimal — OpenClaw uses ID as the key
        models_dict[mid] = {}

    patch = {
        "agents": {
            "defaults": {
                "model": {
                    "primary": primary_id,
                    "fallbacks": fallback_ids
                },
                "models": models_dict
            }
        }
    }

    ok, output = patch_config(patch)
    if ok:
        print(json.dumps({
            "success": True,
            "hot_reloaded": True,
            "primary": primary_id,
            "enabled_count": len(enabled_ids),
            "message": "Config updated and hot-reloaded. No restart needed."
        }))
    else:
        print(json.dumps({
            "success": False,
            "hot_reloaded": False,
            "error": output
        }))
        sys.exit(1)

if __name__ == "__main__":
    main()
