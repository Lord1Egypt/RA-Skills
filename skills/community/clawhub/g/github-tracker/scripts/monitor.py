import os
import json
import logging
import time
from collections import defaultdict
from pathlib import Path

import requests
from datetime import datetime, timedelta, timezone


ORG = "OpenPecha"
WINDOW_DAYS = 3
TEAM_SLUG = "openpecha-dev-team"
_ISO_TZ_OFFSET = "+00:00"
# (connect, read) avoids hanging indefinitely on slow TLS/handshake vs slow body.
_REQUEST_TIMEOUT = (15, 120)
# Initial request + 2 retries for transient API failures.
_GET_JSON_MAX_ATTEMPTS = 3
_RETRYABLE_HTTP = frozenset({429, 500, 502, 503, 504})

logger = logging.getLogger(__name__)


def _api_headers():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError(
            "Set GITHUB_TOKEN in your environment (Personal Access Token with repo scope)."
        )
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2026-03-10",
    }


def get_team():
    headers = _api_headers()
    logger.info("Fetching team members org=%s team=%s", ORG, TEAM_SLUG)
    url = f"https://api.github.com/orgs/{ORG}/teams/{TEAM_SLUG}/members"
    res = requests.get(url, headers=headers, timeout=_REQUEST_TIMEOUT)
    res.raise_for_status()
    members = [user["login"] for user in res.json()]
    logger.info("Fetched %d team members: %s", len(members), members)
    return members


def load_data(file, default):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return default


def _utc_today_date():
    return datetime.now(timezone.utc).date()


def commit_window_bounds():
    """
    Last WINDOW_DAYS calendar days in UTC, excluding the day of execution.
    Returns (start_date, end_date_exclusive) as date objects,
    and a range string for display (same as former GitHub committer-date search).
    """
    today = _utc_today_date()
    end = today  # exclusive upper bound (today is not included)
    start = today - timedelta(days=WINDOW_DAYS)
    last_inclusive = end - timedelta(days=1)
    date_range = f"{start.isoformat()}..{last_inclusive.isoformat()}"
    return start, end, date_range


def _window_to_since_until_iso(window_start, window_end_exclusive):
    """ISO timestamps for GET /repos/.../commits (since / until)."""
    since_dt = datetime(
        window_start.year,
        window_start.month,
        window_start.day,
        0,
        0,
        0,
        tzinfo=timezone.utc,
    )
    until_dt = datetime(
        window_end_exclusive.year,
        window_end_exclusive.month,
        window_end_exclusive.day,
        0,
        0,
        0,
        tzinfo=timezone.utc,
    )
    return (
        since_dt.isoformat().replace(_ISO_TZ_OFFSET, "Z"),
        until_dt.isoformat().replace(_ISO_TZ_OFFSET, "Z"),
    )


def _datetime_utc_midnight(d):
    """Start of calendar day d in UTC."""
    return datetime(d.year, d.month, d.day, 0, 0, 0, tzinfo=timezone.utc)


def _parse_github_iso_datetime(raw):
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", _ISO_TZ_OFFSET))
    except ValueError:
        return None


def _repo_pushed_before_window(repo, window_start_date):
    """
    True if repo's last push was strictly before the commit window start (UTC).
    Unknown/missing pushed_at -> False (still scan). Heuristic: can miss rare
    backdated commits pushed before the window.
    """
    pushed = _parse_github_iso_datetime(repo.get("pushed_at"))
    if pushed is None:
        return False
    window_start = _datetime_utc_midnight(window_start_date)
    return pushed < window_start


def _get_json_allow_missing(url, headers, params=None):
    """GET JSON; return None on 403/404 so one repo cannot stop the run."""
    params = params or {}
    for attempt in range(_GET_JSON_MAX_ATTEMPTS):
        try:
            r = requests.get(
                url, headers=headers, params=params, timeout=_REQUEST_TIMEOUT
            )
        except requests.RequestException as e:
            if attempt < _GET_JSON_MAX_ATTEMPTS - 1:
                time.sleep(1 + attempt)
                continue
            logger.warning(
                "skipped (request error after %s tries): %s (%r)",
                _GET_JSON_MAX_ATTEMPTS,
                url,
                e,
            )
            return None

        if r.status_code in (403, 404):
            return None
        if r.ok:
            return r.json()
        if r.status_code in _RETRYABLE_HTTP:
            if attempt < _GET_JSON_MAX_ATTEMPTS - 1:
                time.sleep(1 + attempt)
                continue
            logger.warning(
                "skipped (HTTP %s after %s tries): %s",
                r.status_code,
                _GET_JSON_MAX_ATTEMPTS,
                url,
            )
            return None
        r.raise_for_status()
        return r.json()


def get_org_repo_total(headers):
    """
    Approximate total repos in the org (public + private when the API exposes both).
    Used only to report repos_skipped_stale_push after early exit.
    """
    data = _get_json_allow_missing(f"https://api.github.com/orgs/{ORG}", headers)
    if not data:
        return None
    pub = data.get("public_repos") or 0
    priv = data.get("total_private_repos")
    if priv is None:
        return pub
    return pub + priv


