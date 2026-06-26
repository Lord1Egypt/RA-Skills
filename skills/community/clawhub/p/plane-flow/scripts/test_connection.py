#!/usr/bin/env python3
"""
Minimal connectivity test for the Plane API.

Checks:
1. Environment variables are set
2. Can reach the Plane instance
3. API token is accepted (list_projects succeeds)

Run with:
    python3 scripts/test_connection.py
"""
from __future__ import annotations

import os


def main() -> int:
    print("=== Plane Connection Test ===\n")

    # 1. Check env vars
    required = ["PLANE_BASE_URL", "PLANE_API_TOKEN", "PLANE_WORKSPACE_ID"]
    missing = [v for v in required if not os.getenv(v)]

    if missing:
        print(f"FAIL: missing env vars: {missing}")
        print(
            "\nSet them with:\n"
            "  export PLANE_BASE_URL='https://your-plane.example.com'\n"
            "  export PLANE_API_TOKEN='your_token'\n"
            "  export PLANE_WORKSPACE_ID='your_workspace_id'\n"
        )
        return 1

    print(f"OK  PLANE_BASE_URL = {os.getenv('PLANE_BASE_URL')}")
    print(f"OK  PLANE_WORKSPACE_ID = {os.getenv('PLANE_WORKSPACE_ID')}")
    print(f"OK  PLANE_API_TOKEN is set\n")

    # 2. Try importing and listing projects
    try:
        try:
            from .client import PlaneAPIError, PlaneClient
            from .config import load_settings
            from .service import PlaneService
        except ImportError:
            from client import PlaneAPIError, PlaneClient
            from config import load_settings
            from service import PlaneService
    except ImportError as e:
        print(f"FAIL: cannot import module: {e}")
        return 1

    try:
        settings = load_settings()
        client = PlaneClient(
            base_url=settings.base_url,
            api_token=settings.api_token,
            workspace_id=settings.workspace_id,
        )
        service = PlaneService(client=client, settings=settings)
    except Exception as e:
        print(f"FAIL: config / client init error: {e}")
        return 1

    print("OK  Client initialised\n")

    # 3. Ping the API
    try:
        projects = service.list_projects()
        print(f"OK  list_projects returned {len(projects)} project(s)\n")

        if projects:
            print("Projects found:")
            for p in projects:
                print(
                    f"  - {p.get('name')} "
                    f"(id={p.get('id')}, identifier={p.get('identifier')})"
                )
        else:
            print("  (no projects returned – workspace may be empty)")

        print()
        return 0

    except Exception as e:
        print(f"FAIL: API call failed: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
