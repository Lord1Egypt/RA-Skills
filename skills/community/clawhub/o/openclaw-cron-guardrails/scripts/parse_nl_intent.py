#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path


CN_NUM = {
    "一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5,
    "六": 6, "七": 7, "八": 8, "九": 9, "十": 10,
}


def load_text(path_arg: str | None):
    if path_arg and path_arg != "-":
        return Path(path_arg).read_text().strip()
    return sys.stdin.read().strip()


def parse_small_number(text: str):
    text = text.strip()
    if text.isdigit():
        return int(text)
    if text in CN_NUM:
        return CN_NUM[text]
    if len(text) == 2 and text[0] == "十" and text[1] in CN_NUM:
        return 10 + CN_NUM[text[1]]
    if len(text) == 2 and text[1] == "十" and text[0] in CN_NUM:
        return CN_NUM[text[0]] * 10
    if len(text) == 3 and text[1] == "十" and text[0] in CN_NUM and text[2] in CN_NUM:
        return CN_NUM[text[0]] * 10 + CN_NUM[text[2]]
    return None


def extract_interval(text: str):
    patterns = [
        r"每隔\s*(\d+)\s*(分钟|分|小时|钟头)",
        r"每\s*(\d+)\s*(分钟|分|小时|钟头)",
        r"every\s*(\d+)\s*(minutes?|hours?)",
        r"(\d+)\s*(分钟|分|小时|钟头)后",
    ]
    for p in patterns:
        m = re.search(p, text, re.I)
        if not m:
            continue
        n = int(m.group(1))
        unit = m.group(2).lower()
        if unit in {"分钟", "分", "minute", "minutes"}:
            return {"value": n, "unit": "minutes", "normalized": f"{n}m"}
        return {"value": n, "unit": "hours", "normalized": f"{n}h"}

    cn = re.search(r"每隔\s*([一二两三四五六七八九十]+)\s*(分钟|分|小时|钟头)", text)
    if cn:
        n = parse_small_number(cn.group(1))
        if n is not None:
            unit = cn.group(2)
            if unit in {"分钟", "分"}:
                return {"value": n, "unit": "minutes", "normalized": f"{n}m"}
            return {"value": n, "unit": "hours", "normalized": f"{n}h"}
    return None


def extract_run_count(text: str):
    patterns = [
        r"总共执行\s*(\d+)\s*次",
        r"执行\s*(\d+)\s*次",
        r"run\s*(\d+)\s*times",
        r"for\s*(\d+)\s*runs",
    ]
    for p in patterns:
        m = re.search(p, text, re.I)
        if m:
            return int(m.group(1))
    cn = re.search(r"总共执行\s*([一二两三四五六七八九十]+)\s*次", text)
    if cn:
        return parse_small_number(cn.group(1))
    return None


def infer_intent(text: str):
    low = text.lower()
    flags = {
        "has_reminder": any(k in text for k in ["提醒我", "设个闹钟", "给我设个闹钟"]) or "remind me" in low or "alarm" in low,
        "has_session_injection": any(k in text for k in ["当前 session", "当前session", "当前 thread", "当前thread", "prompt 注入", "prompt注入", "push 一下", "持续推进", "继续推这个 thread", "继续推这个 session"]) or "inject prompt" in low or "current session" in low or "current thread" in low or "nudge this session" in low or "nudging this session" in low or ("this session" in low and any(k in low for k in ["nudge", "push", "inject", "advance", "forward"])) or ("this thread" in low and any(k in low for k in ["push", "inject", "advance", "forward"])),
        "has_worker": any(k in text for k in ["scan", "watch", "monitor", "定时检查", "定时汇总", "定时抓取", "nightly", "daily", "每晚", "每天"]),
        "has_repeat": any(k in text for k in ["每隔", "循环", "loop", "tick", "每 "]) or bool(re.search(r"every\s*\d+", low)),
        "has_visible_delivery": any(k in text for k in ["发到", "发送到", "post 到", "发个总结", "发总结"]) or "send to" in low or "post to" in low or bool(re.search(r"\bpost\b.*\bto\b", low)) or bool(re.search(r"\bsend\b.*\bto\b", low)),
    }

    if flags["has_session_injection"]:
        return "session-injection", 0.88
    if flags["has_reminder"]:
        if flags["has_repeat"] or any(k in text for k in ["每天", "每晚", "每周"]) or any(k in low for k in ["daily", "nightly", "weekly", "weekday"]):
            return "reminder", 0.86
        return "reminder", 0.90
    if flags["has_worker"] or flags["has_visible_delivery"]:
        return "scheduled-worker", 0.80
    if flags["has_repeat"]:
        return "repeat-loop", 0.72
    return "unknown", 0.35


