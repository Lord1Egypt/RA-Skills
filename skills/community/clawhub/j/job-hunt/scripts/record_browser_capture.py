#!/usr/bin/env python3
"""Import an actual read-only browser snapshot; never execute arbitrary browser code.

Records are tamper-evident, not proof of origin or of unjournaled actions.
Exit 0: recorded (including a site refusal); 2: invalid input, nothing recorded.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re
import sys
from urllib.parse import urlsplit

import journal
import browser_budget
from check_opencli_result import GUEST_LOGIN_WALL, read_journal, recovery_guidance

ACTION = "browser_call"
REASONS = ("preferred_browser", "cli_missing", "bridge_disconnected", "unsupported_extraction")
# Older names are accepted for historical receipts, never invoked by this script.
BACKENDS = ("builtin-cdp", "web-access", "chrome-devtools", "host-browser")
STOP_CLASSES = {"platform_limit", "not_logged_in", "no_auth_adapter"}
# Look for actual wall language, not an ordinary navigation link saying Login.
WALL = re.compile(
    r"(?:enter|complete|solve) (?:the |this |a )?captcha|(?:verify|verifying|confirm) (?:that )?you are (?:a )?human|access denied|too many requests|"
    r"please (?:sign|log) in|(?:sign|log) in (?:required|to continue|to view)|"
    r"(?:请输入|请完成|请填写).{0,12}验证码|验证您是人类|访问受限|访问过于频繁|请先登[录入]|"
    r"请按住滑块[，,\s]*拖动到最右边|为了更好的访问体验[，,\s]*请进行验证|"
    r"(?:验证|确认)(?:您|你)(?:是否)?是(?:真人|人类)|(?:正在|请|需要).{0,8}(?:真人验证|人机验证)|"
    r"验证成功[。.!！\s]*正在等待|verification successful[.!\s]*waiting for|checking your browser|"
    r"認証が必要|ログインが必要|로그인이 필요|접근이 제한|人机验证|真人验证|请按住滑块|"
    r"unusual traffic|需要进行其他验证", re.I)


def web_url(value):
    if not isinstance(value, str) or any(c.isspace() for c in value):
        return False
    try:
        parsed = urlsplit(value)
        return (parsed.scheme in {"http", "https"} and bool(parsed.hostname)
                and parsed.username is None and parsed.password is None)
    except ValueError:
        return False


def known_security_page(url):
    """A confirmed platform interstitial can initially show only a loading label."""
    parsed = urlsplit(url)
    host = (parsed.hostname or '').lower()
    return ((host == 'zhipin.com' or host.endswith('.zhipin.com'))
            and parsed.path == '/web/passport/zp/security.html')


def validate_snapshot(snapshot, rows):
    if not isinstance(snapshot, dict) or not isinstance(rows, list):
        raise ValueError("snapshot must be an object and rows must be an array")
    if not web_url(snapshot.get("url")) or not isinstance(snapshot.get("text"), str):
        raise ValueError("snapshot requires an HTTP(S) url and original text")
    if "requested_url" in snapshot and not web_url(snapshot["requested_url"]):
        raise ValueError("requested_url must be an HTTP(S) URL without credentials")
    stamp = snapshot.get("retrieved_at")
    if not isinstance(stamp, str):
        raise ValueError("snapshot requires retrieved_at with a timezone")
    try:
        parsed = dt.datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("invalid retrieved_at") from exc
    if parsed.tzinfo is None:
        raise ValueError("retrieved_at must include a timezone")
    links = snapshot.get("links")
    if not isinstance(links, list) or any(not web_url(u) for u in links):
        raise ValueError("links must be an array of original HTTP(S) URLs")
    status = snapshot.get("http_status")
    if status is not None and (type(status) is not int or not 100 <= status <= 599):
        raise ValueError("http_status must be an HTTP status integer or null")
    blocked = snapshot.get("blocked", False)
    if type(blocked) is not bool:
        raise ValueError("blocked must be boolean")
    load_timed_out = snapshot.get("load_timed_out", False)
    if type(load_timed_out) is not bool:
        raise ValueError("load_timed_out must be boolean")
    visible_text = " ".join(snapshot["text"].split())
    if GUEST_LOGIN_WALL.search(visible_text):
        if rows:
            raise ValueError("login wall must have no extracted rows")
        return "not_logged_in"
    if (blocked or status in (401, 403, 429) or WALL.search(visible_text)
            or known_security_page(snapshot["url"])):
        if rows:
            raise ValueError("site refusal must have no extracted rows")
        return "platform_limit"
    if status is not None and status >= 400:
        if rows:
            raise ValueError("HTTP failure must have no extracted rows")
        return "transport"
    urls = set(links) | {snapshot["url"]}
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("each row must be an object")
        for key in ("source_id", "url", "title", "raw_text"):
            if not isinstance(row.get(key), str) or not row[key].strip():
                raise ValueError(f"each row requires {key}")
        if row["url"] not in urls:
            raise ValueError("row URL is absent from the snapshot")
        if len(row["source_id"]) < 4 or not any(
                row["source_id"] in s for s in [snapshot["text"], *urls]):
            raise ValueError("source_id is absent from the snapshot or too short")
        if row["raw_text"] not in snapshot["text"] or row["title"] not in row["raw_text"]:
            raise ValueError("title/card text must be copied verbatim from the snapshot")
        if row["source_id"] in seen:
            raise ValueError("duplicate source_id in capture")
        seen.add(row["source_id"])
    # A loading or textless page is not evidence of zero matches. Image-only
    # recruitment landing pages can settle successfully without exposing a JD.
    # Actual rows still require the same verbatim-text and URL checks above.
    return "transport" if (snapshot.get('navigation_error') or snapshot.get('budget_exceeded') or snapshot.get('catalog_accounting_pending')
                           or (not rows and (load_timed_out or not snapshot["text"].strip()))) else "ok"


def _host(record):
    """The registrable-ish host this record read, lowercased, or "".

    Only browser records carry a URL; an `adapter_call` names its adapter and
    nothing else, because the command line *is* the adapter name and opencli
    would not run an invented one.
    """
    url = journal.as_mapping(record).get("url")
    if not isinstance(url, str):
        return ""
    try:
        host = (urlsplit(url).hostname or "").lower()
    except ValueError:
        return ""
    return host[4:] if host.startswith("www.") else host


def _labels(value):
    """The comparable parts of a site name or a host: `www.51job.com` -> {51job}.

    Applied to NAMES as well as hosts, because a name is how the two backends
    are joined and `51job` / `51job.com` / `www.51job` are one site written
    three ways. Domain suffixes and labels of two characters or fewer are
    dropped: they carry no source identity and would link unrelated sites.
    """
    value = (value or "").strip().lower()
    if value.startswith("www."):
        value = value[4:]
    labels = value.split(".")
    if len(labels) > 1:
        labels.pop()  # A domain suffix does not identify a recruitment source.
        while labels and labels[-1] in {"com", "co", "org", "net", "edu", "gov"}:
            labels.pop()
    return {label for label in labels if len(label) > 2}


def _linked(a, b):
    """Do these two site identifiers plainly name the same site?

    A bare name matches a whole non-suffix label: `51job` links to
    `we.51job.com`, `51job.com` and `www.51job`. Two hosts must match
    exactly or be parent/subdomain; shared TLDs or `jobs` labels are insufficient.

    Substring containment was tried and removed. Measured, it bought exactly one
    hypothetical pairing (`boss` to `bossjobs.com`) and cost three plausible
    wrong ones -- `job` would have linked to `51job.com` and to `jobsdb.com`,
    `ind` to `indeed.com` -- and a stop lock that fires on a site which never
    refused is the cry-wolf this repo treats as the worse failure. Speculative
    generality is not worth a false stop.

    Deliberately no alias table either: BOSS直聘 serves `zhipin.com` and a
    hand-maintained map would have to be right about every adapter in every
    market before this function could be trusted at all. The journal supplies
    those pairings instead, from hosts the run actually read.
    """
    a, b = (value.strip().lower().removeprefix("www.") for value in (a, b))
    if "." in a and "." in b:
        # Shared TLDs or generic subdomains such as jobs identify no common site.
        return a == b or a.endswith("." + b) or b.endswith("." + a)
    x, y = _labels(a), _labels(b)
    return bool(x & y)


def check_stop_order(records):
    """A refusal stops the site for the round, across BOTH backends.

    Locked on three keys, not one. `site` alone was evadable, and not only by an
    adversary: measured 2026-09-08, a refusal on `51job` did not stop a later
    read declaring `51job.com` or `www.51job`, and an agent that names the same
    site two ways across two calls defeats the lock without ever intending to.

    `51-job` is deliberately NOT joined to `51job`: nothing but a guess connects
    them, and the guess that would — substring matching — also joins `job` to
    `51job.com`. See `_linked`.

    So a refusal records the declared name, the host actually read, and the
    hosts that name has been seen using; a later read matches on any of them.
    What this CANNOT do is connect a rename with no shared text and no shared
    host -- `qiancheng` after `51job` -- and `references/browser-fallback.md`
    says that in those words rather than promising the whole property.
    """
    stopped_names, stopped_hosts = set(), set()
    seen_hosts = {}
    findings = []
    # `journal.as_mapping` and the hashable guard below are not decoration. This
    # reads journal.jsonl, which is a file on disk that a person can edit and a
    # corrupt run can half-write, and the gate contract is 0 clean / 1 findings /
    # 2 could-not-run with exactly one receipt. An exception escaping here is
    # exit 1 with NO receipt -- indistinguishable from a gate nobody ran, which
    # is the failure `journal.as_mapping`'s own docstring records from
    # 2026-09-05. Fuzzed 2026-09-08: a non-mapping row and an unhashable
    # `classification` each raised, in this function and in the one it replaced.
    # `records` itself is a caller's argument, and one caller reads it from the
    # journal. A string is iterable and would be walked character by character;
    # everything non-iterable would raise. `as_mapping` is the row-level twin of
    # this guard and journal has no list-level one, so it is inline.
    for entry in (records if isinstance(records, (list, tuple)) else ()):
        record = journal.as_mapping(entry)
        if record.get("action") not in ("adapter_call", ACTION, "search_call"):
            continue
        name = str(record.get("site") or "").strip().lower()
        host = _host(record)
        if host:
            seen_hosts.setdefault(name, set()).add(host)
        # `host in stopped_hosts` used to sit here and was removed as dead: this
        # record's own host has already been added to seen_hosts above, so the
        # last clause subsumes it exactly. Mutation testing found it — deleting
        # it changed no test — and a redundant clause inside a safety check is
        # worse than none, because the next reader may weaken the live one while
        # believing the dead one still covers the case.
        hit = (name in stopped_names
               or any(_linked(n, name) for n in stopped_names)
               or (host and any(_linked(n, host) for n in stopped_names))
               or (host and any(_linked(h, host) for h in stopped_hosts))
               or any(h in stopped_hosts for h in seen_hosts.get(name, ())))
        if hit:
            findings.append(
                f"READ_AFTER_STOP: {name or '<unnamed>'} was read after a site "
                f"refusal or catalog-budget failure; changing tools or renaming the source does not reset "
                f"the round")
        classification = record.get("classification")
        if ((isinstance(classification, str) and classification in STOP_CLASSES)
                or record.get('budget_error')):
            stopped_names.add(name)
            if host:
                stopped_hosts.add(host)
            stopped_hosts.update(seen_hosts.get(name, ()))
    return findings


def validate_record(record, workspace):
    """Fail closed on unknown actions, altered metadata or missing raw files."""
    findings = []
    if (record.get("backend") not in BACKENDS or record.get("operation") != "snapshot"
            or record.get("command") not in ("search", "detail")
            or record.get("fallback_reason") not in REASONS
            or record.get("command_line")
            or not journal.receipt_intact({k: v for k, v in record.items() if k != "_lineno"})):
        return ["INVALID_BROWSER_RECORD: expected an intact read-only snapshot import"]
    root = pathlib.Path(workspace).resolve()
    try:
        files = []
        for key in ("snapshot_file", "rows_file"):
            name = record[key]
            path = (root / name).resolve()
            if (not isinstance(name, str) or not name.startswith("raw/")
                    or path.parent != root / "raw"
                    or not path.name.startswith(record["site"] + "-")):
                raise ValueError("capture must be a site-prefixed file directly under raw/")
            if journal.sha256_file(path) != record["input_hashes"][name]:
                raise ValueError("capture hash changed")
            files.append(json.loads(path.read_text(encoding="utf-8")))
        snapshot, rows = files
        classification = validate_snapshot(snapshot, rows)
        accounting = browser_budget.usage(snapshot, validate_rows=validate_snapshot)
        if record.get('command') == 'search' and classification == 'ok' and accounting is None:
            raise ValueError('NAVIGATION_BUDGET_MISSING: successful search requires complete DOM catalog accounting')
        if accounting is not None:
            count, pages, _ = accounting
            if record.get('search_row_count') != count or record.get('search_pages') != pages:
                raise ValueError('NAVIGATION_BUDGET: imported counts differ from intermediate catalogs')
            budget = snapshot['navigation_budget']
            if budget.get('workspace') != str(root) or budget.get('site') != record['site']:
                raise ValueError('NAVIGATION_BUDGET: capture belongs to another round/source')
            prior = []
            for call in read_retrieval_calls(root):
                if call.get('snapshot_file') == record['snapshot_file']:
                    break
                prior.append(call)
            used_rows, used_pages = browser_budget.used(prior, record['site'])
            if budget.get('used_rows') != used_rows or budget.get('used_pages') != used_pages:
                raise ValueError('NAVIGATION_BUDGET: prior round consumption changed or was omitted')
            brief = journal.load_yaml(root / 'brief.yaml', dict)
            if (budget.get('max_rows') != brief.get('max_rows_per_round') or
                    budget.get('max_pages') != brief.get('max_pages_per_site')):
                raise ValueError('NAVIGATION_BUDGET: limits differ from the search brief')
            if snapshot.get('budget_exceeded'):
                raise ValueError('NAVIGATION_BUDGET_EXCEEDED: the page returned more rows than reserved')
        if snapshot.get('navigation_error'):
            raise ValueError('NAVIGATION_INCOMPLETE: inspect the preserved partial journey before continuing')
        if (type(record["row_count"]) is not int
                or type(record["exit_code"]) is not int):
            raise ValueError("counts and exit code must be integers")
        if (classification != record["classification"] or len(rows) != record["row_count"]
                or record["exit_code"] != (0 if classification == "ok" else 1)
                or record.get('empty_result') != (classification == 'ok' and not rows and not (accounting and accounting[0]))
                or record["retrieved_at"] != snapshot["retrieved_at"]
                or record["url"] != snapshot["url"]
                or type(record["page"]) is not int or record["page"] < 1
                or not isinstance(record["query"], str)
                or (record["command"] == "search" and not record["query"].strip())):
            raise ValueError("capture metadata does not match the recorded result")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        findings.append(f"INVALID_BROWSER_CAPTURE: {exc}")
    return findings


def read_retrieval_calls(workspace):
    return [r for r in read_journal(workspace)
            if r.get("action") in ("adapter_call", ACTION, "search_call")]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True, type=pathlib.Path)
    parser.add_argument("--site", required=True)
    parser.add_argument("--command", choices=("search", "detail"), default="search")
    parser.add_argument("--snapshot-file", required=True, type=pathlib.Path)
    parser.add_argument("--rows-file", required=True, type=pathlib.Path)
    parser.add_argument("--backend", choices=BACKENDS, default="builtin-cdp")
    parser.add_argument("--fallback-reason", choices=REASONS, required=True)
    parser.add_argument("--query", default="")
    parser.add_argument("--page", type=int, default=1)
    args = parser.parse_args(argv)
    try:
        if not args.workspace.is_dir():
            raise ValueError("workspace does not exist")
        if not re.fullmatch(r"[a-z0-9_]+", args.site):
            raise ValueError("site must be a stable lowercase source name without hyphens")
        if args.page < 1 or (args.command == "search" and not args.query.strip()):
            raise ValueError("search requires a query and page must be positive")
        paths = [args.snapshot_file.resolve(), args.rows_file.resolve()]
        root = args.workspace.resolve()
        if paths[0] == paths[1] or any(
                p.parent != root / "raw" or not p.name.startswith(args.site + "-")
                or p.suffix != ".json" for p in paths):
            raise ValueError("use two distinct raw/<site>-*.json files inside the workspace")
        snapshot, rows = [json.loads(p.read_text(encoding="utf-8")) for p in paths]
        classification = validate_snapshot(snapshot, rows)
        # Check before recording; do not turn an already-stopped site into a
        # newly successful backend. Malformed prior lines fail closed too.
        records = read_journal(root)
        if any("_unparsable" in r for r in records):
            raise ValueError("journal contains an unparsable line")
        if check_stop_order(records + [{"action": ACTION, "site": args.site,
                                       "url": snapshot["url"]}]):
            raise ValueError("READ_AFTER_STOP: site already stopped in this round")
        record = {
            "action": ACTION, "backend": args.backend, "operation": "snapshot",
            "mode": journal.current_mode(root), "site": args.site,
            "command": args.command, "fallback_reason": args.fallback_reason,
            "query": args.query, "page": args.page,
            "ts": dt.datetime.now(dt.timezone.utc).isoformat(),
            "url": snapshot["url"], "retrieved_at": snapshot["retrieved_at"],
            "classification": classification, "row_count": len(rows),
            "exit_code": 0 if classification == "ok" else 1,
            "empty_result": classification == "ok" and not rows,
            "identity_field": "title", "empty_identity_rows": [],
            "needs_detail_recovery": False, "detail_command": None,
            "snapshot_file": paths[0].relative_to(root).as_posix(),
            "rows_file": paths[1].relative_to(root).as_posix(),
            "input_hashes": {p.relative_to(root).as_posix(): journal.sha256_file(p) for p in paths},
        }
        # Always preserve an actual retrieval, including an unaccounted legacy
        # journey. Its missing accounting fails validation instead of vanishing.
        try:
            accounting = browser_budget.usage(snapshot, validate_rows=validate_snapshot)
            if args.command == 'search' and classification == 'ok' and accounting is None:
                raise ValueError('NAVIGATION_BUDGET_MISSING: successful search requires complete DOM catalog accounting')
            if accounting is not None:
                record['search_row_count'], record['search_pages'], _ = accounting
                record['empty_result'] = classification == 'ok' and not rows and accounting[0] == 0
        except ValueError as exc:
            record['budget_error'] = str(exc)
            if classification == 'ok':
                classification = 'transport'
                record.update(classification=classification, exit_code=1, empty_result=False)
        if classification == "not_logged_in":
            record["remedy"] = ("The site identifies this session as a guest and requires login. "
                                + recovery_guidance("login"))
        elif classification == "platform_limit":
            kind = "rate_limit" if snapshot.get("http_status") == 429 else "platform"
            record["remedy"] = recovery_guidance(kind)
        elif classification == "transport":
            reason = ("Catalog accounting is incomplete or exceeded its allowance; inspect the preserved stage evidence. "
                      if record.get('budget_error') or snapshot.get('budget_exceeded') else
                      "Navigation stopped before completion; earlier catalogs are preserved in the snapshot. "
                      if snapshot.get('navigation_error') else
                      f"HTTP {snapshot['http_status']} returned no successful page. "
                      if (snapshot.get("http_status") or 0) >= 400 else
                      "Page load deadline reached without extracted rows. "
                      if snapshot.get("load_timed_out") else
                      "The page exposed no readable text or extracted rows. ")
            if record.get('budget_error') or snapshot.get('budget_exceeded'):
                record['remedy'] = (reason + 'Follow references/browser-fallback.md to inspect the DOM and its accounting; '
                                   'do not retry an unaccounted catalog or call it an empty search result.')
            else:
                record["remedy"] = (reason +
                                    "Inspect the preserved snapshot and follow references/network-recovery.md; "
                                    "this is not an empty search result.")
        record = journal.sign_receipt(record)
        journal.append(root, record)
        print(json.dumps(record, ensure_ascii=False))
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print(f"INVALID_BROWSER_CAPTURE: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    raise SystemExit(main())
