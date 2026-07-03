#!/usr/bin/env python3
"""Fetch secrets from Infisical via REST API."""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error


def load_env():
    """Load INFISICAL_CLIENT_ID and INFISICAL_CLIENT_SECRET from ~/.openclaw/.env."""
    env_path = os.path.expanduser("~/.openclaw/.env")
    result = {}
    if os.path.exists(env_path):
        for line in open(env_path):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k in ("INFISICAL_CLIENT_ID", "INFISICAL_CLIENT_SECRET"):
                    result[k] = v
    # env vars override file
    result["INFISICAL_CLIENT_ID"] = os.environ.get("INFISICAL_CLIENT_ID", result.get("INFISICAL_CLIENT_ID", ""))
    result["INFISICAL_CLIENT_SECRET"] = os.environ.get("INFISICAL_CLIENT_SECRET", result.get("INFISICAL_CLIENT_SECRET", ""))
    return result


def login(client_id, client_secret):
    """Authenticate and return access token."""
    url = "https://app.infisical.com/api/v1/auth/universal-auth/login"
    body = json.dumps({"clientId": client_id, "clientSecret": client_secret}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    try:
        resp = json.loads(urllib.request.urlopen(req, timeout=15).read())
        return resp["accessToken"]
    except urllib.error.HTTPError as e:
        err = json.loads(e.read().decode())
        print(f"Login failed: {err.get('message', e)}", file=sys.stderr)
        sys.exit(1)


def list_projects(token):
    """List all accessible projects."""
    url = "https://app.infisical.com/api/v1/workspace"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    data = json.loads(urllib.request.urlopen(req, timeout=15).read())
    return data.get("workspaces", [])


def get_secrets(token, workspace_id, environment, secret_path="/", recursive=False):
    """Fetch secrets from a project/environment."""
    url = f"https://app.infisical.com/api/v3/secrets/raw?workspaceId={workspace_id}&environment={environment}&secretPath={secret_path}"
    if recursive:
        url += "&recursive=true"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        data = json.loads(urllib.request.urlopen(req, timeout=15).read())
        return data.get("secrets", [])
    except urllib.error.HTTPError as e:
        err = json.loads(e.read().decode())
        print(f"Error: {err.get('message', e)}", file=sys.stderr)
        return []


def get_secret(token, workspace_id, environment, secret_name, secret_path="/"):
    """Fetch a single secret by name."""
    url = f"https://app.infisical.com/api/v3/secrets/raw/{secret_name}?workspaceId={workspace_id}&environment={environment}&secretPath={secret_path}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        data = json.loads(urllib.request.urlopen(req, timeout=15).read())
        return data.get("secret", {})
    except urllib.error.HTTPError as e:
        err = json.loads(e.read().decode())
        print(f"Error: {err.get('message', e)}", file=sys.stderr)
        return {}


def mask_value(val, show=8):
    """Mask a secret value for display."""
    if len(val) <= show + 4:
        return val
    return val[:show] + "..." + val[-4:]


def main():
    parser = argparse.ArgumentParser(description="Fetch secrets from Infisical")
    parser.add_argument("--workspace-id", "-w", help="Project workspace ID")
    parser.add_argument("--env", "-e", default="dev", help="Environment slug (dev, prod, etc.)")
    parser.add_argument("--path", "-p", default="/", help="Secret path (default /)")
    parser.add_argument("--key", "-k", help="Get a single secret by key name")
    parser.add_argument("--raw", action="store_true", help="Print raw value (no masking)")
    parser.add_argument("--json", action="store_true", dest="json_out", help="JSON output")
    parser.add_argument("--list-projects", action="store_true", help="List accessible projects")
    args = parser.parse_args()

    creds = load_env()
    if not creds["INFISICAL_CLIENT_ID"] or not creds["INFISICAL_CLIENT_SECRET"]:
        print("Error: Set INFISICAL_CLIENT_ID and INFISICAL_CLIENT_SECRET in ~/.openclaw/.env", file=sys.stderr)
        sys.exit(1)

    token = login(creds["INFISICAL_CLIENT_ID"], creds["INFISICAL_CLIENT_SECRET"])

    if args.list_projects:
        projects = list_projects(token)
        if args.json_out:
            print(json.dumps(projects, indent=2))
        else:
            for p in projects:
                envs = ", ".join(e["slug"] for e in p.get("environments", []))
                print(f"  {p['slug']}  (id: {p['id']}, envs: {envs})")
        return

    if not args.workspace_id:
        print("Error: --workspace-id is required (use --list-projects to find IDs)", file=sys.stderr)
        sys.exit(1)

    if args.key:
        secret = get_secret(token, args.workspace_id, args.env, args.key, args.path)
        if secret:
            if args.raw:
                print(secret.get("secretValue", ""))
            else:
                print(f"{secret.get('secretKey', '')} = {mask_value(secret.get('secretValue', ''))}")
    else:
        secrets = get_secrets(token, args.workspace_id, args.env, args.path)
        if args.json_out:
            print(json.dumps(secrets, indent=2))
        elif secrets:
            for s in secrets:
                val = s.get("secretValue", "")
                if args.raw:
                    print(f"{s['secretKey']}={val}")
                else:
                    print(f"  {s['secretKey']} = {mask_value(val)}")
        else:
            print("  (no secrets found)")


if __name__ == "__main__":
    main()
