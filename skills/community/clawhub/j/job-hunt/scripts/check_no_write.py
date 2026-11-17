#!/usr/bin/env python3
"""Gate: no write command was run (spec D7, risk register row 13).

A greeting that went out cannot be recalled and leaves no local trace, so the
guard has to be an after-the-fact scan against the tool's own metadata.

KNOWN BOUND, stated rather than papered over: this gate can only see commands
that were journaled. It proves nothing about a command nobody recorded. The
load-bearing half of the guarantee is that no write command appears anywhere in
this skill's instructions and every command the mode file names is access: read.

Exit codes: 0 = passed, 1 = findings on stdout, 2 = could not run. On exit 2 one
receipt with verdict "could_not_run" is appended — EXCEPT when the workspace
directory itself does not exist, because then there is nothing to append to. If
you find no receipt at all, that is the case you are in.
"""
from __future__ import annotations

import argparse
import pathlib
import shlex
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import journal  # noqa: E402  (Plan 1)
import opencli_meta  # noqa: E402
from check_opencli_result import ADAPTER_CALL_ACTION, read_journal  # noqa: E402

from record_browser_capture import ACTION, validate_record, check_stop_order

GATE = "check_no_write"

# opencli's non-adapter namespaces (`opencli auth --help -f yaml` returns
# `namespace: auth` and publishes NO access: field). Only the commands this
# skill actually needs are allow-listed; everything else in those namespaces
# falls through to UNKNOWN_ACCESS and fails closed. Every genuine write command
# in the toolset lives on an adapter, where the tool's own metadata governs.
NON_ADAPTER_READS = {("auth", "status")}

GLOBAL_VALUE_FLAGS = {"--profile"}


def parse_command_line(text):
    """('boss', 'greet') from 'opencli boss greet --job-id X'; None otherwise.

    Site and command are the first two positional tokens and always precede any
    flag, so the scan stops at the first token starting with '-'. That means
    `opencli boss --help -f yaml` correctly yields None rather than ('boss',
    'yaml'). A command line that buries the site behind other leading flags will
    not be recognised — which is why the mode records site/command as structured
    fields and this parser is only the backstop.
    """
    if not text:
        return None
    try:
        tokens = shlex.split(text)
    except ValueError:
        tokens = text.split()
    tokens = [t for t in tokens if t]
    if not tokens:
        return None
    if pathlib.PurePath(tokens[0]).name != "opencli":
        return None
    rest = tokens[1:]
    while rest and rest[0] in GLOBAL_VALUE_FLAGS:
        rest = rest[2:]
    positional = []
    for token in rest:
        if token.startswith("-"):
            break
        positional.append(token)
    if len(positional) < 2:
        return None
    return positional[0], positional[1]


def resolve_access(site, command, cache_dir, allow_fetch):
    if (site, command) in NON_ADAPTER_READS:
        return "read"
    return opencli_meta.access_for(site, command, cache_dir=cache_dir,
                                   allow_fetch=allow_fetch)


def scan(records, cache_dir, allow_fetch, workspace=None):
    from search_capture import ACTION as SEARCH_ACTION, validate_record as validate_search
    findings = check_stop_order(records)
    for record in records:
        lineno = record.get("_lineno")
        if "_unparsable" in record:
            findings.append(
                f"UNPARSABLE_JOURNAL_LINE: journal.jsonl line {lineno} is not "
                "JSON, so a command hidden in it cannot be checked")
            continue
        if record.get('action') == SEARCH_ACTION:
            findings.extend(validate_search(record, workspace) if workspace else
                            ['INVALID_SEARCH_CAPTURE: workspace required'])
            continue
        if record.get("action") == ACTION:
            findings.extend(validate_record(record, workspace) if workspace else
                            ["INVALID_BROWSER_RECORD: workspace required to verify capture"])
        pairs = []
        if (record.get("action") == ADAPTER_CALL_ACTION
                and record.get("site") and record.get("command")):
            pairs.append((str(record["site"]), str(record["command"])))
        parsed = parse_command_line(record.get("command_line") or "")
        if parsed and parsed not in pairs:
            pairs.append(parsed)
        for site, command in pairs:
            access = resolve_access(site, command, cache_dir, allow_fetch)
            if access == "write":
                findings.append(
                    f"WRITE_COMMAND: journal.jsonl line {lineno} ran `opencli "
                    f"{site} {command}` — `opencli {site} --help -f yaml` "
                    "publishes access: write. This skill is read-only and has "
                    "no confirm-then-send path.")
            elif access is None:
                findings.append(
                    f"UNKNOWN_ACCESS: journal.jsonl line {lineno} ran `opencli "
                    f"{site} {command}` — no access metadata available, so this "
                    "cannot be shown to be a read. Save `opencli {0} --help -f "
                    "yaml` into the metadata cache and re-run.".format(site))
    return findings


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Gate: no opencli write command was run in this workspace.")
    parser.add_argument("--workspace", required=True, type=pathlib.Path)
    parser.add_argument("--metadata-cache", type=pathlib.Path,
                        help="default: <workspace>/raw/opencli-help")
    parser.add_argument("--no-fetch", action="store_true",
                        help="never shell out to opencli; use the cache only")
    args = parser.parse_args(argv)

    workspace = args.workspace
    if not workspace.is_dir():
        print(f"workspace not found: {workspace}", file=sys.stderr)
        return 2
    journal_path = workspace / "journal.jsonl"
    if not journal_path.is_file():
        journal.receipt(workspace, GATE, {}, "could_not_run",
                        [f"missing input: {journal_path}"])
        print(f"missing input: {journal_path}", file=sys.stderr)
        return 2

    cache_dir = args.metadata_cache or (workspace / "raw" / "opencli-help")
    findings = scan(read_journal(workspace), cache_dir, not args.no_fetch, workspace)

    input_hashes = {"journal.jsonl": journal.sha256_file(journal_path)}
    journal.receipt(workspace, GATE, input_hashes,
                    "fail" if findings else "pass", findings)
    for line in findings:
        print(line)
    return 1 if findings else 0


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    raise SystemExit(main())
