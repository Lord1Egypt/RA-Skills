#!/usr/bin/env python3
"""Gate: protected personal data must not survive into a Cluster-1 application.

The renderer suppresses these fields for a Cluster-1 target, but the renderer is
the last line, not the rule. cv-craft requires the *tailoring* step to strip
them, because a tailored profile that still carries a DOB leaks the moment
anyone re-renders it against a different market string — and the market string
is the one field a returning user changes.

Exit 0 = clean. Exit 1 = findings. Exit 2 = no tailored profile to check.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import journal
import render_cv

GATE = "check_personal_data"


def findings_for(profile) -> list:
    # Same class as render_cv.missing_required_fields: a non-dict `meta`
    # sailed past `or {}` and raised AttributeError, so the gate exited 1
    # with no finding and no receipt.
    market = journal.as_mapping(journal.as_mapping(profile).get("meta")).get(
        "target_market")
    fields = render_cv.protected_fields(profile)
    if not fields:
        return []
    named = ", ".join(fields)
    if not str(market or "").strip():
        return [f"NO_TARGET_MARKET: the tailored profile carries {named} but sets no "
                f"meta.target_market, so no CV-convention rule can be applied to it"]
    cluster = render_cv.resolve_cluster(market)
    if cluster is None:
        return [f"MARKET_UNRECOGNIZED: meta.target_market {market!r} matches no known "
                f"CV-convention cluster while the profile carries {named}; set a "
                f"recognised country name so the interlock can decide"]
    if cluster == 1:
        return [f"CLUSTER1_PERSONAL_DATA: {named} are present in the tailored profile "
                f"for a Cluster-1 target ({market!r}); strip them at the tailoring "
                f"step and tell the user you did and why — the renderer's suppression "
                f"is defence in depth, not the rule"]
    return []


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", required=True)
    ap.add_argument("--profile", default=None,
                    help="default: <workspace>/tailored-profile.yaml")
    args = ap.parse_args(argv)

    ws = pathlib.Path(args.workspace)
    if not ws.is_dir():
        # journal.receipt() would mkdir it, and a gate that creates the
        # workspace it is auditing has manufactured its own evidence.
        print(f"cannot run {GATE}: workspace {ws} does not exist", file=sys.stderr)
        return 2
    path = pathlib.Path(args.profile) if args.profile else ws / "tailored-profile.yaml"
    if not path.exists():
        journal.receipt(ws, GATE, {}, "could_not_run", [f"MISSING_INPUT: {path}"])
        print(f"cannot run {GATE}: {path} does not exist", file=sys.stderr)
        return 2

    try:
        profile = journal.load_yaml(path)
    except journal.YamlUnreadable as exc:
        journal.receipt(ws, GATE, {}, "could_not_run", [exc.finding])
        print(f"cannot run {GATE}: {exc}", file=sys.stderr)
        return 2

    findings = findings_for(profile)
    for f in findings:
        print(f)
    journal.receipt(ws, GATE, {path.name: journal.sha256_file(path)},
                    "fail" if findings else "pass", findings)
    return 1 if findings else 0


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    sys.exit(main())
