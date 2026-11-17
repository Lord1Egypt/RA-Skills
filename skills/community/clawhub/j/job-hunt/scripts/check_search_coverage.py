#!/usr/bin/env python3
"""Check declared search coverage, independently of shortlist size or round limits.

Register search-coverage.yaml's plan before retrieval with --record-plan. The
mutable checks and lead dispositions are verified again at delivery. This is
tamper evidence for recorded work, not proof of unrecorded actions or market
exhaustion. A passing shortlist is deliberately not a completion receipt.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re
import shlex
import sys
from urllib.parse import parse_qs, urlsplit

import journal
import browser_budget
from check_candidate_match import _quote_in_capture, _safe_path
from check_opencli_result import IDENTITY_FIELD
from check_shortlist import _contains_source_id
from record_browser_capture import read_retrieval_calls, validate_record, STOP_CLASSES
from search_capture import ACTION as SEARCH_ACTION, validate_record as validate_search

FILE = "search-coverage.yaml"
ACTION = "search_plan"
EXCLUSIONS = {"wrong_year", "closed", "wrong_location", "wrong_role", "wrong_level",
              "eligibility", "duplicate", "not_a_posting", "not_selected"}
# Adapter rows name the posting in different fields: boss uses `name`, and
# indeed returns rows whose `title` is present but empty (discovery-sources.md).
TITLE_KEYS = ("title", "jobName", "job_name")
ID_KEYS = ("source_id", "jobId", "job_id", "id", "jobkey")
# Secondary spellings a shortlist may use (boss: security_id); never preferred
# over the id in the posting URL, which is what shortlists normally record.
EXTRA_ID_KEYS = ("security_id", "securityId", "encryptJobId")
_URL = re.compile(r"https?://[^\s)\]>\"'<]+")
# Path words that name no posting; the full URL is then the identity.
GENERIC_SEGMENTS = {"link", "apply", "job", "jobs", "detail", "details", "view", "viewjob",
                    "index", "default", "home", "redirect", "position", "positions", "search",
                    "vacancy", "vacancies", "vacature", "vacatures", "stelle", "stellen", "offre", "page"}
URL_ID_PARAMS = ("currentJobId", "jk", "jobId", "job_id")
_PAGE_SUFFIX = re.compile(r"\.(?:s?html?|php|aspx?|jsp)$", re.I)


def _capture_path(root, name):
    """Normalize historical journal paths, keeping evidence inside round/raw."""
    if not isinstance(name, str) or not name:
        return None
    try:
        path = (root / name).resolve()
        relative = path.relative_to(root.resolve()).as_posix()
    except (ValueError, OSError, RuntimeError):
        return None
    return _safe_path(root, relative, raw=True)


def _nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def _plan(value):
    if not isinstance(value, dict):
        raise ValueError("coverage requires a plan mapping")
    for key in ("sources", "directions"):
        items = value.get(key)
        if (not isinstance(items, list) or not items
                or any(not isinstance(x, dict) or not _nonempty(x.get("id"))
                       or not _nonempty(x.get("label")) for x in items)
                or len({x["id"] for x in items}) != len(items)):
            raise ValueError(f"plan.{key} requires distinct ids and labels")
    for source in value["sources"]:
        if not _nonempty(source.get("site")) or source.get("method") not in {"search", "catalog"}:
            raise ValueError("each source requires site and method search/catalog")
    if len({s["site"] for s in value["sources"]}) != len(value["sources"]):
        raise ValueError("source sites must be distinct")
    if any(s["method"] == "search" for s in value["sources"]):
        if any(not _nonempty(d.get("query")) for d in value["directions"]):
            raise ValueError("search directions require an actual query")
    search_sources = {s["id"] for s in value["sources"] if s["method"] == "search"}
    for direction in value["directions"]:
        overrides = direction.get("query_by_source", {})
        if (not isinstance(overrides, dict)
                or any(key not in search_sources or not _nonempty(query)
                       for key, query in overrides.items())):
            raise ValueError("query_by_source requires nonempty queries keyed by registered search source ids")
    return value


def _extends(old, new):
    return (all(all(item in new[key] for item in old[key]) for key in ("sources", "directions"))
            and all(item in new.get("rounds", []) for item in old.get("rounds", [])))


def _stamp(value):
    stamp = dt.datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if stamp.tzinfo is None:
        raise ValueError("coverage timestamps require a timezone")
    return stamp


def _registrations(workspace, plan):
    records = journal._records(workspace)
    entries = [r for r in records if r.get("action") == ACTION]
    if not entries:
        raise ValueError("search coverage requires a preregistered plan before retrieval")
    previous = None
    previous_stamp = None
    for entry in entries:
        if not journal.receipt_intact(entry):
            raise ValueError("search plan registration is altered")
        current = _plan(entry.get("plan"))
        if previous and not _extends(previous, current):
            raise ValueError("registered search scope cannot shrink or change")
        stamp = _stamp(entry.get("ts"))
        if previous_stamp is not None and stamp < previous_stamp:
            raise ValueError("search plan registration timestamps are out of order")
        previous_stamp = stamp
        previous = current
    if previous != plan:
        raise ValueError("search plan differs from its registration; only registered additions are allowed")
    first = records.index(entries[0])
    if any(r.get("action") in {"browser_call", "adapter_call", SEARCH_ACTION} for r in records[:first]):
        raise ValueError("search plan was registered after retrieval")
    return entries


def record_plan(workspace):
    data = journal.load_yaml(workspace / FILE, dict)
    plan = _plan(data.get("plan"))
    if journal.corrupt_lines(workspace):
        raise ValueError("search journal is corrupt")
    entries = [r for r in journal._records(workspace) if r.get("action") == ACTION]
    if entries:
        _registrations(workspace, entries[-1].get("plan"))
        if not _extends(entries[-1]["plan"], plan):
            raise ValueError("registered search scope cannot shrink or change")
        if entries[-1]["plan"] == plan:
            return
    elif read_retrieval_calls(workspace):
        raise ValueError("cannot register a first search plan after retrieval")
    journal.append(workspace, journal.sign_receipt({"action": ACTION,
        "ts": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "plan": plan}))


def _url_ids(url):
    """Posting ids a URL carries: known query parameters, then path segments."""
    parts = urlsplit(str(url).strip())
    if parts.scheme not in ("http", "https") or not parts.netloc:
        return []
    query = parse_qs(parts.query)
    ids = [query[p][0].strip() for p in URL_ID_PARAMS if query.get(p) and query[p][0].strip()]
    segments = [seg for part in parts.path.split("/") if (seg := _PAGE_SUFFIX.sub("", part))]
    if segments and segments[-1].casefold() not in GENERIC_SEGMENTS:
        # The last segment names the posting: a numeric id, or the title slug
        # boards such as Workday, Philips and 实习僧 use. A generic word
        # ("link" on weixin.sogou.com, "apply", "view") names nothing, and a
        # dated or categorised parent ("/vacatures/2026/") is not an identity.
        ids.append(segments[-1])
        ids += [token for token in re.split(r"[-_]", segments[-1])
                if any(ch.isdigit() for ch in token) and any(ch.isalpha() for ch in token)]
    ids += [seg for seg in reversed(segments[:-1]) if any(ch.isdigit() for ch in seg)]
    return [i for i in dict.fromkeys(ids) if i]


def _lead_id(value):
    """The identity a shortlist row records as source_id; a URL names its posting,
    or is itself the identity when it carries no id."""
    text = str(value).strip()
    return next(iter(_url_ids(text)), text)


def _lead_ids(row):
    """Every spelling of this row's identity; the first is its lead key."""
    ids = [str(row[k]).strip() for k in ID_KEYS if row.get(k) not in (None, "")]
    url = str(row.get("url") or "").strip()
    ids += _url_ids(url)
    if urlsplit(url).scheme in ("http", "https"):
        ids.append(url)
    ids += [str(row[k]).strip() for k in EXTRA_ID_KEYS if row.get(k) not in (None, "")]
    return [i for i in dict.fromkeys(ids) if i]


