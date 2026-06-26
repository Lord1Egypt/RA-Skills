"""PVM CLI entry point — pvm command."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

from .models import Decision
from .notifier import Notifier
from .vault import Vault

DEFAULT_CONFIG = os.environ.get("PVM_CONFIG", "./config.yaml")


def _vault(cfg: str) -> Vault:
    import yaml
    path = Path(cfg)
    if path.exists():
        raw = yaml.safe_load(path.read_text())
        db_path = raw.get("vault", {}).get("db_path", "./grants.db")
    else:
        db_path = "./grants.db"
    return Vault(db_path)


def cmd_request(args: argparse.Namespace) -> int:
    vault = _vault(args.config)
    notifier = Notifier(args.config)

    from .models import PermissionRequest
    from .approval.polling import ApprovalPoller

    ttl = min(
        args.duration or notifier.default_ttl_minutes(),
        notifier.max_ttl_minutes(),
    )
    agent_id = args.agent_id or os.environ.get("AGENT_ID", "default")

    # Create the permission request in the vault
    request = PermissionRequest.create(
        agent_id=agent_id,
        operation=args.operation or "unknown",
        scope=args.scope,
        scope_type=args.scope_type or "path",
        reason=args.reason or "",
        ttl_minutes=ttl,
    )

    vault.create_request(
        agent_id=agent_id,
        operation=args.operation or "unknown",
        scope=args.scope,
        scope_type=args.scope_type or "path",
        reason=args.reason or "",
        ttl_minutes=ttl,
        approval_token=request.approval_token,
    )

    print(f"Requesting approval for: {request.scope}")
    print(f"Token: {request.approval_token}")
    print(f"Duration: {request.ttl_minutes}min")
    print(f"Notifying: {', '.join(notifier.enabled_channels)}...")

    results = notifier.notify_approvers(
        message=args.reason or "Please approve this operation.",
        approval_token=request.approval_token,
        agent_id=agent_id,
        scope=request.scope,
        reason=request.reason,
        ttl_minutes=request.ttl_minutes,
    )

    for ch, result in results.items():
        status = "✅" if result.success else f"❌ {result.error}"
        print(f"  {ch}: {status}")

    # Wait for approval if blocking
    if args.block:
        print(f"\nWaiting up to {args.timeout}s for approval...")
        poller = ApprovalPoller(vault)

        def on_approve(req):
            print(f"\n✅ Request approved! Grant ready.")

        grant = poller.wait_for_decision(
            request=request,
            timeout_seconds=args.timeout,
            on_approve=on_approve,
        )
        if grant:
            print(f"✅ Approved! Grant: {grant.grant_id}")
        else:
            print("⏰ Timed out — no approval received.")
            return 1
    else:
        print("\nNot blocking. Approve via any configured channel:")
        print(f"  - iMessage: reply APPROVE {request.approval_token}")
        print(f"  - Email: reply APPROVE in the email thread")
        print(f"  - HTTP: POST http://localhost:8080/approve/{request.approval_token}")
        print(f"\nOr start `pvm approve-daemon` to auto-detect approvals from all channels.")

    return 0


def cmd_status(args: argparse.Namespace) -> int:
    vault = _vault(args.config)
    grants = vault.get_active_grants(agent_id=args.agent_id)

    if not grants:
        print("No active grants found.")
        return 0

    print(f"Active grants for {args.agent_id or 'all agents'}:\n")
    for g in grants:
        remaining = g.remaining_minutes()
        print(f"  {g.grant_id}")
        print(f"    scope:    {g.scope}")
        print(f"    reason:   {g.reason}")
        print(f"    expires:  in {remaining:.1f} min")
        print(f"    by:       {g.approved_by or 'N/A'}")
        print()
    return 0


def cmd_revoke(args: argparse.Namespace) -> int:
    vault = _vault(args.config)
    grant = vault.get_grant(args.grant_id)
    if not grant:
        print(f"Grant not found: {args.grant_id}")
        return 1
    vault.revoke_grant(args.grant_id)
    print(f"Revoked: {args.grant_id} ({grant.scope})")
    return 0


def cmd_log(args: argparse.Namespace) -> int:
    vault = _vault(args.config)
    decision = Decision(args.decision) if args.decision else None
    entries = vault.get_audit_log(
        agent_id=args.agent_id,
        decision=decision,
        limit=args.limit,
    )

    if not entries:
        print("No audit entries found.")
        return 0

    print(f"Audit log (last {len(entries)} entries):\n")
    for e in entries:
        decision_str = f"[{e.decision.value}]" if e.decision else ""
        print(f"  {e.timestamp.strftime('%Y-%m-%d %H:%M:%S')} {decision_str}")
        print(f"    {e.details}")
        print()
    return 0


def cmd_serve(args: argparse.Namespace) -> int:
    """Run the HTTP approval server (part of approve-daemon)."""
    vault = _vault(args.config)

    from .approval.server import run_server

    def on_approve(token: str, approver: str) -> None:
        req = vault.get_request_by_token(token)
        if not req:
            # Fallback: create grant with defaults
            from .models import AuditEntryType, Decision
            entries = vault.get_audit_log(limit=1000)
            matching = [e for e in entries if token in (e.details or "")]
            latest = matching[0] if matching else None
            vault.create_grant(
                agent_id=req["agent_id"] if req else (latest.agent_id if latest else "default"),
                scope=req["scope"] if req else (latest.scope if latest else "/"),
                scope_type=req["scope_type"] if req else "path",
                reason=f"Approved by {approver}",
                ttl_minutes=req["ttl_minutes"] if req else 30,
                approved_by=approver,
                approval_token=token,
            )
            return
        vault.create_grant(
            agent_id=req["agent_id"],
            scope=req["scope"],
            scope_type=req["scope_type"],
            reason=f"Approved by {approver} via HTTP",
            ttl_minutes=req["ttl_minutes"],
            approved_by=approver,
            approval_token=token,
        )
        print(f"[server] Grant created: token={token} by={approver}")

    def on_deny(token: str, approver: str) -> None:
        vault.deny_request(token, approver)
        print(f"[server] Request denied: token={token} by={approver}")

    print(f"Starting HTTP approval server on :{args.port}...")
    print("Endpoints:")
    print(f"  POST /approve/<token>  — Approve a request")
    print(f"  POST /deny/<token>    — Deny a request")
    print(f"  GET  /                — Status page")
    run_server(
        on_approve=on_approve,
        on_deny=on_deny,
        host=args.host,
        port=args.port,
        approver_name=args.approver or "Tyler",
    )
    return 0


def cmd_approve_daemon(args: argparse.Namespace) -> int:
    """Run the full approval daemon (email + Sendblue + HTTP server)."""
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    vault = _vault(args.config)

    from .approval.daemon import ApprovalDaemon
    daemon = ApprovalDaemon(
        vault=vault,
        config_path=args.config,
        http_port=args.port,
        approver_name=args.approver or "Tyler",
    )

    print("PVM Approval Daemon")
    print("==================")
    print(f"Config: {args.config}")
    print(f"HTTP server: http://localhost:{args.port}")
    print(f"Approve via: HTTP POST, email reply, Sendblue iMessage")
    print()

    daemon.start()
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    vault = _vault(args.config)
    scope_type = args.scope_type or "path"
    if scope_type == "path":
        ok = vault.check_grant_glob(args.agent_id or "default", args.scope, scope_type)
    else:
        ok = vault.check_grant(args.agent_id or "default", args.scope)
    if ok:
        print(f"GRANTED: {args.scope}")
        return 0
    print(f"DENIED:  {args.scope}")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(prog="pvm", description="Permission Vending Machine")
    parser.add_argument("--config", default=DEFAULT_CONFIG, help="Config file path")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # pvm request
    r = sub.add_parser("request", help="Request a permission grant")
    r.add_argument("--scope", required=True, help="Scope to request (e.g. path or repo URL)")
    r.add_argument("--scope-type", default="path", choices=["path", "repo"], help="Scope type")
    r.add_argument("--reason", default="", help="Reason for the request")
    r.add_argument("--duration", type=int, help="Duration in minutes")
    r.add_argument("--agent-id", help="Agent ID (default: from AGENT_ID env)")
    r.add_argument("--operation", help="Operation name")
    r.add_argument("--block", action="store_true", help="Block until approved or timeout")
    r.add_argument("--timeout", type=int, default=300, help="Timeout for --block (seconds)")
    r.set_defaults(func=cmd_request)

    # pvm status
    s = sub.add_parser("status", help="List active grants")
    s.add_argument("--agent-id", help="Filter by agent ID")
    s.set_defaults(func=cmd_status)

    # pvm revoke
    rv = sub.add_parser("revoke", help="Revoke a grant")
    rv.add_argument("--grant-id", dest="grant_id", required=True)
    rv.set_defaults(func=cmd_revoke)

    # pvm log
    l = sub.add_parser("log", help="Show audit log")
    l.add_argument("--agent-id", dest="agent_id", help="Filter by agent ID")
    l.add_argument("--decision", choices=[d.value for d in Decision], help="Filter by decision")
    l.add_argument("--limit", type=int, default=100)
    l.set_defaults(func=cmd_log)

    # pvm check
    c = sub.add_parser("check", help="Check if a grant exists for scope")
    c.add_argument("--scope", required=True)
    c.add_argument("--agent-id", dest="agent_id", default="default")
    c.add_argument("--scope-type", default="path", choices=["path", "repo"])
    c.set_defaults(func=cmd_check)

    # pvm serve (HTTP server only)
    sv = sub.add_parser("serve", help="Run the HTTP approval server")
    sv.add_argument("--host", default="0.0.0.0")
    sv.add_argument("--port", type=int, default=7823)
    sv.add_argument("--approver", help="Approver name")
    sv.set_defaults(func=cmd_serve)

    # pvm approve-daemon (full daemon)
    ad = sub.add_parser("approve-daemon", help="Run full approval daemon (email + Sendblue + HTTP)")
    ad.add_argument("--port", type=int, default=7823)
    ad.add_argument("--approver", help="Approver name")
    ad.set_defaults(func=cmd_approve_daemon)

    # pvm init — interactive setup wizard
    init = sub.add_parser("init", help="Run interactive setup wizard")
    init.set_defaults(func=lambda args: __import__("pvm.setup_wizard", fromlist=["main"]).main())

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
