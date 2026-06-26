#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bottle Drift relay server with a built-in web dashboard.
Standard library only.
"""
from __future__ import annotations

import argparse
import html
import json
import mimetypes
import random
import secrets
import sqlite3
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, List
from urllib.parse import parse_qs, urlparse

BASE_DIR = Path(__file__).resolve().parent.parent
RESOURCE_DIR = BASE_DIR / "resources"
REPLY_TEMPLATE_PATH = RESOURCE_DIR / "reply_page.html"
DASHBOARD_PATH = RESOURCE_DIR / "dashboard.html"
DASHBOARD_JS_PATH = RESOURCE_DIR / "dashboard.js"
MESSAGE_SCHEMA_PATH = RESOURCE_DIR / "message_schema.json"
DEFAULT_DB_PATH = BASE_DIR / "bottle_drift.sqlite3"

ONLINE_WINDOW_SECONDS = 120
HEARTBEAT_INTERVAL_SECONDS = 30
MAX_MESSAGE_LEN = 240
MAX_NAME_LEN = 40
MAX_USER_ID_LEN = 40
MAX_FANOUT = 3
DEFAULT_TTL = 86400
MAX_TTL = 7 * 24 * 3600
SEND_RATE_LIMIT_PER_MINUTE = 5
REPLY_RATE_LIMIT_PER_MINUTE = 8
BAD_WORDS = {"spam", "诈骗", "辱骂示例词"}


def now_ts() -> int:
    return int(time.time())


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def ensure_paths() -> None:
    required = [
        REPLY_TEMPLATE_PATH,
        DASHBOARD_PATH,
        DASHBOARD_JS_PATH,
        MESSAGE_SCHEMA_PATH,
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing resources: " + ", ".join(missing))


def html_escape(value: Any) -> str:
    return html.escape(str(value))


def clamp(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(value, maximum))


def contains_blocked_word(text: str) -> bool:
    lowered = text.lower()
    return any(word.lower() in lowered for word in BAD_WORDS)


def iso_time(ts: int) -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))


def json_response(handler: BaseHTTPRequestHandler, code: int, payload: Dict[str, Any]) -> None:
    raw = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    handler.send_response(code)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Cache-Control", "no-store")
    handler.send_header("Content-Length", str(len(raw)))
    handler.end_headers()
    handler.wfile.write(raw)


def html_response(handler: BaseHTTPRequestHandler, code: int, body: str) -> None:
    raw = body.encode("utf-8")
    handler.send_response(code)
    handler.send_header("Content-Type", "text/html; charset=utf-8")
    handler.send_header("Cache-Control", "no-store")
    handler.send_header("Content-Length", str(len(raw)))
    handler.end_headers()
    handler.wfile.write(raw)


def static_response(handler: BaseHTTPRequestHandler, path: Path) -> None:
    raw = path.read_bytes()
    mime, _ = mimetypes.guess_type(str(path))
    handler.send_response(200)
    handler.send_header("Content-Type", mime or "application/octet-stream")
    handler.send_header("Cache-Control", "no-store")
    handler.send_header("Content-Length", str(len(raw)))
    handler.end_headers()
    handler.wfile.write(raw)


def bad_request(handler: BaseHTTPRequestHandler, message: str, code: int = 400) -> None:
    json_response(handler, code, {"ok": False, "error": message})


def validate_user_id(user_id: str, field_name: str = "user_id") -> str:
    value = user_id.strip()
    if not value:
        raise ValueError(f"{field_name} is required")
    if len(value) > MAX_USER_ID_LEN:
        raise ValueError(f"{field_name} must be <= {MAX_USER_ID_LEN} chars")
    for ch in value:
        if not (ch.isalnum() or ch in ("-", "_")):
            raise ValueError(f"{field_name} may only contain letters, numbers, '-' and '_'")
    return value


def validate_name(name: str, field_name: str) -> str:
    value = name.strip()
    if not value:
        raise ValueError(f"{field_name} is required")
    if len(value) > MAX_NAME_LEN:
        raise ValueError(f"{field_name} must be <= {MAX_NAME_LEN} chars")
    return value


def validate_message(text: str, field_name: str) -> str:
    value = text.strip()
    if not value:
        raise ValueError(f"{field_name} is required")
    if len(value) > MAX_MESSAGE_LEN:
        raise ValueError(f"{field_name} must be <= {MAX_MESSAGE_LEN} chars")
    if contains_blocked_word(value):
        raise PermissionError(f"{field_name} contains blocked words")
    return value


class RelayDB:
    def __init__(self, db_path: Path, base_url: str) -> None:
        self.db_path = db_path
        self.base_url = base_url.rstrip("/")
        self.conn = sqlite3.connect(str(db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.init_db()

    def init_db(self) -> None:
        cur = self.conn.cursor()
        cur.executescript(
            """
            PRAGMA journal_mode=WAL;

            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                display_name TEXT NOT NULL,
                callback_url TEXT,
                accept_bottles INTEGER NOT NULL DEFAULT 1,
                last_seen INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS rate_limits (
                action TEXT NOT NULL,
                actor_id TEXT NOT NULL,
                ts INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS bottles (
                bottle_id TEXT PRIMARY KEY,
                sender_id TEXT NOT NULL,
                sender_name TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at INTEGER NOT NULL,
                expires_at INTEGER NOT NULL,
                fanout INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS deliveries (
                delivery_id TEXT PRIMARY KEY,
                bottle_id TEXT NOT NULL,
                recipient_id TEXT NOT NULL,
                reply_token TEXT NOT NULL UNIQUE,
                delivered_at INTEGER NOT NULL,
                expires_at INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS replies (
                reply_id TEXT PRIMARY KEY,
                bottle_id TEXT NOT NULL,
                delivery_id TEXT NOT NULL UNIQUE,
                sender_id TEXT NOT NULL,
                recipient_id TEXT NOT NULL,
                replier_name TEXT NOT NULL,
                reply_text TEXT NOT NULL,
                created_at INTEGER NOT NULL
            );
            """
        )
        self.conn.commit()

    def log_action(self, action: str, actor_id: str) -> None:
        self.conn.execute(
            "INSERT INTO rate_limits(action, actor_id, ts) VALUES (?, ?, ?)",
            (action, actor_id, now_ts()),
        )
        self.conn.commit()

    def count_recent_actions(self, action: str, actor_id: str, within_seconds: int) -> int:
        cutoff = now_ts() - within_seconds
        row = self.conn.execute(
            "SELECT COUNT(*) AS c FROM rate_limits WHERE action=? AND actor_id=? AND ts>=?",
            (action, actor_id, cutoff),
        ).fetchone()
        return int(row["c"]) if row else 0

    def heartbeat(
        self,
        user_id: str,
        display_name: str,
        callback_url: str | None,
        accept_bottles: bool,
    ) -> Dict[str, Any]:
        ts = now_ts()
        self.conn.execute(
            """
            INSERT INTO users(user_id, display_name, callback_url, accept_bottles, last_seen)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                display_name=excluded.display_name,
                callback_url=excluded.callback_url,
                accept_bottles=excluded.accept_bottles,
                last_seen=excluded.last_seen
            """,
            (user_id, display_name, callback_url, 1 if accept_bottles else 0, ts),
        )
        self.conn.commit()
        return {
            "ok": True,
            "user_id": user_id,
            "display_name": display_name,
            "accept_bottles": bool(accept_bottles),
            "last_seen": ts,
            "heartbeat_interval_seconds": HEARTBEAT_INTERVAL_SECONDS,
        }

    def online_users(self, exclude_user_id: str | None = None) -> List[Dict[str, Any]]:
        cutoff = now_ts() - ONLINE_WINDOW_SECONDS
        if exclude_user_id:
            rows = self.conn.execute(
                """
                SELECT user_id, display_name, callback_url, accept_bottles, last_seen
                FROM users
                WHERE accept_bottles=1 AND last_seen>=? AND user_id<>?
                ORDER BY last_seen DESC
                """,
                (cutoff, exclude_user_id),
            ).fetchall()
        else:
            rows = self.conn.execute(
                """
                SELECT user_id, display_name, callback_url, accept_bottles, last_seen
                FROM users
                WHERE accept_bottles=1 AND last_seen>=?
                ORDER BY last_seen DESC
                """,
                (cutoff,),
            ).fetchall()
        output = []
        for row in rows:
            item = dict(row)
            item["last_seen_text"] = iso_time(int(item["last_seen"]))
            output.append(item)
        return output

    def create_bottle(
        self,
        sender_id: str,
        sender_name: str,
        message: str,
        fanout: int,
        ttl_seconds: int,
    ) -> Dict[str, Any]:
        if self.count_recent_actions("send", sender_id, 60) >= SEND_RATE_LIMIT_PER_MINUTE:
            raise ValueError("send rate limit exceeded; try again later")

        recipients = self.online_users(exclude_user_id=sender_id)
        if not recipients:
            raise LookupError("no online subscribers available")

        fanout = clamp(fanout, 1, MAX_FANOUT)
        ttl_seconds = clamp(ttl_seconds, 60, MAX_TTL)
        selected = random.sample(recipients, k=min(fanout, len(recipients)))

        bottle_id = "btl_" + secrets.token_hex(8)
        created_at = now_ts()
        expires_at = created_at + ttl_seconds
        self.conn.execute(
            """
            INSERT INTO bottles(bottle_id, sender_id, sender_name, message, created_at, expires_at, fanout)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (bottle_id, sender_id, sender_name, message, created_at, expires_at, len(selected)),
        )

        deliveries = []
        for recipient in selected:
            delivery_id = "dly_" + secrets.token_hex(8)
            reply_token = "rpl_" + secrets.token_hex(12)
            self.conn.execute(
                """
                INSERT INTO deliveries(delivery_id, bottle_id, recipient_id, reply_token, delivered_at, expires_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (delivery_id, bottle_id, recipient["user_id"], reply_token, created_at, expires_at),
            )
            deliveries.append(
                {
                    "delivery_id": delivery_id,
                    "recipient_id": recipient["user_id"],
                    "recipient_name": recipient["display_name"],
                    "reply_token": reply_token,
                    "reply_url": f"{self.base_url}/r/{reply_token}",
                    "delivered_at": created_at,
                    "delivered_at_text": iso_time(created_at),
                }
            )

        self.conn.commit()
        self.log_action("send", sender_id)
        return {
            "ok": True,
            "bottle_id": bottle_id,
            "created_at": created_at,
            "created_at_text": iso_time(created_at),
            "expires_at": expires_at,
            "expires_at_text": iso_time(expires_at),
            "deliveries": deliveries,
        }

    def get_delivery_by_token(self, token: str) -> sqlite3.Row | None:
        return self.conn.execute(
            """
            SELECT
                d.delivery_id,
                d.reply_token,
                d.recipient_id,
                d.expires_at,
                b.bottle_id,
                b.sender_id,
                b.sender_name,
                b.message,
                EXISTS(
                    SELECT 1 FROM replies r WHERE r.delivery_id = d.delivery_id
                ) AS already_replied
            FROM deliveries d
            JOIN bottles b ON b.bottle_id = d.bottle_id
            WHERE d.reply_token=?
            """,
            (token,),
        ).fetchone()

    def create_reply(self, token: str, replier_name: str, reply_text: str) -> Dict[str, Any]:
        delivery = self.get_delivery_by_token(token)
        if not delivery:
            raise LookupError("reply token not found")
        if int(delivery["expires_at"]) < now_ts():
            raise ValueError("reply token expired")
        if int(delivery["already_replied"]):
            raise ValueError("this bottle has already been replied to")
        recipient_id = str(delivery["recipient_id"])
        if self.count_recent_actions("reply", recipient_id, 60) >= REPLY_RATE_LIMIT_PER_MINUTE:
            raise ValueError("reply rate limit exceeded; try again later")

        reply_id = "rep_" + secrets.token_hex(8)
        ts = now_ts()
        self.conn.execute(
            """
            INSERT INTO replies(reply_id, bottle_id, delivery_id, sender_id, recipient_id, replier_name, reply_text, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                reply_id,
                delivery["bottle_id"],
                delivery["delivery_id"],
                delivery["sender_id"],
                recipient_id,
                replier_name,
                reply_text,
                ts,
            ),
        )
        self.conn.commit()
        self.log_action("reply", recipient_id)
        return {
            "ok": True,
            "reply_id": reply_id,
            "bottle_id": delivery["bottle_id"],
            "created_at": ts,
            "created_at_text": iso_time(ts),
        }

    def inbox(self, user_id: str) -> Dict[str, Any]:
        received_rows = self.conn.execute(
            """
            SELECT
                d.delivery_id,
                d.reply_token,
                d.delivered_at,
                d.expires_at,
                b.bottle_id,
                b.sender_id,
                b.sender_name,
                b.message,
                b.created_at,
                EXISTS(
                    SELECT 1 FROM replies r WHERE r.delivery_id = d.delivery_id
                ) AS has_replied
            FROM deliveries d
            JOIN bottles b ON b.bottle_id = d.bottle_id
            WHERE d.recipient_id=?
            ORDER BY b.created_at DESC
            """,
            (user_id,),
        ).fetchall()

        sent_rows = self.conn.execute(
            """
            SELECT bottle_id, sender_id, sender_name, message, created_at, expires_at, fanout
            FROM bottles
            WHERE sender_id=?
            ORDER BY created_at DESC
            """,
            (user_id,),
        ).fetchall()

        replies_rows = self.conn.execute(
            """
            SELECT reply_id, bottle_id, recipient_id, replier_name, reply_text, created_at
            FROM replies
            WHERE sender_id=?
            ORDER BY created_at DESC
            """,
            (user_id,),
        ).fetchall()

        received_bottles = []
        for row in received_rows:
            item = dict(row)
            item["created_at_text"] = iso_time(int(item["created_at"]))
            item["delivered_at_text"] = iso_time(int(item["delivered_at"]))
            item["expires_at_text"] = iso_time(int(item["expires_at"]))
            item["reply_url"] = f"{self.base_url}/r/{item['reply_token']}"
            item["has_replied"] = bool(item["has_replied"])
            received_bottles.append(item)

        sent_bottles = []
        for row in sent_rows:
            item = dict(row)
            item["created_at_text"] = iso_time(int(item["created_at"]))
            item["expires_at_text"] = iso_time(int(item["expires_at"]))
            deliveries = self.conn.execute(
                """
                SELECT
                    d.delivery_id,
                    d.recipient_id,
                    u.display_name AS recipient_name,
                    d.reply_token,
                    d.delivered_at,
                    EXISTS(
                        SELECT 1 FROM replies r WHERE r.delivery_id = d.delivery_id
                    ) AS has_reply
                FROM deliveries d
                LEFT JOIN users u ON u.user_id = d.recipient_id
                WHERE d.bottle_id=?
                ORDER BY d.delivered_at DESC
                """,
                (item["bottle_id"],),
            ).fetchall()
            item["deliveries"] = []
            for delivery in deliveries:
                d = dict(delivery)
                d["delivered_at_text"] = iso_time(int(d["delivered_at"]))
                d["reply_url"] = f"{self.base_url}/r/{d['reply_token']}"
                d["has_reply"] = bool(d["has_reply"])
                item["deliveries"].append(d)
            item["reply_count"] = sum(1 for d in item["deliveries"] if d["has_reply"])
            sent_bottles.append(item)

        replies_received = []
        for row in replies_rows:
            item = dict(row)
            item["created_at_text"] = iso_time(int(item["created_at"]))
            replies_received.append(item)

        return {
            "ok": True,
            "user_id": user_id,
            "received_bottles": received_bottles,
            "sent_bottles": sent_bottles,
            "replies_received": replies_received,
        }


class RelayHandler(BaseHTTPRequestHandler):
    db: RelayDB = None  # type: ignore
    base_url: str = ""

    server_version = "BottleDriftRelay/2.0"

    def log_message(self, format: str, *args: Any) -> None:
        sys.stderr.write("[relay] " + (format % args) + "\n")

    def _parse_json(self) -> Dict[str, Any]:
        content_length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(content_length) if content_length else b"{}"
        try:
            return json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSON: {exc}") from exc

    def _parse_form(self) -> Dict[str, str]:
        content_length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(content_length).decode("utf-8")
        form = parse_qs(raw, keep_blank_values=True)
        return {k: (v[0] if v else "") for k, v in form.items()}

    def _render_reply_page(self, token: str, status_html: str = "") -> None:
        delivery = self.db.get_delivery_by_token(token)
        if not delivery:
            html_response(self, 404, "<h1>404</h1><p>reply token not found</p>")
            return

        reply_state = ""
        if int(delivery["already_replied"]):
            reply_state = '<div class="ok">这个漂流瓶已经回信成功，默认不再接受第二次回信。</div>'

        template = read_text(REPLY_TEMPLATE_PATH)
        body = (
            template.replace("{{BASE_URL}}", html_escape(self.base_url))
            .replace("{{SENDER_NAME}}", html_escape(delivery["sender_name"]))
            .replace("{{BOTTLE_ID}}", html_escape(delivery["bottle_id"]))
            .replace("{{ORIGINAL_MESSAGE}}", html_escape(delivery["message"]))
            .replace("{{TOKEN}}", html_escape(token))
            .replace("{{STATUS_BLOCK}}", status_html or reply_state)
            .replace("{{DISABLED_ATTR}}", "disabled" if int(delivery["already_replied"]) else "")
        )
        html_response(self, 200, body)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)

        if parsed.path == "/" or parsed.path == "/dashboard":
            html_response(self, 200, read_text(DASHBOARD_PATH).replace("{{BASE_URL}}", html_escape(self.base_url)))
            return
        if parsed.path == "/assets/dashboard.js":
            static_response(self, DASHBOARD_JS_PATH)
            return
        if parsed.path == "/healthz":
            json_response(self, 200, {
                "ok": True,
                "service": "bottle-drift-relay",
                "base_url": self.base_url,
            })
            return
        if parsed.path == "/api/users/online":
            qs = parse_qs(parsed.query)
            exclude = qs.get("exclude", [None])[0]
            users = self.db.online_users(exclude_user_id=exclude)
            json_response(self, 200, {"ok": True, "online_users": users})
            return
        if parsed.path.startswith("/api/inbox/"):
            user_id = validate_user_id(parsed.path.rsplit("/", 1)[-1])
            json_response(self, 200, self.db.inbox(user_id))
            return
        if parsed.path.startswith("/r/"):
            token = parsed.path.rsplit("/", 1)[-1]
            self._render_reply_page(token)
            return
        bad_request(self, "not found", code=404)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        try:
            if parsed.path == "/api/presence/heartbeat":
                data = self._parse_json()
                user_id = validate_user_id(str(data.get("user_id", "")))
                display_name = validate_name(str(data.get("display_name", "")), "display_name")
                callback_url = str(data.get("callback_url", "")).strip() or None
                accept_bottles = bool(data.get("accept_bottles", True))
                result = self.db.heartbeat(user_id, display_name, callback_url, accept_bottles)
                json_response(self, 200, result)
                return

            if parsed.path == "/api/bottles/send":
                data = self._parse_json()
                sender_id = validate_user_id(str(data.get("sender_id", "")), "sender_id")
                sender_name = validate_name(str(data.get("sender_name", "")), "sender_name")
                message = validate_message(str(data.get("message", "")), "message")
                fanout = int(data.get("fanout", 1))
                ttl_seconds = int(data.get("ttl_seconds", DEFAULT_TTL))
                result = self.db.create_bottle(
                    sender_id=sender_id,
                    sender_name=sender_name,
                    message=message,
                    fanout=fanout,
                    ttl_seconds=ttl_seconds,
                )
                json_response(self, 200, result)
                return

            if parsed.path == "/api/bottles/reply":
                data = self._parse_json()
                token = str(data.get("token", "")).strip()
                if not token:
                    raise ValueError("token is required")
                replier_name = validate_name(str(data.get("replier_name", "")), "replier_name")
                reply_text = validate_message(str(data.get("reply_text", "")), "reply_text")
                result = self.db.create_reply(token=token, replier_name=replier_name, reply_text=reply_text)
                json_response(self, 200, result)
                return

            if parsed.path.startswith("/r/"):
                token = parsed.path.rsplit("/", 1)[-1]
                if not token:
                    self._render_reply_page(token, '<div class="err">缺少回信 token。</div>')
                    return
                form = self._parse_form()
                try:
                    replier_name = validate_name(form.get("replier_name", ""), "replier_name")
                    reply_text = validate_message(form.get("reply_text", ""), "reply_text")
                    self.db.create_reply(token=token, replier_name=replier_name, reply_text=reply_text)
                except PermissionError as exc:
                    self._render_reply_page(token, f'<div class="err">{html_escape(exc)}</div>')
                    return
                except Exception as exc:
                    self._render_reply_page(token, f'<div class="err">发送失败：{html_escape(exc)}</div>')
                    return
                self._render_reply_page(token, '<div class="ok">回信已送达。你可以关闭此页面，或返回漂流瓶控制台继续查看动态。</div>')
                return

            bad_request(self, "not found", code=404)
        except LookupError as exc:
            bad_request(self, str(exc), code=404)
        except PermissionError as exc:
            bad_request(self, str(exc), code=403)
        except ValueError as exc:
            message = str(exc)
            code = 429 if "rate limit" in message else 400
            bad_request(self, message, code=code)
        except Exception as exc:
            bad_request(self, f"server error: {exc}", code=500)


def build_base_url(host: str, port: int, public_base_url: str | None) -> str:
    if public_base_url:
        return public_base_url.rstrip("/")
    if host in ("0.0.0.0", "::"):
        return f"http://127.0.0.1:{port}"
    return f"http://{host}:{port}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bottle Drift relay server with dashboard")
    parser.add_argument("--host", default="127.0.0.1", help="listen host")
    parser.add_argument("--port", default=8765, type=int, help="listen port")
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH), help="sqlite db path")
    parser.add_argument("--public-base-url", default="", help="public base URL used in reply_url generation")
    return parser.parse_args()


def main() -> int:
    ensure_paths()
    args = parse_args()
    base_url = build_base_url(args.host, args.port, args.public_base_url or None)
    db = RelayDB(Path(args.db), base_url)

    RelayHandler.db = db
    RelayHandler.base_url = base_url

    server = ThreadingHTTPServer((args.host, args.port), RelayHandler)
    print(json.dumps({
        "ok": True,
        "service": "bottle-drift-relay",
        "listen": f"{args.host}:{args.port}",
        "base_url": base_url,
        "db": str(Path(args.db).resolve()),
        "dashboard_url": f"{base_url}/",
    }, ensure_ascii=False, indent=2))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nrelay stopped", file=sys.stderr)
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
