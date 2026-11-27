#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""git-author-guard: detect env-var identity overrides and audit commit authorship.

Modes:
  detect                              Compare GIT_AUTHOR_*/GIT_COMMITTER_* env vars
                                      against `git config user.*`; report shadowing.
  scan   [--repo PATH] [--expect "Name <email>"]
         [-n N] [--since REF] [--include-committer]
                                        List recent commits whose author (default) or
                                        committer identity is not the expected one.

Exit codes: 0 = clean/no shadowing, 1 = problem found, 2 = usage or repo error.
"""
import argparse
import os
import re
import subprocess
import sys

ENV_KEYS = ("GIT_AUTHOR_NAME", "GIT_AUTHOR_EMAIL",
            "GIT_COMMITTER_NAME", "GIT_COMMITTER_EMAIL")
IDENT_RE = re.compile(r"^\s*(.+?)\s*<([^>]*)>\s*$")


def run_git(repo, args):
    cmd = ["git", "-C", repo] + args
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        sys.stderr.write(p.stderr.strip() + "\n")
        sys.exit(2)
    return p.stdout


def cmd_detect(_args):
    overrides = {k: os.environ[k] for k in ENV_KEYS if os.environ.get(k)}
    if not overrides:
        print("OK: no GIT_AUTHOR_*/GIT_COMMITTER_* environment overrides.")
        return
    print("WARNING: environment overrides detected — they beat git config on every commit:")
    for k, v in overrides.items():
        print("  %s=%s" % (k, v))
    for side in ("user.name", "user.email"):
        p = subprocess.run(["git", "config", side], capture_output=True, text=True)
        cfg = p.stdout.strip() if p.returncode == 0 else "(unset)"
        print("  git config %s = %s" % (side, cfg))
    print("Fix: prefix commits with "
          "`env -u GIT_AUTHOR_NAME -u GIT_AUTHOR_EMAIL "
          "-u GIT_COMMITTER_NAME -u GIT_COMMITTER_EMAIL git commit ...` "
          "and set --author=\"Name <email>\" explicitly.")
    sys.exit(1)


def parse_ident(raw):
    m = IDENT_RE.match(raw)
    return (m.group(1), m.group(2)) if m else (raw, "")


def cmd_scan(args):
    repo = os.path.abspath(args.repo)
    if args.expect:
        m = IDENT_RE.match(args.expect)
        if not m:
            sys.stderr.write('--expect must look like "Name <email>"\n')
            sys.exit(2)
        exp_name, exp_mail = m.group(1), m.group(2)
    else:
        exp_name = run_git(repo, ["config", "user.name"]).strip()
        exp_mail = run_git(repo, ["config", "user.email"]).strip()
        if not exp_name and not exp_mail:
            sys.stderr.write("No expected identity: pass --expect or set git config user.*\n")
            sys.exit(2)

    rev = ["-%d" % args.n]
    if args.since:
        rev.append(args.since)
    rev.append("--format=%H%x09%an%x09%ae%x09%cn%x09%ce%x09%s")
    lines = run_git(repo, ["log"] + rev).splitlines()

    bad = []
    for line in lines:
        parts = line.split("\t", 5)
        if len(parts) < 6:
            continue
        h, an, ae, cn, ce, subj = parts
        author_bad = not (an == exp_name and ae == exp_mail)
        committer_bad = args.include_committer and not (cn == exp_name and ce == exp_mail)
        if author_bad or committer_bad:
            bad.append((h[:10], an, ae, cn, ce, subj,
                        ("author" if author_bad else "") +
                        ("+committer" if committer_bad else "")))
    if bad:
        print("FOUND %d commit(s) with unexpected identity (expected %s <%s>):"
              % (len(bad), exp_name, exp_mail))
        for h, an, ae, cn, ce, subj, why in bad:
            print("  %s [%s] %s\n    author:    %s <%s>\n    committer: %s <%s>\n    %s"
                  % (h, why, subj, an, ae, cn, ce, subj))
        sys.exit(1)
    print("OK: last %d commit(s) authored as %s <%s>."
          % (len(lines), exp_name, exp_mail))
    sys.exit(0)


def main():
    ap = argparse.ArgumentParser(description="git commit identity guard")
    sub = ap.add_subparsers(dest="mode", required=True)
    sub.add_parser("detect", help="report env-var identity overrides")
    s = sub.add_parser("scan", help="audit recent commit identities")
    s.add_argument("--repo", default=".")
    s.add_argument("--expect", default=None, help='"Name <email>" expected identity')
    s.add_argument("-n", type=int, default=30, help="how many commits to scan (default 30)")
    s.add_argument("--since", default=None, help="git rev, e.g. origin/main@{1}")
    s.add_argument("--include-committer", action="store_true",
                   help="also audit committer identity (note: GitHub web-UI squash "
                        "merges legitimately set committer to GitHub, so author-only "
                        "is the default)")
    args = ap.parse_args()
    cmd_detect(args) if args.mode == "detect" else cmd_scan(args)


if __name__ == "__main__":
    main()
