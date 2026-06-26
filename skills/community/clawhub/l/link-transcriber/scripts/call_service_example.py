#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime
from urllib import error, parse, request

DEFAULT_API_BASE_URL = "https://linktranscriber.store"
IN_PROGRESS_STATUSES = {
    "queued",
    "running",
}
DEFAULT_POLL_MAX_ATTEMPTS = 60
DEFAULT_POLL_INTERVAL_SECONDS = 1.0
FULL_RESULT_FLAG = "--json"
SUMMARY_ONLY_FLAG = "--summary-only"


def infer_platform(url: str) -> str | None:
    lowered = url.lower()
    if "douyin.com" in lowered or "v.douyin.com" in lowered:
        return "douyin"
    if "xiaohongshu.com" in lowered or "xhslink.com" in lowered:
        return "xiaohongshu"
    return None


def http_json(method: str, url: str, *, payload: dict | None = None) -> dict:
    body = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = request.Request(url, data=body, headers=headers, method=method)
    try:
        with request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
    except error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as json_exc:
            raise RuntimeError(f"HTTP {exc.code}: {raw.strip()}") from json_exc
        if isinstance(parsed, dict):
            return parsed
        raise RuntimeError(f"HTTP {exc.code}: {raw.strip()}")
    except error.URLError as exc:
        raise RuntimeError(f"Request failed: {exc.reason}") from exc
    return json.loads(raw)


def extract_message(payload: dict | None) -> str:
    if not isinstance(payload, dict):
        return "未知错误"
    data = payload.get("data")
    if isinstance(data, dict):
        error_message = data.get("error_message")
        if isinstance(error_message, str) and error_message.strip():
            return error_message.strip()
    msg = payload.get("msg")
    if isinstance(msg, str) and msg.strip():
        return msg.strip()
    return "未知错误"


def format_failure(payload: dict | None) -> str:
    message = extract_message(payload)
    if "Cookie 缺失" in message or "cookie" in message.lower():
        return f"服务端配置问题: {message}"
    return message


def _first_summary_paragraph(summary_markdown: str) -> str:
    if not summary_markdown:
        return ""
    lines = []
    for raw_line in summary_markdown.replace("\r", "\n").split("\n"):
        line = str(raw_line or "").strip()
        if not line:
            continue
        if line.startswith("#"):
            continue
        if line.startswith(("-", "*")):
            line = line[1:].strip()
        if line:
            lines.append(line)
        if len(lines) >= 1:
            break
    return lines[0] if lines else summary_markdown.strip()


def _todo_lines(payload: dict) -> list[str]:
    card = payload.get("card") if isinstance(payload.get("card"), dict) else {}
    actions = card.get("actions") if isinstance(card.get("actions"), list) else []
    cleaned = [str(item or "").strip() for item in actions if str(item or "").strip()]
    return cleaned[:7]


def _format_reminder(payload: dict) -> str:
    card = payload.get("card") if isinstance(payload.get("card"), dict) else {}
    suggested = str(card.get("suggested_remind_at") or "").strip()
    if not suggested:
        return "暂未生成建议提醒时间"
    try:
        dt = datetime.fromisoformat(suggested.replace("Z", "+00:00"))
    except ValueError:
        return suggested
    return dt.strftime("%Y-%m-%d %H:%M")


def render_structured_output(payload: dict) -> str:
    summary = _first_summary_paragraph(str(payload.get("summary_markdown") or "").strip())
    todos = _todo_lines(payload)
    comment_candidates = payload.get("comment_candidates") if isinstance(payload.get("comment_candidates"), list) else []

    parts = [
        "【总结】",
        summary or "暂无总结",
        "",
        "【Todo List】",
    ]
    if todos:
        parts.extend(todos)
    else:
        parts.append("暂无 Todo")
    parts.extend(
        [
            "",
            "【推荐提醒时间】",
            _format_reminder(payload),
        ]
    )
    if comment_candidates:
        parts.extend(["", "【评论参考】"])
        cleaned_comments = [str(item or "").strip() for item in comment_candidates if str(item or "").strip()]
        for index, comment in enumerate(cleaned_comments):
            if index:
                parts.append("")
            parts.append(comment)
    return "\n".join(parts).strip()


def main() -> int:
    raw_args = sys.argv[1:]
    output_full_result = True
    if FULL_RESULT_FLAG in raw_args:
        raw_args = [arg for arg in raw_args if arg != FULL_RESULT_FLAG]
        output_full_result = True
    if SUMMARY_ONLY_FLAG in raw_args:
        raw_args = [arg for arg in raw_args if arg != SUMMARY_ONLY_FLAG]
        output_full_result = False

    if len(raw_args) not in {1, 2}:
        print("Usage: call_service_example.py <url> [platform] [--json|--summary-only]", file=sys.stderr)
        return 1

    base_url = os.getenv("LINK_SKILL_API_BASE_URL", DEFAULT_API_BASE_URL).strip().rstrip("/")
    poll_max_attempts = int(os.getenv("LINK_SKILL_POLL_MAX_ATTEMPTS", str(DEFAULT_POLL_MAX_ATTEMPTS)))
    poll_interval_seconds = float(
        os.getenv("LINK_SKILL_POLL_INTERVAL_SECONDS", str(DEFAULT_POLL_INTERVAL_SECONDS))
    )

    url = raw_args[0]
    platform = raw_args[1] if len(raw_args) == 2 else None
    platform = platform or infer_platform(url)
    if not platform:
        print("Platform could not be inferred. Pass platform explicitly: douyin or xiaohongshu.", file=sys.stderr)
        return 1

    create_payload = {
        "url": url,
    }
    create_result = http_json("POST", f"{base_url}/public/transcriptions", payload=create_payload)
    task_id = create_result.get("task_id") if isinstance(create_result, dict) else None
    if not task_id:
        print(format_failure(create_result), file=sys.stderr)
        return 1

    final_result = create_result
    for _ in range(poll_max_attempts):
        polled = http_json("GET", f"{base_url}/public/transcriptions/{parse.quote(str(task_id))}")
        final_result = polled
        status = (polled.get("status") if isinstance(polled, dict) else None) or ""
        if status not in IN_PROGRESS_STATUSES:
            break
        time.sleep(poll_interval_seconds)

    final_status = (final_result.get("status") if isinstance(final_result, dict) else None) or ""
    if final_status in IN_PROGRESS_STATUSES:
        print(f"转写任务仍在处理中: {task_id} ({final_status})", file=sys.stderr)
        return 1
    if final_status != "completed":
        print(format_failure(final_result), file=sys.stderr)
        return 1

    if FULL_RESULT_FLAG in sys.argv[1:]:
        print(json.dumps(final_result, ensure_ascii=False, indent=2))
        return 0

    if output_full_result:
        print(render_structured_output(final_result))
        return 0

    summary_markdown = final_result.get("summary_markdown") if isinstance(final_result, dict) else None
    if summary_markdown:
        print(summary_markdown)
        return 0

    print(format_failure(final_result), file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
