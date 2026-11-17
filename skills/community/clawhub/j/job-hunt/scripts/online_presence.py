#!/usr/bin/env python3
"""Ask once for a candidate's public profiles, watch them, confirm, write back.

The record lives at <profile_dir>/online-presence.yaml (scripts/paths.py). Sources
are GitHub, Google Scholar and a personal website; nothing needing a login.
Design: docs/superpowers/specs/2026-11-01-online-presence-design.md.
"""
from __future__ import annotations

import argparse
import contextlib
import datetime
import difflib
import json
import os
import pathlib
import re
import sys
import tempfile
import unicodedata
import urllib.error
import urllib.request

import journal
import paths

SOURCES = ("github", "scholar", "website")
ASK_STATUSES = ("given", "none", "declined")
OUTCOMES = ("ok", "refused", "failed", "not_checked")
STALE_DAYS = 14
LINK_KEYS = {"github": "github", "scholar": "scholar", "website": "website"}


def empty_record() -> dict:
    return {"sources": {}, "checks": {}, "findings": [], "writebacks": []}


def load_record(path) -> dict:
    """The record at `path`, or an empty one when absent. Unreadable raises YamlUnreadable."""
    path = pathlib.Path(path)
    if not path.exists():
        return empty_record()
    data = journal.load_yaml(path)
    record = empty_record()
    for key, kind in (("sources", dict), ("checks", dict), ("findings", list), ("writebacks", list)):
        value = data.get(key, record[key])
        if not isinstance(value, kind):
            raise journal.YamlUnreadable(path, f"`{key}` must be a {kind.__name__}")
        record[key] = value
    for key, value in data.items():
        record.setdefault(key, value)
    return record


def save_record(path, record: dict) -> None:
    """Write atomically, so a crash never leaves half a record."""
    import yaml
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".online-presence-", suffix=".yaml")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        yaml.safe_dump(record, fh, allow_unicode=True, sort_keys=False)
    os.replace(tmp, path)


def resolve_record_path(path) -> pathlib.Path:
    """Follow a `shared_with` stub to the record it points at (one hop)."""
    path = pathlib.Path(path)
    if not path.exists():
        return path
    shared = journal.load_yaml(path).get("shared_with")
    if not shared:
        return path
    target = path.parent.parent / str(shared) / paths.ONLINE_PRESENCE_NAME
    if not target.exists():
        raise ValueError(f"{path} is shared with {shared!r}, which has no online-presence record")
    return target


def _record_path(name: str) -> pathlib.Path:
    return resolve_record_path(paths.online_presence(name))


def _other_records(name: str) -> list:
    own = paths.online_presence(name)
    if own.exists() and journal.load_yaml(own).get("shared_with"):
        return []
    out = []
    root = paths.PROFILES_ROOT
    if not root.is_dir():
        return out
    for directory in sorted(root.iterdir()):
        candidate = directory / paths.ONLINE_PRESENCE_NAME
        if directory == own.parent or not candidate.is_file():
            continue
        try:
            if journal.load_yaml(candidate).get("shared_with"):
                continue
        except journal.YamlUnreadable:
            continue
        out.append(directory.name)
    return out


def link(name: str, other: str, words: str) -> None:
    """Point this person's directory at another directory's record."""
    if not (words or "").strip():
        raise ValueError("record the user's own words")
    slug = paths.slugify(other)
    target = paths.PROFILES_ROOT / slug / paths.ONLINE_PRESENCE_NAME if slug else None
    if target is None or not target.is_file():
        raise ValueError(f"{other!r} has no online-presence record to share")
    own = paths.online_presence(name)
    if own.exists():
        existing = load_record(own)
        if existing["sources"] or existing["findings"] or existing["writebacks"]:
            raise ValueError(f"{own} already holds its own answers; it cannot become a link")
    save_record(own, {"shared_with": slug, "words": words, "date": datetime.date.today().isoformat()})


def _seed_from_masters(name: str, record: dict) -> bool:
    """Copy github/scholar/website links a master already holds; True if anything changed."""
    changed = False
    for master in paths.master_profiles(name).values():
        try:
            data = journal.load_yaml(master)
        except journal.YamlUnreadable:
            continue
        links = journal.as_mapping(journal.as_mapping(data.get("contact")).get("links"))
        for source, key in LINK_KEYS.items():
            value = links.get(key)
            if isinstance(value, dict):
                value = value.get("url")
            if source not in record["sources"] and isinstance(value, str) and value.strip():
                value = value.strip()
                if source == "github":
                    with contextlib.suppress(ValueError):
                        value = github_username(value)
                record["sources"][source] = {"status": "given", "value": value,
                                             "words": "from master contact.links",
                                             "date": datetime.date.today().isoformat()}
                changed = True
    return changed


