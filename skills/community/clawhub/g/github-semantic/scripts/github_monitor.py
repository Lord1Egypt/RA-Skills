#!/usr/bin/env python3
"""
GitHub Proactive Monitor — track repo activity and send alerts to Feishu.
Usage:
  python github_monitor.py watch owner/repo --events issues,prs,ci --keywords bug,broken,urgent
  python github_monitor.py status
  python github_monitor.py unwatch owner/repo
"""
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass, asdict
from pathlib import Path

os.environ.setdefault("OLLAMA_MODELS", r"D:\ChatAI\OpenClaw\.ollama\models")
os.environ.setdefault("PYTHONIOENCODING", "utf-8")

GH_EXE = r"C:\Program Files\GitHub CLI\gh.exe"
STATE_FILE = r"D:\ChatAI\OpenClaw\github_monitor_state.json"
CST = timezone(timedelta(hours=8))


@dataclass
class WatchConfig:
    repo: str
    events: list  # issues, prs, ci
    keywords: list
    last_check: str  # ISO timestamp


def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"watches": {}}


def save_state(state: dict):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def gh(args: str) -> dict:
    result = subprocess.run(
        f'"{GH_EXE}" {args}',
        capture_output=True, text=True, shell=False
    )
    if result.returncode != 0:
        return {}
    try:
        return json.loads(result.stdout) if result.stdout.strip() else {}
    except:
        return {}


def gh_list(args: str) -> list:
    result = subprocess.run(
        f'"{GH_EXE}" {args}',
        capture_output=True, text=True, shell=False
    )
    if result.returncode != 0:
        return []
    try:
        data = json.loads(result.stdout)
        return data if isinstance(data, list) else []
    except:
        return []


def send_feishu(message: str, user_id: str = "ou_4bf3393b288ddc97e3bfe1759bf99f43"):
    """Send alert to Feishu via openclaw."""
    result = subprocess.run(
        f'openclaw message send --channel feishu --to user:{user_id} --message {json.dumps(message)}',
        capture_output=True, text=True, shell=False
    )
    return result.returncode == 0


def check_new_issues(repo: str, since: str) -> list:
    """Find issues created after `since`."""
    items = gh_list(f"issue list --repo {repo} --state open --limit 50 --json number,title,body,createdAt,labels,url,author")
    return [i for i in items if i.get("createdAt", "") > since]


def check_new_prs(repo: str, since: str) -> list:
    """Find PRs created after `since`."""
    items = gh_list(f"pr list --repo {repo} --state open --limit 50 --json number,title,body,createdAt,labels,url,author,isDraft")
    return [i for i in items if i.get("createdAt", "") > since]


def check_ci_failures(repo: str, since: str) -> list:
    """Find failed CI runs after `since`."""
    items = gh_list(f"run list --repo {repo} --limit 30 --json id,name,status,conclusion,createdAt,headBranch,url")
    failures = []
    for r in items:
        if r.get("conclusion") == "failure" and r.get("createdAt", "") > since:
            failures.append(r)
    return failures


def keyword_match(text: str, keywords: list) -> list:
    """Check if text contains any keyword (case-insensitive)."""
    matched = []
    text_lower = text.lower()
    for kw in keywords:
        if kw.lower() in text_lower:
            matched.append(kw)
    return matched


def check_watch(watch: WatchConfig) -> list:
    """Check a single watched repo, return list of alerts."""
    since = watch.last_check
    alerts = []
    now = datetime.now(CST).isoformat()

    if "issues" in watch.events:
        new_issues = check_new_issues(watch.repo, since)
        for issue in new_issues:
            title = issue.get("title", "")
            body = issue.get("body", "") or ""
            matched_kw = keyword_match(title + " " + body, watch.keywords)
            labels = [l.get("name", "") for l in issue.get("labels", [])]
            alerts.append({
                "event": "issue",
                "number": issue["number"],
                "title": title,
                "url": issue.get("url", ""),
                "author": issue.get("author", {}).get("login", "unknown") if isinstance(issue.get("author"), dict) else str(issue.get("author", "unknown")),
                "labels": labels,
                "keywords": matched_kw,
                "priority": "high" if matched_kw else "normal",
                "repo": watch.repo
            })

    if "prs" in watch.events:
        new_prs = check_new_prs(watch.repo, since)
        for pr in new_prs:
            title = pr.get("title", "")
            body = pr.get("body", "") or ""
            matched_kw = keyword_match(title + " " + body, watch.keywords)
            labels = [l.get("name", "") for l in pr.get("labels", [])]
            is_draft = pr.get("isDraft", False)
            alerts.append({
                "event": "PR",
                "number": pr["number"],
                "title": title,
                "url": pr.get("url", ""),
                "author": pr.get("author", {}).get("login", "unknown") if isinstance(pr.get("author"), dict) else str(pr.get("author", "unknown")),
                "labels": labels,
                "keywords": matched_kw,
                "priority": "high" if matched_kw else "normal",
                "is_draft": is_draft,
                "repo": watch.repo
            })

    if "ci" in watch.events:
        failures = check_ci_failures(watch.repo, since)
        for run in failures:
            matched_kw = keyword_match(run.get("name", ""), watch.keywords)
            alerts.append({
                "event": "ci_failure",
                "workflow": run.get("name", "unknown"),
                "branch": run.get("headBranch", "unknown"),
                "url": run.get("url", ""),
                "conclusion": run.get("conclusion", "failure"),
                "repo": watch.repo,
                "keywords": matched_kw,
                "priority": "high"
            })

    return alerts


