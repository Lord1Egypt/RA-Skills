#!/usr/bin/env python3
"""Gate a weekly digest email before it is sent.

Exit 0 = send it. Exit 1 = findings (one `DIGEST_<CODE>: …` line each); send
nothing. Checks: the discover round itself passes check_shortlist; at most five
roles, each in the shortlist, read in full, with a link, a reason and gaps, and not
sent before; every source that could not be checked is named in the email; no prediction language
(lint_no_prediction); the email was composed from the current picks.
"""
from __future__ import annotations

import argparse
import contextlib
import datetime
import io
import json
import pathlib
import sys

import digest_compose
import digest_ledger
import journal

GATE = "check_digest"


def cannot_run(workspace: pathlib.Path, reason: str, code: str = "NO_INPUT") -> int:
    print(f"cannot run: {reason}", file=sys.stderr)
    if workspace.is_dir():
        journal.receipt(workspace, GATE, {}, "could_not_run", [f"{code}: {reason}"])
    return 2


def _hashes(workspace: pathlib.Path) -> dict:
    return {name: journal.sha256_file(workspace / name)
            for name in ("digest-email.json", "digest-email.txt", "digest-picks.yaml",
                         "digest-sources.yaml", "shortlist.yaml") if (workspace / name).exists()}


def _quiet(fn, argv) -> tuple[int, str]:
    out = io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
        code = fn(argv)
    return code, out.getvalue()


def _journal(workspace: pathlib.Path) -> list:
    path = workspace / "journal.jsonl"
    records = []
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                record = json.loads(line)
            except ValueError:
                continue
            if isinstance(record, dict):
                records.append(record)
    return records


def check(workspace: pathlib.Path, name: str) -> list:
    import check_shortlist
    import lint_no_prediction
    findings = []
    # The email is linted first: check_shortlist re-verifies every lint receipt in the
    # journal, so linting afterwards left the previous email's receipt stale after a
    # re-compose and failed the round's own gate (STALE_RECEIPT).
    text_path = workspace / "digest-email.txt"
    code, out = _quiet(lint_no_prediction.main, ["--workspace", str(workspace), "--files", str(text_path)])
    if code != 0:
        for line in out.splitlines():
            if line.strip() and not line.startswith(("PASS", "NOTICE")):
                findings.append(f"DIGEST_PREDICTION: {line}")
    code, out = _quiet(check_shortlist.main, ["--workspace", str(workspace)])
    if code != 0:
        first = next((l for l in out.splitlines() if l.strip() and not l.startswith("PASS")), "")
        findings.append(f"DIGEST_SHORTLIST_GATE: check_shortlist exit {code}: {first}")
    email_path = workspace / "digest-email.json"
    email = json.loads(email_path.read_text(encoding="utf-8"))
    if email.get("inputs_sha256") != digest_compose.inputs_hash(workspace):
        findings.append("DIGEST_EMAIL_STALE: picks, sources or shortlist changed after compose; compose again")
    picks, sources, rows = digest_compose.load_inputs(workspace)
    chosen = picks.get("roles") or []
    if len(chosen) > digest_compose.MAX_ROLES:
        findings.append(f"DIGEST_TOO_MANY_ROLES: {len(chosen)} > {digest_compose.MAX_ROLES}")
    ledger = digest_ledger.load_ledger(name)
    batch = {"roles": []}
    for pick in chosen:
        rid = pick.get("id")
        row = rows.get(rid)
        if row is None:
            findings.append(f"DIGEST_ROW_NOT_IN_SHORTLIST: {rid}")
            continue
        if row.get("quality") != "complete":
            findings.append(f"DIGEST_ROW_NOT_READ: {rid} quality={row.get('quality')}; read the full posting")
        if not str(row.get("url") or "").strip():
            findings.append(f"DIGEST_NO_LINK: {rid}")
        if not str(pick.get("why") or "").strip() or not str(pick.get("gaps") or "").strip():
            findings.append(f"DIGEST_NO_REASON: {rid} needs both `why` and `gaps`")
        if digest_ledger.is_seen(row, ledger) or digest_ledger.is_seen(row, batch):
            findings.append(f"DIGEST_ROW_ALREADY_SENT: {rid}")
        batch = digest_ledger.record_sent(batch, [row], datetime.date.today())
    shortlist = journal.load_yaml(workspace / "shortlist.yaml")
    records = _journal(workspace)
    named = {str(u.get("site", "")).lower() for u in sources.get("unchecked") or [] if isinstance(u, dict)}
    failed = {str(r.get("site")).lower() for r in records
              if r.get("site") and r.get("classification") not in (None, "ok")}
    for source in shortlist.get("sources") or []:
        if isinstance(source, dict) and source.get("classification") not in (None, "ok"):
            failed.add(str(source.get("site", "")).lower())
    for site in sorted(failed - named):
        findings.append(f"DIGEST_UNCHECKED_NOT_NAMED: {site} was not checked fully; name it with its reason")
    return findings


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workspace", required=True, type=pathlib.Path)
    ap.add_argument("--name", required=True)
    args = ap.parse_args(argv)
    workspace = args.workspace
    if not workspace.is_dir():
        return cannot_run(workspace, f"workspace {workspace} does not exist")
    for name in ("digest-email.json", "digest-picks.yaml", "digest-sources.yaml", "shortlist.yaml"):
        if not (workspace / name).is_file():
            hint = " (run `digest.py compose` first)" if name.startswith("digest-email") else ""
            return cannot_run(workspace, f"{name} is missing{hint}", "MISSING_INPUT")
    try:
        findings = check(workspace, args.name)
    except journal.YamlUnreadable as exc:
        return cannot_run(workspace, str(exc), "UNREADABLE_INPUT")
    except (OSError, ValueError) as exc:
        return cannot_run(workspace, str(exc), "UNREADABLE_INPUT")
    for line in findings:
        print(line)
    journal.receipt(workspace, GATE, _hashes(workspace), "fail" if findings else "pass", findings)
    return 1 if findings else 0


if __name__ == "__main__":
    from cli_io import configure_output
    configure_output()
    raise SystemExit(main())
