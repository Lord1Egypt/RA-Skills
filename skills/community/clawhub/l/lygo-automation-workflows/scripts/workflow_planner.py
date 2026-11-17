#!/usr/bin/env python3
"""
LYGO Automation Workflows — local planner (advisor only).

Scores automation opportunities, emits a consent-aware workflow plan JSON.
No network. No subprocess. No auto-connect to Zapier/Make/n8n/CRM.

Signature: Delta9Phi963-AUTOMATION-WORKFLOWS-v1.0.0
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SIG = "Delta9Phi963-AUTOMATION-WORKFLOWS-v1.0.0"
VERSION = "1.0.0"

SENSITIVE_FIELDS = {
    "ssn",
    "password",
    "api_key",
    "secret",
    "token",
    "card",
    "cvv",
    "bank",
    "medical",
    "biometric",
    "cookie",
    "session",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def hours_per_month(minutes: float, frequency_per_month: float) -> float:
    return (minutes * frequency_per_month) / 60.0


def score_task(
    *,
    minutes: float,
    frequency_per_month: float,
    repetitive: bool,
    judgment_required: bool,
    touches_pii: bool,
    external_vendors: int,
) -> dict[str, Any]:
    time_h = hours_per_month(minutes, frequency_per_month)
    base = time_h * 10.0
    if repetitive:
        base *= 1.4
    if judgment_required:
        base *= 0.35
    if touches_pii:
        base *= 0.7  # still possible, but lower priority without strong controls
    # vendor sprawl penalty
    base *= max(0.4, 1.0 - 0.15 * max(0, external_vendors - 1))
    return {
        "hours_per_month": round(time_h, 3),
        "priority_score": round(base, 3),
        "recommend_automate": bool(repetitive and not judgment_required and time_h >= 1.0),
        "privacy_flags": {
            "touches_pii": touches_pii,
            "external_vendors": external_vendors,
            "require_consent_review": touches_pii or external_vendors >= 2,
        },
    }


def plan_workflow(
    *,
    name: str,
    trigger: str,
    conditions: list[str],
    actions: list[str],
    data_fields: list[str],
    tools: list[str],
    error_notify: str,
) -> dict[str, Any]:
    sensitive = sorted({f for f in data_fields if any(s in f.lower() for s in SENSITIVE_FIELDS)})
    local_preferred = any(
        t.lower() in {"sandcastle", "lygo", "n8n-self-hosted", "ollama", "local"} for t in tools
    )
    return {
        "ok": True,
        "signature": SIG,
        "version": VERSION,
        "created_utc": utc_now(),
        "workflow": {
            "name": name,
            "trigger": trigger,
            "conditions": conditions,
            "actions": actions,
            "tools": tools,
            "error_handling": error_notify or "Notify steward on failure; do not silently drop events",
        },
        "data_minimization": {
            "fields": data_fields,
            "sensitive_hits": sensitive,
            "rules": [
                "Move the minimum fields required for the action",
                "Prefer local/self-hosted tools when PII or payments involved",
                "Never put secrets in Slack/email alert bodies",
                "Document retention + how to disable the workflow",
                "Human consent before connecting new vendors",
            ],
        },
        "lygo_alignment": {
            "p0_gate": "Validate untrusted inbound payloads before acting",
            "consent": "No auto-publish / no silent CRM or payment sync without steward approval",
            "local_preferred": local_preferred,
            "pair_skills": [
                "lygo-sandcastle",
                "lygo-continuum",
                "lygo-continuum-integrator",
                "lygo-mint-verifier",
                "lygo-pure-data-witness",
                "lygo-protocol-stack-operator",
            ],
        },
        "warnings": [
            "Advisor only — this skill does not connect accounts or run automations.",
            "Review privacy / least-privilege before implementing in Zapier/Make/n8n/CRM.",
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="LYGO Automation Workflow planner (local advisor)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_a = sub.add_parser("audit-task", help="Score one recurring task for automation")
    p_a.add_argument("--name", required=True)
    p_a.add_argument("--minutes", type=float, required=True)
    p_a.add_argument("--frequency-per-month", type=float, required=True)
    p_a.add_argument("--repetitive", action="store_true")
    p_a.add_argument("--judgment-required", action="store_true")
    p_a.add_argument("--touches-pii", action="store_true")
    p_a.add_argument("--external-vendors", type=int, default=1)
    p_a.add_argument("--write")
    p_a.add_argument("--i-consent", action="store_true")

    p_p = sub.add_parser("plan", help="Emit a consent-aware workflow plan JSON")
    p_p.add_argument("--name", required=True)
    p_p.add_argument("--trigger", required=True)
    p_p.add_argument("--condition", action="append", default=[])
    p_p.add_argument("--action", action="append", default=[])
    p_p.add_argument("--field", action="append", default=[], help="Data field moved between tools")
    p_p.add_argument("--tool", action="append", default=[], help="Tools involved")
    p_p.add_argument("--error-notify", default="")
    p_p.add_argument("--write")
    p_p.add_argument("--i-consent", action="store_true")

    p_d = sub.add_parser("demo", help="Sample audit + plan")
    args = ap.parse_args()

    if args.cmd == "audit-task":
        scored = score_task(
            minutes=args.minutes,
            frequency_per_month=args.frequency_per_month,
            repetitive=args.repetitive,
            judgment_required=args.judgment_required,
            touches_pii=args.touches_pii,
            external_vendors=args.external_vendors,
        )
        out = {
            "ok": True,
            "signature": SIG,
            "task": args.name,
            **scored,
            "plain_english": (
                "Good automate candidate."
                if scored["recommend_automate"]
                else "Keep manual or redesign process before automating."
            ),
        }
        print(json.dumps(out, indent=2))
        if args.write:
            if not args.i_consent:
                raise SystemExit("Refusing write without --i-consent")
            Path(args.write).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
        return 0

    if args.cmd == "plan":
        out = plan_workflow(
            name=args.name,
            trigger=args.trigger,
            conditions=list(args.condition),
            actions=list(args.action) or ["Define actions"],
            data_fields=list(args.field),
            tools=list(args.tool) or ["unspecified"],
            error_notify=args.error_notify,
        )
        print(json.dumps(out, indent=2))
        if args.write:
            if not args.i_consent:
                raise SystemExit("Refusing write without --i-consent")
            Path(args.write).write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
        return 0

    if args.cmd == "demo":
        audit = score_task(
            minutes=15,
            frequency_per_month=20,
            repetitive=True,
            judgment_required=False,
            touches_pii=True,
            external_vendors=2,
        )
        plan = plan_workflow(
            name="Form → CRM → welcome (LYGO-hardened)",
            trigger="New public form submission",
            conditions=["email present", "P0 gate pass on payload"],
            actions=[
                "Store minimal fields locally / sandcastle workflow",
                "Optional CRM sync only after steward consent",
                "Send templated welcome without secrets in logs",
                "Notify steward channel with redacted summary",
            ],
            data_fields=["name", "email", "source"],
            tools=["lygo-sandcastle", "n8n-self-hosted"],
            error_notify="Steward alert on failure; quarantine payload",
        )
        print(json.dumps({"ok": True, "signature": SIG, "audit_example": audit, "plan_example": plan}, indent=2))
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