def status(name: str, today: datetime.date) -> dict:
    path = _record_path(name)
    record = load_record(path)
    if _seed_from_masters(name, record):
        save_record(path, record)
    to_ask, stale, broken, refused, malformed = [], [], [], [], []
    for source in SOURCES:
        raw = record["sources"].get(source)
        if raw is not None and (not isinstance(raw, dict) or raw.get("status") not in ASK_STATUSES
                                or (raw.get("status") == "given" and not _usable(source, raw.get("value")))):
            # The user answered once; a hand-edited or damaged entry is shown for
            # repair, never turned back into a question they already answered.
            malformed.append(source)
            continue
        answer = journal.as_mapping(raw)
        if answer.get("status") not in ASK_STATUSES:
            to_ask.append(source)
            continue
        if answer["status"] != "given":
            continue
        check = journal.as_mapping(record["checks"].get(source))
        if check.get("outcome") == "failed" and check.get("code") == 404:
            broken.append(source)
            continue
        if check.get("outcome") == "refused":
            refused.append(source)
        try:
            last = datetime.date.fromisoformat(str(check.get("date")))
        except ValueError:
            last = None
        # Only a successful check is current. A refusal or a failure must be tried
        # again next run, never shown as "fresh" (that would read as "nothing new").
        if last is None or check.get("outcome") != "ok" or (today - last).days > STALE_DAYS:
            stale.append(source)
    own = paths.online_presence(name)
    shared_with = journal.load_yaml(own).get("shared_with") if own.exists() else None
    return {"to_ask": to_ask, "stale": stale, "broken": broken, "refused": refused,
            "malformed": malformed, "shared_with": shared_with, "other_records": _other_records(name),
            "pending_for_master": _pending_for_master(name, record)}


# Underscores appear only in Enterprise Managed User names (e.g. jane_acme).
_GITHUB_USER = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9_]|-(?=[A-Za-z0-9])){0,38}$")
_GITHUB_URL = re.compile(r"^(?:https?://)?(?:www\.)?github\.com/(?P<user>[^/?#]+)/?(?:[?#].*)?$", re.I)


def github_username(value: str) -> str:
    """The username in `jane`, `@jane`, `github.com/jane` or `https://www.github.com/jane/`.

    Anything else (another site, a repository URL, characters GitHub does not
    allow) raises ValueError: guessing would send the check to a wrong account.
    """
    text = str(value or "").strip()
    match = _GITHUB_URL.match(text)
    user = match.group("user") if match else text.lstrip("@")
    if not _GITHUB_USER.match(user):
        raise ValueError(f"{value!r} is not a GitHub username or profile URL "
                         "(give the username, e.g. octocat, or https://github.com/octocat)")
    return user


def _usable(source: str, value) -> bool:
    if not (isinstance(value, str) and value.strip()):
        return False
    if source == "github":
        try:
            github_username(value)
        except ValueError:
            return False
    return True


def record_answer(name: str, source: str, status: str, value, words: str,
                  extra: list | None = None) -> None:
    if source not in SOURCES or status not in ASK_STATUSES:
        raise ValueError(f"unknown source/status {source!r}/{status!r}")
    if status == "given" and not (value or "").strip():
        raise ValueError(f"{source}: status given needs the profile value")
    if status == "given" and source == "github":
        value = github_username(value)
    if not (words or "").strip():
        raise ValueError("record the user's own words")
    path = _record_path(name)
    record = load_record(path)
    entry = {"status": status, "value": (value or "").strip() or None, "words": words,
             "date": datetime.date.today().isoformat()}
    if extra:
        entry["extra"] = list(extra)
    record["sources"][source] = entry
    save_record(path, record)


GITHUB_API = "https://api.github.com"
REFUSED_CODES = (401, 403, 429)
PER_PAGE = 100
MAX_PAGES = 10


def http_get(url: str) -> tuple[int, bytes]:
    """GET `url`; (status, body). Never raises: a transport error is (0, b"")."""
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "job-hunt-online-presence"}
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as exc:
        try:
            body = exc.read() if exc.fp else b""
        except OSError:
            body = b""
        return exc.code, body
    except (urllib.error.URLError, OSError, TimeoutError):
        return 0, b""


class _Stop(Exception):
    def __init__(self, outcome, code, reason=""):
        self.outcome, self.code, self.reason = outcome, code, reason


