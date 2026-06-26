#!/usr/bin/env python3
"""Moltbook operations helper.

Commands:
- heartbeat: compact actionable summary for cron/agents
- home / notifications / following / trading-hot: raw-ish JSON dump
- post-detail / post-comments / search / dm-check / agent-me / agent-profile: fetch more context
- create-post / create-comment / verify: explicit content creation flows
- post-upvote / post-downvote / comment-upvote: engagement actions
- follow-agent / unfollow-agent: follow management
- mark-all-read / mark-post-read: notification handling
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

DEFAULT_BASE = os.environ.get("MOLTBOOK_BASE", "https://www.moltbook.com/api/v1")
DEFAULT_KEY = os.environ.get("MOLTBOOK_API_KEY", "")


def clean(text: Any, limit: int = 120) -> str:
    if text is None:
        return ""
    s = str(text).replace("\n", " ").replace("\r", " ").strip()
    return s[:limit]


class MoltbookClient:
    def __init__(self, api_key: str, base: str = DEFAULT_BASE) -> None:
        if not api_key:
            raise SystemExit("Missing Moltbook API key. Pass --api-key or set MOLTBOOK_API_KEY.")
        self.api_key = api_key
        self.base = base.rstrip("/")

    def request(self, method: str, path: str, payload: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.base}{path}"
        data = None
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "openclaw-moltbook-ops/1.2",
        }
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read()
                if not raw:
                    return {"success": True, "status": resp.status}
                return json.loads(raw)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")[:1200]
            raise SystemExit(f"HTTP {e.code} for {method} {path}: {body}")
        except urllib.error.URLError as e:
            raise SystemExit(f"Request failed for {method} {path}: {e}")

    def get(self, path: str) -> Any:
        return self.request("GET", path)

    def post(self, path: str, payload: Optional[Dict[str, Any]] = None) -> Any:
        return self.request("POST", path, payload)

    def delete(self, path: str, payload: Optional[Dict[str, Any]] = None) -> Any:
        return self.request("DELETE", path, payload)

    def home(self) -> Dict[str, Any]:
        return self.get("/home")

    def notifications(self, limit: int = 8) -> Dict[str, Any]:
        return self.get(f"/notifications?limit={limit}")

    def following(self, limit: int = 8) -> Dict[str, Any]:
        return self.get(f"/feed?filter=following&sort=new&limit={limit}")

    def trading_hot(self, limit: int = 5) -> Dict[str, Any]:
        return self.get(f"/posts?submolt=trading&sort=hot&limit={limit}")

    def post_detail(self, post_id: str) -> Dict[str, Any]:
        return self.get(f"/posts/{post_id}")

    def post_comments(self, post_id: str, limit: int = 20, sort: str = "best") -> Dict[str, Any]:
        return self.get(f"/posts/{post_id}/comments?sort={urllib.parse.quote(sort)}&limit={limit}")

    def search(self, query: str, result_type: str = "all", limit: int = 20) -> Dict[str, Any]:
        return self.get(
            f"/search?q={urllib.parse.quote(query)}&type={urllib.parse.quote(result_type)}&limit={limit}"
        )

    def dm_check(self) -> Dict[str, Any]:
        return self.get("/agents/dm/check")

    def agent_me(self) -> Dict[str, Any]:
        return self.get("/agents/me")

    def agent_profile(self, name: str) -> Dict[str, Any]:
        return self.get(f"/agents/profile?name={urllib.parse.quote(name)}")

    def create_post(
        self,
        submolt_name: str,
        title: str,
        content: str = "",
        post_type: str = "text",
        url: str = "",
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "submolt_name": submolt_name,
            "title": title,
            "type": post_type,
        }
        if content:
            payload["content"] = content
        if url:
            payload["url"] = url
        return self.post("/posts", payload)

    def create_comment(self, post_id: str, content: str, parent_id: str = "") -> Dict[str, Any]:
        payload: Dict[str, Any] = {"content": content}
        if parent_id:
            payload["parent_id"] = parent_id
        return self.post(f"/posts/{post_id}/comments", payload)

    def verify(self, verification_code: str, answer: str) -> Dict[str, Any]:
        return self.post("/verify", {"verification_code": verification_code, "answer": answer})

    def post_upvote(self, post_id: str) -> Dict[str, Any]:
        return self.post(f"/posts/{post_id}/upvote")

    def post_downvote(self, post_id: str) -> Dict[str, Any]:
        return self.post(f"/posts/{post_id}/downvote")

    def comment_upvote(self, comment_id: str) -> Dict[str, Any]:
        return self.post(f"/comments/{comment_id}/upvote")

    def follow_agent(self, agent_name: str) -> Dict[str, Any]:
        return self.post(f"/agents/{urllib.parse.quote(agent_name)}/follow")

    def unfollow_agent(self, agent_name: str) -> Dict[str, Any]:
        return self.delete(f"/agents/{urllib.parse.quote(agent_name)}/follow")

    def mark_all_read(self) -> Dict[str, Any]:
        return self.post("/notifications/read-all")

    def mark_post_read(self, post_id: str) -> Dict[str, Any]:
        return self.post(f"/notifications/read-by-post/{post_id}")


def print_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def summarize_home(home: Dict[str, Any]) -> List[str]:
    lines: List[str] = []
    acct = home.get("your_account", {})
    dm = home.get("your_direct_messages", {})
    lines.append(
        "Account: "
        f"{acct.get('name','?')} | karma={acct.get('karma','?')} | unread={acct.get('unread_notification_count','?')} "
        f"| dm_pending={dm.get('pending_request_count','?')} | dm_unread={dm.get('unread_message_count','?')}"
    )
    activity = home.get("activity_on_your_posts", [])
    lines.append(f"Activity on your posts: {len(activity)}")
    for item in activity[:5]:
        actor = item.get("actor_name") or item.get("author_name") or item.get("username") or "?"
        preview = clean(item.get("preview") or item.get("content_preview") or item.get("content"), 110)
        lines.append(f" - {item.get('type','activity')} by {actor}: {preview}")
    follow = home.get("posts_from_accounts_you_follow", {})
    posts = follow.get("posts", [])
    lines.append(f"Following feed preview: {len(posts)} posts")
    for p in posts[:5]:
        lines.append(
            f" - @{p.get('author_name','?')} [{p.get('submolt_name','?')}] "
            f"▲{p.get('upvotes',0)} 💬{p.get('comment_count',0)} :: {clean(p.get('title'), 90)}"
        )
    return lines


def summarize_notifications(notes: Dict[str, Any]) -> List[str]:
    items = notes.get("notifications", notes if isinstance(notes, list) else [])
    lines = [f"Notifications: total={len(items)} unread={notes.get('unread_count','?')}"]
    for item in items[:8]:
        post = item.get("post") or {}
        suffix = f" | post: {clean(post.get('title'), 80)}" if post else ""
        line = clean(item.get("content") or item.get("message") or item.get("preview"), 120)
        lines.append(f" - {item.get('type','?')} | read={item.get('isRead','?')} | {line}{suffix}")
    return lines


def summarize_following(feed: Dict[str, Any]) -> List[str]:
    posts = feed.get("posts", [])
    lines = [f"Following feed(full endpoint): {len(posts)} posts"]
    for p in posts[:8]:
        author = (p.get("author") or {}).get("name") or p.get("author_name") or "?"
        lines.append(
            f" - @{author} [{p.get('submolt_name','?')}] ▲{p.get('upvotes',0)} 💬{p.get('comment_count',0)} :: {clean(p.get('title'), 90)}"
        )
        preview = clean(p.get("content_preview") or p.get("content"), 120)
        if preview:
            lines.append(f"   {preview}")
    return lines


def summarize_trading(trading: Dict[str, Any]) -> List[str]:
    posts = trading.get("posts", [])
    lines = ["Trading hot:"]
    for p in posts[:5]:
        lines.append(f" - ▲{p.get('upvotes',0)} 💬{p.get('comment_count',0)} :: {clean(p.get('title'), 90)}")
    return lines


def heartbeat_assessment(home: Dict[str, Any], notes: Dict[str, Any], feed: Dict[str, Any]) -> List[str]:
    acct = home.get("your_account", {})
    dm = home.get("your_direct_messages", {})
    activity = home.get("activity_on_your_posts", [])
    items = notes.get("notifications", [])
    unread = notes.get("unread_count", acct.get("unread_notification_count", 0))
    old_unread = [x for x in items if not x.get("isRead")]
    fresh_posts = feed.get("posts", [])[:5]

    lines = ["=== Assessment ==="]
    if dm.get("pending_request_count") not in (None, "0", 0):
        lines.append(f"DM requests pending: {dm.get('pending_request_count')}")
    else:
        lines.append("DM requests: none")

    if activity:
        lines.append(f"New activity on your posts: {len(activity)}")
        for item in activity[:3]:
            lines.append(f" - {item.get('type','activity')}: {clean(item.get('preview') or item.get('content_preview') or item.get('content'), 100)}")
    else:
        lines.append("New activity on your posts: none")

    lines.append(f"Unread notifications: {unread}")
    if old_unread:
        for item in old_unread[:4]:
            lines.append(f" - {item.get('type','?')}: {clean(item.get('content'), 100)}")

    lines.append("Fresh following posts worth manual review:")
    for p in fresh_posts[:3]:
        author = (p.get("author") or {}).get("name") or p.get("author_name") or "?"
        lines.append(f" - @{author}: {clean(p.get('title'), 95)}")

    if not activity and str(dm.get("pending_request_count", "0")) in ("0", "", "None") and int(unread or 0) == 0:
        lines.append("Verdict: quiet right now; no urgent action required.")
    else:
        lines.append("Verdict: there is actionable activity; inspect comments/mentions before replying.")
    return lines


def cmd_heartbeat(client: MoltbookClient, _: argparse.Namespace) -> None:
    home = client.home()
    notes = client.notifications(limit=8)
    feed = client.following(limit=8)
    trading = client.trading_hot(limit=5)

    print(f"=== Moltbook heartbeat ===")
    for section in (
        summarize_home(home),
        summarize_notifications(notes),
        summarize_following(feed),
        summarize_trading(trading),
        heartbeat_assessment(home, notes, feed),
    ):
        for line in section:
            print(line)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Moltbook operations helper")
    p.add_argument("--api-key", default=DEFAULT_KEY)
    p.add_argument("--base", default=DEFAULT_BASE)
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("heartbeat")
    sub.add_parser("home")
    sub.add_parser("notifications")
    sub.add_parser("following")
    sub.add_parser("trading-hot")
    sub.add_parser("agent-me")

    ap = sub.add_parser("agent-profile")
    ap.add_argument("name")

    pd = sub.add_parser("post-detail")
    pd.add_argument("post_id")

    pc = sub.add_parser("post-comments")
    pc.add_argument("post_id")
    pc.add_argument("--limit", type=int, default=20)
    pc.add_argument("--sort", default="best")

    s = sub.add_parser("search")
    s.add_argument("query")
    s.add_argument("--type", default="all", choices=["all", "posts", "comments"])
    s.add_argument("--limit", type=int, default=20)

    sub.add_parser("dm-check")

    cp = sub.add_parser("create-post")
    cp.add_argument("submolt_name")
    cp.add_argument("title")
    cp.add_argument("content", nargs="?", default="")
    cp.add_argument("--type", default="text", choices=["text", "link", "image"])
    cp.add_argument("--url", default="")

    cc = sub.add_parser("create-comment")
    cc.add_argument("post_id")
    cc.add_argument("content")
    cc.add_argument("--parent-id", default="")

    v = sub.add_parser("verify")
    v.add_argument("verification_code")
    v.add_argument("answer")

    pu = sub.add_parser("post-upvote")
    pu.add_argument("post_id")

    pdv = sub.add_parser("post-downvote")
    pdv.add_argument("post_id")

    cu = sub.add_parser("comment-upvote")
    cu.add_argument("comment_id")

    fa = sub.add_parser("follow-agent")
    fa.add_argument("agent_name")

    ufa = sub.add_parser("unfollow-agent")
    ufa.add_argument("agent_name")

    mr = sub.add_parser("mark-post-read")
    mr.add_argument("post_id")

    sub.add_parser("mark-all-read")
    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    client = MoltbookClient(api_key=args.api_key, base=args.base)

    if args.command == "heartbeat":
        cmd_heartbeat(client, args)
    elif args.command == "home":
        print_json(client.home())
    elif args.command == "notifications":
        print_json(client.notifications())
    elif args.command == "following":
        print_json(client.following())
    elif args.command == "trading-hot":
        print_json(client.trading_hot())
    elif args.command == "agent-me":
        print_json(client.agent_me())
    elif args.command == "agent-profile":
        print_json(client.agent_profile(args.name))
    elif args.command == "post-detail":
        print_json(client.post_detail(args.post_id))
    elif args.command == "post-comments":
        print_json(client.post_comments(args.post_id, limit=args.limit, sort=args.sort))
    elif args.command == "search":
        print_json(client.search(args.query, result_type=args.type, limit=args.limit))
    elif args.command == "dm-check":
        print_json(client.dm_check())
    elif args.command == "create-post":
        print_json(client.create_post(args.submolt_name, args.title, args.content, post_type=args.type, url=args.url))
    elif args.command == "create-comment":
        print_json(client.create_comment(args.post_id, args.content, parent_id=args.parent_id))
    elif args.command == "verify":
        print_json(client.verify(args.verification_code, args.answer))
    elif args.command == "post-upvote":
        print_json(client.post_upvote(args.post_id))
    elif args.command == "post-downvote":
        print_json(client.post_downvote(args.post_id))
    elif args.command == "comment-upvote":
        print_json(client.comment_upvote(args.comment_id))
    elif args.command == "follow-agent":
        print_json(client.follow_agent(args.agent_name))
    elif args.command == "unfollow-agent":
        print_json(client.unfollow_agent(args.agent_name))
    elif args.command == "mark-post-read":
        print_json(client.mark_post_read(args.post_id))
    elif args.command == "mark-all-read":
        print_json(client.mark_all_read())
    else:
        parser.error(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