def _iter_org_repos(headers):
    page = 1
    while True:
        data = _get_json_allow_missing(
            f"https://api.github.com/orgs/{ORG}/repos",
            headers,
            {
                "per_page": 100,
                "page": page,
                "type": "all",
                "sort": "pushed",
                "direction": "desc",
            },
        )
        if not data:
            break
        yield from data
        if len(data) < 100:
            break
        page += 1


def _iter_repo_branches(headers, owner, repo):
    page = 1
    while True:
        data = _get_json_allow_missing(
            f"https://api.github.com/repos/{owner}/{repo}/branches",
            headers,
            {"per_page": 100, "page": page},
        )
        if not data:
            break
        yield from data
        if len(data) < 100:
            break
        page += 1


def _committer_date(commit_obj):
    commit = commit_obj.get("commit") or {}
    committer = commit.get("committer") or {}
    raw = committer.get("date")
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", _ISO_TZ_OFFSET)).date()
    except ValueError:
        return None


def _commit_author_login(commit_obj):
    """GitHub user login for the commit author, if present (matches `author` API filter)."""
    author = commit_obj.get("author")
    if not author:
        return None
    return author.get("login")


def _paginate_commits_for_branch(
    headers, owner, repo, branch_name, since_iso, until_iso, author=None
):
    """
    Newest-first commits reachable from branch_name, optionally filtered by author.
    Stops early once the page is entirely before the window (descending order).
    """
    page = 1
    while True:
        params = {
            "sha": branch_name,
            "since": since_iso,
            "until": until_iso,
            "per_page": 100,
            "page": page,
        }
        if author:
            params["author"] = author
        batch = _get_json_allow_missing(
            f"https://api.github.com/repos/{owner}/{repo}/commits",
            headers,
            params,
        )
        if not batch:
            break
        yield from batch
        if len(batch) < 100:
            break
        oldest = _committer_date(batch[-1])
        if oldest is not None:
            window_start = datetime.fromisoformat(
                since_iso.replace("Z", _ISO_TZ_OFFSET)
            ).date()
            if oldest < window_start:
                break
        page += 1


def fetch_team_commit_days_all_branches(members, window_start, window_end_exclusive):
    """
    GitHub /search/commits only indexes the default branch. To count activity on
    any branch, list commits per branch with since/until (one pass for the whole
    team), attribute by author login, dedupe by SHA per user.

    Org repos are listed with sort=pushed desc. On the first repo whose
    pushed_at is before the commit window start (UTC), we stop: all later
    repos are older or equal and are omitted (saves API calls). Rare false
    negatives if commits are backdated and pushed before the window.

    Returns (user -> days_with_commits_iso_set, user -> meta_dict).
    """
    headers = _api_headers()
    org_repo_total = get_org_repo_total(headers)
    since_iso, until_iso = _window_to_since_until_iso(
        window_start, window_end_exclusive
    )
    team_logins = set(members)
    seen_shas = {u: set() for u in members}
    days = {u: set() for u in members}
    # Per user: full_name -> branch -> count (first branch wins for duplicate SHAs)
    breakdown = {u: defaultdict(lambda: defaultdict(int)) for u in members}
    repos_scanned = 0
    branch_requests = 0
    skipped_repos = 0
    stale_push_early_exit = False

    logger.info("Fetching commits (one org pass for all team members)")
    for repo in _iter_org_repos(headers):
        full = repo.get("full_name") or ""
        if "/" not in full:
            continue
        if _repo_pushed_before_window(repo, window_start):
            stale_push_early_exit = True
            logger.info(
                "Stale push cutoff — remaining repos omitted (sort=pushed desc): "
                "%s pushed_at=%s",
                full,
                repo.get("pushed_at"),
            )
            break
        owner, name = full.split("/", 1)
        repos_scanned += 1
        logger.info("repo %s: %s", repos_scanned, full)
        branches = list(_iter_repo_branches(headers, owner, name))
        if not branches:
            skipped_repos += 1
            continue
        for br in branches:
            branch_name = br.get("name")
            if not branch_name:
                continue
            branch_requests += 1
            for commit_obj in _paginate_commits_for_branch(
                headers, owner, name, branch_name, since_iso, until_iso
            ):
                login = _commit_author_login(commit_obj)
                if not login or login not in team_logins:
                    continue
                sha = commit_obj.get("sha")
                if not sha or sha in seen_shas[login]:
                    continue
                seen_shas[login].add(sha)
                d = _committer_date(commit_obj)
                if d is None:
                    continue
                if window_start <= d < window_end_exclusive:
                    days[login].add(d.isoformat())
                    breakdown[login][full][branch_name] += 1

    if stale_push_early_exit and org_repo_total is not None:
        repos_skipped_stale_push = max(0, org_repo_total - repos_scanned)
    elif stale_push_early_exit:
        repos_skipped_stale_push = None
    else:
        repos_skipped_stale_push = 0

    def _breakdown_plain(u):
        out = {}
        for repo in sorted(breakdown[u].keys()):
            br = breakdown[u][repo]
            out[repo] = {b: br[b] for b in sorted(br.keys())}
        return out

    shared_meta = {
        "mode": "all_branches",
        "repos_scanned": repos_scanned,
        "branch_requests": branch_requests,
        "repos_with_no_branches": skipped_repos,
        "stale_push_early_exit": stale_push_early_exit,
        "org_repo_total": org_repo_total,
        "repos_skipped_stale_push": repos_skipped_stale_push,
        "since": since_iso,
        "until": until_iso,
    }
    meta_by_user = {
        u: {
            **shared_meta,
            "unique_commits_in_window": len(seen_shas[u]),
            "commit_breakdown": _breakdown_plain(u),
        }
        for u in members
    }
    return days, meta_by_user