def fetch_github(username: str, extra: list, get) -> dict:
    """Public repositories the user owns or contributed to, as one snapshot.

    Forks, archived repositories and organisation repositories without a commit
    by the user are left out. Any 401/403/429 refuses the whole fetch: a partial
    listing would read as "these are all the repositories".
    """
    raw = []

    def call(url, missing_ok=False, empty_ok=False):
        status, body = get(url)
        raw.append((url, status, body))
        if status in REFUSED_CODES:
            raise _Stop("refused", status)
        if status == 404 and missing_ok:
            return None
        if empty_ok and status in (202, 204):
            # 204: an empty repository has no contributors. 202: GitHub is still
            # computing the list; the repository is left out this run, not the fetch.
            return []
        if status != 200:
            raise _Stop("failed", status or None)
        try:
            return json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            raise _Stop("failed", status)

    def call_list(url, missing_ok=False, empty_ok=False):
        """Every page of a listing; a listing longer than MAX_PAGES is not complete."""
        items = call(url, missing_ok=missing_ok, empty_ok=empty_ok)
        if items is None:
            return None
        page, last = 1, items
        while isinstance(last, list) and len(last) >= PER_PAGE:
            if page >= MAX_PAGES:
                raise _Stop("failed", None, f"partial listing: more than {MAX_PAGES * PER_PAGE} entries at {url}")
            page += 1
            last = call(f"{url}&page={page}") or []
            items = items + last
        return items

    user = username.strip().lower()
    candidates, missing = [], []
    try:
        owned = call_list(f"{GITHUB_API}/users/{username}/repos?per_page=100&type=owner")
        candidates += [(r, "owner") for r in owned or []]
        for item in extra or []:
            item = item.strip().strip("/")
            if "/" in item:
                found = call(f"{GITHUB_API}/repos/{item}", missing_ok=True)
                if found is None:
                    missing.append(item)
                else:
                    candidates.append((found, None))
            elif item:
                listing = call_list(f"{GITHUB_API}/orgs/{item}/repos?per_page=100", missing_ok=True)
                if listing is None:
                    missing.append(item)
                else:
                    candidates += [(r, None) for r in listing]
        repos, seen = [], set()
        for data, role in candidates:
            full = data.get("full_name")
            if not full or full in seen or data.get("fork") or data.get("archived"):
                continue
            seen.add(full)
            if role is None:
                if str(journal.as_mapping(data.get("owner")).get("login", "")).lower() == user:
                    role = "owner"
                else:
                    people = call_list(f"{GITHUB_API}/repos/{full}/contributors?per_page=100",
                                       missing_ok=True, empty_ok=True) or []
                    logins = [str(p.get("login", "")).lower() for p in people if isinstance(p, dict)]
                    if user not in logins:
                        continue
                    role = "top_contributor" if logins[0] == user else "contributor"
            release = call(f"{GITHUB_API}/repos/{full}/releases/latest", missing_ok=True)
            repos.append({
                "full_name": full, "html_url": data.get("html_url"),
                "description": data.get("description"), "created_at": data.get("created_at"),
                "pushed_at": data.get("pushed_at"), "stars": data.get("stargazers_count"),
                "forks": data.get("forks_count"),
                "latest_release": (release or {}).get("tag_name") if isinstance(release, dict) else None,
                "topics": data.get("topics") or [], "role": role})
    except _Stop as stop:
        return {"outcome": stop.outcome, "code": stop.code, "reason": stop.reason, "repos": [],
                "missing_extra": missing, "raw": raw}
    return {"outcome": "ok", "code": 200, "repos": repos, "missing_extra": missing, "raw": raw}


def write_snapshot(name: str, source: str, snapshot: dict, today: datetime.date,
                   workspace=None) -> pathlib.Path:
    """Save the snapshot (without raw bodies) and each raw response beside it."""
    base = paths.online_presence_dir(name)
    (base / "snapshots").mkdir(parents=True, exist_ok=True)
    (base / "raw").mkdir(parents=True, exist_ok=True)
    stem = f"{today.isoformat()}-{source}"
    n_same_day = 1
    while (base / "snapshots" / f"{stem}.json").exists():
        # A forced re-check on the same day must not overwrite the snapshot it is
        # compared against: the diff would then compare a file with itself.
        n_same_day += 1
        stem = f"{today.isoformat()}-{source}-{n_same_day}"
    raw_files = []
    for n, (url, status, body) in enumerate(snapshot.get("raw", []), 1):
        rel = f"raw/{stem}-{n}.json"
        (base / rel).write_bytes(json.dumps({"url": url, "status": status}).encode() + b"\n" + body)
        raw_files.append(rel)
    data = {k: v for k, v in snapshot.items() if k != "raw"}
    data.update(source=source, date=today.isoformat(), raw_files=raw_files)
    path = base / "snapshots" / f"{stem}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if workspace is not None:
        journal.append(workspace, {"action": "online_presence_fetch", "source": source,
                                   "outcome": data.get("outcome"), "code": data.get("code"),
                                   "snapshot": str(path), "date": today.isoformat()})
    return path


_VENUE_YEAR = re.compile(r"^(?P<venue>.+?),\s*(?P<year>(?:19|20)\d{2})$")
_YEAR_LINE = re.compile(r"^(?:19|20)\d{2}$")
_CITES_LINE = re.compile(r"^(?:\d[\d,.]*|\*)$")
_SCHOLAR_HEADER = ("title", "cited by", "year")
_SCHOLAR_FOOTER = re.compile(r"^(?:articles\s+\d|show more$|privacy$|terms$|help$)", re.I)
_SCHOLAR_TOTAL = re.compile(r"^articles\s+\d+\s*[–-]\s*(?P<n>\d+)", re.I)
_SCHOLAR_EMPTY = re.compile(r"no articles|没有(?:任何)?文章|記事はありません", re.I)


