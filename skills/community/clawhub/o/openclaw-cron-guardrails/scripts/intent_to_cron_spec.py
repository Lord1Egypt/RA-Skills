#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

DEFAULT_TZ = "America/New_York"
DEFAULT_TIMEOUT = 300


def load_obj(path_arg: str | None):
    if path_arg and path_arg != "-":
        return json.loads(Path(path_arg).read_text())
    return json.load(sys.stdin)


def interval_to_ms(interval: dict | None):
    if not isinstance(interval, dict):
        return None
    value = interval.get("value")
    unit = interval.get("unit")
    if not isinstance(value, int):
        return None
    if unit == "minutes":
        return value * 60 * 1000
    if unit == "hours":
        return value * 60 * 60 * 1000
    return None


def make_name(intent_type: str, text: str):
    prefixes = {
        "reminder": "Reminder",
        "repeat-loop": "Repeat loop",
        "session-injection": "Session push loop",
        "scheduled-worker": "Scheduled worker",
        "unknown": "Scheduled action",
    }
    base = prefixes.get(intent_type, "Scheduled action")
    tail = text.strip().replace("\n", " ")[:48]
    return f"{base}: {tail}"


def transform(parsed: dict):
    if not parsed.get("ok"):
        return {"ok": False, "error": "input parser result is not ok"}

    intent = parsed.get("intent") or {}
    intent_type = intent.get("intentType") or "unknown"
    schedule_type = intent.get("scheduleType") or "at"
    interval = intent.get("interval")
    run_count = intent.get("runCount")
    target_scope = intent.get("targetScope")
    delivery_mode = intent.get("deliveryMode")
    text = intent.get("taskText") or parsed.get("sourceText") or ""
    needs_review = bool(parsed.get("needsReview"))
    confidence = parsed.get("confidence")
    prompt_diag = parsed.get("promptDiagnostics") or {}

    review_reasons = []
    if needs_review:
        review_reasons.append("parser marked this request as needsReview")
    if prompt_diag.get("containsFileReference"):
        review_reasons.append("prompt appears to contain a file reference; preserve it as opaque payload and verify referenced path")
    if prompt_diag.get("promptLooksLong"):
        review_reasons.append("prompt is relatively long for inline transport; verify before creation")

    spec = {
        "name": make_name(intent_type, text),
        "multiChannelConfigured": True,
    }

    if schedule_type == "every":
        every_ms = interval_to_ms(interval)
        if every_ms is None:
            return {"ok": False, "error": "every schedule requires parseable interval"}
        spec["schedule"] = {"kind": "every", "everyMs": every_ms}
    elif schedule_type == "cron":
        review_reasons.append("raw cron expression path not fully inferred yet")
        spec["schedule"] = {"kind": "cron", "expr": "*/10 * * * *", "tz": DEFAULT_TZ}
    else:
        spec["schedule"] = {"kind": "at", "at": "REVIEW_REQUIRED"}
        review_reasons.append("exact wall-clock time still needs resolution")

    if intent_type == "reminder":
        spec["sessionTarget"] = "main"
        spec["wakeMode"] = "now"
        spec["payload"] = {
            "kind": "systemEvent",
            "text": text,
        }
        if schedule_type == "at" and interval_to_ms(interval) is not None:
            spec["notes"] = {"deriveAtFromNow": interval.get("normalized")}

    elif intent_type == "session-injection":
        spec["sessionTarget"] = "isolated"
        spec["wakeMode"] = "now"
        spec["payload"] = {
            "kind": "agentTurn",
            "message": text,
            "timeoutSeconds": DEFAULT_TIMEOUT,
        }
        spec["delivery"] = {"mode": "none"}
        spec["notes"] = {
            "targetScope": target_scope,
            "sessionBindingRequired": True,
        }
        if target_scope not in {"current-session", "current-thread"}:
            review_reasons.append("session injection should bind explicitly to current session/thread")

    elif intent_type == "repeat-loop":
        reminder_like = target_scope == "main" and delivery_mode == "none"
        if reminder_like:
            spec["sessionTarget"] = "main"
            spec["wakeMode"] = "now"
            spec["payload"] = {
                "kind": "systemEvent",
                "text": text,
            }
        else:
            spec["sessionTarget"] = "isolated"
            spec["wakeMode"] = "now"
            spec["payload"] = {
                "kind": "agentTurn",
                "message": text,
                "timeoutSeconds": DEFAULT_TIMEOUT,
            }
            spec["delivery"] = {"mode": "none"}
        if run_count is not None:
            spec.setdefault("notes", {})["runCount"] = run_count
            spec["notes"]["deleteAfterRunWhenCountReached"] = True
        else:
            review_reasons.append("repeat loop has no explicit runCount/stopCondition")

    elif intent_type == "scheduled-worker":
        spec["sessionTarget"] = "isolated"
        spec["wakeMode"] = "now"
        spec["payload"] = {
            "kind": "agentTurn",
            "message": text,
            "timeoutSeconds": DEFAULT_TIMEOUT,
        }
        if delivery_mode == "announce":
            spec["delivery"] = {"mode": "announce", "channel": None, "to": None}
            review_reasons.append("visible scheduled worker still needs explicit delivery target")
        else:
            spec["delivery"] = {"mode": "none"}
        if schedule_type == "at":
            spec.setdefault("schedule", {})["kind"] = "at"
            spec["schedule"]["at"] = "REVIEW_REQUIRED"

    else:
        return {
            "ok": False,
            "error": "unknown intent type cannot be safely transformed",
            "parsed": parsed,
        }

    spec.setdefault("notes", {})["promptDiagnostics"] = prompt_diag

    result = {
        "ok": True,
        "cronSpec": spec,
        "needsReview": len(review_reasons) > 0,
        "reviewReasons": review_reasons,
        "confidence": confidence,
    }
    return result


def main():
    parser = argparse.ArgumentParser(description="Transform normalized intent JSON into cron spec JSON")
    parser.add_argument("input", nargs="?", help="Path to parsed intent JSON or omit / use - for stdin")
    args = parser.parse_args()

    try:
        obj = load_obj(args.input)
    except Exception as e:
        print(json.dumps({"ok": False, "error": f"failed to load input: {e}"}, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    result = transform(obj)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result.get("ok") else 1)


if __name__ == "__main__":
    main()
