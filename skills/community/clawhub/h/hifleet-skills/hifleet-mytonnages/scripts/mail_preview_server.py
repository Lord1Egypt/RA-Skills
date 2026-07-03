#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
原始邮件预览 HTTP 服务（供前端「查看原邮件」按钮跳转）。

启动:
  python scripts/mail_preview_server.py
  python scripts/mail_preview_server.py --host 0.0.0.0 --port 8765

前端:
  GET /api/mail/preview-url?message_id=<urlencoded>
  或直接使用 search / query-by-port 返回的 preview_url 字段
"""

from __future__ import annotations

import argparse
import html
import json
import logging
import re
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from imap_mail import (  # noqa: E402
    build_preview_url,
    fetch_raw_by_preview_token,
    fetch_raw_email,
    get_attachment_part,
    load_preview_config,
    parse_for_preview,
    preview_token_for_message_id,
)
from webmail_locate import build_webmail_locate  # noqa: E402
from mail_reply import (  # noqa: E402
    build_reply_url,
    prepare_reply_draft,
    send_reply_by_token,
    smtp_is_configured,
)

logger = logging.getLogger("mail_preview_server")

_PREVIEW_CFG = load_preview_config()
_PREVIEW_SECRET = _PREVIEW_CFG.get("mail_preview_token") or ""


def _cors_origin() -> str:
    return "*"  # 前端与预览服务常不同端口；生产可改为配置白名单


def _json_response(handler: BaseHTTPRequestHandler, status: int, payload: Any) -> None:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Access-Control-Allow-Origin", _cors_origin())
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _html_response(handler: BaseHTTPRequestHandler, status: int, content: str) -> None:
    body = content.encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "text/html; charset=utf-8")
    handler.send_header("Access-Control-Allow-Origin", _cors_origin())
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _bytes_response(
    handler: BaseHTTPRequestHandler,
    status: int,
    data: bytes,
    content_type: str,
    filename: str = "",
) -> None:
    handler.send_response(status)
    handler.send_header("Content-Type", content_type)
    handler.send_header("Access-Control-Allow-Origin", _cors_origin())
    if filename:
        safe = re.sub(r'[^\w\-. ]', "_", filename)[:200]
        handler.send_header("Content-Disposition", f'inline; filename="{safe}"')
    handler.send_header("Content-Length", str(len(data)))
    handler.end_headers()
    handler.wfile.write(data)


def _check_auth(handler: BaseHTTPRequestHandler) -> bool:
    if not _PREVIEW_SECRET:
        return True
    qs = urllib.parse.parse_qs(urllib.parse.urlparse(handler.path).query)
    qtok = (qs.get("auth") or qs.get("token") or [""])[0]
    header = handler.headers.get("X-HIFLEET-Preview-Token", "")
    return qtok == _PREVIEW_SECRET or header == _PREVIEW_SECRET


def _render_preview_page(token: str, parsed: dict[str, Any], meta: dict[str, Any]) -> str:
    subject = html.escape(parsed.get("subject") or meta.get("subject") or "(无主题)")
    from_addr = html.escape(parsed.get("from_addr") or meta.get("from_addr") or "")
    to_addr = html.escape(parsed.get("to_addr") or "")
    date = html.escape(parsed.get("date") or meta.get("email_date_utc") or "")
    message_id = html.escape(str(meta.get("message_id") or ""))

    att_rows = ""
    for att in parsed.get("attachments") or []:
        name = html.escape(str(att.get("filename") or "attachment"))
        size = int(att.get("size") or 0)
        url = html.escape(str(att.get("url") or ""))
        att_rows += f'<li><a href="{url}" target="_blank" rel="noopener">{name}</a> ({size} bytes)</li>'

    attachments_html = ""
    if att_rows:
        attachments_html = f"<h3>附件</h3><ul>{att_rows}</ul>"

    webmail_btn = ""
    locate = build_webmail_locate(
        message_id=str(meta.get("message_id") or ""),
        from_addr=str(parsed.get("from_addr") or meta.get("from_addr") or ""),
        subject=str(parsed.get("subject") or meta.get("subject") or ""),
        email_date_utc=str(parsed.get("date") or meta.get("email_date_utc") or ""),
    )
    wurl = locate.get("webmail_url") or ""
    if wurl:
        whint = html.escape(str(locate.get("webmail_hint") or ""))
        webmail_btn = (
            f'<p style="margin:12px 0">'
            f'<a class="btn-webmail" href="{html.escape(wurl)}" target="_blank" rel="noopener noreferrer" '
            f'title="{whint}">在网页邮箱中打开</a>'
            f'<span class="hint">（使用浏览器已登录的邮箱；未登录请先登录）</span></p>'
        )
        tiers = locate.get("webmail_search_tiers") or []
        if len(tiers) > 1:
            fallback_rows = ""
            for t in tiers[1:]:
                label = html.escape(str(t.get("label") or t.get("method") or "放宽搜索"))
                q = html.escape(str(t.get("query") or ""))
                tu = html.escape(str(t.get("url") or ""))
                fallback_rows += (
                    f'<li><a href="{tu}" target="_blank" rel="noopener noreferrer">{label}</a>'
                    f'<span class="hint"> — {q}</span></li>'
                )
            webmail_btn += (
                f'<details class="webmail-fallback"><summary>搜不到？尝试放宽搜索（{len(tiers) - 1} 档）</summary>'
                f'<ul>{fallback_rows}</ul></details>'
            )

    reply_actions = ""
    reply_url = html.escape(build_reply_url(token))
    if wurl:
        reply_actions = (
            f'<div class="reply-actions">'
            f'<span class="badge">回复</span> '
            f'<a class="btn-reply" href="{html.escape(wurl)}" target="_blank" rel="noopener noreferrer" '
            f'title="在已登录的网页邮箱中打开原信，使用邮箱自带的「回复」">在网页邮箱中回复</a>'
        )
        if smtp_is_configured():
            reply_actions += (
                f'<a class="btn-reply secondary" href="{reply_url}">或用 SMTP 回复</a>'
            )
        else:
            reply_actions += (
                f'<span class="hint">（系统内 SMTP 回复需配置 smtp_host / smtp_port）</span>'
            )
        reply_actions += "</div>"
    elif smtp_is_configured():
        reply_actions = (
            f'<div class="reply-actions">'
            f'<a class="btn-reply" href="{reply_url}">回复邮件（SMTP）</a>'
            f'<span class="hint">未识别网页邮箱，将使用 SMTP 发送</span></div>'
        )

    html_body = parsed.get("html_body") or ""
    text_body = html.escape(parsed.get("text_body") or "")
    if html_body:
        body_block = (
            f'<div class="mail-html"><iframe sandbox="" srcdoc="{html.escape(html_body, quote=True)}"></iframe></div>'
        )
    elif text_body:
        body_block = f'<pre class="mail-text">{text_body}</pre>'
    else:
        body_block = '<p class="empty">（无正文）</p>'

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>{subject}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; background: #f4f6f8; color: #1a1a1a; }}
    .wrap {{ max-width: 960px; margin: 0 auto; padding: 16px; }}
    .card {{ background: #fff; border-radius: 8px; box-shadow: 0 1px 4px rgba(0,0,0,.08); padding: 20px; }}
    h1 {{ font-size: 1.25rem; margin: 0 0 12px; }}
    .meta {{ font-size: 0.875rem; color: #555; line-height: 1.6; margin-bottom: 16px; }}
    .meta dt {{ font-weight: 600; display: inline; }}
    .meta dd {{ display: inline; margin: 0 16px 0 4px; }}
    .mail-html iframe {{ width: 100%; min-height: 480px; border: 1px solid #e0e0e0; border-radius: 4px; background: #fff; }}
    pre.mail-text {{ white-space: pre-wrap; word-break: break-word; background: #fafafa; padding: 12px; border-radius: 4px; border: 1px solid #eee; }}
    ul {{ padding-left: 1.2rem; }}
    .badge {{ display: inline-block; background: #e8f0fe; color: #1967d2; font-size: 12px; padding: 2px 8px; border-radius: 4px; }}
    .btn-webmail {{ display: inline-block; background: #fff; border: 1px solid #1967d2; color: #1967d2; padding: 6px 14px; border-radius: 4px; text-decoration: none; font-size: 14px; }}
    .btn-webmail:hover {{ background: #e8f0fe; }}
    .hint {{ font-size: 12px; color: #666; margin-left: 8px; }}
    .webmail-fallback {{ margin: 8px 0 16px; font-size: 13px; }}
    .webmail-fallback summary {{ cursor: pointer; color: #1967d2; }}
    .webmail-fallback ul {{ margin: 8px 0 0; padding-left: 1.2rem; }}
    .btn-reply {{ display: inline-block; background: #1967d2; color: #fff; padding: 6px 14px; border-radius: 4px; text-decoration: none; font-size: 14px; margin-right: 8px; }}
    .btn-reply.secondary {{ background: #fff; color: #1967d2; border: 1px solid #1967d2; }}
    .reply-actions {{ margin: 12px 0; }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <p><span class="badge">原始邮件</span></p>
      {webmail_btn}
      {reply_actions}
      <h1>{subject}</h1>
      <dl class="meta">
        <dt>发件人</dt><dd>{from_addr}</dd>
        <dt>收件人</dt><dd>{to_addr or "—"}</dd>
        <dt>时间</dt><dd>{date}</dd>
      </dl>
      {attachments_html}
      <h3>正文</h3>
      {body_block}
      <p class="meta" style="margin-top:24px"><small>Message-ID: {message_id}</small></p>
    </div>
  </div>
</body>
</html>"""


