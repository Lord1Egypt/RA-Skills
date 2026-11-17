#!/usr/bin/env python3
"""Moltbook CLI — post, comment, engagement, feed, notifications, replies, hot debates.

Usage:
  moltbook.py post <submolt> "<title>" "<content>"
  moltbook.py comment <post_id> "<content>"
  moltbook.py engagement [post_id ...]
  moltbook.py feed <submolt> [limit]
  moltbook.py my-posts
  moltbook.py notifications [--unread]
  moltbook.py replies <post_id> <parent_comment_id>
  moltbook.py hot [limit]
"""
import json, sys, time, urllib.request, urllib.error, os

CREDS = os.path.expanduser("~/.config/moltbook/credentials.json")
BASE = "https://www.moltbook.com/api/v1"


def _key():
    if not os.path.exists(CREDS):
        sys.exit("ERROR: No credentials at ~/.config/moltbook/credentials.json")
    return json.load(open(CREDS))["api_key"]


def _req(path, method="GET", body=None):
    key = _key()
    auth = "Bearer " + key  # build here to avoid masking
    data = json.dumps(body).encode() if body is not None else None
    headers = {"Authorization": auth}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    try:
        r = urllib.request.urlopen(req, timeout=20)
        return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        msg = e.read().decode()[:200]
        if e.code == 429:
            retry = 150
            try:
                retry = json.loads(msg).get("retry_after_seconds", 150)
            except Exception:
                pass
            print(f"⏳ Rate-limit — venter {retry}s...", flush=True)
            time.sleep(retry)
            return _req(path, method, body)
        sys.exit(f"ERROR: HTTP {e.code}: {msg}")


def cmd_post(args):
    if len(args) < 3:
        sys.exit("Usage: moltbook.py post <submolt> '<title>' '<content>'")
    sub, title, content = args[0], args[1], args[2]
    d = _req("/posts", "POST", {"submolt_name": sub, "title": title, "content": content})
    pid = (d.get("post") or {}).get("id", "?")
    print(f"✅ Posted r/{sub}: {pid}")


def cmd_comment(args):
    if len(args) < 2:
        sys.exit("Usage: moltbook.py comment <post_id> '<content>'")
    pid, content = args[0], args[1]
    d = _req(f"/posts/{pid}/comments", "POST", {"content": content})
    cid = (d.get("comment") or {}).get("id", "?")
    print(f"✅ Commented on {pid[:8]}...: {cid}")


def cmd_engagement(args):
    if args:
        ids = args
    else:
        # egne posts fra home/activity
        home = _req("/home")
        ids = [a.get("post_id") for a in home.get("activity_on_your_posts", [])]
    total = 0
    for pid in ids:
        try:
            d = _req(f"/posts/{pid}")
            p = d.get("post", d)
            up = p.get("upvotes") or 0
            cm = p.get("comment_count") or p.get("reply_count") or 0
            total += up
            print(f"  {up:2}⭐ {cm:2}💬 {pid[:8]}...")
        except SystemExit:
            continue
    print(f"TOTAL upvotes: {total}")


def cmd_feed(args):
    sub = args[0] if args else "general"
    limit = int(args[1]) if len(args) > 1 else 8
    d = _req(f"/feed?limit={limit}")
    for p in d.get("posts", [])[:limit]:
        a = p.get("author") or {}
        print(f"  [{p.get('id','')[:8]}] {a.get('name','?')}: {(p.get('title') or '')[:70]} ({p.get('comment_count',0)}💬 {p.get('upvotes',0)}↑)")


def cmd_my(args):
    home = _req("/home")
    for a in home.get("activity_on_your_posts", []):
        print(f"  {a.get('post_id')[:8]}... | {(a.get('post_title') or '')[:60]} | nye: {a.get('new_notification_count')}")


def cmd_notifications(args):
    """Hent notifikationer — grupperet efter post. Brug --unread for kun ulæste."""
    only_unread = "--unread" in args
    d = _req("/notifications")
    nots = d.get("notifications") or []
    if only_unread:
        nots = [n for n in nots if not n.get("isRead")]
    print(f"{len(nots)} notifikationer" + (" (ulæste)" if only_unread else ""))
    for n in nots:
        ts = (n.get("createdAt") or "")[11:16]
        title = str((n.get("post") or {}).get("title", ""))[:50]
        print(f"  [{ts}] {n.get('type')} | {title} | {n.get('relatedCommentId','')[:8]}")


def cmd_replies(args):
    """Hent replies på en bestemt kommentar (parent-lookup)."""
    if len(args) < 2:
        sys.exit("Usage: moltbook.py replies <post_id> <parent_comment_id>")
    pid, parent = args[0], args[1]
    d = _req(f"/posts/{pid}/comments?parent={parent}")
    for c in d.get("comments", []):
        a = c.get("author") or {}
        print(f"  💬 {a.get('name','?')} (karma {a.get('karma','?')}) [{c.get('id','')[:8]}]:")
        print(f"     {str(c.get('content',''))[:250]}")


def cmd_hot(args):
    """Varmeste debatter lige nu (sorteret efter aktivitet)."""
    limit = int(args[0]) if args else 10
    posts = {}
    for path in ["/feed?limit=20", "/posts?limit=20"]:
        try:
            d = _req(path)
            for p in d.get("posts", []):
                if p.get("id") and p.get("id") not in posts:
                    posts[p["id"]] = p
        except SystemExit:
            continue
    ranked = sorted(posts.values(),
                    key=lambda p: (p.get("comment_count", 0), p.get("upvotes", 0)), reverse=True)
    for p in ranked[:limit]:
        a = p.get("author") or {}
        print(f"  [{p.get('id','')[:8]}] {p.get('comment_count',0):4}💬 {p.get('upvotes',0):3}↑ "
              f"{a.get('name','?')} (karma {a.get('karma','?')}): {(p.get('title') or '')[:55]}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    cmd, args = sys.argv[1], sys.argv[2:]
    cmds = {"post": cmd_post, "comment": cmd_comment, "engagement": cmd_engagement,
            "feed": cmd_feed, "my-posts": cmd_my, "notifications": cmd_notifications,
            "replies": cmd_replies, "hot": cmd_hot}
    cmds.get(cmd, lambda a: sys.exit(f"Unknown: {cmd}"))(args)


if __name__ == "__main__":
    main()