def infer_target_scope(text: str, intent_type: str):
    low = text.lower()
    if any(k in text for k in ["当前 session", "当前session"]) or "current session" in low or "this session" in low:
        return "current-session"
    if any(k in text for k in ["当前 thread", "当前thread"]) or "current thread" in low or "this thread" in low:
        return "current-thread"
    if intent_type == "reminder":
        return "main"
    if intent_type == "scheduled-worker":
        return "internal-worker"
    return "main"


def infer_delivery(intent_type: str, text: str):
    low = text.lower()
    if "webhook" in low:
        return "webhook", True
    visible = any(k in text for k in ["发到", "发送到", "post 到", "发个总结", "发总结"]) \
        or "send to" in low or "post to" in low \
        or bool(re.search(r"\bpost\b.*\bto\b", low)) \
        or bool(re.search(r"\bsend\b.*\bto\b", low)) \
        or any(k in low for k in ["discord", "feishu", "telegram", "slack"]) and any(k in low for k in ["post", "send"]) \
        or "发到discord" in low or "发到 discord" in low
    if visible:
        return "announce", True
    if intent_type in {"scheduled-worker", "session-injection"}:
        return "none", False
    return "none", True


def infer_schedule_type(text: str, interval, run_count):
    low = text.lower()
    if re.search(r"\b\d+\s+\*\s+\*\s+\*\s+\*", text) or re.search(r"\bcron\b", low):
        return "cron"
    if re.search(r"\d+\s*(分钟|分|小时|钟头)后", text):
        return "at"
    if any(k in text for k in ["每天", "每晚", "每周", "明天", "今晚", "早上", "下午"]) or any(k in low for k in ["daily", "nightly", "weekly", "tomorrow"]):
        if interval is None or run_count is None:
            return "at"
    if interval is not None:
        return "every"
    return "at"


def detect_file_reference(text: str):
    patterns = [
        r"\bread\b.+\.(md|txt|json|py|yaml|yml|csv)\b",
        r"去读.{0,12}文件",
        r"读取.{0,12}文件",
        r"/[^\s]+\.(md|txt|json|py|yaml|yml|csv)\b",
        r"[A-Za-z]:\\[^\s]+\.(md|txt|json|py|yaml|yml|csv)\b",
    ]
    return any(re.search(p, text, re.I) for p in patterns)


def main():
    parser = argparse.ArgumentParser(description="Parse natural-language scheduling request into normalized intent JSON")
    parser.add_argument("input", nargs="?", help="Text file path or omit / use - for stdin")
    args = parser.parse_args()

    text = load_text(args.input)
    if not text:
        print(json.dumps({"ok": False, "error": "empty input"}, ensure_ascii=False, indent=2))
        raise SystemExit(2)

    interval = extract_interval(text)
    run_count = extract_run_count(text)
    intent_type, confidence = infer_intent(text)
    schedule_type = infer_schedule_type(text, interval, run_count)
    target_scope = infer_target_scope(text, intent_type)
    delivery_mode, user_visible = infer_delivery(intent_type, text)
    contains_file_reference = detect_file_reference(text)
    prompt_looks_long = len(text) > 180

    needs_review = confidence < 0.75 or intent_type == "unknown"
    if intent_type == "scheduled-worker" and delivery_mode == "announce":
        needs_review = True
    if intent_type == "repeat-loop" and run_count is None and interval is not None and any(k in text for k in ["未来", "接下来"]):
        needs_review = True
    if prompt_looks_long:
        needs_review = True

    result = {
        "ok": True,
        "sourceText": text,
        "intent": {
            "intentType": intent_type,
            "scheduleType": schedule_type,
            "timeExpression": text,
            "interval": interval,
            "runCount": run_count,
            "stopCondition": None,
            "targetScope": target_scope,
            "deliveryMode": delivery_mode,
            "userVisible": user_visible,
            "taskText": text,
        },
        "confidence": round(confidence, 2),
        "needsReview": needs_review,
        "promptDiagnostics": {
            "containsFileReference": contains_file_reference,
            "promptLooksLong": prompt_looks_long,
            "inlineLength": len(text)
        },
        "heuristics": {
            "matchedReminder": any(k in text for k in ["提醒我", "设个闹钟", "给我设个闹钟"]) or "remind me" in text.lower(),
            "matchedSessionInjection": any(k in text for k in ["当前 session", "当前session", "当前 thread", "当前thread", "prompt 注入", "prompt注入", "push 一下", "持续推进"]),
            "matchedWorker": any(k in text for k in ["scan", "watch", "monitor", "定时检查", "定时汇总", "定时抓取", "nightly", "daily", "每晚", "每天"]),
            "matchedRepeat": any(k in text for k in ["每隔", "循环", "loop", "tick"]) or bool(re.search(r"every\s*\d+", text.lower())),
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