def _render_reply_page(token: str, draft: dict[str, Any]) -> str:
    to_addr = html.escape(str(draft.get("to") or ""))
    subject = html.escape(str(draft.get("subject") or ""))
    from_email = html.escape(str(draft.get("from_email") or ""))
    preview_url = html.escape(f"/mail/preview/{token}")
    wurl = html.escape(str((draft.get("webmail") or {}).get("webmail_url") or ""))
    webmail_link = ""
    if wurl:
        webmail_link = (
            f'<p><a class="btn-webmail" href="{wurl}" target="_blank" rel="noopener noreferrer">'
            f"优先：在网页邮箱中打开并回复</a></p>"
        )
    smtp_note = ""
    if not draft.get("smtp_configured"):
        smtp_note = '<p class="hint">未配置 SMTP，无法从此页发送。请配置 smtp_host、smtp_port，或使用上方网页邮箱回复。</p>'
    quote_hint = html.escape(str(draft.get("quote_suffix") or "")[:200])

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>回复 — {subject}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 0; background: #f4f6f8; }}
    .wrap {{ max-width: 720px; margin: 0 auto; padding: 16px; }}
    .card {{ background: #fff; border-radius: 8px; padding: 20px; box-shadow: 0 1px 4px rgba(0,0,0,.08); }}
    label {{ display: block; font-size: 13px; color: #555; margin: 12px 0 4px; }}
    input, textarea {{ width: 100%; box-sizing: border-box; padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 4px; }}
    textarea {{ min-height: 200px; }}
    .actions {{ margin-top: 16px; }}
    button {{ background: #1967d2; color: #fff; border: none; padding: 10px 20px; border-radius: 4px; font-size: 14px; cursor: pointer; }}
    .hint {{ font-size: 12px; color: #666; }}
    .btn-webmail {{ color: #1967d2; }}
    a {{ color: #1967d2; }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      <p><a href="{preview_url}">← 返回原邮件预览</a></p>
      <h1>回复邮件（SMTP）</h1>
      {webmail_link}
      {smtp_note}
      <form method="post" action="/api/mail/send-reply">
        <input type="hidden" name="preview_token" value="{html.escape(token)}"/>
        <label>发件人</label>
        <input type="text" value="{from_email}" readonly/>
        <label>收件人</label>
        <input type="text" name="to" value="{to_addr}" readonly/>
        <label>主题</label>
        <input type="text" name="subject" value="{subject}"/>
        <label>正文</label>
        <textarea name="body" placeholder="输入回复内容…" required></textarea>
        <label><input type="checkbox" name="include_quote" value="1" checked/> 附上引用原文</label>
        <p class="hint">引用预览：{quote_hint}…</p>
        <div class="actions">
          <button type="submit" {"disabled" if not draft.get("smtp_configured") else ""}>发送回复</button>
        </div>
      </form>
    </div>
  </div>
</body>
</html>"""


class MailPreviewHandler(BaseHTTPRequestHandler):
    server_version = "HiFleetMailPreview/1.0"

    def log_message(self, fmt: str, *args: Any) -> None:
        logger.info("%s - %s", self.address_string(), fmt % args)

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", _cors_origin())
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "X-HIFLEET-Preview-Token, Content-Type")
        self.end_headers()

    def _read_post_body(self) -> tuple[dict[str, str], dict[str, Any]]:
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b""
        ctype = (self.headers.get("Content-Type") or "").split(";")[0].strip().lower()
        if ctype == "application/json":
            try:
                data = json.loads(raw.decode("utf-8") or "{}")
                if isinstance(data, dict):
                    return {k: str(v) for k, v in data.items()}, data
            except json.JSONDecodeError:
                pass
        # application/x-www-form-urlencoded
        form = urllib.parse.parse_qs(raw.decode("utf-8", errors="replace"))
        flat = {k: (v[0] if v else "") for k, v in form.items()}
        return flat, flat

    def do_POST(self) -> None:
        if not _check_auth(self):
            _json_response(self, 401, {"ok": False, "error": "unauthorized"})
            return
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path.rstrip("/") or "/"
        if path != "/api/mail/send-reply":
            _json_response(self, 404, {"ok": False, "error": "not found"})
            return
        try:
            flat, _raw = self._read_post_body()
            token = (flat.get("preview_token") or "").strip()
            body = flat.get("body") or ""
            subject = flat.get("subject") or ""
            include_quote = flat.get("include_quote") in ("1", "true", "True", "on", "yes")
            if not token:
                _json_response(self, 400, {"ok": False, "error": "preview_token required"})
                return
            if not body.strip():
                _json_response(self, 400, {"ok": False, "error": "body required"})
                return
            result = send_reply_by_token(
                token,
                body,
                subject=subject,
                include_quote=include_quote,
            )
            accept = (self.headers.get("Accept") or "").lower()
            if "application/json" in accept or flat.get("_json"):
                _json_response(self, 200 if result.get("ok") else 400, result)
                return
            if result.get("ok"):
                page = (
                    f"<html><body><h1>已发送</h1><p>收件人：{html.escape(str(result.get('to')))}</p>"
                    f'<p><a href="/mail/preview/{html.escape(token)}">返回预览</a></p></body></html>'
                )
                _html_response(self, 200, page)
            else:
                err = html.escape(str(result.get("hint") or result.get("error") or "send failed"))
                if result.get("webmail_url"):
                    w = html.escape(str(result["webmail_url"]))
                    err += f'<p><a href="{w}" target="_blank">在网页邮箱中回复</a></p>'
                _html_response(self, 400, f"<html><body><h1>发送失败</h1><p>{err}</p></body></html>")
        except Exception as e:
            logger.exception("send-reply failed")
            _json_response(self, 500, {"ok": False, "error": str(e)})

    def do_GET(self) -> None:
        if not _check_auth(self):
            _json_response(self, 401, {"ok": False, "error": "unauthorized"})
            return

        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path.rstrip("/") or "/"
        qs = urllib.parse.parse_qs(parsed_path.query)

        try:
            if path == "/health":
                _json_response(self, 200, {"ok": True, "service": "mail_preview"})
                return

            if path == "/api/mail/preview-url":
                mid = (qs.get("message_id") or [""])[0]
                if not mid:
                    _json_response(self, 400, {"ok": False, "error": "message_id required"})
                    return
                url = build_preview_url(mid)
                from_addr = (qs.get("from_addr") or [""])[0]
                subject = (qs.get("subject") or [""])[0]
                date_u = (qs.get("email_date_utc") or [""])[0]
                locate = build_webmail_locate(
                    message_id=mid,
                    from_addr=from_addr,
                    subject=subject,
                    email_date_utc=date_u,
                )
                _json_response(
                    self,
                    200,
                    {
                        "ok": True,
                        "message_id": mid,
                        "preview_token": preview_token_for_message_id(mid),
                        "preview_url": url,
                        **locate,
                    },
                )
                return

            if path == "/api/mail/webmail-url":
                mid = (qs.get("message_id") or [""])[0]
                from_addr = (qs.get("from_addr") or [""])[0]
                subject = (qs.get("subject") or [""])[0]
                date_u = (qs.get("email_date_utc") or [""])[0]
                locate = build_webmail_locate(
                    message_id=mid,
                    from_addr=from_addr,
                    subject=subject,
                    email_date_utc=date_u,
                )
                if not locate.get("webmail_url"):
                    _json_response(self, 404, {"ok": False, **locate})
                    return
                _json_response(self, 200, {"ok": True, **locate})
                return

            m = re.match(r"^/mail/reply/([a-f0-9]{32})$", path)
            if m:
                token = m.group(1)
                draft = prepare_reply_draft(token)
                page = _render_reply_page(token, draft)
                _html_response(self, 200, page)
                return

            m = re.match(r"^/api/mail/reply-draft/([a-f0-9]{32})$", path)
            if m:
                draft = prepare_reply_draft(m.group(1))
                _json_response(self, 200, {"ok": True, **draft})
                return

            m = re.match(r"^/mail/preview/([a-f0-9]{32})$", path)
            if m:
                token = m.group(1)
                raw, meta = fetch_raw_by_preview_token(token)
                parsed = parse_for_preview(raw, token)
                page = _render_preview_page(token, parsed, meta)
                _html_response(self, 200, page)
                return

            m = re.match(r"^/mail/attachment/([a-f0-9]{32})/(\d+)$", path)
            if m:
                token = m.group(1)
                part_index = int(m.group(2))
                raw, _meta = fetch_raw_by_preview_token(token)
                part, filename, ctype = get_attachment_part(raw, part_index)
                data = part.get_payload(decode=True) or b""
                _bytes_response(self, 200, data, ctype, filename)
                return

            m = re.match(r"^/api/mail/raw/([a-f0-9]{32})$", path)
            if m:
                token = m.group(1)
                raw, meta = fetch_raw_by_preview_token(token)
                parsed = parse_for_preview(raw, token)
                _json_response(
                    self,
                    200,
                    {"ok": True, "meta": meta, "preview": parsed},
                )
                return

            if path == "/api/mail/fetch":
                mid = (qs.get("message_id") or [""])[0]
                if not mid:
                    _json_response(self, 400, {"ok": False, "error": "message_id required"})
                    return
                raw, meta = fetch_raw_email(mid)
                token = preview_token_for_message_id(mid)
                parsed = parse_for_preview(raw, token)
                _json_response(self, 200, {"ok": True, "meta": meta, "preview": parsed})
                return

            _json_response(self, 404, {"ok": False, "error": "not found"})
        except FileNotFoundError as e:
            _html_response(
                self,
                404,
                f"<html><body><h1>邮件未找到</h1><p>{html.escape(str(e))}</p></body></html>",
            )
        except ValueError as e:
            _json_response(self, 400, {"ok": False, "error": str(e)})
        except Exception as e:
            logger.exception("request failed: %s", self.path)
            _json_response(self, 500, {"ok": False, "error": str(e)})


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    cfg = load_preview_config()
    p = argparse.ArgumentParser(description="HiFleet 原始邮件预览服务")
    p.add_argument("--host", default=cfg["mail_preview_host"])
    p.add_argument("--port", type=int, default=cfg["mail_preview_port"])
    args = p.parse_args(argv)

    server = ThreadingHTTPServer((args.host, args.port), MailPreviewHandler)
    base = cfg["mail_preview_base_url"]
    logger.info("邮件预览服务: http://%s:%s  (对外 base: %s)", args.host, args.port, base)
    logger.info("示例: %s/mail/preview/<token>  |  API: %s/api/mail/preview-url?message_id=...", base, base)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("已停止")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
