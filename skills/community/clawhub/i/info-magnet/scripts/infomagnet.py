#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
infomagnet — 信息磁铁 / Info Magnet

设置关注点，让信息主动找你。
Set up magnets that attract relevant information to you.

Usage:
  python infomagnet.py add --name "..." --topics "a,b,c" [--sources web,rss] [--schedule daily]
  python infomagnet.py list
  python infomagnet.py show --id MAG_ID
  python infomagnet.py remove --id MAG_ID
  python infomagnet.py scan [--id MAG_ID] [--all]
  python infomagnet.py digest [--id MAG_ID] [--since 24h]
  python infomagnet.py mark-read --url "..."
  python infomagnet.py pause --id MAG_ID
  python infomagnet.py resume --id MAG_ID
  python infomagnet.py import-rss --url "..." --name "..."
"""

import json, sys, time, argparse, os, hashlib, re, urllib.request, urllib.error, xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timezone, timedelta
from urllib.parse import urlparse, quote_plus

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def get_data_dir():
    d = Path.home() / ".openclaw" / "memory"
    d.mkdir(parents=True, exist_ok=True)
    return d


def get_magnets_file():
    return get_data_dir() / "magnets.json"


def get_seen_file():
    return get_data_dir() / "magnet-seen.jsonl"


def get_digests_dir():
    d = get_data_dir() / "magnet-digests"
    d.mkdir(parents=True, exist_ok=True)
    return d


def gen_id():
    return f"mag_{hashlib.sha256(str(time.time()).encode()).hexdigest()[:10]}"


def now_iso():
    return datetime.now(timezone(timedelta(hours=8))).isoformat()


def parse_since(since_str):
    """Parse '24h', '7d', '1h30m' etc."""
    if not since_str:
        return timedelta(hours=24)
    total = timedelta()
    for value, unit in re.findall(r"(\d+)([hdm])", since_str.lower()):
        v = int(value)
        if unit == "h":
            total += timedelta(hours=v)
        elif unit == "d":
            total += timedelta(days=v)
        elif unit == "m":
            total += timedelta(minutes=v)
    return total if total else timedelta(hours=24)


# ────────────────────────────────────────
# Storage
# ────────────────────────────────────────

def load_magnets():
    f = get_magnets_file()
    if not f.exists():
        return []
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except:
        return []


def save_magnets(magnets):
    get_magnets_file().write_text(
        json.dumps(magnets, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def load_seen():
    f = get_seen_file()
    if not f.exists():
        return set()
    seen = set()
    for line in f.read_text(encoding="utf-8").strip().split("\n"):
        if line.strip():
            try:
                data = json.loads(line)
                seen.add(data.get("url", ""))
            except:
                continue
    return seen


def mark_seen(url, title=""):
    f = get_seen_file()
    with open(f, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"url": url, "title": title, "seen_at": now_iso()}, ensure_ascii=False) + "\n")


# ────────────────────────────────────────
# Commands
# ────────────────────────────────────────

def cmd_add(args):
    """Add a new magnet."""
    magnets = load_magnets()

    magnet = {
        "id": gen_id(),
        "name": args.name,
        "topics": [t.strip() for t in args.topics.split(",") if t.strip()],
        "sources": [s.strip() for s in (args.sources or "web").split(",")],
        "schedule": args.schedule or "daily",
        "created_at": now_iso(),
        "last_check": None,
        "status": "active",
        "notes": args.notes or "",
        "rss_urls": [u.strip() for u in args.rss.split(",")] if args.rss else [],
        "check_urls": [u.strip() for u in args.urls.split(",")] if args.urls else [],
    }

    magnets.append(magnet)
    save_magnets(magnets)

    print(f"🧲 磁铁已创建!")
    print(f"   ID:      {magnet['id']}")
    print(f"   名称:    {magnet['name']}")
    print(f"   关注点:  {', '.join(magnet['topics'])}")
    print(f"   信源:    {', '.join(magnet['sources'])}")
    print(f"   频率:    {magnet['schedule']}")
    if magnet['rss_urls']:
        print(f"   RSS:     {', '.join(magnet['rss_urls'])}")
    if magnet['check_urls']:
        print(f"   URL:     {', '.join(magnet['check_urls'])}")


def cmd_list(args):
    """List all magnets."""
    magnets = load_magnets()
    if not magnets:
        print("没有磁铁。用 `add` 创建一个。")
        return

    print(f"\n🧲 磁铁列表 ({len(magnets)} 个)\n")
    for m in magnets:
        icon = "🟢" if m["status"] == "active" else "⏸️"
        topics = ", ".join(m["topics"][:3])
        if len(m["topics"]) > 3:
            topics += f" +{len(m['topics'])-3}"
        last = m.get("last_check", "从未检查")
        if last:
            last = last[:16]
        print(f"  {icon} [{m['id']}] {m['name']}")
        print(f"     关注: {topics}")
        print(f"     信源: {', '.join(m['sources'])} | 频率: {m['schedule']}")
        print(f"     上次: {last}")
        print()


def cmd_show(args):
    """Show magnet details."""
    magnets = load_magnets()
    magnet = next((m for m in magnets if m["id"] == args.id), None)
    if not magnet:
        print(f"磁铁不存在: {args.id}")
        return

    print(f"\n🧲 {magnet['name']}")
    print(f"{'='*50}")
    print(f"  ID:       {magnet['id']}")
    print(f"  状态:     {magnet['status']}")
    print(f"  创建:     {magnet.get('created_at', '?')[:16]}")
    print(f"  上次检查: {magnet.get('last_check', '从未')[:16] if magnet.get('last_check') else '从未'}")
    print(f"  频率:     {magnet['schedule']}")
    print(f"  关注点:")
    for t in magnet["topics"]:
        print(f"    • {t}")
    print(f"  信源:     {', '.join(magnet['sources'])}")
    if magnet.get("rss_urls"):
        print(f"  RSS:")
        for u in magnet["rss_urls"]:
            print(f"    • {u}")
    if magnet.get("check_urls"):
        print(f"  URL:")
        for u in magnet["check_urls"]:
            print(f"    • {u}")
    if magnet.get("notes"):
        print(f"  备注:     {magnet['notes']}")


def cmd_remove(args):
    """Remove a magnet."""
    magnets = load_magnets()
    magnets = [m for m in magnets if m["id"] != args.id]
    save_magnets(magnets)
    print(f"🗑️ 已删除: {args.id}")


def cmd_pause(args):
    """Pause a magnet."""
    magnets = load_magnets()
    for m in magnets:
        if m["id"] == args.id:
            m["status"] = "paused"
            break
    save_magnets(magnets)
    print(f"⏸️ 已暂停: {args.id}")


def cmd_resume(args):
    """Resume a magnet."""
    magnets = load_magnets()
    for m in magnets:
        if m["id"] == args.id:
            m["status"] = "active"
            break
    save_magnets(magnets)
    print(f"▶️ 已恢复: {args.id}")


def cmd_mark_read(args):
    """Mark a URL as seen."""
    mark_seen(args.url, args.title or "")
    print(f"✅ 已标记已读: {args.url[:80]}")


def fetch_rss(url, limit=20):
    """Fetch and parse an RSS/Atom feed."""
    items = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "InfoMagnet/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
        root = ET.fromstring(data)

        # Handle RSS 2.0
        for item in root.iter("item"):
            title = item.findtext("title", "").strip()
            link = item.findtext("link", "").strip()
            desc = item.findtext("description", "").strip()
            pub = item.findtext("pubDate", "").strip()
            if link:
                items.append({
                    "title": title,
                    "url": link,
                    "description": desc[:300],
                    "published": pub,
                    "source": "rss",
                })
            if len(items) >= limit:
                break

        # Handle Atom
        if not items:
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            for entry in root.findall(".//atom:entry", ns):
                title = entry.findtext("atom:title", "", ns).strip()
                link_el = entry.find("atom:link", ns)
                link = link_el.get("href", "") if link_el is not None else ""
                summary = entry.findtext("atom:summary", "", ns).strip()
                pub = entry.findtext("atom:updated", "", ns).strip()
                if link:
                    items.append({
                        "title": title,
                        "url": link,
                        "description": summary[:300],
                        "published": pub,
                        "source": "atom",
                    })
                if len(items) >= limit:
                    break

    except Exception as e:
        print(f"  ⚠️ RSS 获取失败: {url} - {e}", file=sys.stderr)

    return items


def check_web_page(url):
    """Check a web page for changes (compare content hash)."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "InfoMagnet/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8", errors="replace")
        # Simple: extract text, hash it
        text = re.sub(r"<[^>]+>", " ", content)
        text = re.sub(r"\s+", " ", text).strip()[:5000]
        h = hashlib.sha256(text.encode()).hexdigest()[:16]
        return {"url": url, "hash": h, "snippet": text[:300]}
    except Exception as e:
        return {"url": url, "hash": "", "error": str(e)}


