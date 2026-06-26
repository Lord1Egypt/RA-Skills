#!/usr/bin/env python3
"""
GitHub Repo Growth Tracker
Track stars, forks, issues, and commits across repos with trend analysis.
Compare your repos against a watchlist of repos you care about.

Usage:
    python github_tracker.py setup --token TOKEN
    python github_tracker.py fetch
    python github_tracker.py digest
    python github_tracker.py add owner/repo [owner/repo2 ...] [--watch]
    python github_tracker.py remove owner/repo
    python github_tracker.py list
"""

import argparse
import json
import os
import sys
from datetime import date, timedelta
from urllib.request import Request, urlopen
from urllib.error import HTTPError

VERSION = "1.2.0"
MAX_HISTORY_DAYS = 90

# Paths — data lives outside the skill folder so it persists across skill updates
# SKILL_DATA_DIR is set by agent platforms; falls back to ~/.config/github-growth-tracker/
DATA_DIR = os.path.expanduser(
    os.environ.get("SKILL_DATA_DIR", "~/.config/github-growth-tracker")
)
CONFIG_PATH = os.path.join(DATA_DIR, "config.json")
REPOS_DIR = os.path.join(DATA_DIR, "repos")
CREDENTIALS_PATH = os.path.join(os.path.expanduser(
    os.environ.get("SKILL_DATA_DIR", "~/.config/github-growth-tracker")
), "github.json")


# ── GitHub API ──────────────────────────────────────────────────────────────

def github_api(endpoint, token):
    """Authenticated GitHub REST API v3 request. Returns parsed JSON or None."""
    url = f"https://api.github.com{endpoint}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "github-growth-tracker/1.0",
    }
    try:
        with urlopen(Request(url, headers=headers), timeout=15) as resp:
            return json.loads(resp.read().decode())
    except HTTPError as e:
        body = e.read().decode()[:200] if e.fp else ""
        print(f"API {e.code} on {endpoint}: {body}", file=sys.stderr)
        return None


def get_token():
    """Resolve token: env var > credentials file."""
    env = os.environ.get("GITHUB_TOKEN")
    if env:
        return env
    if os.path.exists(CREDENTIALS_PATH):
        with open(CREDENTIALS_PATH) as f:
            return json.load(f).get("github_token", "")
    return ""


def save_token(token):
    """Save token to <DATA_DIR>/github.json."""
    creds_dir = os.path.dirname(CREDENTIALS_PATH)
    os.makedirs(creds_dir, exist_ok=True)
    with open(CREDENTIALS_PATH, "w") as f:
        json.dump({"github_token": token}, f, indent=2)
        f.write("\n")
    os.chmod(CREDENTIALS_PATH, 0o600)


# ── Config & Storage ────────────────────────────────────────────────────────

def _ensure_dirs():
    os.makedirs(REPOS_DIR, exist_ok=True)


def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {"repos": [], "watched_repos": []}


def save_config(cfg):
    _ensure_dirs()
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)
        f.write("\n")


def _rkey(repo):
    """owner/repo → owner__repo (filesystem-safe)."""
    return repo.replace("/", "__")


