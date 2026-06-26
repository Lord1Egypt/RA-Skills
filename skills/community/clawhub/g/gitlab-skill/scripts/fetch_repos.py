#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fetch and display GitLab repositories
Uses secure credential loading from environment variables or config files
"""

import subprocess
import json
import sys
import argparse
from pathlib import Path


def load_credentials():
    """Load GitLab credentials using secure credential manager"""
    try:
        from credential_loader import load_credentials
        return load_credentials(allow_prompt=False)
    except ImportError:
        print("Error: credential_loader.py not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading credentials: {e}")
        sys.exit(1)


def fetch_projects(host, token, per_page=100, insecure=False):
    """Fetch projects using curl

    Args:
        host: GitLab host URL
        token: GitLab access token
        per_page: Number of results per page
        insecure: If True, bypass SSL certificate verification

    Returns:
        List of project dictionaries
    """
    cmd = ["curl", "-s", "-H", f"PRIVATE-TOKEN: {token}"]

    if insecure:
        cmd.append("-k")

    cmd.append(f"{host}/api/v4/projects?membership=true&per_page={per_page}"
              f"&order_by=updated_at&sort=desc")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error fetching projects: {result.stderr}")
        sys.exit(1)

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"Error parsing response: {e}")
        sys.exit(1)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Fetch and display GitLab repositories"
    )
    parser.add_argument("--insecure", action="store_true",
                       help="Bypass SSL certificate verification")
    parser.add_argument("--per-page", type=int, default=100,
                       help="Number of results per page (default: 100)")

    args = parser.parse_args()

    # Load credentials securely
    host, token = load_credentials()

    # Fetch and display projects
    print(f"Fetching repositories from {host}...")
    projects = fetch_projects(host, token, per_page=args.per_page, insecure=args.insecure)

    print(f"\n共 {len(projects)} 个仓库:\n")
    print(f"{'名称':<50} {'可见性':<10} {'最后活动时间'}")
    print("-" * 100)

    for p in projects:
        name = p.get("path_with_namespace", p.get("name", "unknown"))
        visibility = p.get("visibility", "unknown")
        last_activity = p.get("last_activity_at", "unknown")[:10]
        print(f"{name:<50} {visibility:<10} {last_activity}")


if __name__ == "__main__":
    main()