def _capture_outcome(data: dict) -> tuple[str, int | None]:
    """ok / refused / failed for a browser capture, using the shared stop signals."""
    status = data.get("http_status")
    code = status if isinstance(status, int) else None
    if data.get("blocked") or code in REFUSED_CODES:
        return "refused", code
    text = str(data.get("text") or "")
    import check_opencli_result
    for signal in check_opencli_result.load_signals(check_opencli_result.DEFAULT_SIGNALS_FILE):
        if signal["regex"].search(text):
            return "refused", code
    if code is not None and code >= 400:
        return "failed", code
    if not text.strip():
        return "failed", code
    return "ok", code or 200


def _read_capture(path) -> dict:
    data = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: a browser capture is a JSON object")
    return data


def _scholar_rows(lines: list) -> tuple[list, list]:
    """Split the article table into rows; (rows, lines that fit no row).

    A row is title / authors / venue, then optional citation and "*" lines, then
    the year. Citations or a year close a row, so a paper with neither runs into
    the next one: such a run is cut into threes, the last three being the closed
    row, and a remainder that is not a multiple of three is reported, not guessed.
    A run the table ends on without any closing line is never cut: lines nothing
    delimits are not evidence of papers. Neither is a run longer than three that
    is not a multiple of three: some paper lacks a line and the boundaries are
    unknown, so the whole run is reported instead of guessed (guessing turned a
    venue into a "paper" the user could confirm). A number or year that opens a
    row, or follows a lone title, is that row's text: a title can be "2048".
    """
    rows, skipped, text, cites, closed = [], [], [], None, False

    def flush(year, at_end=False):
        nonlocal text, cites, closed
        if (at_end and not closed and len(text) > 3) or (len(text) > 3 and len(text) % 3):
            skipped.extend(text)
            text = []
        if text:
            head, tail = text[:-3], text[-3:]
            if len(text) <= 3:
                head, tail = [], text
            whole = len(head) - len(head) % 3
            for k in range(0, whole, 3):
                rows.append((head[k:k + 3], None, None))
            skipped.extend(head[whole:])
            rows.append((tail, cites, year))
        text, cites, closed = [], None, False

    for line in lines:
        if _YEAR_LINE.match(line) and text:
            flush(int(line))
        elif _CITES_LINE.match(line) and (len(text) >= 2 or (line == "*" and text)):
            if line != "*" and text:
                cites = int(re.sub(r"[,.]", "", line))
            closed = bool(text)
        else:
            if line == "*":
                continue
            if closed:
                flush(None)
            text.append(line)
    flush(None, at_end=True)
    return rows, skipped


def ingest_scholar(capture) -> dict:
    """Papers listed on a captured Google Scholar profile page (English layout).

    Only the article table counts: the lines after the "Title / Cited by / Year"
    header up to the "Articles 1–N" footer. Everything above it (the citation
    chart, whose year axis looks like rows) is ignored. When the footer gives a
    total and fewer papers were read, the snapshot carries a `warning`.
    """
    data = _read_capture(capture)
    outcome, code = _capture_outcome(data)
    if outcome != "ok":
        return {"outcome": outcome, "code": code, "papers": []}
    text = str(data.get("text", ""))
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    lowered = [line.lower() for line in lines]
    start = next((k + 3 for k in range(len(lines) - 2)
                  if tuple(lowered[k:k + 3]) == _SCHOLAR_HEADER), None)
    papers, skipped, expected = [], [], None
    if start is not None:
        table = lines[start:]
        total_at = next((k for k, line in enumerate(table) if _SCHOLAR_TOTAL.match(line)), None)
        if total_at is not None:
            expected = int(_SCHOLAR_TOTAL.match(table[total_at]).group("n"))
            table = table[:total_at]
        else:
            # Without the total line, only the trailing run of footer words is the
            # footer: a paper may be titled "Help".
            while table and _SCHOLAR_FOOTER.match(table[-1]):
                table = table[:-1]
        rows, skipped = _scholar_rows(table)
        for parts, cites, year in rows:
            if len(parts) < 2:
                skipped.extend(parts)
                continue
            venue = parts[2] if len(parts) > 2 else ""
            match = _VENUE_YEAR.match(venue)
            if match and (year is None or int(match.group("year")) == year):
                venue, year = match.group("venue").strip(), int(match.group("year"))
            papers.append({"title": parts[0], "authors": parts[1], "venue": venue,
                           "year": year, "citations": cites})
    if not papers and not _SCHOLAR_EMPTY.search(text):
        # A layout this parser does not know must not read as "no new papers".
        where = "no \"Title / Cited by / Year\" header" if start is None else "an empty table"
        return {"outcome": "failed", "code": code, "papers": [],
                "reason": f"no papers recognised in {len(lines)} lines ({where}); capture the "
                          "profile with hl=en and check the capture by eye"}
    result = {"outcome": "ok", "code": code, "url": data.get("url"), "papers": papers,
              "expected": expected}
    if not papers:
        return result  # the page says the profile has no articles
    problems = []
    if expected is not None and len(papers) < expected:
        problems.append(f"read {len(papers)} of the {expected} articles the page lists")
    if skipped:
        problems.append(f"{len(skipped)} line(s) fit no row: " + " | ".join(skipped[:3]))
    if problems:
        result["warning"] = "; ".join(problems) + " — check the capture by eye"
    return result