def _breakdown_rows_sorted_by_commit_count(bd):
    """(repo, branch, n) sorted by n descending, then repo and branch name."""
    rows = []
    for repo, branches in bd.items():
        for branch, n in branches.items():
            rows.append((repo, branch, n))
    rows.sort(key=lambda x: (-x[2], x[0], x[1]))
    return rows


def _apply_skip_credits(state_user, skip_dates_iso):
    """
    Increment total_skips once per calendar day with no commits, only the first time we credit it.
    """
    credited = set(state_user.get("skip_credited_dates") or [])
    added = 0
    for d in sorted(skip_dates_iso):
        if d not in credited:
            credited.add(d)
            added += 1
    state_user["skip_credited_dates"] = sorted(credited)
    state_user["total_skips"] = state_user.get("total_skips", 0) + added
    return added


def run_monitor():
    members = get_team()
    state = load_data("state.json", {})

    start_d, end_d, date_range = commit_window_bounds()
    window_dates = [
        (start_d + timedelta(days=i)).isoformat() for i in range(WINDOW_DAYS)
    ]
    lines = [
        f"Window (UTC): {date_range} (exclusive of today, {WINDOW_DAYS} days); "
        f"commits from all branches (not search API); "
        f"repos listed sort=pushed desc; stop at first pushed_at before window (omit rest)"
    ]
    days_by_user, meta_by_user = fetch_team_commit_days_all_branches(
        members, start_d, end_d
    )
    if members:
        fm = meta_by_user[members[0]]
        rss = fm["repos_skipped_stale_push"]
        rss_s = "unknown" if rss is None else str(rss)
        lines.append(
            f"Repo pass: repos_scanned={fm['repos_scanned']}, "
            f"repos_skipped_stale_push={rss_s}, "
            f"branch_requests={fm['branch_requests']}"
        )
    for user in members:
        days_with_commits = days_by_user[user]
        fetch_meta = meta_by_user[user]

        if user not in state:
            state[user] = {"total_skips": 0, "skip_credited_dates": []}
        else:
            su = state[user]
            su.setdefault("skip_credited_dates", [])
            su.setdefault("total_skips", 0)

        skip_dates = [d for d in window_dates if d not in days_with_commits]
        window_skip_days = len(skip_dates)
        _apply_skip_credits(state[user], skip_dates)

        state[user]["fetch_meta"] = fetch_meta
        state[user]["commit_breakdown"] = fetch_meta.get("commit_breakdown") or {}
        state[user]["window_skip_days"] = window_skip_days
        state[user]["window_dates"] = window_dates
        state[user]["days_with_commits_in_window"] = sorted(days_with_commits)

    lines.append("")
    lines.append("Active:")
    active = []
    for user in members:
        bd = meta_by_user[user].get("commit_breakdown") or {}
        total = meta_by_user[user]["unique_commits_in_window"]
        if total > 0:
            active.append((user, total, bd))
    active.sort(key=lambda x: (-x[1], x[0]))
    if not active:
        lines.append("  (none)")
    else:
        for user, _total, bd in active:
            lines.append(user)
            for repo, branch, n in _breakdown_rows_sorted_by_commit_count(bd):
                lines.append(f"  {repo} @ {branch}: {n} commit(s)")

    lines.append("")
    lines.append("Inactive:")
    inactive = sorted(
        u for u in members if meta_by_user[u]["unique_commits_in_window"] == 0
    )
    if not inactive:
        lines.append("  (none)")
    else:
        for user in inactive:
            lines.append(user)

    with open("state.json", "w") as f:
        json.dump(state, f, indent=4)

    return "\n".join(lines)


if __name__ == "__main__":
    _lvl = os.environ.get("MONITOR_LOG_LEVEL", "INFO").upper()
    _log_file = Path(
        os.environ.get("MONITOR_LOG_FILE", Path(__file__).resolve().parent / "monitor.log")
    )
    _log_file.parent.mkdir(parents=True, exist_ok=True)
    _handler = logging.FileHandler(_log_file, encoding="utf-8")
    _fmt = logging.Formatter(
        fmt="%(asctime)s UTC | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    _fmt.converter = time.gmtime
    _handler.setFormatter(_fmt)
    logging.basicConfig(
        level=getattr(logging, _lvl, logging.INFO),
        handlers=[_handler],
        force=True,
    )
    print(run_monitor())
