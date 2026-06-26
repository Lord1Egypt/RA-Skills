#!/usr/bin/env python3
"""Manage n8n credentials. Subcommands:

  create     — POST /api/v1/credentials with values from .env.<env> (Path A).
  list-link  — GET /api/v1/credentials and link an existing credential into the YAML (Path B).

Path A flow (agent-mediated creation):
  1. Agent appends required secret env-var names to <workspace>/n8n-config/.env.example
     and tells the user to copy those entries into .env.<env> with real values.
  2. Agent runs:
        manage_credentials.py create --env <env> --key <yaml-key> \\
          --type <n8n-credential-type> --name "<display name>" \\
          --env-vars KEY1,KEY2,...
  3. Helper loads .env.<env> via config.py:load_env(), builds the credential `data`
     payload, POSTs to /api/v1/credentials, and writes the returned id+name into
     <workspace>/n8n-config/<env>.yml under credentials.<key>.

Path B flow (user-mediated):
  1. User creates the credential in the n8n UI.
  2. Agent runs:
        manage_credentials.py list-link --env <env> --key <yaml-key> \\
          --type <n8n-credential-type> [--from-name "<existing display name>"]
  3. Helper GETs /credentials, filters by type (and name if --from-name), writes
     the matching id+name into the YAML.

POLICY (encoded here AND in skills/manage-credentials.md):
  - The agent NEVER reads .env* files itself.
  - The agent NEVER collects secrets in chat.
  - This helper is the SOLE code path that loads .env.<env> for credential creation.
"""
import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import yaml

from helpers.workspace import workspace_root
from helpers.config import load_env, load_yaml
from helpers.n8n_client import N8nClient


def _client_for(env_name: str, workspace: Path) -> N8nClient:
    data = load_yaml(env_name, workspace)
    load_env(env_name, workspace)
    api_key = os.environ.get("N8N_API_KEY", "")
    instance = data.get("n8n", {}).get("instanceName", "")
    return N8nClient(base_url=instance, api_key=api_key)


def _save_yaml(yaml_file: Path, data: dict) -> None:
    yaml_file.write_text(yaml.dump(data, default_flow_style=False, sort_keys=False))


def _get_schema(client: N8nClient, cred_type: str) -> dict:
    """Best-effort: GET /credentials/schema/{type}. Returns empty dict on failure."""
    try:
        return client.get(f"credentials/schema/{cred_type}")
    except Exception:
        return {}


def _build_data_payload(env_vars: list[str]) -> dict:
    """Map declared env-var names to their values. The keys in the returned dict
    are the n8n field names — convention: same casing as the env var (e.g. CLIENT_ID
    becomes the field 'CLIENT_ID' OR 'clientId' depending on the cred type schema).
    For simplicity, we pass the env var name as-is and let the schema's `data` shape
    drive the mapping. The agent typically passes camelCased var names.
    """
    data = {}
    for raw in env_vars:
        var = raw.strip()
        if not var:
            continue
        if "=" in var:
            field, _, env_var = var.partition("=")
            data[field.strip()] = os.environ.get(env_var.strip(), "")
        else:
            data[var] = os.environ.get(var, "")
    return data