def cmd_scan(args):
    """Scan magnets for new content."""
    magnets = load_magnets()
    seen = load_seen()

    if args.id:
        magnets = [m for m in magnets if m["id"] == args.id]
    elif not args.all:
        magnets = [m for m in magnets if m["status"] == "active"]

    if not magnets:
        print("没有需要扫描的磁铁。")
        return

    all_findings = []

    for magnet in magnets:
        if magnet["status"] != "active":
            continue

        print(f"\n🧲 扫描: {magnet['name']}...")
        findings = []

        # Scan RSS feeds
        for rss_url in magnet.get("rss_urls", []):
            items = fetch_rss(rss_url, limit=15)
            for item in items:
                if item["url"] not in seen:
                    findings.append(item)
                    mark_seen(item["url"], item.get("title", ""))

        # Scan web (returns search queries for the agent to execute)
        if "web" in magnet["sources"]:
            for topic in magnet["topics"]:
                # Generate a search query instruction
                findings.append({
                    "title": f"[待搜索] {topic}",
                    "url": f"web-search://{quote_plus(topic)}",
                    "description": f"需要通过 web_search 搜索: {topic}",
                    "source": "web-pending",
                    "topic": topic,
                    "magnet_id": magnet["id"],
                })

        # Check specific URLs
        for check_url in magnet.get("check_urls", []):
            result = check_web_page(check_url)
            if result.get("hash") and result["hash"] not in seen:
                findings.append({
                    "title": f"页面更新: {check_url}",
                    "url": check_url,
                    "description": result.get("snippet", "")[:200],
                    "source": "url-check",
                })
                mark_seen(result["url"], result.get("snippet", "")[:50])

        # Update last check time
        magnet["last_check"] = now_iso()

        if findings:
            all_findings.extend(findings)
            # Save digest
            digest_file = get_digests_dir() / f"{magnet['id']}_{int(time.time())}.json"
            digest_file.write_text(
                json.dumps({
                    "magnet_id": magnet["id"],
                    "magnet_name": magnet["name"],
                    "scanned_at": now_iso(),
                    "findings": findings,
                }, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            print(f"  📡 发现 {len(findings)} 条新内容")
        else:
            print(f"  ✓ 没有新内容")

    save_magnets(magnets)

    # Output summary
    if all_findings:
        # Separate pending web searches from actual findings
        web_pending = [f for f in all_findings if f["source"] == "web-pending"]
        real_findings = [f for f in all_findings if f["source"] != "web-pending"]

        print(f"\n{'='*50}")
        print(f"📊 扫描完成: {len(real_findings)} 条已有内容, {len(web_pending)} 个待搜索")

        if web_pending:
            print(f"\n🔍 需要 Agent 执行的搜索:")
            for f in web_pending:
                print(f"  web_search \"{f['topic']}\"")

        if real_findings:
            print(f"\n📡 已获取的新内容:")
            for f in real_findings[:20]:
                title = f.get("title", "无标题")[:60]
                print(f"  • {title}")
                print(f"    {f.get('url', '')[:80]}")
    else:
        print(f"\n✓ 所有磁铁扫描完毕，没有新内容。")


def cmd_digest(args):
    """Show a digest of recent findings."""
    digests_dir = get_digests_dir()
    if not digests_dir.exists():
        print("没有历史摘要。先运行 scan。")
        return

    since = parse_since(args.since)
    cutoff = datetime.now(timezone(timedelta(hours=8))) - since

    all_items = []
    for f in sorted(digests_dir.glob("*.json"), reverse=True):
        try:
            digest = json.loads(f.read_text(encoding="utf-8"))
            scanned = datetime.fromisoformat(digest["scanned_at"])
            if scanned < cutoff:
                continue
            if args.id and digest["magnet_id"] != args.id:
                continue
            for item in digest["findings"]:
                if item["source"] != "web-pending":
                    item["_magnet"] = digest["magnet_name"]
                    item["_time"] = digest["scanned_at"][:16]
                    all_items.append(item)
        except:
            continue

    if not all_items:
        print(f"过去 {args.since or '24h'} 没有新内容。")
        return

    print(f"\n📬 信息摘要 ({args.since or '24h'}, {len(all_items)} 条)\n")

    current_magnet = None
    for item in all_items:
        if item.get("_magnet") != current_magnet:
            current_magnet = item.get("_magnet")
            print(f"\n🧲 {current_magnet}")
            print(f"{'─'*40}")

        title = item.get("title", "无标题")[:60]
        url = item.get("url", "")[:70]
        desc = item.get("description", "")[:100]
        time_str = item.get("_time", "")

        print(f"  • [{time_str}] {title}")
        if desc:
            print(f"    {desc}")
        print(f"    🔗 {url}")
        print()


def cmd_import_rss(args):
    """Import an RSS feed as a magnet."""
    # Parse feed to get title
    items = fetch_rss(args.url, limit=1)
    name = args.name
    if not name and items:
        name = items[0].get("title", "RSS Feed")[:30]

    magnets = load_magnets()
    magnet = {
        "id": gen_id(),
        "name": name or "RSS Feed",
        "topics": [args.topic] if args.topic else [name or "rss"],
        "sources": ["rss"],
        "schedule": args.schedule or "daily",
        "created_at": now_iso(),
        "last_check": None,
        "status": "active",
        "notes": f"Imported from {args.url}",
        "rss_urls": [args.url],
        "check_urls": [],
    }
    magnets.append(magnet)
    save_magnets(magnets)
    print(f"🧲 RSS 磁铁已创建: {magnet['id']} ({name})")


# ────────────────────────────────────────
# Main
# ────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="infomagnet",
        description="Info Magnet / 信息磁铁 — 让信息主动找你",
    )
    sub = parser.add_subparsers(dest="command")

    # add
    p = sub.add_parser("add", help="Add a new magnet")
    p.add_argument("--name", required=True)
    p.add_argument("--topics", required=True, help="Comma-separated topics")
    p.add_argument("--sources", default="web", help="web,rss,url")
    p.add_argument("--schedule", default="daily")
    p.add_argument("--rss", default="", help="RSS feed URLs")
    p.add_argument("--urls", default="", help="URLs to monitor")
    p.add_argument("--notes", default="")

    # list
    sub.add_parser("list", help="List all magnets")

    # show
    p = sub.add_parser("show", help="Show magnet details")
    p.add_argument("--id", required=True)

    # remove
    p = sub.add_parser("remove", help="Remove a magnet")
    p.add_argument("--id", required=True)

    # scan
    p = sub.add_parser("scan", help="Scan for new content")
    p.add_argument("--id", default=None)
    p.add_argument("--all", action="store_true")

    # digest
    p = sub.add_parser("digest", help="Show recent digest")
    p.add_argument("--id", default=None)
    p.add_argument("--since", default="24h")

    # mark-read
    p = sub.add_parser("mark-read", help="Mark URL as seen")
    p.add_argument("--url", required=True)
    p.add_argument("--title", default="")

    # pause
    p = sub.add_parser("pause", help="Pause a magnet")
    p.add_argument("--id", required=True)

    # resume
    p = sub.add_parser("resume", help="Resume a magnet")
    p.add_argument("--id", required=True)

    # import-rss
    p = sub.add_parser("import-rss", help="Import RSS feed as magnet")
    p.add_argument("--url", required=True)
    p.add_argument("--name", default="")
    p.add_argument("--topic", default="")
    p.add_argument("--schedule", default="daily")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    cmds = {
        "add": cmd_add,
        "list": cmd_list,
        "show": cmd_show,
        "remove": cmd_remove,
        "scan": cmd_scan,
        "digest": cmd_digest,
        "mark-read": cmd_mark_read,
        "pause": cmd_pause,
        "resume": cmd_resume,
        "import-rss": cmd_import_rss,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
