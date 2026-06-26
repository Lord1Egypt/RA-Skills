#!/usr/bin/env python3
"""Hemlane MCP server - wraps existing Hemlane scripts."""
import json
import subprocess
import sys
import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("hemlane")

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"

AUTHORIZED_DISCORD_SENDER_SHA256 = "d40800cb299a0988be92536d6ac5a7e99659ec6d9fef7b7779a8fdeb980f8da1"
READ_CAPTURE_ENDPOINTS = {
    "get-properties", "get-tenants", "get-transactions", "get-maintenance",
    "financials-recurring", "financials-transactions",
}
WRITE_CAPTURE_ENDPOINTS = {
    "send-tenant-reply", "submit-referral", "work-order-comment", "maintenance-comment",
}


def _requester_discord_id() -> str | None:
    """Return verified caller id from runtime env, never from tool args."""
    for key in ("OPENCLAW_DISCORD_SENDER_ID", "OPENCLAW_SENDER_ID", "DISCORD_SENDER_ID", "OPENCLAW_AUTHOR_ID", "OPENCLAW_USER_ID"):
        val = os.environ.get(key)
        if val:
            return str(val)
    for key in ("OPENCLAW_INBOUND_META", "OPENCLAW_MESSAGE_META", "OPENCLAW_REQUEST_META", "OPENCLAW_CONTEXT_JSON"):
        raw = os.environ.get(key)
        if not raw:
            continue
        try:
            meta = json.loads(raw)
        except Exception:
            continue
        for field in ("sender_id", "author_id", "user_id", "member_id", "senderId", "authorId", "userId"):
            val = meta.get(field)
            if val:
                return str(val)
    return None


def _deny_write(tool: str) -> dict:
    return {
        "error": "write_blocked",
        "tool": tool,
        "message": "Hemlane write tools require a verified privileged caller. Current runtime caller is not verified, so this fails closed.",
        "read_only_fallback": "Use read-only tools for reads, or have an authorized operator approve the write from Discord.",
    }


def _require_earl(tool: str) -> dict | None:
    caller = _requester_discord_id()
    if caller and __import__("hashlib").sha256(caller.encode()).hexdigest() == AUTHORIZED_DISCORD_SENDER_SHA256:
        return None
    return _deny_write(tool)

def run_script(script_name: str, args: list = None) -> dict:
    """Run a Hemlane script and return the result."""
    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        return {"error": f"Script not found: {script_name}"}
    
    cmd = ["python3", str(script_path)] + (args or [])
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            return {"error": result.stderr, "stdout": result.stdout}
        return {"success": True, "output": result.stdout}
    except subprocess.TimeoutExpired:
        return {"error": "Script timed out"}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def capture_auth(endpoint_kind: str = "get-properties", out_file: str = None) -> dict:
    """Capture Hemlane auth headers from browser CDP session.
    
    Args:
        endpoint_kind: One of get-properties, get-tenants, get-transactions, 
                       get-maintenance, send-tenant-reply, submit-referral,
                       work-order-comment, maintenance-comment
        out_file: Optional file path to save captured headers
    
    Returns:
        dict with targetId, capturedUrl, capturedMethod, headers
    """
    if endpoint_kind in WRITE_CAPTURE_ENDPOINTS:
        denied = _require_earl("capture_auth:" + endpoint_kind)
        if denied:
            return denied
    elif endpoint_kind not in READ_CAPTURE_ENDPOINTS:
        return {"error": "endpoint_kind not allowed", "allowed_read": sorted(READ_CAPTURE_ENDPOINTS), "allowed_write_for_earl_only": sorted(WRITE_CAPTURE_ENDPOINTS)}
    args = ["--endpoint-kind", endpoint_kind]
    if out_file:
        args.extend(["--out-file", out_file])
    return run_script("capture_hemlane_auth_via_cdp.py", args)

@mcp.tool()
def send_tenant_reply(tenant_group_id: str, message: str, auth_file: str) -> dict:
    """Send a tenant reply via Hemlane GraphQL API.
    
    Args:
        tenant_group_id: The tenant group ID to message
        message: The message content
        auth_file: Path to captured auth headers JSON file
    
    Returns:
        dict with success/error status
    """
    denied = _require_earl("send_tenant_reply")
    if denied:
        return denied
    # Auth is supplied to replay_hemlane_graphql.py via env or its own runtime auth handling.
    return run_script("send_hemlane_tenant_reply.py", [
        "--tenant-group-id", tenant_group_id,
        "--body", message
    ])

