#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def load_spec(path_arg: str | None):
    if path_arg and path_arg != "-":
        return json.loads(Path(path_arg).read_text())
    return json.load(sys.stdin)


def err(msg: str):
    return {"ok": False, "error": msg}


def main():
    path_arg = sys.argv[1] if len(sys.argv) > 1 else None
    try:
        spec = load_spec(path_arg)
    except Exception as e:
        print(json.dumps(err(f"failed to load spec: {e}"), ensure_ascii=False))
        raise SystemExit(2)

    if not isinstance(spec, dict):
        print(json.dumps(err("spec must be a JSON object"), ensure_ascii=False))
        raise SystemExit(2)

    issues: list[str] = []
    warnings: list[str] = []

    name = spec.get("name")
    if not isinstance(name, str) or not name.strip():
        issues.append("name is required")

    schedule = spec.get("schedule")
    if not isinstance(schedule, dict):
        issues.append("schedule object is required")
        schedule_kind = None
    else:
        schedule_kind = schedule.get("kind")
        if schedule_kind not in {"at", "every", "cron"}:
            issues.append("schedule.kind must be one of: at, every, cron")
        if schedule_kind == "at" and not schedule.get("at"):
            issues.append("schedule.at is required when schedule.kind=at")
        if schedule_kind == "every" and not isinstance(schedule.get("everyMs"), int):
            issues.append("schedule.everyMs must be an integer when schedule.kind=every")
        if schedule_kind == "cron" and not schedule.get("expr"):
            issues.append("schedule.expr is required when schedule.kind=cron")
        if schedule_kind == "cron" and not schedule.get("tz"):
            warnings.append("schedule.tz is missing for recurring cron job; prefer explicit timezone")

    session_target = spec.get("sessionTarget")
    if session_target not in {"main", "isolated"}:
        issues.append("sessionTarget must be main or isolated")

    payload = spec.get("payload")
    payload_kind = payload.get("kind") if isinstance(payload, dict) else None
    if not isinstance(payload, dict):
        issues.append("payload object is required")
    elif payload_kind not in {"systemEvent", "agentTurn"}:
        issues.append("payload.kind must be systemEvent or agentTurn")

    if session_target == "main" and payload_kind != "systemEvent":
        issues.append("main jobs must use payload.kind=systemEvent")
    if session_target == "isolated" and payload_kind != "agentTurn":
        issues.append("isolated jobs must use payload.kind=agentTurn")

    if payload_kind == "systemEvent" and not payload.get("text"):
        issues.append("payload.text is required for systemEvent jobs")
    if payload_kind == "agentTurn" and not payload.get("message"):
        issues.append("payload.message is required for agentTurn jobs")

    timeout_seconds = payload.get("timeoutSeconds") if isinstance(payload, dict) else None
    message = payload.get("message", "") if isinstance(payload, dict) else ""
    if timeout_seconds is not None:
        if not isinstance(timeout_seconds, int) or timeout_seconds <= 0:
            issues.append("payload.timeoutSeconds must be a positive integer when provided")
        elif timeout_seconds < 120 and isinstance(message, str) and len(message) > 120:
            warnings.append("payload.timeoutSeconds looks short for a non-trivial prompt")

    delivery = spec.get("delivery")
    delivery_mode = None
    delivery_channel = None
    delivery_to = None
    if isinstance(delivery, dict):
        delivery_mode = delivery.get("mode")
        delivery_channel = delivery.get("channel")
        delivery_to = delivery.get("to")
        if delivery_mode not in {"none", "announce", "webhook", None}:
            issues.append("delivery.mode must be none, announce, or webhook")
        if session_target == "main" and delivery_mode == "announce":
            issues.append("delivery.mode=announce is only valid for isolated jobs")
        if delivery_mode == "webhook" and not delivery_to:
            issues.append("delivery.to is required for webhook delivery")
        if delivery_mode == "announce":
            if delivery_channel == "last":
                warnings.append("delivery.channel=last is fragile for isolated jobs in multi-channel setups")
            if not delivery_channel:
                warnings.append("announce delivery without explicit channel may rely on implicit last-route resolution")
            if not delivery_to and delivery_channel not in {None, "last"}:
                warnings.append("announce delivery has explicit channel but no explicit target")
    else:
        if session_target == "isolated":
            warnings.append("isolated job without delivery config will default to announce")

    multi_channel = spec.get("multiChannelConfigured")
    if multi_channel is True and session_target == "isolated":
        if delivery is None:
            issues.append("isolated job in multi-channel setup must not rely on implicit default announce delivery")
        elif delivery_mode == "announce" and delivery_channel in {None, "last"}:
            issues.append("isolated announce job in multi-channel setup requires explicit delivery.channel")

    result = {
        "ok": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "summary": {
            "name": name,
            "sessionTarget": session_target,
            "payloadKind": payload_kind,
            "scheduleKind": schedule_kind,
            "deliveryMode": delivery_mode,
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
