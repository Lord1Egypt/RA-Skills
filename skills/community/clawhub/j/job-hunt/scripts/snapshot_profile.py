#!/usr/bin/env python3
"""Freeze the profile used for one discovery round without touching its master.

A later CV edit must not silently change the evidence behind an already-ranked
shortlist.  The destination is therefore created once and never overwritten by
this helper; a new round is the honest way to use a newer profile.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import journal  # noqa: E402


DESTINATION = "candidate-profile.yaml"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", required=True, type=pathlib.Path)
    parser.add_argument("--profile", required=True, type=pathlib.Path)
    args = parser.parse_args(argv)

    if not args.workspace.is_dir():
        print(f"workspace does not exist: {args.workspace}", file=sys.stderr)
        return 2
    if not args.profile.is_file():
        print(f"profile does not exist: {args.profile}", file=sys.stderr)
        return 2
    try:
        # Parse before copying so an unreadable master never becomes an opaque
        # snapshot that a later matcher treats as meaningful evidence.
        journal.load_yaml(args.profile)
        source = args.profile.read_bytes()
    except journal.YamlUnreadable as exc:
        print(exc.finding, file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"could not read profile {args.profile}: {exc}", file=sys.stderr)
        return 2

    destination = args.workspace / DESTINATION
    # `exists()` is false for a broken symlink. Without this explicit check, a
    # later write could follow a workspace-controlled link outside the round.
    if destination.is_symlink():
        print(f"PROFILE_SNAPSHOT_PATH_UNSAFE: {destination} is a symlink; refuse to "
              "write or trust evidence outside this workspace", file=sys.stderr)
        return 2
    if destination.exists():
        try:
            existing = destination.read_bytes()
        except OSError as exc:
            print(f"could not read existing snapshot {destination}: {exc}", file=sys.stderr)
            return 2
        if existing == source:
            print(destination)
            return 0
        print(f"PROFILE_SNAPSHOT_EXISTS: {destination} already contains a different "
              "profile; start a new round instead of changing this round's evidence",
              file=sys.stderr)
        return 2

    try:
        destination.write_bytes(source)
    except OSError as exc:
        print(f"could not write snapshot {destination}: {exc}", file=sys.stderr)
        return 2
    print(destination)
    return 0


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    raise SystemExit(main())