def _job_rows(value, site=None):
    if isinstance(value, list):
        for item in value:
            yield from _job_rows(item, site)
    elif isinstance(value, dict):
        keys = tuple(dict.fromkeys((IDENTITY_FIELD.get(site, "title"),) + TITLE_KEYS))
        ids = _lead_ids(value)
        if ids and any(k in value for k in keys):
            title = next((str(value[k]) for k in keys if value.get(k)), "")
            yield ids[0], title, value
        else:
            for item in value.values():
                yield from _job_rows(item, site)


def inspect(workspace):
    """Pure check: never append receipts or accept a stale pass during delivery."""
    try:
        return _inspect(pathlib.Path(workspace).resolve())
    except (OSError, UnicodeError, ValueError, TypeError, KeyError, journal.YamlUnreadable) as exc:
        return [f"SEARCH_COVERAGE: {exc}"]


def _inspect(workspace):
    collection = workspace / "collection.yaml"
    config = journal.load_yaml(collection if collection.exists() else workspace / "brief.yaml", dict)
    scope = config.get("report_scope", "complete")
    if scope == "preliminary":
        return [] if _nonempty(config.get("preliminary_request")) else [
            "SEARCH_COVERAGE: preliminary delivery requires the user's explicit request"]
    if scope != "complete":
        raise ValueError("unknown report_scope")
    if not (workspace / FILE).is_file():
        raise ValueError("search coverage requires a preregistered plan before retrieval")
    data = journal.load_yaml(workspace / FILE, dict)
    plan = _plan(data.get("plan"))
    entries = _registrations(workspace, plan)
    report = (workspace / "report.md").read_text(encoding="utf-8")
    rounds = config.get("rounds") if collection.exists() else [{"workspace": "."}]
    if not isinstance(rounds, list) or not rounds:
        raise ValueError("search coverage requires nonempty rounds")
    if collection.exists():
        registered_rounds = plan.get("rounds")
        if (not isinstance(registered_rounds, list) or not registered_rounds
                or {(workspace / r).expanduser().resolve() for r in registered_rounds}
                != {(workspace / r["workspace"]).expanduser().resolve() for r in rounds}):
            raise ValueError("collection rounds must match the registered plan; rounds cannot disappear")
    calls, retained, observed = {}, {}, {}
    roots = {workspace}
    for item in rounds:
        root = (workspace / item["workspace"]).expanduser().resolve()
        if root in calls:
            raise ValueError("duplicate search round")
        roots.add(root)
        calls[root] = read_retrieval_calls(root)
        rows = journal.load_yaml(root / "shortlist.yaml", dict).get("rows", [])
        for row in rows:
            if "ids" not in item or row.get("id") in item["ids"]:
                retained.setdefault((row.get("source_site"), str(row.get("source_id"))), []).append(row)
    for root in roots:
        if journal.corrupt_lines(root):
            raise ValueError("search journal is corrupt")
    # Even captures in the owner outside selected rounds cannot disappear.
    calls.setdefault(workspace, read_retrieval_calls(workspace))
    sources = {s["site"]: s for s in plan["sources"]}
    for root, records in calls.items():
        for call in records:
            site = call.get("site")
            if site not in sources:
                raise ValueError(f"unplanned source: {site}")
            registered = next(e for e in entries if sources[site] in e["plan"]["sources"])
            if _stamp(call.get("retrieved_at") or call.get("ts")) < _stamp(registered["ts"]):
                raise ValueError(f"source {site} was read before plan registration")
            if collection.exists() and root != workspace:
                registered_round = next(e for e in entries if root in {
                    (workspace / r).expanduser().resolve() for r in e["plan"].get("rounds", [])})
                if _stamp(call.get("retrieved_at") or call.get("ts")) < _stamp(registered_round["ts"]):
                    raise ValueError("collection round was read before its registration")
            if call.get("action") == "browser_call" and validate_record(call, root):
                raise ValueError(f"invalid browser coverage evidence: {site}")
            if call.get('action') == SEARCH_ACTION and validate_search(call, root):
                raise ValueError(f'invalid native search coverage evidence: {site}')
            name = call.get("rows_file") or call.get("stdout_file")
            path = _capture_path(root, name)
            if path is None:
                raise ValueError(f"missing raw retrieval evidence: {site}")
            if call.get('action') == 'browser_call':
                snapshot = json.loads(_capture_path(root, call.get('snapshot_file')).read_text(encoding='utf-8'))
                for view in browser_budget.views(snapshot):
                    for identity, title, row in _job_rows(view.get('catalog_rows', []), site):
                        observed.setdefault((site, identity), []).append((root, title, row))
            if call.get("classification") != "ok":
                continue
            try:
                value = json.loads(path.read_text(encoding="utf-8"))
            except ValueError as exc:
                raise ValueError(f"successful retrieval needs structured rows: {name}") from exc
            for identity, title, row in _job_rows(value, site):
                observed.setdefault((site, identity), []).append((root, title, row))

    def evidence(ref, site):
        if not isinstance(ref, dict):
            raise ValueError("coverage result requires capture evidence")
        root = (workspace / ref.get("workspace", ".")).expanduser().resolve()
        if root not in calls:
            raise ValueError("coverage evidence is outside declared rounds")
        path = _capture_path(root, ref.get("file"))
        if path is None or journal.sha256_file(path) != ref.get("sha256"):
            raise ValueError("coverage capture hash changed or path is invalid")
        text = path.read_text(encoding="utf-8")
        if not _nonempty(ref.get("quote")) or not _quote_in_capture(ref["quote"], text):
            raise ValueError("coverage quote is absent from capture")
        matches = [c for c in calls[root] if c.get("site") == site and path in
                   [_capture_path(root, c.get(k)) for k in ("stdout_file", "stderr_file", "snapshot_file", "rows_file")]]
        if not matches:
            raise ValueError("coverage capture lacks a same-source retrieval record")
        return matches[-1], text

    def blocked(item, call):
        if not _nonempty(item.get("reason")) or item["reason"] not in report:
            raise ValueError("blocked coverage needs its reason visible in report.md")
        if not (call.get("classification") in STOP_CLASSES or
                (call.get("classification") == "transport" and type(call.get("exit_code")) is int
                 and call["exit_code"] != 0)):
            raise ValueError("blocked coverage requires a captured access failure")

    checks = data.get("checks", [])
    expected = {(s["id"], d["id"]) for s in plan["sources"] for d in plan["directions"]}
    if (not isinstance(checks, list) or any(not isinstance(c, dict) for c in checks)
            or len(checks) != len(expected)
            or {(c.get("source"), c.get("direction")) for c in checks} != expected):
        raise ValueError("every planned source and direction requires one coverage result")
    for item in checks:
        source = next(s for s in plan["sources"] if s["id"] == item["source"])
        direction = next(d for d in plan["directions"] if d["id"] == item["direction"])
        status = item.get("status")
        if status not in {"done", "blocked"}:
            raise ValueError(f"pending source/direction: {item['source']}/{item['direction']}")
        call, _ = evidence(item.get("evidence"), source["site"])
        if status == "blocked":
            blocked(item, call)
            if call.get("classification") not in STOP_CLASSES and call.get("command") != "search":
                raise ValueError("one failed detail read does not close source search coverage")
        else:
            registration = next(e for e in entries if direction in e["plan"]["directions"])
            if _stamp(call.get("retrieved_at") or call.get("ts")) < _stamp(registration["ts"]):
                raise ValueError("direction was added after its claimed coverage capture")
            if call.get("classification") != "ok" or call.get("command") != "search":
                raise ValueError("done coverage requires a successful search/catalog capture")
            if not _nonempty(item.get("reason")):
                raise ValueError("done coverage requires a review reason")
            if source["method"] == "search":
                query = call.get("query")
                planned_query = direction.get("query_by_source", {}).get(source["id"], direction["query"])
                matches_query = (query == planned_query if query else
                                 planned_query in shlex.split(call.get("command_line") or ""))
                if not matches_query:
                    raise ValueError("coverage search does not match planned direction query")

    dispositions = data.get("leads", [])
    if not isinstance(dispositions, list) or any(not isinstance(d, dict) for d in dispositions):
        raise ValueError("coverage leads must be a list of dispositions")
    # A delivered posting retains its lead under any spelling of its identity
    # (explicit id, URL query id or URL path id), as check_shortlist accepts.
    handled = {key for key, values in observed.items()
               if any((key[0], i) in retained for _, _, row in values for i in _lead_ids(row))}
    spellings = {}
    for key, values in observed.items():
        for _, _, row in values:
            for spelling in _lead_ids(row):
                spellings.setdefault((key[0], spelling), key)
    report_ids = set()
    for url in _URL.findall(report):
        report_ids.update([url, *_url_ids(url)])
    seen = set()
    for item in dispositions:
        named = str(item.get("source_id")).strip()
        key = spellings.get((item.get("site"), named)) or spellings.get((item.get("site"), _lead_id(named)))
        if key is None or key in seen:
            raise ValueError("unknown or duplicate lead disposition")
        seen.add(key)
        status = item.get("status")
        if status == "retained":
            matches = [r for values in retained.values() for r in values
                       if r.get("id") == item.get("row_id") and
                       (r.get("source_site") == key[0] or key[0] == 'anysearch')]
            matched = (any(r.get('url') == row.get('url') and r.get('source_site') != 'anysearch'
                           for r in matches for _, _, row in observed[key]) if key[0] == 'anysearch' else
                       any(r.get("title") == title for r in matches for _, title, _ in observed[key]))
            if not matched:
                raise ValueError("retained catalog lead does not match a delivered posting")
        elif status in {"excluded", "blocked"}:
            call, text = evidence(item.get("evidence"), key[0])
            if status == "blocked":
                blocked(item, call)
                if (call.get("classification") not in STOP_CLASSES
                        and call.get("command") != "search"
                        and key[1] not in text + str(call.get("url") or "")
                        + str(call.get("command_line") or "")):
                    raise ValueError("failed detail capture does not identify this blocked lead")
            else:
                if item.get("reason_code") not in EXCLUSIONS or not _nonempty(item.get("reason")):
                    raise ValueError("excluded lead requires a supported exclusion reason")
                quote = item["evidence"]["quote"]
                if not any(_quote_in_capture(quote, json.dumps(row, ensure_ascii=False))
                           for _, _, row in observed[key]):
                    raise ValueError("exclusion quote must belong to this observed lead")
                if not _contains_source_id(key[1], text):
                    raise ValueError("exclusion capture must identify this lead")
                # Visible means its posting link (any spelling of its id, so a
                # tracking query does not matter) or, lacking a URL, its title.
                if item["reason_code"] == "not_selected" and not any(
                        any(i in report_ids for i in _lead_ids(row) if len(i) >= 4)
                        or (not row.get("url") and title and title in report)
                        for _, title, row in observed[key]):
                    raise ValueError("not_selected lead must stay visible in report.md: "
                                     f"list {key[0]}/{key[1]} with its posting link")
        else:
            raise ValueError("pending lead disposition")
        handled.add(key)
    pending = set(observed) - handled
    if pending:
        raise ValueError("unprocessed discovered leads: " + ", ".join(f"{s}/{i}" for s, i in sorted(pending)))
    return []


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True, type=pathlib.Path)
    parser.add_argument("--record-plan", action="store_true")
    args = parser.parse_args(argv)
    if args.record_plan:
        try:
            record_plan(args.workspace)
            return 0
        except (OSError, ValueError, TypeError, KeyError, journal.YamlUnreadable) as exc:
            print(f"SEARCH_COVERAGE: {exc}")
            return 2
    try:
        owner = args.workspace / "collection.yaml"
        config = journal.load_yaml(owner if owner.exists() else args.workspace / "brief.yaml", dict)
        if config.get("report_scope") != "preliminary":
            journal.load_yaml(args.workspace / FILE, dict)
    except (OSError, journal.YamlUnreadable) as exc:
        findings = [f"SEARCH_COVERAGE: cannot read primary input: {exc}"]
        journal.receipt(args.workspace, "check_search_coverage", {}, "could_not_run", findings)
        print(findings[0], file=sys.stderr)
        return 2
    findings = inspect(args.workspace)
    hashes = {n: journal.sha256_file(args.workspace / n) for n in
              (FILE, "brief.yaml", "collection.yaml", "report.md", "journal.jsonl")
              if (args.workspace / n).is_file()}
    journal.receipt(args.workspace, "check_search_coverage", hashes,
                    "fail" if findings else "pass", findings)
    print("\n".join(findings) if findings else "PASS: declared search coverage complete")
    return 2 if findings else 0


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    raise SystemExit(main())