@mcp.tool()
def submit_referral(first_name: str, last_name: str, email: str, phone: str, 
                     referrer_name: str, referrer_email: str, auth_file: str) -> dict:
    """Submit a referral via Hemlane HubSpot form.
    
    Args:
        first_name: Referral first name
        last_name: Referral last name  
        email: Referral email
        phone: Referral phone
        referrer_name: Name of person making referral
        referrer_email: Email of person making referral
        auth_file: Path to captured auth headers JSON file
    
    Returns:
        dict with success/error status
    """
    denied = _require_earl("submit_referral")
    if denied:
        return denied
    return run_script("submit_hemlane_referral.py", [
        "--first-name", first_name,
        "--last-name", last_name,
        "--email", email,
        "--phone", phone,
        "--referrer-name", referrer_name,
        "--referrer-email", referrer_email
    ])

@mcp.tool()
def post_workorder_comment(work_order_id: str, comment: str, auth_file: str,
                           hidden_from_tenants: bool = False, 
                           hidden_from_owners: bool = False) -> dict:
    """Post a comment on a work order.
    
    Args:
        work_order_id: The work order ID
        comment: The comment content
        auth_file: Path to captured auth headers JSON file
        hidden_from_tenants: Whether to hide from tenants
        hidden_from_owners: Whether to hide from owners
    
    Returns:
        dict with success/error status
    """
    denied = _require_earl("post_workorder_comment")
    if denied:
        return denied
    args = [
        "--workorder-id", work_order_id,
        "--body", comment
    ]
    if hidden_from_tenants:
        args.append("--hide-from-tenants")
    if hidden_from_owners:
        args.append("--hide-from-owners")
    return run_script("post_hemlane_workorder_comment.py", args)

@mcp.tool()
def post_maintenance_comment(request_id: str, comment: str, auth_file: str,
                             hidden_from_tenants: bool = False,
                             hidden_from_owners: bool = False) -> dict:
    """Post a comment on a maintenance request.
    
    Args:
        request_id: The maintenance request ID
        comment: The comment content
        auth_file: Path to captured auth headers JSON file
        hidden_from_tenants: Whether to hide from tenants
        hidden_from_owners: Whether to hide from owners
    
    Returns:
        dict with success/error status
    """
    denied = _require_earl("post_maintenance_comment")
    if denied:
        return denied
    args = [
        "--request-id", request_id,
        "--body", comment
    ]
    if hidden_from_tenants:
        args.append("--hide-from-tenants")
    if hidden_from_owners:
        args.append("--hide-from-owners")
    return run_script("post_hemlane_maintenance_request_comment.py", args)

@mcp.tool()
def extract_rent_roll(property_id: str, auth_file: str) -> dict:
    """Extract rent roll data for a property.
    
    Args:
        property_id: The Hemlane property ID
        auth_file: Path to captured auth headers JSON file
    
    Returns:
        dict with rent roll data
    """
    return run_script("extract_rent_roll.py", [
        "--property-id", property_id,
        "--auth-file", auth_file
    ])

@mcp.tool()
def query_recurring_payment_requests(auth_file: str, search: str = None, property_id: str = None,
                                     property_unit_id: str = None, status: str = "Active",
                                     all_pages: bool = True) -> dict:
    """Query Hemlane recurring rent/payment requests via HAR-derived GraphQL.

    Args:
        auth_file: Path to captured auth headers JSON file
        search: Optional text filter across property/unit/tenant/request fields, e.g. "1518 Dille 1520"
        property_id: Optional Hemlane property ID filter
        property_unit_id: Optional Hemlane property unit ID filter
        status: Recurring request status, defaults to Active
        all_pages: Fetch all pages when true

    Returns:
        dict with count and recurring request summaries
    """
    args = ["--auth-file", auth_file, "--limit", "50"]
    if search:
        args.extend(["--search", search])
    if property_id:
        args.extend(["--property-id", property_id])
    if property_unit_id:
        args.extend(["--property-unit-id", property_unit_id])
    if status is not None:
        args.extend(["--status", status])
    if all_pages:
        args.append("--all-pages")
    result = run_script("query_recurring_payment_requests.py", args)
    if result.get("success"):
        try:
            return json.loads(result.get("output") or "{}")
        except Exception:
            return result
    return result

