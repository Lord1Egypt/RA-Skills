#!/usr/bin/env python3
"""行动层：每日摘要。把 P2 队列打包成一条 Telegram 消息，同时把摘要文档入库 2brain。

队列为空 → 静默退出（exit 0）。发送成功后队列归档到 queue/archive/。
"""
import html
import json
import sys
from datetime import datetime
from pathlib import Path

from common import QUEUE_FILE, CONFIG, append_outbox, kb_hint, log_run, notify_mode, now_iso
from kb import get_kb
from notify_telegram import send


def load_queue():
    if not QUEUE_FILE.exists():
        return []
    return [json.loads(l) for l in QUEUE_FILE.read_text().splitlines() if l.strip()]


def render_digest(entries):
    e = html.escape
    day = datetime.now().strftime("%Y-%m-%d")
    lines = [f"📋 <b>JobWatcher 日摘要 · {day}</b>（P2 · {len(entries)} 条）\n"]
    by_company = {}
    for q in entries:
        by_company.setdefault(q["item"]["company"], []).append(q)
    for company, qs in by_company.items():
        lines.append(f"\n<b>{e(company)}</b>")
        for q in qs:
            it, j = q["item"], q["judgment"]
            flag = " ⚠️AI判断失败" if j["match"] == "judgment_failed" else ""
            lines.append(f"• <a href=\"{e(it['detail_url'])}\">{e(it['title'])}</a>"
                         f"（{e(it['location'] or 'N/A')}）{flag}\n"
                         f"  {e(j['summary_zh'][:120])}")
    lines.append(f"\n🧠 {e(kb_hint())}")
    return "\n".join(lines)


def render_digest_doc(entries):
    day = datetime.now().strftime("%Y-%m-%d")
    out = [f"# JobWatcher 日摘要 {day}\n\n共 {len(entries)} 条 P2。\n"]
    for q in entries:
        it, j = q["item"], q["judgment"]
        out.append(f"## {it['company']} — {it['title']}\n\n"
                   f"- 地点: {it['location']}\n- 链接: {it['detail_url']}\n"
                   f"- 标签: {' '.join(j['tags'])}\n\n{j['summary_zh']}\n")
    return "\n".join(out)


def followup_section():
    """投递后 7 天无更新的跟进提醒（tracker 数据）。"""
    try:
        from tracker import stale
        items = stale(7)
    except Exception:  # noqa: BLE001
        return ""
    if not items:
        return ""
    lines = ["", "⏰ 投递跟进提醒（7 天无更新）："]
    for doc_id, v in list(items.items())[:8]:
        lines.append(f"• {v.get('title', doc_id)} — {v['status']}，上次更新 {v['updated_at'][:10]}")
    return "\n".join(lines)


def main():
    entries = load_queue()
    fu = followup_section()
    if not entries and not fu:
        log_run({"kind": "digest", "sent": False, "count": 0})
        return {"sent": False, "count": 0}
    if not entries and fu:  # 没有 P2 但有跟进提醒，也值得发
        if notify_mode() == "telegram":
            send(fu.strip(), disable_preview=True)
        else:
            append_outbox("digest", fu.strip())
        log_run({"kind": "digest", "sent": True, "count": 0, "followups": True})
        return {"sent": True, "count": 0, "followups": True}

    text = render_digest(entries) + followup_section()
    if notify_mode() == "telegram":
        send(text, disable_preview=True)
    else:  # agent 播报：outbox 里放纯文本（去掉 HTML 标签）
        import re
        append_outbox("digest", re.sub(r"</?b>|</?a[^>]*>", "", text))

    errors = []
    try:
        day = datetime.now().strftime("%Y%m%d")
        get_kb().upload_doc(f"{day}-daily-digest.md", render_digest_doc(entries))
    except Exception as e:  # noqa: BLE001
        errors.append(str(e)[:300])

    archive = QUEUE_FILE.parent / "archive"
    archive.mkdir(exist_ok=True)
    QUEUE_FILE.rename(archive / f"p2_digest.{datetime.now():%Y%m%d-%H%M%S}.jsonl")
    log_run({"kind": "digest", "sent": True, "count": len(entries), "errors": errors})
    return {"sent": True, "count": len(entries), "errors": errors}


if __name__ == "__main__":
    print(json.dumps(main(), ensure_ascii=False))
