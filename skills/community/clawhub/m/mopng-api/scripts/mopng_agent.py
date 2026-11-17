#!/usr/bin/env python3
"""Small stdlib-only client for motu-agent's public MoPNG Agent API."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from urllib import parse

try:
    from _http import JsonHttpClient
except ImportError:  # executed as a module (`python -m scripts.mopng_agent`)
    from scripts._http import JsonHttpClient


DEFAULT_BASE_URL = "https://agent-api.mopng.cn"
API_PREFIX = "/api/v1/open/agent"


def _json(value: str) -> object:
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON: {exc.msg}") from exc


class AgentClient:
    def __init__(self, base_url: str, api_key: str, timeout: float = 90) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self._http = JsonHttpClient(
            self.base_url + API_PREFIX,
            {"Accept": "application/json", "X-API-Key": api_key},
            timeout,
            service="motu-agent",
        )

    def call(self, method: str, path: str, body: dict | None = None) -> dict:
        return self._http.request(method, path, data=body)


def _client(args: argparse.Namespace) -> AgentClient:
    key = os.getenv("MOPNG_API_KEY")
    if not key:
        raise ValueError("MOPNG_API_KEY is required")
    return AgentClient(os.getenv("MOPNG_AGENT_BASE_URL", DEFAULT_BASE_URL), key, args.timeout)


def _brief(args: argparse.Namespace) -> dict:
    references = args.reference_url or []
    if len(references) > 14:
        raise ValueError("at most 14 --reference-url values are allowed")
    reference = references[0] if references else "prompt-only"
    subject_type = "image" if references else "text"
    style = {}
    if args.style_constraint:
        style["constraint"] = args.style_constraint
    if args.avoid:
        style["avoid"] = args.avoid
    brief = {
        "user_intent": args.intent,
        "spec": {
            "goal": args.goal,
            "usage": args.usage,
            "subject": {"type": subject_type, "reference": reference},
            "style": style,
            "format": args.format,
        },
        "budget": {
            "cost_mode": args.cost_mode,
            "max_cost_points": args.max_cost_points,
            "max_time_sec": args.max_time_sec,
        },
    }
    if references:
        brief["spec"]["subject"]["references"] = references
    if args.width or args.height:
        if not args.width or not args.height:
            raise ValueError("--width and --height must be provided together")
        brief["spec"]["size"] = {"width": args.width, "height": args.height}
    return brief


def _print(value: dict) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def _add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--timeout", type=float, default=90)


def _add_brief_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--intent", required=True)
    parser.add_argument("--goal", required=True)
    parser.add_argument("--reference-url", action="append", help="reference image URL; repeat up to 14 times")
    parser.add_argument("--usage")
    parser.add_argument("--style-constraint")
    parser.add_argument("--avoid")
    parser.add_argument("--width", type=int)
    parser.add_argument("--height", type=int)
    parser.add_argument("--format", choices=("png", "jpg", "jpeg", "webp"), default="png")
    parser.add_argument("--cost-mode", choices=("economy", "balanced", "premium"), default="balanced")
    parser.add_argument("--max-cost-points", type=int, default=10)
    parser.add_argument("--max-time-sec", type=int, default=120)


def _watch(client: AgentClient, session_id: str, interval: float) -> dict:
    while True:
        result = client.call("GET", f"/session/{session_id}/exec")
        status = result.get("status")
        if status in {"success", "partial_failed", "failed", "terminated"}:
            return result
        time.sleep(interval)


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    # Keep the skill-facing form ``... mopng_agent.py agent run`` while also
    # allowing the shorter CLI form ``... mopng_agent.py run``.
    if argv and argv[0] == "agent":
        argv = argv[1:]
    parser = argparse.ArgumentParser(description="Call motu-agent MoPNG Agent OpenAPI")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="create a Brief and optionally auto-approve a cheap Plan")
    _add_common(run)
    _add_brief_args(run)
    run.add_argument("--no-auto-approve", action="store_true")
    run.add_argument("--watch", action="store_true")
    run.add_argument("--poll-interval", type=float, default=3)

    brief = sub.add_parser("brief", help="create a session and return its Plan")
    _add_common(brief)
    _add_brief_args(brief)

    plan = sub.add_parser("plan")
    _add_common(plan)
    plan.add_argument("session_id")

    revision = sub.add_parser("revision")
    _add_common(revision)
    revision.add_argument("session_id")
    revision.add_argument("--plan-id", required=True)
    revision.add_argument("--round", type=int, required=True)
    revision.add_argument("--feedback-json", required=True)
    revision.add_argument("--reason")

    approve = sub.add_parser("approve")
    _add_common(approve)
    approve.add_argument("session_id")

    status = sub.add_parser("status")
    _add_common(status)
    status.add_argument("session_id")
    status.add_argument("--watch", action="store_true")
    status.add_argument("--poll-interval", type=float, default=3)

    models = sub.add_parser("models", help="list models currently exposed by motu-agent")
    _add_common(models)
    models.add_argument("--capability", default="text-to-image")

    for name in ("interrupt", "delete"):
        command = sub.add_parser(name)
        _add_common(command)
        command.add_argument("session_id")

    args = parser.parse_args(argv)
    try:
        client = _client(args)
        if args.command in {"run", "brief"}:
            result = client.call("POST", "/session", _brief(args))
            _print(result)
            if args.command == "run" and not args.no_auto_approve:
                plan_data = result.get("plan", {})
                threshold = int(os.getenv("MOPNG_AGENT_AUTO_APPROVE_COST_POINTS", "5"))
                llm_billing = plan_data.get("llm_billing") or {}
                total_estimated_cost = plan_data.get("total_cost", threshold + 1) + llm_billing.get("cost_virtual", 0)
                if total_estimated_cost <= threshold:
                    session_id = result["session_id"]
                    approved = client.call("POST", f"/session/{session_id}/approve")
                    _print(approved)
                    if args.watch:
                        _print(_watch(client, session_id, args.poll_interval))
        elif args.command == "plan":
            _print(client.call("GET", f"/session/{args.session_id}/plan"))
        elif args.command == "models":
            capability = parse.quote(args.capability, safe="-_")
            _print(client.call("GET", f"/models?capability={capability}"))
        elif args.command == "revision":
            feedback = _json(args.feedback_json)
            if not isinstance(feedback, list):
                raise ValueError("--feedback-json must be a JSON array")
            body = {"plan_id": args.plan_id, "round": args.round, "feedback": feedback}
            if args.reason:
                body["reason"] = args.reason
            _print(client.call("POST", f"/session/{args.session_id}/revision", body))
        elif args.command == "approve":
            _print(client.call("POST", f"/session/{args.session_id}/approve"))
        elif args.command == "status":
            result = _watch(client, args.session_id, args.poll_interval) if args.watch else client.call("GET", f"/session/{args.session_id}/exec")
            _print(result)
        elif args.command == "interrupt":
            _print(client.call("POST", f"/session/{args.session_id}/interrupt"))
        else:
            client.call("DELETE", f"/session/{args.session_id}")
    except (RuntimeError, ValueError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