@mcp.tool()
def query_financials_operation(auth_file: str, operation_name: str, variables_json: str = "{}",
                               page: int = None, limit: int = None, all_pages: bool = False) -> dict:
    """Replay a read-oriented Hemlane Financials GraphQL operation from captured HAR samples.

    Useful operations from the financials HARs include RecurringNextCursorQuery,
    TransactionsNextCursorQuery, PagedFinancialTransactions,
    FinancialsScheduledActionPanelStats, BankTransactionsPageFiltersQuery, and
    GetPlaidSyncItems. Pass variables_json as a JSON object merged into the HAR
    sample variables.
    """
    args = ["--auth-file", auth_file, "--operation-name", operation_name, "--variables-json", variables_json]
    if page is not None:
        args.extend(["--page", str(page)])
    if limit is not None:
        args.extend(["--limit", str(limit)])
    if all_pages:
        args.append("--all-pages")
    result = run_script("query_financials_operation.py", args)
    if result.get("success"):
        try:
            return json.loads(result.get("output") or "{}")
        except Exception:
            return result
    return result

def _json_output(result: dict) -> dict:
    if result.get("success"):
        try:
            return json.loads(result.get("output") or "{}")
        except Exception:
            return result
    return result


@mcp.tool()
def query_catalog_operation(auth_file: str, operation_name: str, variables_json: str = "{}", dry_run: bool = False) -> dict:
    """Replay any read-only Hemlane GraphQL operation from the HAR-derived catalog.

    Args:
        auth_file: Path to captured auth headers JSON file. Can be omitted only when HEMLANE_* env auth is set.
        operation_name: Operation from references/operation-catalog.json, e.g. ODGetContextValues.
        variables_json: JSON object merged into the captured sample variables.
        dry_run: Return redacted request plan without sending it.
    """
    args = ["--operation-name", operation_name, "--variables-json", variables_json]
    if auth_file:
        args.extend(["--auth-file", auth_file])
    if dry_run:
        args.append("--dry-run")
    return _json_output(run_script("query_catalog_operation.py", args))


@mcp.tool()
def get_context_values(auth_file: str, variables_json: str = "{}") -> dict:
    """Get Hemlane owner dashboard context values/properties from ODGetContextValues."""
    return query_catalog_operation(auth_file, "ODGetContextValues", variables_json)


@mcp.tool()
def get_tenant_groups(auth_file: str, variables_json: str = "{}") -> dict:
    """Query tenant groups / leases using ODTenantsAndLeasesTenantGroups."""
    return query_catalog_operation(auth_file, "ODTenantsAndLeasesTenantGroups", variables_json)


@mcp.tool()
def get_maintenance_requests(auth_file: str, variables_json: str = "{}") -> dict:
    """Query maintenance request list using ODMaintenanceRequests."""
    return query_catalog_operation(auth_file, "ODMaintenanceRequests", variables_json)


@mcp.tool()
def get_transactions(auth_file: str, variables_json: str = "{}", page: int = None, limit: int = None, all_pages: bool = False) -> dict:
    """Query financial transactions using the HAR-derived TransactionsNextCursorQuery."""
    args = ["--auth-file", auth_file, "--operation-name", "TransactionsNextCursorQuery", "--variables-json", variables_json]
    if page is not None:
        args.extend(["--page", str(page)])
    if limit is not None:
        args.extend(["--limit", str(limit)])
    if all_pages:
        args.append("--all-pages")
    return _json_output(run_script("query_financials_operation.py", args))


@mcp.tool()
def list_graphql_operations(kind: str = None, read_only: bool = False) -> list | dict:
    """List available Hemlane GraphQL operations from HAR captures.

    Args:
        kind: Optional filter, usually query or mutation.
        read_only: When true, return only query operations.
    """
    catalog_path = SCRIPTS_DIR.parent / "references" / "operation-catalog.json"
    if not catalog_path.exists():
        return {"error": "Operation catalog not found"}
    try:
        catalog = json.loads(catalog_path.read_text())
        ops = catalog if isinstance(catalog, list) else catalog.get("operations", [])
        out = []
        for op in ops:
            name = op.get("operationName") or op.get("name")
            op_kind = op.get("kind")
            if kind and str(op_kind).lower() != str(kind).lower():
                continue
            if read_only and str(op_kind).lower() != "query":
                continue
            out.append({
                "operationName": name,
                "kind": op_kind,
                "files": op.get("files", []),
                "count": op.get("count"),
            })
        return out
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()
