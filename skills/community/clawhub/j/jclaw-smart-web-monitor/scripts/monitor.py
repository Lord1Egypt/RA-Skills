#!/usr/bin/env python3
"""
web-monitor v2: fetch → extract/match (keyword/regex/css/jsonpath) → pause
LLM matching is handled externally by the cron agent.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

SKILL_DIR = Path(__file__).resolve().parent.parent
MONITORS_DIR = SKILL_DIR / "monitors"
REPORTS_DIR = SKILL_DIR / "reports"

MONITORS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def slugify(name: str) -> str:
    return re.sub(r'[^a-z0-9_-]', '_', name.lower())


def load_monitor(name: str) -> dict:
    path = MONITORS_DIR / f"{slugify(name)}.json"
    if not path.exists():
        print(f"❌ Monitor '{name}' not found at {path}")
        sys.exit(1)
    with open(path) as f:
        return json.load(f)


def save_monitor(config: dict):
    path = MONITORS_DIR / f"{slugify(config['name'])}.json"
    with open(path, 'w') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved: {path}")


def fetch_url(url: str, headers: dict = None) -> str:
    req_headers = {"User-Agent": USER_AGENT}
    if headers:
        req_headers.update(headers)
    req = Request(url, headers=req_headers)
    try:
        with urlopen(req, timeout=30) as resp:
            charset = resp.headers.get_content_charset() or 'utf-8'
            return resp.read().decode(charset, errors='replace')
    except (URLError, HTTPError) as e:
        print(f"⚠️  Failed to fetch {url}: {e}")
        return ""


def extract_text(html: str) -> str:
    html = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<[^>]+>', '\n', html)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()


# ─── Match Functions (non-LLM) ───

def match_keyword(text: str, keywords_str: str, case_sensitive: bool = False) -> list[dict]:
    flags = 0 if case_sensitive else re.IGNORECASE
    keywords = [k.strip() for k in keywords_str.split(",") if k.strip()]
    matches = []
    lines = text.split('\n')
    for i, line in enumerate(lines):
        for kw in keywords:
            if re.search(re.escape(kw), line, flags):
                ctx_start = max(0, i - 1)
                ctx_end = min(len(lines), i + 2)
                matches.append({
                    "keyword": kw,
                    "line": line.strip(),
                    "context": '\n'.join(lines[ctx_start:ctx_end]).strip()
                })
                break
    return matches


def match_regex(text: str, pattern: str, case_sensitive: bool = False) -> list[dict]:
    flags = 0 if case_sensitive else re.IGNORECASE
    matches = []
    for m in re.compile(pattern, flags).finditer(text):
        start = max(0, m.start() - 100)
        end = min(len(text), m.end() + 100)
        matches.append({"match": m.group(), "context": text[start:end].strip()})
    return matches


def match_css(html: str, selector: str) -> list[dict]:
    flags = re.IGNORECASE
    if selector.startswith('.'):
        pattern = re.compile(rf'class=["\'][^"\']*\b{re.escape(selector[1:])}\b[^"\']*["\']', flags)
    elif selector.startswith('#'):
        pattern = re.compile(rf'id=["\']{re.escape(selector[1:])}["\']', flags)
    else:
        pattern = re.compile(rf'<{re.escape(selector)}[\s>]', flags)
    matches = []
    for m in pattern.finditer(html):
        start = max(0, m.start() - 50)
        end = min(len(html), m.end() + 200)
        matches.append({"match": m.group(), "context": html[start:end].strip()})
    return matches


def match_jsonpath(text: str, path: str) -> list[dict]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        print("⚠️  Response is not valid JSON")
        return []
    path = path.strip().lstrip('$.')
    current = [data]
    for part in path.split('.'):
        next_items = []
        if part.endswith('[*]'):
            key = part[:-3]
            for item in current:
                if isinstance(item, dict) and key in item and isinstance(item[key], list):
                    next_items.extend(item[key])
        else:
            for item in current:
                if isinstance(item, dict) and part in item:
                    next_items.append(item[part])
        current = next_items
    results = []
    for item in current:
        val = json.dumps(item, ensure_ascii=False) if isinstance(item, (dict, list)) else str(item)
        results.append({"match": val[:200], "context": val})
    return results


def run_match(html: str, text: str, match_cfg: dict) -> list[dict]:
    mtype = match_cfg["type"]
    value = match_cfg["value"]
    cs = match_cfg.get("caseSensitive", False)
    if mtype == "keyword":
        return match_keyword(text, value, cs)
    elif mtype == "regex":
        return match_regex(text, value, cs)
    elif mtype == "css":
        return match_css(html, value)
    elif mtype == "jsonpath":
        return match_jsonpath(text, value)
    else:
        return []


# ─── State Management ───

def set_state(config: dict, state: str) -> dict:
    config["state"] = state
    config["stateUpdatedAt"] = datetime.now(timezone.utc).isoformat()
    save_monitor(config)
    return config


# ─── Fetch Command ───

def cmd_fetch(args):
    """Fetch URL(s) and output extracted text as JSON (for LLM processing)."""
    config = load_monitor(args.event)
    results = []
    for url_entry in config["urls"]:
        url = url_entry["url"]
        label = url_entry.get("label", url)
        headers = url_entry.get("headers")
        html = fetch_url(url, headers=headers)
        if html:
            text = extract_text(html)
            results.append({
                "url": url,
                "label": label,
                "text": text[:20000],  # Cap at ~20k chars for LLM context
                "truncated": len(text) > 20000,
                "full_length": len(text)
            })
        else:
            results.append({"url": url, "label": label, "text": "", "error": "fetch_failed"})

    # Output as JSON for the agent to process
    print(json.dumps(results, indent=2, ensure_ascii=False))


# ─── Run Command ───

def run_monitor(config: dict, verbose: bool = False) -> dict:
    name = config["name"]
    state = config.get("state", "active")

    if state in ("paused", "disabled"):
        if verbose:
            print(f"⏸️  Monitor '{name}' is {state}. Skipping.")
        return {"event": name, "status": state, "skipped": True}

    match_cfg = config["match"]
    report = {
        "event": name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "urls_checked": 0,
        "total_matches": 0,
        "results": []
    }

    for url_entry in config["urls"]:
        url = url_entry["url"]
        label = url_entry.get("label", url)
        headers = url_entry.get("headers")

        print(f"🔍 {label}: {url}")
        html = fetch_url(url, headers=headers)
        if not html:
            report["results"].append({"url": label, "status": "fetch_failed", "matches": []})
            continue

        text = extract_text(html)

        # For LLM match type, we can't do matching in the script
        # Output text for external LLM processing
        if match_cfg["type"] == "llm":
            matches = [{"match": "[LLM match pending]", "context": text[:5000], "needs_llm": True}]
            report["urls_checked"] += 1
            report["total_matches"] += 1  # Always "match" for LLM — agent decides
            report["results"].append({
                "url": label, "status": "llm_pending",
                "text": text[:20000], "matches": matches
            })
            if verbose:
                print(f"  🤖 LLM matching needed")
        else:
            matches = run_match(html, text, match_cfg)
            report["urls_checked"] += 1
            report["total_matches"] += len(matches)
            report["results"].append({
                "url": label,
                "status": "matched" if matches else "no_match",
                "matches": matches
            })
            if verbose:
                print(f"  {'✅' if matches else '⚪'} {len(matches)} matches")

    return report


def cmd_run(args):
    config = load_monitor(args.event) if args.event else None

    if args.all:
        monitors = sorted(MONITORS_DIR.glob("*.json"))
        if not monitors:
            print("No monitors found.")
            return
        for mpath in monitors:
            with open(mpath) as f:
                config = json.load(f)
            if not config.get("enabled", True):
                continue
            print(f"\n{'='*50}")
            print(f"Running: {config['name']} [{config.get('state', 'active')}]")
            print(f"{'='*50}")
            report = run_monitor(config, verbose=True)
            if not report.get("skipped") and report["total_matches"] > 0:
                # Check if LLM match is pending
                has_llm = any(r.get("status") == "llm_pending" for r in report["results"])
                if not has_llm:
                    # Non-LLM matches found — report and pause
                    save_report(config, report["results"], config["match"]["type"])
                    set_state(config, "paused")
                    print(f"\n⏸️ '{config['name']}' paused. Use 'resume' to continue.")
    elif args.event:
        config = load_monitor(args.event)
        print(f"Running: {config['name']} [{config.get('state', 'active')}]")
        print(f"Match: {config['match']['type']} → \"{config['match']['value'][:60]}\"")
        print()
        report = run_monitor(config, verbose=True)

        print(f"\n{'='*50}")
        print(f"📊 Results: {report['urls_checked']} URLs, {report['total_matches']} matches")

        if report.get("skipped"):
            print(f"   Status: {report['status']}")
            return

        has_llm = any(r.get("status") == "llm_pending" for r in report["results"])
        if has_llm:
            # Output raw JSON for agent to process with LLM
            if args.json:
                print(json.dumps(report, indent=2, ensure_ascii=False))
            else:
                # Save text chunks for agent
                for r in report["results"]:
                    if r.get("text"):
                        out_path = SKILL_DIR / "reports" / f"_pending_{slugify(config['name'])}_{r['label']}.txt"
                        with open(out_path, 'w') as f:
                            f.write(r["text"])
                        print(f"📄 Text saved for LLM processing: {out_path}")
        elif report["total_matches"] > 0:
            save_report(config, report["results"], config["match"]["type"])
            set_state(config, "paused")
            print(f"\n⏸️ 监控已暂停。有匹配内容！")
            print(f"   继续: python3 scripts/monitor.py resume --event {config['name']}")
            print(f"   停用: python3 scripts/monitor.py disable --event {config['name']}")
        else:
            print("   No matches. Monitor stays active.")

        if args.json and not has_llm:
            print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print("Specify --event <name> or --all")


def format_report(config: dict, results: list[dict], match_type: str) -> str:
    name = config["name"]
    desc = config.get("description", "")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"# 🔔 Web Monitor Alert: {name}", f"",
             f"**描述:** {desc}", f"**时间:** {now}", f"**匹配模式:** {match_type}", f""]
    for r in results:
        lines.append(f"## {r['url']}")
        lines.append(f"**找到 {len(r['matches'])} 个匹配**\n")
        for i, item in enumerate(r["matches"], 1):
            match_text = item.get("match", item.get("line", ""))
            lines.append(f"### {i}. {match_text[:150]}")
            if item.get("context"):
                lines.append(f"> {item['context'][:300]}")
            lines.append("")
    lines.append("---")
    lines.append(f"⏸️ 监控已暂停。回复 `resume {name}` 继续。")
    return '\n'.join(lines)


def save_report(config: dict, results: list[dict], match_type: str) -> Path:
    now = datetime.now()
    filename = f"web-monitor_{slugify(config['name'])}_{now.strftime('%Y%m%d_%H%M')}.md"
    path = REPORTS_DIR / filename
    with open(path, 'w') as f:
        f.write(format_report(config, results, match_type))
    print(f"📄 Report: {path}")
    return path


# ─── CLI Commands ───

def cmd_create(args):
    config = {
        "name": args.name,
        "description": args.description or f"Monitor: {args.name}",
        "urls": [{"url": args.url, "label": args.url_label or args.url}],
        "match": {
            "type": args.match_type,
            "value": args.match_value,
            "caseSensitive": args.case_sensitive
        },
        "interval": args.interval,
        "state": "active",
        "enabled": True,
        "createdAt": datetime.now(timezone.utc).isoformat()
    }
    save_monitor(config)


def cmd_list(args):
    monitors = list(MONITORS_DIR.glob("*.json"))
    if not monitors:
        print("No monitors. Use 'create' to add one.")
        return
    print(f"📋 Monitors ({len(monitors)}):\n")
    for mpath in sorted(monitors):
        with open(mpath) as f:
            c = json.load(f)
        state = c.get("state", "active")
        icon = {"active": "🟢", "paused": "⏸️", "disabled": "⏹️"}.get(state, "❓")
        print(f"  {icon} {c['name']} [{state}]")
        print(f"     {c.get('description', '')}")
        print(f"     URLs: {len(c.get('urls', []))} | Match: {c['match']['type']} | Interval: {c.get('interval', 'N/A')}s")
        print()


def cmd_show(args):
    config = load_monitor(args.event)
    print(json.dumps(config, indent=2, ensure_ascii=False))


def cmd_delete(args):
    path = MONITORS_DIR / f"{slugify(args.event)}.json"
    if path.exists():
        path.unlink()
        print(f"🗑️  Deleted: {args.event}")
    else:
        print(f"❌ Not found: {args.event}")


def cmd_add_url(args):
    config = load_monitor(args.event)
    config["urls"].append({"url": args.url, "label": args.label or args.url})
    save_monitor(config)
    print(f"✅ Added URL to '{args.event}'")


def cmd_resume(args):
    config = load_monitor(args.event)
    if config.get("state") == "active":
        print(f"ℹ️  '{args.event}' is already active.")
    else:
        set_state(config, "active")
        print(f"▶️  Resumed: {args.event}")


def cmd_pause(args):
    config = load_monitor(args.event)
    set_state(config, "paused")
    print(f"⏸️  Paused: {args.event}")


def cmd_disable(args):
    config = load_monitor(args.event)
    set_state(config, "disabled")
    print(f"⏹️  Disabled: {args.event}")


def cmd_enable(args):
    config = load_monitor(args.event)
    set_state(config, "active")
    print(f"🟢 Enabled: {args.event}")


def main():
    parser = argparse.ArgumentParser(description="Web Monitor v2 — fetch, match (keyword/regex/css/jsonpath), or extract for LLM")
    sub = parser.add_subparsers(dest="command")

    # create
    p = sub.add_parser("create", help="Create a new monitor")
    p.add_argument("--name", required=True)
    p.add_argument("--url", required=True)
    p.add_argument("--url-label")
    p.add_argument("--match-type", required=True, choices=["keyword", "regex", "css", "jsonpath", "llm"])
    p.add_argument("--match-value", required=True)
    p.add_argument("--interval", type=int, default=7200)
    p.add_argument("--description")
    p.add_argument("--case-sensitive", action="store_true")

    # run
    p = sub.add_parser("run", help="Run monitor(s)")
    p.add_argument("--event")
    p.add_argument("--all", action="store_true")
    p.add_argument("--json", action="store_true")

    # fetch — extract text only (for LLM match)
    p = sub.add_parser("fetch", help="Fetch page text (for LLM processing)")
    p.add_argument("--event", required=True)

    # list/show/delete/add-url/resume/pause/disable/enable
    sub.add_parser("list", help="List all monitors")

    for cmd in ["show", "delete", "add-url", "resume", "pause", "disable", "enable"]:
        p = sub.add_parser(cmd)
        p.add_argument("--event", required=True)
        if cmd == "add-url":
            p.add_argument("--url", required=True)
            p.add_argument("--label")

    args = parser.parse_args()

    commands = {
        "create": cmd_create, "run": cmd_run, "fetch": cmd_fetch,
        "list": cmd_list, "show": cmd_show, "delete": cmd_delete,
        "add-url": cmd_add_url, "resume": cmd_resume, "pause": cmd_pause,
        "disable": cmd_disable, "enable": cmd_enable,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
