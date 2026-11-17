#!/usr/bin/env python3
"""行动层：Telegram 推送。P1 实时、日摘要、故障告警共用 send()。

凭证来源（两道门都在 common.py 里强制，不是文档约定）：
  1. token 取 env `TELEGRAM_BOT_TOKEN`、chat_id 取 env/config——也就是**你自己填的**；
  2. 只有额外显式设了 `JOBWATCH_ALLOW_HOST_CREDS=1`，才会回落到宿主
     `openclaw.json` 的 bot token / `allowFrom` 名单，且每次读取都会往 stderr
     打一行指名读了哪一把。没设这个开关又没自己填，`telegram_token()` /
     `telegram_chat_id()` 直接抛错，不会静默借用宿主凭证。
另外每次发送前还要过 `require_egress_consent("telegram")`，没出网许可同样直接抛错。

消息模板（script 钉死）：标题 + 摘要 + 来源 + 2brain 提问入口 + 原文链接。
"""
import html
import json
import sys

from common import (CONFIG, http_json, kb_hint, require_egress_consent,
                    telegram_chat_id, telegram_token)


def send(text, disable_preview=True):
    """Send one message. Returns message_id."""
    require_egress_consent("telegram", "the notification message body")
    # Resolved explicitly (rather than inline in the request) so the enforcement
    # order is visible here: egress consent first, then credentials — and both
    # raise rather than proceed. telegram_token()/telegram_chat_id() only reach
    # outside this skill's own .env when JOBWATCH_ALLOW_HOST_CREDS=1; see common.py.
    token = telegram_token()
    chat_id = telegram_chat_id()
    resp = http_json(
        f"https://api.telegram.org/bot{token}/sendMessage",
        method="POST",
        json_body={
            "chat_id": chat_id,
            "text": text[:4000],
            "parse_mode": "HTML",
            "disable_web_page_preview": disable_preview,
        },
    )
    if not resp.get("ok"):
        raise RuntimeError(f"telegram send failed: {resp}")
    return resp["result"]["message_id"]


def render_p1(item, judgment):
    e = html.escape
    tags = " ".join(e(t) for t in judgment.get("tags", []))
    return (
        f"🎯 <b>P1 · Kill Shot</b>\n"
        f"<b>{e(item['company'])} — {e(item['title'])}</b>\n"
        f"📍 {e(item['location'] or 'N/A')}\n\n"
        f"{e(judgment['summary_zh'])}\n\n"
        f"{tags}\n"
        f"判断：{e(judgment['reasons'])}\n\n"
        f"🔗 <a href=\"{e(item['detail_url'])}\">原文（投递入口）</a>\n"
        f"🧠 {e(kb_hint())}\n"
        f"来源：{e(item['source'])} · JobWatcher"
    )


def send_p1(item, judgment):
    return send(render_p1(item, judgment))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('usage: notify_telegram.py "<text>"')
    print(json.dumps({"message_id": send(" ".join(sys.argv[1:]))}))


def render_p1_plain(item, judgment):
    """渠道无关的纯文本版（outbox/agent 播报用）。"""
    tags = " ".join(judgment.get("tags", []))
    return (f"🎯 P1 · Kill Shot\n"
            f"{item['company']} — {item['title']}\n"
            f"📍 {item['location'] or 'N/A'}\n\n"
            f"{judgment['summary_zh']}\n\n{tags}\n"
            f"判断：{judgment['reasons']}\n"
            f"原文（投递入口）：{item['detail_url']}\n"
            f"来源：{item['source']} · JobWatcher")