def ingest_website(capture) -> dict:
    data = _read_capture(capture)
    outcome, code = _capture_outcome(data)
    if outcome != "ok":
        return {"outcome": outcome, "code": code, "url": data.get("url"), "text": ""}
    return {"outcome": "ok", "code": code, "url": data.get("url"), "text": data.get("text")}


def note_check(name: str, source: str, snapshot_path, outcome: str, code, today: datetime.date) -> None:
    """Remember the latest check of `source` in the record."""
    path = _record_path(name)
    record = load_record(path)
    before = journal.as_mapping(record["checks"].get(source))
    previous = before.get("snapshot") if before.get("outcome") == "ok" else before.get("previous_snapshot")
    record["checks"][source] = {"date": today.isoformat(), "outcome": outcome, "code": code,
                                "snapshot": str(snapshot_path), "previous_snapshot": previous,
                                "diffed": False}
    save_record(path, record)


SHOW_PER_RUN = 4


def _norm(text) -> str:
    """Letters and digits of any script, case-folded; "" when there are none."""
    return "".join(ch for ch in unicodedata.normalize("NFKC", str(text)).casefold() if ch.isalnum())


def _master_text(master: dict) -> tuple[str, set]:
    """(everything the master says, normalised) and the set of normalised project names."""
    projects = master.get("projects")
    names = {_norm(p.get("name", "")) for p in projects if isinstance(p, dict)} \
        if isinstance(projects, list) else set()
    blob = _norm(json.dumps(master, ensure_ascii=False, default=str))
    return blob, {n for n in names if n}


def _days_since(value, today: datetime.date) -> int:
    try:
        return max(0, (today - datetime.date.fromisoformat(str(value)[:10])).days)
    except ValueError:
        return 3650


def diff(source: str, previous, current: dict, master: dict, today: datetime.date) -> list:
    """Findings in `current` that `previous` and the master do not already account for."""
    if not current or current.get("outcome") != "ok":
        return []
    blob, project_names = _master_text(master or {})
    found = []
    if source == "github":
        before = {r["full_name"].lower(): r for r in (previous or {}).get("repos", [])}
        for r in current.get("repos", []):
            full = r["full_name"]
            short = _norm(full.split("/")[-1])
            # A short name only counts when a project is named exactly that:
            # "tool" must not be hidden by a project called "Toolkit for MRI".
            mentioned = (_norm(r.get("html_url", "")) in blob or short in project_names
                         or (len(short) >= 6 and short in blob))
            rank = 1000 - _days_since(r.get("pushed_at"), today) + (100 if r.get("role") == "owner" else 0) \
                + min(r.get("stars") or 0, 500) / 5
            payload = {k: r.get(k) for k in ("full_name", "html_url", "description", "role")}
            old = before.get(full.lower())
            if old is None and not mentioned:
                found.append({"id": f"github:{full}", "source": "github", "kind": "new_repo",
                              "summary": f"{full}: {r.get('description') or 'no description'} (role: {r.get('role')})",
                              "evidence_url": r.get("html_url"), "rank": rank, "repo": payload})
            release = r.get("latest_release")
            if release and (old is not None or mentioned) and release != (old or {}).get("latest_release"):
                found.append({"id": f"github:{full}@{release}", "source": "github", "kind": "new_release",
                              "summary": f"{full} released {release}", "evidence_url": r.get("html_url"),
                              "rank": rank, "repo": payload})
    elif source == "scholar":
        before = {_norm(p.get("title", "")) for p in (previous or {}).get("papers", [])} - {""}
        for paper in current.get("papers", []):
            key = _norm(paper.get("title", ""))
            if not key:  # a title of punctuation only cannot be matched; never propose it
                continue
            if key in before or key in blob:
                continue
            year = paper.get("year")
            where = ", ".join(str(x) for x in (paper.get("venue"), year) if x)
            found.append({"id": f"scholar:{key}", "source": "scholar", "kind": "new_paper",
                          "summary": f"{paper['title']} — {where or 'no venue'} ({paper.get('authors', '')})",
                          "evidence_url": current.get("url"),
                          "rank": 1000 - 365 * max(0, today.year - int(year)) if year else 500,
                          "paper": dict(paper)})
    elif source == "website" and previous and previous.get("outcome") == "ok":
        old_lines = str(previous.get("text", "")).splitlines()
        added = [line[1:].strip() for line in difflib.ndiff(old_lines, str(current.get("text", "")).splitlines())
                 if line.startswith("+ ") and line[1:].strip()]
        if added:
            found.append({"id": f"website:{today.isoformat()}", "source": "website", "kind": "page_changed",
                          "summary": "Added on the page: " + " | ".join(added[:5]),
                          "evidence_url": current.get("url"), "rank": 900})
    return found


def _load_snapshot(path):
    try:
        return json.loads(pathlib.Path(path).read_text(encoding="utf-8")) if path else None
    except (OSError, ValueError):
        return None


