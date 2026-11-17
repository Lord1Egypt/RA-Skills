"""Explicit creator approval commands; notices never invoke this module."""

import hashlib
import json
import uuid

from echo_cli.compat import subparsers
from echo_cli.credentials import atomic_json
from echo_cli.user_ids import user_reference


def commands(root):
    group = root.add_parser("access", help="View requests and explicitly authorize work access")
    choices = subparsers(group, dest="access_command")
    for name in ("requests", "grants", "notices"):
        page = choices.add_parser(name)
        if name == "grants":
            page.add_argument("site_id", type=uuid.UUID)
        if name == "requests":
            page.add_argument("--site-id", type=uuid.UUID)
        page.add_argument("--limit", type=int, choices=range(1, 11), default=10)
        page.add_argument("--cursor")
    for name in ("request", "approve", "reject"):
        cmd = choices.add_parser(name)
        cmd.add_argument("id", type=uuid.UUID)
        if name != "request":
            cmd.add_argument("--operation-id", type=uuid.UUID)
    for name in ("grant", "revoke"):
        cmd = choices.add_parser(name)
        cmd.add_argument("site_id", type=uuid.UUID)
        cmd.add_argument("--to", required=True, type=user_reference)
        cmd.add_argument("--operation-id", type=uuid.UUID)
    share = root.add_parser("sharing", help="Set one complete sharing policy")
    share.add_argument("site_id", type=uuid.UUID)
    share.add_argument("value", choices=["public", "link", "password", "approval"])
    share.add_argument("--password-file", type=__import__("pathlib").Path)
    share.add_argument("--revision", type=int, required=True)


def execute(api, args):
    command = args.access_command
    params = {}
    body = None
    method = "GET"
    if command == "requests":
        path = "/v1/hosting/access-requests"
        if args.site_id:
            params["site_id"] = str(args.site_id)
    elif command == "notices":
        path = "/v1/hosting/notices"
    elif command == "grants":
        path = "/v1/hosting/sites/%s/grants" % args.site_id
    elif command == "request":
        path = "/v1/hosting/access-requests/" + str(args.id)
    elif command in ("approve", "reject"):
        path = "/v1/hosting/access-requests/%s/decision" % args.id
        method, body = "POST", {"decision": "approved" if command == "approve" else "rejected"}
    else:
        path = "/v1/hosting/sites/%s/grants/%s" % (args.site_id, args.to)
        method = "PUT" if command == "grant" else "DELETE"
    if command in ("requests", "grants", "notices"):
        params["limit"] = args.limit
        if args.cursor:
            params["cursor"] = args.cursor
    if method == "GET":
        return api.request(method, path, authenticated=True, params=params)
    credential = api.credential()
    fingerprint = hashlib.sha256(
        json.dumps(
            [api.server, credential["agent_id"], method, path, body], sort_keys=True
        ).encode()
    ).hexdigest()
    name = str(args.operation_id) if args.operation_id else fingerprint
    receipt_path = api.store.path.parent / ("access-" + name + ".json")
    with api.store.lock():
        if receipt_path.is_symlink():
            raise RuntimeError("Access receipt must not be a symlink")
        record = json.loads(receipt_path.read_text()) if receipt_path.exists() else None
        if record and record["request_hash"] != fingerprint:
            raise RuntimeError("Keep the original access operation")
        # Completed identical commands are new user actions; unknown outcomes reuse the key.
        if not record or record.get("complete") and not args.operation_id:
            record = {
                "operation_id": str(args.operation_id or uuid.uuid4()),
                "request_hash": fingerprint,
            }
            atomic_json(receipt_path, record)
    result = api.request(
        method,
        path,
        authenticated=True,
        json=body,
        headers={"Idempotency-Key": record["operation_id"]},
    )
    with api.store.lock():
        record["complete"] = True
        atomic_json(receipt_path, record)
    return result
