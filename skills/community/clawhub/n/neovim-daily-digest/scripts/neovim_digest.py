#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import sys
import textwrap
import urllib.request
import xml.etree.ElementTree as ET
from collections import OrderedDict
from html import unescape

ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}
FEEDS = OrderedDict(
    [
        ("top_day", "https://www.reddit.com/r/neovim/top.rss?t=day"),
        ("new", "https://www.reddit.com/r/neovim/new.rss"),
        ("hot", "https://www.reddit.com/r/neovim/hot.rss"),
        ("top_week", "https://www.reddit.com/r/neovim/top.rss?t=week"),
    ]
)
USER_AGENT = "Mozilla/5.0 OpenClawNeovimDigest/1.0"
STRONG_DROP_RE = re.compile(
    r"weekly|monthly|questions thread|dotfile review thread|startup dashboard",
    re.IGNORECASE,
)
SHOWCASE_RE = re.compile(
    r"theme|colorscheme|color palette|dashboard|journal|apple supremacy|still loving",
    re.IGNORECASE,
)
STRONG_KEEP_RE = re.compile(
    r"plugin|\.nvim|lsp|treesitter|tree-sitter|cmp|diff|keepalt|markdown|notes|aws|ai|agent|preview|highlight|dictionary|render|filetree|treeview|import|workflow",
    re.IGNORECASE,
)
TIP_RE = re.compile(
    r":keepalt|\btil\b|preserve alt buffer|inline diff|document_highlight|auto-import",
    re.IGNORECASE,
)
PLUGIN_RE = re.compile(r"new plugin|plugin|\.nvim\b|nvim plugin|update|released|supports", re.IGNORECASE)
SUPPORT_RE = re.compile(
    r"^how to\b|^can't get\b|shows nothing|annoying .* error|looking for|recommendations? for|what should you include|what services and plugins|is there any other option",
    re.IGNORECASE,
)
CHATTER_RE = re.compile(r"really cool|let go of tmux|vibe coders", re.IGNORECASE)
URL_RE = re.compile(r"https?://\S+")
HREF_RE = re.compile(r'href=["\'](https?://[^"\']+)["\']', re.IGNORECASE)
RAW_URL_RE = re.compile(r'https?://[^\s"\'<>]+')
GITHUB_RE = re.compile(r"https?://github\.com/[^\s\"'<>]+", re.IGNORECASE)
EDITOR_WORKFLOW_RE = re.compile(
    r"lsp|treesitter|tree-sitter|cmp|auto-import|document_highlight|highlight|diff|buffer|markdown|notes",
    re.IGNORECASE,
)
TOPIC_RESCUE_RE = re.compile(r"lsp|treesitter|tree-sitter|cmp|diff|buffer|auto-import|highlight", re.IGNORECASE)
THEME_TITLE_RE = re.compile(r"theme|colorscheme|color palette", re.IGNORECASE)
AI_PLUGIN_RE = re.compile(r"claude-preview|agenttally|agent tally|copilot|ai agents?", re.IGNORECASE)
RELEASE_RE = re.compile(r"new plugin|update|added|supports|released", re.IGNORECASE)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.read().decode("utf-8", "replace")
    except Exception:
        # Reddit RSS occasionally trips Python's TLS stack in some environments;
        # fall back to curl because it is usually more tolerant here.
        result = subprocess.run(
            ["curl", "-L", "--silent", "--show-error", "--fail", "-A", USER_AGENT, url],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout


def clean_text(value):
    text = unescape(value or "")
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def parse_hrefs(content):
    decoded = unescape(content or "")
    hrefs = []
    for regex in (HREF_RE, GITHUB_RE, RAW_URL_RE, URL_RE):
        for match in regex.findall(decoded):
            href = match.rstrip(').,]">')
            if href.startswith("https://www.reddit.com/user/"):
                continue
            if href not in hrefs:
                hrefs.append(href)
    return hrefs


def parse_feed(xml_text, source_name):
    root = ET.fromstring(xml_text)
    items = []
    for idx, entry in enumerate(root.findall("atom:entry", ATOM_NS), start=1):
        title = (entry.findtext("atom:title", default="", namespaces=ATOM_NS) or "").strip()
        link = ""
        for link_node in entry.findall("atom:link", ATOM_NS):
            href = link_node.attrib.get("href")
            if href:
                link = href
                break
        updated = (entry.findtext("atom:updated", default="", namespaces=ATOM_NS) or "").strip()
        author = ""
        author_node = entry.find("atom:author/atom:name", ATOM_NS)
        if author_node is not None and author_node.text:
            author = author_node.text.strip()
        content = entry.findtext("atom:content", default="", namespaces=ATOM_NS) or ""
        summary = clean_text(content)
        hrefs = parse_hrefs(content)
        items.append(
            {
                "title": title,
                "reddit_link": link,
                "updated": updated,
                "author": author,
                "summary": summary,
                "hrefs": hrefs,
                "source": source_name,
                "source_rank": idx,
            }
        )
    return items


def github_link(item):
    for href in item.get("hrefs", []):
        if "github.com/" in href:
            return href.rstrip(').,]')
    return None


def classify(item):
    title = item["title"]
    summary = item["summary"]
    text = f"{title} {summary}"

    if STRONG_DROP_RE.search(text):
        return "drop", 0, "sticky/meta"

    score = 0
    reasons = []

    if item["source"] == "top_day":
        score += 7
        reasons.append("daily top")
    elif item["source"] == "hot":
        score += 3
        reasons.append("hot")
    elif item["source"] == "new":
        score += 2
        reasons.append("new")
    elif item["source"] == "top_week":
        score += 1
        reasons.append("week backfill")

    if TIP_RE.search(text):
        score += 8
        reasons.append("practical tip")

    if RELEASE_RE.search(text):
        score += 6
        reasons.append("concrete update")

    gh = github_link(item)
    if gh:
        score += 4
        reasons.append("repo link")

    if PLUGIN_RE.search(text):
        score += 5
        reasons.append("plugin")

    if EDITOR_WORKFLOW_RE.search(text):
        score += 4
        reasons.append("editor workflow")

    if AI_PLUGIN_RE.search(text):
        score += 3
        reasons.append("ai workflow")

    if SHOWCASE_RE.search(text):
        score -= 5
        reasons.append("showcase/aesthetic")

    if THEME_TITLE_RE.search(title) and not RELEASE_RE.search(text):
        score -= 3
        reasons.append("theme-only")

    if not STRONG_KEEP_RE.search(text):
        score -= 4
        reasons.append("weak signal")

    if SUPPORT_RE.search(title):
        score -= 10
        reasons.append("support thread")
        if TOPIC_RESCUE_RE.search(text):
            score += 1
            reasons.append("topic rescue")
        if not gh:
            score -= 2
            reasons.append("no repo anchor")

    if CHATTER_RE.search(text):
        score -= 5
        reasons.append("chatter")

    if "?" in title and score < 12:
        score -= 2
        reasons.append("generic question")

    bucket = "keep" if score >= 12 else "near_miss" if score >= 7 else "drop"
    return bucket, score, ", ".join(reasons)


def dedupe(items):
    seen = OrderedDict()
    for item in items:
        key = item["reddit_link"] or item["title"]
        bucket, score, reason = classify(item)
        item["bucket"] = bucket
        item["score"] = score
        item["why"] = reason
        if key not in seen or score > seen[key]["score"]:
            seen[key] = item
    return list(seen.values())


def choose_items(include_near_misses=False, limit=10, week_backfill=False):
    feed_order = ["top_day", "new", "hot"]
    if week_backfill:
        feed_order.append("top_week")

    all_items = []
    for name in feed_order:
        all_items.extend(parse_feed(fetch(FEEDS[name]), name))

    items = dedupe(all_items)
    items.sort(key=lambda item: (-item["score"], item["source_rank"], item["title"].lower()))

    selected = []
    for item in items:
        if item["bucket"] == "keep" or (include_near_misses and item["bucket"] == "near_miss"):
            selected.append(item)
        if len(selected) >= limit:
            break
    return selected, items


def sentence(item):
    title = item["title"]
    summary = item["summary"]
    if re.search(r":keepalt", title, re.IGNORECASE):
        return "讲的是 `:keepalt` 这个很实用的小技巧：改 buffer 文件名/路径时保住 alternate buffer，不把 `#` 污染掉。"
    if "mfd.nvim" in title:
        return "`mfd.nvim` 有新一轮更新，这次主打新增主题和界面风格，适合关注终端内仪表盘/装置感 UI 的人。"
    if "aws nvim plugin" in title.lower() or "aws.nvim" in summary.lower():
        return "`aws.nvim` 已经扩到一串常见 AWS 服务，开始从玩具走向真能顺手用的云资源工作台。"
    if "claude-preview.nvim" in title:
        return "这个更新给 AI 改动预览加了 GitHub-style inline diff，在单 buffer 里看修改会顺手很多。"
    if "treeview" in title.lower() or "filetreeasy.nvim" in title.lower():
        return "新文件树方案，卖点是更轻、更简单，目标是避开 Neo-tree 滚动 bug 和老方案的卡顿。"
    if "doc-highlight" in title.lower():
        return "这是一个更克制的引用高亮插件，重点是减少闪烁和多余 LSP 请求。"
    if "mdx dictionary" in title.lower() or "mdict.nvim" in summary.lower():
        return "离线 MDX 词典插件，适合双语阅读、终端内查词这类很垂直但真实存在的场景。"
    if "mdnotes.nvim" in title.lower():
        return "面向把 Neovim 当主力 Markdown 笔记工具的人，强调 WikiLink、assets 管理和更完整的 notes workflow。"
    if "agenttally.nvim" in title.lower():
        return "这是个很 2026 的插件：统计 AI agent 的 token、工具调用和文件热区，适合玩 agentic coding 的人。"
    if "rendering 3d models" in title.lower() or "rndr.nvim" in summary.lower():
        return "能在 Neovim 里渲染 3D model 和 image，未必高频实用，但新鲜度和技术好奇心都很够。"
    if "lsp" in title.lower():
        return "围绕 LSP 生命周期/配置行为的讨论，值得看回复里的诊断思路。"
    short = summary.split(" submitted by ")[0].strip()
    short = textwrap.shorten(short, width=110, placeholder="...") if short else "值得点开看一下具体讨论。"
    return short


def render_markdown(items, all_items):
    lines = []
    top_count = sum(1 for item in all_items if item["source"] == "top_day")
    lines.append(
        f"基于 `r/neovim` 的 `top/day`、`new`、`hot` RSS 做了过滤；当前 `top/day` 可见 {top_count} 条，所以用 `new/hot` 补了美洲时段还在发酵的帖子。"
    )
    lines.append("")
    for item in items:
        line = f"- [{item['title']}]({item['reddit_link']})"
        gh = github_link(item)
        if gh:
            line += f" · [GitHub]({gh})"
        lines.append(line)
        lines.append(f"  {sentence(item)}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Build a high-signal Neovim Reddit digest from RSS feeds.")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--include-near-misses", action="store_true")
    parser.add_argument("--week-backfill", action="store_true")
    args = parser.parse_args()

    try:
        selected, all_items = choose_items(
            include_near_misses=args.include_near_misses,
            limit=args.limit,
            week_backfill=args.week_backfill,
        )
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps({"items": selected, "allCount": len(all_items)}, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(selected, all_items))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