def load_history(repo):
    path = os.path.join(REPOS_DIR, f"{_rkey(repo)}.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {"repo": repo, "history": []}


def save_history(repo, data):
    _ensure_dirs()
    # Trim history to MAX_HISTORY_DAYS
    cutoff = (date.today() - timedelta(days=MAX_HISTORY_DAYS)).isoformat()
    data["history"] = [h for h in data["history"] if h.get("date", "") >= cutoff]
    with open(os.path.join(REPOS_DIR, f"{_rkey(repo)}.json"), "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


# ── Helpers ─────────────────────────────────────────────────────────────────

def trend(cur, prev):
    """Return (arrow, delta) comparing two values."""
    if prev is None:
        return "NEW", 0
    d = cur - prev
    if d > 0:
        return "↑", d
    if d < 0:
        return "↓", d
    return "→", 0


def fetch_snapshot(repo, token):
    """Fetch a point-in-time snapshot of repo metrics."""
    data = github_api(f"/repos/{repo}", token)
    if not data:
        return None

    # Commit activity via participation API (weekly buckets, last 52 weeks)
    commits_4w = 0
    part = github_api(f"/repos/{repo}/stats/participation", token)
    if part and isinstance(part, dict) and "all" in part:
        weeks = part["all"]
        commits_4w = sum(weeks[-4:]) if len(weeks) >= 4 else sum(weeks)

    return {
        "date": date.today().isoformat(),
        "stars": data.get("stargazers_count", 0),
        "forks": data.get("forks_count", 0),
        "open_issues": data.get("open_issues_count", 0),
        "subscribers": data.get("subscribers_count", 0),
        "language": data.get("language"),
        "pushed_at": data.get("pushed_at"),
        "commits_4w": commits_4w,
    }


# ── Commands ────────────────────────────────────────────────────────────────

def cmd_setup(args):
    """List user's repos for initial selection."""
    token = args.token
    if token:
        save_token(token)

    # Resolve token after saving
    token = get_token()
    if not token:
        print("No GitHub token. Pass --token or set GITHUB_TOKEN env var.", file=sys.stderr)
        sys.exit(1)

    repos, page = [], 1
    while True:
        batch = github_api(f"/user/repos?per_page=100&sort=updated&type=owner&page={page}", token)
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1

    if not repos:
        print("No repos found. Ensure your token has public repo read access.")
        return

    repos.sort(key=lambda r: (-r.get("stargazers_count", 0), r.get("pushed_at", "")))
    print(f"Found {len(repos)} repos:\n")
    for i, r in enumerate(repos, 1):
        fork = " (fork)" if r.get("fork") else ""
        print(f"  {i:>3}. {r['full_name']}{fork}  ⭐ {r.get('stargazers_count', 0)}  "
              f"{r.get('language') or '?'}  updated {str(r.get('pushed_at', ''))[:10]}")

    print(f"\nUse 'add owner/repo [owner/repo2 ...]' to start tracking repos.")
    print(f"Use 'add owner/repo --watch' to add repos to your comparison watchlist.")


def cmd_fetch(args):
    """Fetch current metrics for all tracked repos."""
    token = get_token()
    if not token:
        print("No GitHub token. Run 'setup --token TOKEN' or set GITHUB_TOKEN env var.", file=sys.stderr)
        sys.exit(1)

    cfg = load_config()
    all_repos = list(dict.fromkeys(cfg.get("repos", []) + cfg.get("watched_repos", [])))
    if not all_repos:
        print("No repos tracked. Use 'add owner/repo' to start.")
        return

    today = date.today().isoformat()
    fetched = 0
    for repo in all_repos:
        snap = fetch_snapshot(repo, token)
        if not snap:
            print(f"  ⚠ {repo} (API error)")
            continue

        hist = load_history(repo)
        if hist["history"] and hist["history"][-1].get("date") == today:
            print(f"  ✓ {repo} (already recorded today)")
            continue

        hist["history"].append(snap)
        save_history(repo, hist)
        fetched += 1
        print(f"  ✓ {repo}")

    print(f"\nFetched {fetched} repos. Run 'digest' to see trends.")


def cmd_digest(args):
    """Generate a text digest with trend analysis and watchlist comparison."""
    cfg = load_config()
    repos = cfg.get("repos", [])
    watched = cfg.get("watched_repos", [])

    if not repos and not watched:
        print("No repos tracked.")
        return

    # Pre-load all snapshots for watchlist comparison
    watched_snaps = {}
    for repo in watched:
        hist = load_history(repo)
        if hist["history"]:
            watched_snaps[repo] = hist["history"][-1]

    lines = [f"📊 GitHub Growth Digest — {date.today().strftime('%A %B %d, %Y')}", "=" * 52]

    # Tracked repos (yours)
    if repos:
        lines.append("\n📌 Your Repos")
        for repo in repos:
            hist = load_history(repo)
            if not hist["history"]:
                lines.append(f"\n   {repo} — No data (run 'fetch')")
                continue

            cur = hist["history"][-1]
            prev = hist["history"][-2] if len(hist["history"]) >= 2 else None

            lines.append(f"\n   {repo}")
            for label, key in [("Stars", "stars"), ("Forks", "forks"), ("Issues", "open_issues"),
                               ("Subscribers", "subscribers"), ("Commits (4w)", "commits_4w")]:
                val = cur.get(key)
                if val is None:
                    continue
                pv = prev.get(key) if prev else None
                arrow, delta = trend(val, pv)
                if pv is not None and delta != 0:
                    lines.append(f"      {label}: {val:,} {arrow} ({delta:+d})")
                else:
                    lines.append(f"      {label}: {val:,} {arrow}")

            lang = cur.get("language") or "N/A"
            pushed = str(cur.get("pushed_at", ""))[:10] if cur.get("pushed_at") else "?"
            lines.append(f"      Lang: {lang}  Last push: {pushed}")

            # Watchlist verdict
            if watched_snaps:
                avg_commits = sum(s.get("commits_4w", 0) for s in watched_snaps.values()) / len(watched_snaps)
                own_commits = cur.get("commits_4w", 0)
                if own_commits > avg_commits * 1.2:
                    lines.append(f"      vs watchlist: ✅ above avg commit velocity")
                elif own_commits < avg_commits * 0.8:
                    lines.append(f"      vs watchlist: ⚠ below avg commit velocity")
                elif avg_commits > 0:
                    lines.append(f"      vs watchlist: ➡ on par")

    # Watched repos
    if watched:
        lines.append("\n📌 Watchlist")
        for repo in watched:
            hist = load_history(repo)
            if not hist["history"]:
                lines.append(f"\n   {repo} — No data (run 'fetch')")
                continue

            cur = hist["history"][-1]
            prev = hist["history"][-2] if len(hist["history"]) >= 2 else None

            lines.append(f"\n   {repo}")
            for label, key in [("Stars", "stars"), ("Forks", "forks"), ("Issues", "open_issues"),
                               ("Commits (4w)", "commits_4w")]:
                val = cur.get(key)
                if val is None:
                    continue
                pv = prev.get(key) if prev else None
                arrow, delta = trend(val, pv)
                if pv is not None and delta != 0:
                    lines.append(f"      {label}: {val:,} {arrow} ({delta:+d})")
                else:
                    lines.append(f"      {label}: {val:,} {arrow}")

    print("\n".join(lines))


def cmd_add(args):
    """Add repos to tracking."""
    cfg = load_config()
    token = get_token()
    watch = args.watch
    key = "watched_repos" if watch else "repos"

    for repo in args.repos:
        if token:
            data = github_api(f"/repos/{repo}", token)
            if not data:
                print(f"⚠ {repo} — not found or token lacks access", file=sys.stderr)
                continue

        if repo in cfg.get(key, []):
            print(f"  Already {key.rstrip('s').replace('_', ' ')} {repo}")
            continue

        cfg.setdefault(key, []).append(repo)
        print(f"  ✅ {repo}")

        # Fetch initial snapshot
        if token:
            snap = fetch_snapshot(repo, token)
            if snap:
                hist = load_history(repo)
                if not hist["history"] or hist["history"][-1].get("date") != date.today().isoformat():
                    hist["history"].append(snap)
                    save_history(repo, hist)

    save_config(cfg)
    label = "watching" if watch else "tracking"
    print(f"\n✅ Now {label} {len(args.repos)} repo(s)")


def cmd_remove(args):
    """Remove a repo from tracking (keeps history)."""
    cfg = load_config()
    repo = args.repo
    removed = False
    for key in ("repos", "watched_repos"):
        if repo in cfg.get(key, []):
            cfg[key].remove(repo)
            removed = True
    if removed:
        save_config(cfg)
        print(f"✅ Stopped tracking {repo}")
        print(f"   History preserved in {REPOS_DIR}/")
    else:
        print(f"{repo} is not being tracked.")


def cmd_list(args):
    """List tracked repos with latest stats."""
    cfg = load_config()
    repos = cfg.get("repos", [])
    watched = cfg.get("watched_repos", [])

    if not repos and not watched:
        print("No repos tracked. Use 'add owner/repo' to start.")
        return

    if repos:
        print("Your repos:\n")
        for repo in repos:
            hist = load_history(repo)
            if hist["history"]:
                h = hist["history"][-1]
                print(f"  📌 {repo} — ⭐ {h.get('stars', 0)}  🍴 {h.get('forks', 0)}  "
                      f"📋 {h.get('open_issues', 0)}  ({h.get('date', '?')})")
            else:
                print(f"  📌 {repo} — No data yet")

    if watched:
        print("\nWatchlist:\n")
        for repo in watched:
            hist = load_history(repo)
            if hist["history"]:
                h = hist["history"][-1]
                print(f"  👁 {repo} — ⭐ {h.get('stars', 0)}  🍴 {h.get('forks', 0)}  "
                      f"({h.get('date', '?')})")
            else:
                print(f"  👁 {repo} — No data yet")


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser(description="GitHub Repo Growth Tracker")
    p.add_argument("--version", action="version", version=f"github_tracker {VERSION}")
    sub = p.add_subparsers(dest="cmd")

    s = sub.add_parser("setup", help="List your repos for initial setup")
    s.add_argument("--token", help="GitHub PAT (saved to <DATA_DIR>/github.json)")

    sub.add_parser("fetch", help="Fetch current metrics for all tracked + watched repos")

    sub.add_parser("digest", help="Generate growth digest with trends and watchlist comparison")

    a = sub.add_parser("add", help="Add repos to tracking")
    a.add_argument("repos", nargs="+", help="owner/repo (space-separated for multiple)")
    a.add_argument("--watch", action="store_true", help="Add to watchlist instead of tracked repos")

    r = sub.add_parser("remove", help="Remove a repo from tracking (keeps history)")
    r.add_argument("repo", help="owner/repo")

    sub.add_parser("list", help="Show tracked repos and watchlist")

    args = p.parse_args()
    if not args.cmd:
        p.print_help()
        sys.exit(1)

    {"setup": cmd_setup, "fetch": cmd_fetch, "digest": cmd_digest,
     "add": cmd_add, "remove": cmd_remove, "list": cmd_list}[args.cmd](args)


if __name__ == "__main__":
    main()