def _all_masters(name: str) -> dict:
    merged = {}
    for path in paths.master_profiles(name).values():
        try:
            merged[str(path)] = journal.load_yaml(path)
        except journal.YamlUnreadable:
            continue
    return merged


def _merged_masters(name: str) -> dict:
    """Every master's projects and publications in one profile-shaped mapping.

    diff() reads `projects` by name; handing it {path: master} hid every project
    name, so a short-named repository a master already lists was proposed again.
    """
    merged = {"projects": [], "publications": [], "_masters": []}
    for master in _all_masters(name).values():
        merged["projects"] += [p for p in master.get("projects") or [] if isinstance(p, dict)]
        merged["publications"] += [str(x) for x in master.get("publications") or []]
        merged["_masters"].append(master)
    return merged


def check(name: str, workspace, today: datetime.date, force: bool, get=None) -> dict:
    """Fetch stale GitHub, diff every new snapshot once, and return what to show."""
    get = get or http_get
    path = _record_path(name)
    st = status(name, today)  # seeds master links first, so the load below sees them
    record = load_record(path)
    checked, warnings = {}, {}
    github = journal.as_mapping(record["sources"].get("github"))
    if github.get("status") == "given":
        try:
            username = github_username(github.get("value"))
        except ValueError as exc:
            username = None
            checked["github"] = "bad_value"
            warnings["github"] = str(exc)
        if username is None:
            pass
        elif force or "github" in st["stale"]:
            result = fetch_github(username, github.get("extra") or [], get)
            snap = write_snapshot(name, "github", result, today, workspace=workspace)
            note_check(name, "github", snap, result["outcome"], result.get("code"), today)
            checked["github"] = result["outcome"]
        else:
            checked["github"] = "fresh"
    record = load_record(path)
    masters = _merged_masters(name)
    known = {f["id"]: f for f in record["findings"]}
    for source in SOURCES:
        check_entry = journal.as_mapping(record["checks"].get(source))
        checked.setdefault(source, check_entry.get("outcome", "not_checked") if source != "github"
                           else "not_checked")
        if not check_entry or check_entry.get("outcome") != "ok":
            continue
        current = _load_snapshot(check_entry.get("snapshot"))
        if (current or {}).get("warning"):
            warnings.setdefault(source, current["warning"])
        if check_entry.get("diffed"):
            continue
        previous = _load_snapshot(check_entry.get("previous_snapshot"))
        for finding in diff(source, previous, current, masters, today):
            if finding["id"] in known:
                continue
            finding.update(status="pending", evidence_file=check_entry.get("snapshot"),
                           found=today.isoformat())
            record["findings"].append(finding)
            known[finding["id"]] = finding
        check_entry["diffed"] = True
        record["checks"][source] = check_entry
    save_record(path, record)
    pending = sorted((f for f in record["findings"] if f.get("status") == "pending"),
                     key=lambda f: -float(f.get("rank", 0)))
    return {"checked": checked, "warnings": warnings, "shown": pending[:SHOW_PER_RUN],
            "pending_count": max(0, len(pending) - SHOW_PER_RUN)}


FINDING_DECISIONS = ("confirmed", "ignored")


def confirm(name: str, finding_id: str, decision: str, words: str, correction=None) -> None:
    if decision not in FINDING_DECISIONS:
        raise ValueError(f"decision must be one of {FINDING_DECISIONS}")
    if not (words or "").strip():
        raise ValueError("record the user's own words")
    path = _record_path(name)
    record = load_record(path)
    for finding in record["findings"]:
        if finding.get("id") == finding_id:
            finding.update(status=decision, words=words, decided=datetime.date.today().isoformat())
            if correction:
                finding["correction"] = dict(correction)
            save_record(path, record)
            return
    raise ValueError(f"no finding {finding_id!r} in {path}")


ROLE_LABELS = {"owner": "Owner", "top_contributor": "Lead contributor", "contributor": "Contributor"}
WRITTEN = ("confirmed", "confirmed_unwritten")


def _link_value(source: str, value: str) -> str:
    if source == "github" and "/" not in value:
        return f"github.com/{value}"
    return value


class _WrongShape(ValueError):
    pass


def _list_field(master: dict, key: str) -> list:
    value = master.get(key)
    if value is None:
        return []
    if not isinstance(value, list):
        raise _WrongShape(f"`{key}` in the master is a {type(value).__name__}, not a list; "
                          "add the entry by hand or make it a list")
    return list(value)


