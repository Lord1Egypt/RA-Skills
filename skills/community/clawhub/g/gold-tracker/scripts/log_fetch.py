#!/usr/bin/env python3
"""web_fetch 行为记录器（反幻觉硬门槛的配套工具，P0 核心价值 1）。

智能体每次调用 web_fetch 抓取网页后，MUST 立即调用本脚本记录该 URL。
未记录的 URL 不会通过 analyze_check.py 的 sources 校验。

用法:
    python3 scripts/log_fetch.py <url> [标题]
    python3 scripts/log_fetch.py list
    python3 scripts/log_fetch.py clear
"""

import json
import sys
from urllib.parse import urlparse

from common import paths, atomic, timeutil


def log_file():
    return paths.resolve("cache") / "fetch_log.json"


def load_log():
    f = log_file()
    if not f.exists():
        return []
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def save_log(entries):
    atomic.atomic_write_json(log_file(), entries)


def add(url, title=""):
    url = url.strip()
    if not url:
        print("[错误] URL 不能为空", file=sys.stderr)
        sys.exit(1)

    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        print("[错误] 非合法 http(s) URL: {}".format(url), file=sys.stderr)
        sys.exit(1)

    entries = load_log()
    ts = timeutil.now_iso()
    for e in entries:
        if e.get("url") == url:
            e["last_fetch_at"] = ts
            if title:
                e["title"] = title
            save_log(entries)
            print("[已记录] {} (已存在，更新时间)".format(url))
            return e

    entry = {
        "url": url,
        "domain": parsed.netloc,
        "title": title or "",
        "fetched_at": ts,
        "last_fetch_at": ts,
    }
    entries.append(entry)
    save_log(entries)
    print("[已记录] {}".format(url))
    if title:
        print("           标题: {}".format(title))
    return entry


def list_entries():
    entries = load_log()
    if not entries:
        print("(空) 尚未记录任何 web_fetch")
        return
    print("共 {} 条记录:".format(len(entries)))
    domains = set()
    for e in entries:
        domains.add(e.get("domain", "?"))
        print("  - [{}] {}".format(e.get("fetched_at", "?")[:19], e["url"]))
        if e.get("title"):
            print("      标题: {}".format(e["title"]))
    print("\n覆盖 {} 个独立域名: {}".format(len(domains), ", ".join(sorted(domains))))


def clear():
    save_log([])
    print("[已清空] fetch_log.json")


def main():
    paths.ensure_env()
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    arg = sys.argv[1]
    if arg == "list":
        list_entries()
    elif arg == "clear":
        clear()
    elif arg.startswith("http://") or arg.startswith("https://"):
        title = sys.argv[2] if len(sys.argv) > 2 else ""
        add(arg, title)
    else:
        print("[错误] 第一个参数应为 URL 或 list/clear，得到: {}".format(arg), file=sys.stderr)
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