def cmd_create(args) -> None:
    ws = workspace_root(args.workspace)
    yaml_file = ws / "n8n-config" / f"{args.env}.yml"
    yaml_data = load_yaml(args.env, ws)
    client = _client_for(args.env, ws)

    env_var_names = [v.strip() for v in (args.env_vars or "").split(",") if v.strip()]
    data_payload = _build_data_payload(env_var_names)
    # Detect-by-env-var-presence: a token like `field=ENV_VAR` is "missing" iff
    # ENV_VAR isn't set in os.environ. Avoids false positives on legitimately
    # falsy values (empty string, "0", "false") and reports the env-var name
    # the user needs to set, not the raw `field=ENV_VAR` token.
    missing = []
    for raw in env_var_names:
        env_name = raw.split("=", 1)[1].strip() if "=" in raw else raw.strip()
        if env_name not in os.environ:
            missing.append(env_name)
    if missing:
        print(f"WARNING: missing env vars: {missing}. Add them to .env.{args.env}.", file=sys.stderr)

    body = {
        "name": args.name,
        "type": args.type,
        "data": data_payload,
    }

    if args.dry_run:
        redacted = dict(body)
        redacted["data"] = {k: "[REDACTED]" for k in body["data"]}
        print("[dry-run] would POST /credentials:", json.dumps(redacted, indent=2))
        return

    resp = client.post("credentials", body)
    cred_id = resp.get("id")
    cred_name = resp.get("name", args.name)

    creds = yaml_data.setdefault("credentials", {}) or {}
    creds[args.key] = {"id": cred_id, "name": cred_name, "type": args.type}
    yaml_data["credentials"] = creds
    _save_yaml(yaml_file, yaml_data)
    print(f"Created credential '{cred_name}' (id={cred_id}, type={args.type}) → wrote to {yaml_file} under credentials.{args.key}")


def cmd_list_link(args) -> None:
    ws = workspace_root(args.workspace)
    yaml_file = ws / "n8n-config" / f"{args.env}.yml"
    yaml_data = load_yaml(args.env, ws)
    client = _client_for(args.env, ws)

    try:
        all_creds = client.get("credentials")
        if isinstance(all_creds, dict):
            all_creds = all_creds.get("data", [])
    except Exception as e:
        print(f"ERROR: list /credentials failed: {e}", file=sys.stderr)
        sys.exit(1)

    matches = [c for c in all_creds if c.get("type") == args.type]
    if args.from_name:
        matches = [c for c in matches if c.get("name") == args.from_name]
    if not matches:
        print(f"No credentials match type='{args.type}'" + (f" name='{args.from_name}'" if args.from_name else ""), file=sys.stderr)
        sys.exit(1)
    if len(matches) > 1 and not args.from_name:
        print("Multiple credentials match. Use --from-name to disambiguate:", file=sys.stderr)
        for c in matches:
            print(f"  - id={c.get('id')} name='{c.get('name')}'", file=sys.stderr)
        sys.exit(1)

    chosen = matches[0]
    creds = yaml_data.setdefault("credentials", {}) or {}
    creds[args.key] = {"id": chosen.get("id"), "name": chosen.get("name"), "type": args.type}
    yaml_data["credentials"] = creds
    _save_yaml(yaml_file, yaml_data)
    print(f"Linked credential '{chosen.get('name')}' (id={chosen.get('id')}) → {yaml_file} under credentials.{args.key}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_create = sub.add_parser("create", help="POST /credentials from .env.<env> (Path A)")
    p_create.add_argument("--env", required=True)
    p_create.add_argument("--key", required=True, help="YAML key to write under credentials.<key>")
    p_create.add_argument("--type", required=True, help="n8n credential type (e.g. microsoftOAuth2Api)")
    p_create.add_argument("--name", required=True, help="Display name for the credential")
    p_create.add_argument("--env-vars", default=None, dest="env_vars",
                          help="Comma-separated env-var names that map to credential data fields. "
                               "Use 'fieldName=ENV_VAR' for explicit mapping.")
    p_create.add_argument("--dry-run", action="store_true")

    p_link = sub.add_parser("list-link", help="GET /credentials and link an existing one (Path B)")
    p_link.add_argument("--env", required=True)
    p_link.add_argument("--key", required=True)
    p_link.add_argument("--type", required=True)
    p_link.add_argument("--from-name", default=None, dest="from_name")
    p_link.add_argument("--dry-run", action="store_true")

    args = parser.parse_args()
    if args.cmd == "create":
        cmd_create(args)
    else:
        cmd_list_link(args)


if __name__ == "__main__":
    main()