def _apply_finding(master: dict, finding: dict) -> bool:
    """Add one confirmed finding's durable facts to `master`; True if it changed.

    Never edits an entry the user already wrote, and never writes star, fork or
    release numbers (spec decision 6): those are read fresh from a snapshot.
    Raises _WrongShape when the field it would extend is not a list.
    """
    blob, project_names = _master_text(master)
    if finding.get("kind") == "new_repo" and finding.get("repo"):
        repo_data = finding["repo"]
        short = repo_data["full_name"].split("/")[-1]
        if _norm(short) in project_names or _norm(repo_data.get("html_url", "")) in blob:
            return False
        role = journal.as_mapping(finding.get("correction")).get("role") \
            or ROLE_LABELS.get(repo_data.get("role"), "Contributor")
        entry = {"name": short, "role": role}
        if repo_data.get("description"):
            entry["description"] = repo_data["description"]
        entry["links"] = [repo_data["html_url"]]
        master["projects"] = _list_field(master, "projects") + [entry]
        return True
    if finding.get("kind") == "new_paper" and finding.get("paper"):
        paper = finding["paper"]
        key = _norm(paper.get("title", ""))
        if not key or key in blob:
            return False
        where = ", ".join(str(x) for x in (paper.get("venue"), paper.get("year")) if x)
        master["publications"] = _list_field(master, "publications") + [
            f"{paper['title']} — {where}." if where else f"{paper['title']}."]
        return True
    return False  # releases and page changes carry no durable fact to store


def _leading_comments(path: pathlib.Path) -> str:
    lines = []
    for line in path.read_text(encoding="utf-8").splitlines(keepends=True):
        if line.startswith("#") or (lines and not line.strip()):
            lines.append(line)
        else:
            break
    return "".join(lines).rstrip("\n") + ("\n" if lines else "")


def writeback(name: str, language: str, workspace=None) -> list:
    """Write confirmed findings into this language's master through save_profile.py."""
    import yaml
    import save_profile
    record_path = _record_path(name)
    record = load_record(record_path)
    target = paths.master_for_language(name, language)
    todo = [f for f in record["findings"] if f.get("status") in WRITTEN
            and str(target) not in (f.get("written_to") or [])]
    if not todo:
        return []
    if not target.exists():
        for finding in todo:
            finding["status"] = "confirmed_unwritten"
        save_record(record_path, record)
        return []
    master = journal.load_yaml(target)
    changed = False
    if master.get("contact") is None:
        master["contact"] = {}
    contact = master["contact"]
    if isinstance(contact, dict) and contact.get("links") is None:
        contact["links"] = {}
    link_map = contact.get("links") if isinstance(contact, dict) else None
    if isinstance(link_map, dict):  # any other shape is the user's; leave it alone
        for source in SOURCES:
            answer = journal.as_mapping(record["sources"].get(source))
            last = journal.as_mapping(record["checks"].get(source))
            if last.get("outcome") == "failed" and last.get("code") == 404:
                continue  # the address no longer resolves; never publish a dead link
            if answer.get("status") == "given" and answer.get("value") and not link_map.get(source):
                link_map[source] = _link_value(source, answer["value"])
                changed = True
    applied = []
    for finding in todo:
        try:
            changed = _apply_finding(master, finding) or changed
        except _WrongShape as exc:
            finding["skipped_reason"] = str(exc)
            continue
        finding.pop("skipped_reason", None)
        applied.append(finding)
    todo = applied
    written = [f["id"] for f in todo]
    if changed:
        before = journal.sha256_file(target)
        with tempfile.TemporaryDirectory() as tmp:
            staged = pathlib.Path(tmp) / target.name
            staged.write_text(_leading_comments(target)
                              + yaml.safe_dump(master, allow_unicode=True, sort_keys=False),
                              encoding="utf-8")
            with contextlib.redirect_stdout(sys.stderr):
                code = save_profile.main(["--name", name, "--profile", str(staged)])
        if code != 0:
            raise ValueError(f"save_profile.py refused the write-back (exit {code})")
        entry = {"master": str(target), "before_sha256": before,
                 "after_sha256": journal.sha256_file(target), "finding_ids": written,
                 "date": datetime.date.today().isoformat()}
        record["writebacks"].append(entry)
        if workspace is not None:
            journal.append(workspace, {"action": "master_writeback", **entry})
    for finding in todo:
        finding["status"] = "confirmed"
        finding["written_to"] = list(finding.get("written_to") or []) + [str(target)]
    save_record(record_path, record)
    return written


def _pending_for_master(name: str, record: dict) -> dict:
    out = {}
    for lang, path in paths.master_profiles(name).items():
        if not lang:
            continue
        ids = [f["id"] for f in record["findings"] if f.get("status") == "confirmed"
               and f.get("written_to") and str(path) not in f["written_to"]]
        if ids:
            out[lang] = ids
    return out


