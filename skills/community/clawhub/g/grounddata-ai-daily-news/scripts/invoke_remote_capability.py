#!/usr/bin/env python3
"""
invoke_remote_capability.py — Invoke a remote capability

Usage:
    python invoke_remote_capability.py <capability_name> [--param key=value ...]
    python invoke_remote_capability.py <capability_name> --params-json '{"key": "value"}'

Examples:
    python invoke_remote_capability.py download_original --param article_id=202605100000
    python invoke_remote_capability.py analyze_trends --params-json '{"days": 7, "topic": "LLM"}'
"""

import os
import sys
import json
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lib.schemas import NetworkError
from lib.remote_client import invoke_capability
from lib.capabilities import sync_capabilities


def main():
    parser = argparse.ArgumentParser(description="Invoke a remote capability on L2")
    parser.add_argument("capability_name", help="Name of the capability to invoke")
    parser.add_argument("--param", action="append", default=[], help="Parameters as key=value pairs (simple values)")
    parser.add_argument("--params-json", help="Parameters as JSON string (for complex/nested/array params)")
    parser.add_argument("--base-url", default=None, help="L2 API base URL")
    args = parser.parse_args()

    # Parse parameters (priority: --params-json first, then --param)
    params = {}
    if args.params_json:
        try:
            params = json.loads(args.params_json)
        except json.JSONDecodeError as e:
            print(json.dumps({
                "status": "error",
                "message": f"Invalid JSON in --params-json: {e}",
            }, ensure_ascii=False))
            sys.exit(1)
    else:
        # Parse --param key=value into dict
        for kv in args.param:
            if "=" in kv:
                k, v = kv.split("=", 1)
                params[k.strip()] = v.strip()

    api_key = os.getenv("AINEWS_ACCESS_TOKEN")

    manifest = {}
    cap_meta = None

    try:
        # First sync to get capability metadata
        manifest = sync_capabilities(base_url=args.base_url)
        remote_caps = manifest.get("remote_capabilities", [])
        cap_meta = next((c for c in remote_caps if c.get("name") == args.capability_name), None)

        # Validate capability exists
        if not cap_meta:
            print(json.dumps({
                "status": "error",
                "message": f"Unknown capability: {args.capability_name}",
                "hint": "Call sync_capabilities first to discover available capabilities.",
            }, ensure_ascii=False))
            sys.exit(1)

        # Validate tier/require_token (use manifest info)
        if cap_meta.get("requires_token") and not api_key:
            upgrade = manifest.get("upgrade", {})
            print(json.dumps({
                "status": "error",
                "message": f"This capability requires an access token.",
                "hint": cap_meta.get("upgrade_hint", f"Set {upgrade.get('token_env', 'AINEWS_ACCESS_TOKEN')}."),
                "upgrade_url": upgrade.get("url", ""),
            }, ensure_ascii=False))
            sys.exit(1)

        # Validate required params if schema available
        input_schema = cap_meta.get("input_schema")
        if input_schema and isinstance(input_schema, dict):
            required_params = input_schema.get("required", [])
            for p in required_params:
                if p not in params:
                    print(json.dumps({
                        "status": "error",
                        "message": f"Missing required parameter: {p}",
                        "capability": cap_meta,
                    }, ensure_ascii=False))
                    sys.exit(1)

        # Invoke capability
        result = invoke_capability(
            capability_name=args.capability_name,
            params=params,
            base_url=args.base_url,
            api_key=api_key,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))

    except NetworkError as e:
        err_msg = str(e)

        if cap_meta and cap_meta.get("requires_token"):
            upgrade = manifest.get("upgrade", {})
            token_env = upgrade.get("token_env", "AINEWS_ACCESS_TOKEN")
            if (
                "401" in err_msg
                or "403" in err_msg
                or "missing access token" in err_msg.lower()
                or "invalid or missing access token" in err_msg.lower()
                or "not included in your subscription" in err_msg.lower()
            ):
                print(json.dumps({
                    "status": "error",
                    "message": err_msg,
                    "hint": cap_meta.get("upgrade_hint", f"Set {token_env}."),
                    "upgrade_url": upgrade.get("url", ""),
                }, ensure_ascii=False))
                sys.exit(1)

        print(json.dumps({"status": "error", "message": err_msg}, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"status": "error", "message": f"Unexpected error: {e}"}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