def format_alert(alert: dict) -> str:
    """Format alert as readable text."""
    repo = alert["repo"]
    priority = "🔴" if alert["priority"] == "high" else "🟡"
    event_icon = {"issue": "🆕", "PR": "📥", "ci_failure": "❌"}.get(alert["event"], "📌")
    event_label = {"issue": "New Issue", "PR": "New PR", "ci_failure": "CI Failed"}.get(alert["event"], alert["event"])

    lines = [
        f"{priority} **{event_label}** in `{repo}`",
        f"   #{alert['number']} — {alert['title']}",
        f"   Author: @{alert.get('author', 'unknown')} | Labels: {', '.join(alert.get('labels', []) or [])}",
        f"   🔗 {alert.get('url', '')}",
    ]
    if alert.get("keywords"):
        lines.append(f"   ⚠️ Keywords matched: {', '.join(alert['keywords'])}")
    if alert.get("workflow"):
        lines.append(f"   Workflow: {alert['workflow']} | Branch: {alert.get('branch', '?')}")
    return "\n".join(lines)


def cmd_watch(args):
    state = load_state()
    repo = args.repo
    events = [e.strip() for e in args.events.split(",")] if args.events else ["issues", "prs", "ci"]
    keywords = [k.strip() for k in args.keywords.split(",")] if args.keywords else ["bug", "broken", "urgent", "critical", "security"]
    now = datetime.now(CST).strftime("%Y-%m-%dT%H:%M:%S+08:00")
    state["watches"][repo] = asdict(WatchConfig(repo=repo, events=events, keywords=keywords, last_check=now))
    save_state(state)
    print(f"👁 Now watching {repo} for {events} | keywords: {keywords}")


def cmd_unwatch(args):
    state = load_state()
    if args.repo in state["watches"]:
        del state["watches"][args.repo]
        save_state(state)
        print(f"Stopped watching {args.repo}")
    else:
        print(f"Not watching {args.repo}")


def cmd_status(args):
    state = load_state()
    watches = state.get("watches", {})
    if not watches:
        print("No repos being watched. Use: github_monitor.py watch owner/repo")
        return
    print(f"Watching {len(watches)} repos:")
    for repo, cfg in watches.items():
        print(f"  👁 {repo} | events: {cfg['events']} | keywords: {cfg['keywords']} | last_check: {cfg['last_check'][:19]}")


def cmd_check(args):
    """Run all watches and print/send alerts."""
    state = load_state()
    watches = state.get("watches", {})
    if not watches:
        print("No watches configured.")
        return

    all_alerts = []
    for repo, cfg_dict in watches.items():
        watch = WatchConfig(**cfg_dict)
        alerts = check_watch(watch)
        if alerts:
            all_alerts.extend(alerts)
        # Update last_check
        now = datetime.now(CST).strftime("%Y-%m-%dT%H:%M:%S+08:00")
        watch.last_check = now
        state["watches"][repo]["last_check"] = now

    save_state(state)

    if not all_alerts:
        print("✅ No new activity.")
        return

    high_priority = [a for a in all_alerts if a["priority"] == "high"]
    normal = [a for a in all_alerts if a["priority"] == "normal"]

    print(f"📊 Found {len(all_alerts)} alerts ({len(high_priority)} high, {len(normal)} normal)")

    for alert in all_alerts:
        print(f"\n{format_alert(alert)}")

    # Send to Feishu if high priority
    if high_priority and args.feishu:
        msg = f"**🚨 GitHub Alert — {len(high_priority)} high priority event(s)**\n\n"
        msg += "\n\n".join(format_alert(a) for a in high_priority)
        send_feishu(msg)
        print("\n📨 High priority alert sent to Feishu.")


def main():
    parser = argparse.ArgumentParser(description="GitHub Proactive Monitor")
    sub = parser.add_subparsers(dest="cmd")

    watch = sub.add_parser("watch", help="Start watching a repo")
    watch.add_argument("repo", help="owner/repo")
    watch.add_argument("--events", default="issues,prs,ci", help="Events to watch (comma-separated)")
    watch.add_argument("--keywords", default="bug,broken,urgent,critical,security", help="Alert keywords (comma-separated)")

    sub.add_parser("status", help="Show watched repos")
    sub.add_parser("check", help="Run check on all watched repos")
    unwatch = sub.add_parser("unwatch", help="Stop watching a repo")
    unwatch.add_argument("repo", help="owner/repo")

    args = parser.parse_args()

    if args.cmd == "watch":
        cmd_watch(args)
    elif args.cmd == "unwatch":
        cmd_unwatch(args)
    elif args.cmd == "status":
        cmd_status(args)
    elif args.cmd == "check":
        cmd_check(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