def step_notice(workspace) -> str:
    """NOTICE text when this workspace's journal has no online-presence status step."""
    path = pathlib.Path(workspace) / "journal.jsonl"
    try:
        lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    except (OSError, UnicodeError):
        lines = []
    for line in lines:
        try:
            if json.loads(line).get("action") == "online_presence_status":
                return ""
        except (ValueError, AttributeError):
            continue
    return ("NOTICE_NO_ONLINE_PRESENCE_STEP: this workspace never ran "
            "`online_presence.py status`; public GitHub/Scholar/website updates were not "
            "checked for this run (references/online-presence.md)")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="command", required=True)
    st = sub.add_parser("status", help="which profiles to ask for, which are stale or broken")
    st.add_argument("--name", required=True)
    st.add_argument("--today")
    st.add_argument("--workspace", type=pathlib.Path)
    rc = sub.add_parser("record", help="store the user's answer for one source")
    rc.add_argument("--name", required=True)
    rc.add_argument("--source", required=True, choices=SOURCES)
    rc.add_argument("--status", required=True, choices=ASK_STATUSES)
    rc.add_argument("--value")
    rc.add_argument("--extra", nargs="*", default=None,
                    help="GitHub organisations or org/repo the profile page does not list")
    rc.add_argument("--words", required=True, help="the user's answer, verbatim")
    ig = sub.add_parser("ingest", help="turn a Scholar or website capture into a snapshot")
    ig.add_argument("--name", required=True)
    ig.add_argument("--source", required=True, choices=("scholar", "website"))
    ig.add_argument("--capture", required=True, type=pathlib.Path)
    ig.add_argument("--workspace", type=pathlib.Path)
    ig.add_argument("--today")
    ck = sub.add_parser("check", help="fetch stale GitHub, diff new snapshots, list findings")
    ck.add_argument("--name", required=True)
    ck.add_argument("--workspace", type=pathlib.Path)
    ck.add_argument("--today")
    ck.add_argument("--force", action="store_true", help="re-check even if checked within 14 days")
    cf = sub.add_parser("confirm", help="record the user's decision on one finding")
    cf.add_argument("--name", required=True)
    cf.add_argument("--finding", required=True)
    cf.add_argument("--decision", required=True, choices=FINDING_DECISIONS)
    cf.add_argument("--words", required=True)
    cf.add_argument("--role", help="the user's role, when they correct it")
    wb = sub.add_parser("writeback", help="write confirmed findings into a master")
    wb.add_argument("--name", required=True)
    wb.add_argument("--language", required=True)
    wb.add_argument("--workspace", type=pathlib.Path)
    lk = sub.add_parser("link", help="share another directory's record (same person)")
    lk.add_argument("--name", required=True)
    lk.add_argument("--with", dest="other", required=True)
    lk.add_argument("--words", required=True)
    # The top-level --help lists every subcommand's usage, so one call shows the
    # whole interface (and the documented-command guard can see real flags).
    ap.epilog = "subcommands:\n" + "\n".join(
        "  " + parser.format_usage().replace("usage: ", "").strip()
        for parser in sub.choices.values())
    args = ap.parse_args(argv)
    try:
        if args.command == "link":
            link(args.name, args.other, args.words)
            return 0
        if args.command == "writeback":
            written = writeback(args.name, args.language, args.workspace)
            skipped = {f["id"]: f["skipped_reason"] for f in load_record(_record_path(args.name))["findings"]
                       if f.get("skipped_reason") and f.get("status") in WRITTEN}
            print(json.dumps({"written": written, "skipped": skipped}, ensure_ascii=False))
            return 0
        if args.command == "check":
            today = datetime.date.fromisoformat(args.today) if args.today else datetime.date.today()
            print(json.dumps(check(args.name, args.workspace, today, args.force, get=http_get),
                             ensure_ascii=False))
            return 0
        if args.command == "confirm":
            confirm(args.name, args.finding, args.decision, args.words,
                    {"role": args.role} if args.role else None)
            return 0
        if args.command == "ingest":
            today = datetime.date.fromisoformat(args.today) if args.today else datetime.date.today()
            if not args.capture.is_file():
                print(f"ONLINE_PRESENCE_MISSING_INPUT: capture {args.capture} does not exist",
                      file=sys.stderr)
                return 2
            reader = ingest_scholar if args.source == "scholar" else ingest_website
            snapshot = reader(args.capture)
            snapshot["raw"] = [(snapshot.get("url") or str(args.capture), snapshot.get("code"),
                                args.capture.read_bytes())]
            path = write_snapshot(args.name, args.source, snapshot, today, workspace=args.workspace)
            note_check(args.name, args.source, path, snapshot["outcome"], snapshot.get("code"), today)
            summary = {"source": args.source, "outcome": snapshot["outcome"], "snapshot": str(path)}
            if args.source == "scholar":
                summary["papers"] = len(snapshot.get("papers") or [])
            for key in ("reason", "warning"):
                if snapshot.get(key):
                    summary[key] = snapshot[key]
            print(json.dumps(summary, ensure_ascii=False))
            return 0
        if args.command == "status":
            today = datetime.date.fromisoformat(args.today) if args.today else datetime.date.today()
            result = status(args.name, today)
            if args.workspace is not None:
                journal.append(args.workspace, {"action": "online_presence_status",
                                                "date": today.isoformat(), **result})
            print(json.dumps(result, ensure_ascii=False))
            return 0
        record_answer(args.name, args.source, args.status, args.value, args.words, args.extra)
        return 0
    except journal.YamlUnreadable as exc:
        print(f"ONLINE_PRESENCE_UNREADABLE: {exc}; fix or remove the file — it was not changed",
              file=sys.stderr)
        return 2
    except (ValueError, UnicodeDecodeError) as exc:
        print(f"ONLINE_PRESENCE_BAD_INPUT: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    from cli_io import configure_output
    configure_output()
    raise SystemExit(main())
