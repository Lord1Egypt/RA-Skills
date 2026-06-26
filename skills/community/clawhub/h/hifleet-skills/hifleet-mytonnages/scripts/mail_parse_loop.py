#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
路由 A 邮件定时解析：IMAP 增量拉取 →（可选 LLM 解析）→ save → enrich。

默认每 10 分钟一轮（config mail_parse_interval_minutes / HIFLEET_MAIL_PARSE_INTERVAL_MINUTES）。
OpenClaw 宿主可用计划任务执行 `python scripts/mail_parse_loop.py --once` 或 `--daemon`。
"""

from __future__ import annotations

import argparse
import base64
import email
import hashlib
import imaplib
import json
import logging
import os
import sys
import time
import traceback
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, Optional

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from charter_facts_tool import (  # noqa: E402
    CharterFactsDB,
    default_db_path,
    default_skill_dir,
    enrich_database,
)
from desensitize_for_llm import desensitize_for_llm  # noqa: E402

logger = logging.getLogger("mail_parse_loop")


def _load_config() -> dict[str, Any]:
    cfg_path = default_skill_dir() / "config.json"
    if not cfg_path.is_file():
        return {}
    try:
        data = json.loads(cfg_path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _interval_minutes(cfg: dict[str, Any]) -> int:
    env = os.environ.get("HIFLEET_MAIL_PARSE_INTERVAL_MINUTES", "").strip()
    if env:
        try:
            return max(1, int(env))
        except ValueError:
            pass
    try:
        return max(1, int(cfg.get("mail_parse_interval_minutes") or 10))
    except (TypeError, ValueError):
        return 10


def _decode_password(raw: str) -> str:
    if not raw:
        return ""
    s = str(raw).strip()
    if s.startswith("base64:"):
        try:
            return base64.b64decode(s[7:]).decode("utf-8")
        except Exception:
            return s[7:]
    return s


def _state_path() -> Path:
    return default_skill_dir() / "mail_parse_state.json"


def _load_state() -> dict[str, Any]:
    p = _state_path()
    if not p.is_file():
        return {}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def _save_state(state: dict[str, Any]) -> None:
    p = _state_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    state["last_run_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    p.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def _pending_dir() -> Path:
    d = default_skill_dir() / "mail_pending"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _parsed_inbox_dir() -> Path:
    d = default_skill_dir() / "mail_parsed_inbox"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _message_id_from_raw(raw: bytes) -> str:
    msg = email.message_from_bytes(raw, policy=email.policy.default)
    mid = (msg.get("Message-ID") or msg.get("Message-Id") or "").strip()
    if mid:
        return mid
    digest = hashlib.sha256(raw).hexdigest()[:32]
    return f"generated-{digest}@local"


def _email_date_utc(msg: email.message.Message) -> str:
    for hdr in ("Date", "Received"):
        val = msg.get(hdr)
        if not val:
            continue
        try:
            dt = parsedate_to_datetime(val)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            else:
                dt = dt.astimezone(timezone.utc)
            return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        except (TypeError, ValueError, IndexError):
            continue
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _from_addr(msg: email.message.Message) -> str:
    return (msg.get("From") or "").strip()


def _subject(msg: email.message.Message) -> str:
    raw = msg.get("Subject") or ""
    try:
        from email.header import decode_header

        parts = decode_header(raw)
        out = []
        for frag, enc in parts:
            if isinstance(frag, bytes):
                out.append(frag.decode(enc or "utf-8", errors="replace"))
            else:
                out.append(str(frag))
        return "".join(out).strip()
    except Exception:
        return str(raw).strip()


def _body_text(msg: email.message.Message) -> str:
    if msg.is_multipart():
        chunks: list[str] = []
        for part in msg.walk():
            if part.get_content_maintype() == "multipart":
                continue
            if part.get_content_disposition() == "attachment":
                continue
            ctype = (part.get_content_type() or "").lower()
            if ctype not in ("text/plain", "text/html"):
                continue
            payload = part.get_payload(decode=True)
            if not payload:
                continue
            charset = part.get_content_charset() or "utf-8"
            try:
                chunks.append(payload.decode(charset, errors="replace"))
            except Exception:
                chunks.append(payload.decode("utf-8", errors="replace"))
        return "\n".join(chunks)
    payload = msg.get_payload(decode=True)
    if not payload:
        return str(msg.get_payload() or "")
    charset = msg.get_content_charset() or "utf-8"
    try:
        return payload.decode(charset, errors="replace")
    except Exception:
        return payload.decode("utf-8", errors="replace")


def _known_message_ids(db_path: Path) -> set[str]:
    db = CharterFactsDB(db_path)
    conn = db.connect()
    ids: set[str] = set()
    try:
        db.init(conn)
        cur = conn.cursor()
        for table in ("cargo_plate", "openvessel_plate", "mail_unknown"):
            cur.execute(f"SELECT DISTINCT message_id FROM {table}")
            for row in cur.fetchall():
                if row and row[0]:
                    ids.add(str(row[0]))
    finally:
        conn.close()
    return ids


def _imap_fetch_new(cfg: dict[str, Any], state: dict[str, Any]) -> list[dict[str, Any]]:
    host = str(cfg.get("imap_host") or "").strip()
    user = str(cfg.get("email") or cfg.get("imap_user") or "").strip()
    password = _decode_password(str(cfg.get("email_password") or cfg.get("imap_password") or ""))
    port = int(cfg.get("imap_port") or 993)
    if not host or not user or not password:
        logger.warning("IMAP 配置不完整，跳过拉取")
        return []

    last_uid = int(state.get("last_imap_uid") or 0)
    out: list[dict[str, Any]] = []
    max_uid = last_uid

    with imaplib.IMAP4_SSL(host, port) as mail:
        mail.login(user, password)
        mail.select("INBOX")
        if last_uid <= 0:
            status, data = mail.uid("search", None, "ALL")
            if status != "OK" or not data or not data[0]:
                return []
            uids = data[0].split()
            if uids:
                last_uid = int(uids[-1])
                state["last_imap_uid"] = last_uid
                logger.info("IMAP 初始化 last_uid=%s", last_uid)
            return []

        criteria = f"UID {last_uid + 1}:*"
        status, data = mail.uid("search", None, criteria)
        if status != "OK" or not data or not data[0]:
            return []
        for uid_b in data[0].split():
            uid = int(uid_b)
            if uid <= last_uid:
                continue
            status, msg_data = mail.uid("fetch", uid_b, "(RFC822)")
            if status != "OK" or not msg_data or not msg_data[0]:
                max_uid = max(max_uid, uid)
                continue
            raw = msg_data[0][1]
            if not isinstance(raw, (bytes, bytearray)):
                max_uid = max(max_uid, uid)
                continue
            msg = email.message_from_bytes(raw, policy=email.policy.default)
            body = _body_text(msg)
            out.append(
                {
                    "imap_uid": uid,
                    "message_id": _message_id_from_raw(raw),
                    "email_date_utc": _email_date_utc(msg),
                    "from_addr": _from_addr(msg),
                    "subject": _subject(msg),
                    "body_text": body,
                    "body_for_llm": desensitize_for_llm(f"{_subject(msg)}\n\n{body}"),
                }
            )
            max_uid = max(max_uid, uid)

    state["last_imap_uid"] = max_uid
    return out


def _try_charter_ai_parse(email_doc: dict[str, Any]) -> Optional[dict[str, Any]]:
    """若同机存在 charter_ai，则调用大模型解析；否则返回 None。"""
    root = os.environ.get("HIFLEET_CHARTER_AI_ROOT", "").strip()
    if not root:
        candidate = default_skill_dir().parents[2] / "charter_ai"
        if candidate.is_dir():
            root = str(candidate)
    if not root:
        return None
    if root not in sys.path:
        sys.path.insert(0, root)
    try:
        from charter_utils import call_charter_deepseek_api  # type: ignore
    except ImportError:
        return None
    try:
        data = call_charter_deepseek_api(
            email_doc.get("body_for_llm") or "",
            attachments=[],
            from_email=email_doc.get("from_addr") or "",
        )
        if isinstance(data, dict):
            return data
    except Exception as e:
        logger.error("charter_ai 解析失败: %s", e)
        logger.debug(traceback.format_exc())
    return None


def _save_parsed_doc(db_path: Path, doc: dict[str, Any]) -> None:
    db = CharterFactsDB(db_path)
    conn = db.connect()
    try:
        parsed = doc.get("parsed") or doc
        db.save_parsed(
            conn,
            message_id=str(doc.get("message_id") or ""),
            email_date_utc=str(doc.get("email_date_utc") or ""),
            from_addr=str(doc.get("from_addr") or ""),
            subject=str(doc.get("subject") or ""),
            parsed=parsed if isinstance(parsed, dict) else {},
        )
    finally:
        conn.close()


def _write_pending(email_doc: dict[str, Any]) -> None:
    mid = email_doc.get("message_id") or "unknown"
    safe = hashlib.sha256(mid.encode("utf-8")).hexdigest()[:16]
    path = _pending_dir() / f"{safe}.json"
    if path.is_file():
        return
    path.write_text(json.dumps(email_doc, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info("待解析邮件已写入 %s", path.name)


def _process_parsed_inbox(db_path: Path) -> int:
    count = 0
    inbox = _parsed_inbox_dir()
    for path in sorted(inbox.glob("*.json")):
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(doc, dict):
                continue
            _save_parsed_doc(db_path, doc)
            path.unlink(missing_ok=True)
            count += 1
            logger.info("已入库 %s", doc.get("message_id"))
        except Exception as e:
            logger.error("处理 %s 失败: %s", path.name, e)
    return count


def run_cycle(*, skip_imap: bool = False, skip_enrich: bool = False) -> dict[str, Any]:
    cfg = _load_config()
    state = _load_state()
    db_path = default_db_path()
    stats: dict[str, Any] = {
        "fetched": 0,
        "parsed_inline": 0,
        "pending_written": 0,
        "inbox_saved": 0,
        "enrich": None,
        "errors": [],
    }

    known = _known_message_ids(db_path)

    if not skip_imap:
        try:
            emails = _imap_fetch_new(cfg, state)
        except Exception as e:
            logger.error("IMAP 拉取失败: %s", e)
            stats["errors"].append(f"imap: {e}")
            emails = []
        stats["fetched"] = len(emails)
        for doc in emails:
            mid = doc.get("message_id")
            if mid and mid in known:
                continue
            parsed = _try_charter_ai_parse(doc)
            if parsed:
                save_doc = {
                    "message_id": mid,
                    "email_date_utc": doc.get("email_date_utc"),
                    "from_addr": doc.get("from_addr"),
                    "subject": doc.get("subject"),
                    "parsed": parsed,
                }
                try:
                    _save_parsed_doc(db_path, save_doc)
                    stats["parsed_inline"] += 1
                    if mid:
                        known.add(mid)
                except Exception as e:
                    stats["errors"].append(f"save {mid}: {e}")
            else:
                _write_pending(doc)
                stats["pending_written"] += 1

    stats["inbox_saved"] = _process_parsed_inbox(db_path)

    if not skip_enrich:
        try:
            stats["enrich"] = enrich_database(db_path)
        except Exception as e:
            stats["errors"].append(f"enrich: {e}")
            stats["enrich"] = {"ok": False, "error": str(e)}

    _save_state(state)
    stats["ok"] = not stats["errors"]
    return stats


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    p = argparse.ArgumentParser(description="路由 A 邮件定时解析（IMAP → save → enrich）")
    p.add_argument("--once", action="store_true", help="执行一轮后退出（计划任务推荐）")
    p.add_argument("--daemon", action="store_true", help="循环执行，间隔见 config / 环境变量")
    p.add_argument("--skip-imap", action="store_true", help="跳过 IMAP，仅处理 mail_parsed_inbox 并 enrich")
    p.add_argument("--skip-enrich", action="store_true", help="跳过 enrich")
    args = p.parse_args(argv)

    if args.daemon:
        cfg = _load_config()
        interval = _interval_minutes(cfg) * 60
        logger.info("守护模式启动，间隔 %s 秒", interval)
        while True:
            result = run_cycle(skip_imap=args.skip_imap, skip_enrich=args.skip_enrich)
            logger.info("本轮完成: %s", json.dumps(result, ensure_ascii=False))
            time.sleep(interval)
        return 0

    result = run_cycle(skip_imap=args.skip_imap, skip_enrich=args.skip_enrich)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("ok", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
