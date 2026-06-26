#!/usr/bin/env python3
"""Manage n8n environment variables. Subcommands:

  list    — GET /api/v1/variables (optionally filtered by --name).
  create  — POST /api/v1/variables with {key, value}.
  update  — PUT /api/v1/variables/{id} with {key, value}.
  delete  — DELETE /api/v1/variables/{id}; requires --force unless dry-listing.

CLI surface uses `--name` (NOT `--key`) for the n8n variable's name. Reason: in
the rest of the harness, `--key` means a YAML config slot under
`credentials.<key>` or `workflows.<key>`. n8n variables are not version-
controlled and have no YAML representation, so we avoid the semantic overload.

The helper translates `--name` into the n8n request body's `key` field at the
HTTP boundary; that's where n8n's REST contract lives.

JSON output to stdout. Mutations warn on stdout that the change is immediate
and not reflected in n8n-config/<env>.yml.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.workspace import workspace_root
from helpers.config import load_env
from helpers.n8n_client import ensure_client


_NOT_VERSIONED_WARNING = (
    "Note: variables are not version-controlled. The change is immediate; "
    "not reflected in n8n-config/<env>.yml."
)


def _list_variables(client) -> list[dict]:
    resp = client.get("variables")
    if isinstance(resp, dict):
        return resp.get("data") or []
    if isinstance(resp, list):
        return resp
    return []


def cmd_list(args, client) -> None:
    rows = _list_variables(client)
    if args.name:
        rows = [r for r in rows if r.get("key") == args.name]
    print(json.dumps(rows, indent=2))


def cmd_create(args, client) -> None:
    if not args.name or args.value is None:
        raise SystemExit("create requires --name and --value")
    body = {"key": args.name, "value": args.value}
    resp = client.post("variables", body)
    print(json.dumps(resp, indent=2))
    print(_NOT_VERSIONED_WARNING)


def cmd_update(args, client) -> None:
    if not args.id or not args.name or args.value is None:
        raise SystemExit("update requires --id, --name, and --value")
    body = {"key": args.name, "value": args.value}
    resp = client.put(f"variables/{args.id}", body)
    print(json.dumps(resp, indent=2))
    print(_NOT_VERSIONED_WARNING)


def cmd_delete(args, client) -> None:
    if not args.id:
        raise SystemExit("delete requires --id")

    if not args.force:
        # Look up the variable so the dry-run message is specific.
        rows = _list_variables(client)
        match = next((r for r in rows if str(r.get("id")) == str(args.id)), None)
        name = match.get("key") if match else "<not found>"
        print(json.dumps({
            "dry_run": True,
            "id": args.id,
            "name": name,
            "message": f"Variable {args.id} ({name}) will be deleted. Rerun with --force to confirm.",
        }, indent=2))
        return

    resp = client.delete(f"variables/{args.id}")
    print(json.dumps(resp, indent=2))
    print(_NOT_VERSIONED_WARNING)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="GET /variables")
    p_list.add_argument("--env", required=True)
    p_list.add_argument("--name", default=None,
                        help="Filter list to a single variable by name (n8n's `key`).")

    p_create = sub.add_parser("create", help="POST /variables")
    p_create.add_argument("--env", required=True)
    p_create.add_argument("--name", required=True,
                          help="The n8n variable's name (sent as `key` in the request body).")
    p_create.add_argument("--value", required=True)

    p_update = sub.add_parser("update", help="PUT /variables/{id}")
    p_update.add_argument("--env", required=True)
    p_update.add_argument("--id", required=True)
    p_update.add_argument("--name", required=True,
                          help="The n8n variable's name (sent as `key` in the request body).")
    p_update.add_argument("--value", required=True)

    p_delete = sub.add_parser("delete", help="DELETE /variables/{id}")
    p_delete.add_argument("--env", required=True)
    p_delete.add_argument("--id", required=True)
    p_delete.add_argument("--force", action="store_true",
                          help="Actually issue DELETE. Without --force, exit 0 with a confirmation prompt message.")

    args = parser.parse_args()

    ws = workspace_root(args.workspace)
    load_env(args.env, ws)
    client = ensure_client(args.env, ws)

    handlers = {
        "list": cmd_list,
        "create": cmd_create,
        "update": cmd_update,
        "delete": cmd_delete,
    }
    # Defaults so every handler can read the same arg namespace.
    if not hasattr(args, "name"):
        args.name = None
    if not hasattr(args, "value"):
        args.value = None
    if not hasattr(args, "id"):
        args.id = None
    if not hasattr(args, "force"):
        args.force = False
    handlers[args.cmd](args, client)


if __name__ == "__main__":
    main()
