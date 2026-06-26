#!/usr/bin/env python3
"""Manage Pocketbook profile defaults and aliases."""

from __future__ import annotations

import argparse
import sys

from ledger_common import (
    configure_standard_streams,
    PROFILE_ALIAS_FIELDS,
    PROFILE_DEFAULT_FIELDS,
    json_dump,
    load_profile,
    save_profile,
)


def show_command(args: argparse.Namespace) -> dict:
    return {"ok": True, "profile": load_profile(args.data_dir)}


def set_default_command(args: argparse.Namespace) -> dict:
    profile = load_profile(args.data_dir)
    profile.setdefault("defaults", {})[args.field] = args.value
    saved = save_profile(args.data_dir, profile)
    return {"ok": True, "profile": saved}


def remove_default_command(args: argparse.Namespace) -> dict:
    profile = load_profile(args.data_dir)
    profile.setdefault("defaults", {}).pop(args.field, None)
    saved = save_profile(args.data_dir, profile)
    return {"ok": True, "profile": saved}


def set_alias_command(args: argparse.Namespace) -> dict:
    profile = load_profile(args.data_dir)
    profile.setdefault("aliases", {}).setdefault(args.field, {})[args.alias] = args.value
    saved = save_profile(args.data_dir, profile)
    return {"ok": True, "profile": saved}


def remove_alias_command(args: argparse.Namespace) -> dict:
    profile = load_profile(args.data_dir)
    profile.setdefault("aliases", {}).setdefault(args.field, {}).pop(args.alias, None)
    if not profile["aliases"][args.field]:
        profile["aliases"].pop(args.field, None)
    saved = save_profile(args.data_dir, profile)
    return {"ok": True, "profile": saved}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage Pocketbook profile.json.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    show = subparsers.add_parser("show")
    show.add_argument("--data-dir", default=None, help="Ledger data root.")

    set_default = subparsers.add_parser("set-default")
    set_default.add_argument("--data-dir", default=None, help="Ledger data root.")
    set_default.add_argument("--field", choices=sorted(PROFILE_DEFAULT_FIELDS), required=True)
    set_default.add_argument("--value", required=True)

    remove_default = subparsers.add_parser("remove-default")
    remove_default.add_argument("--data-dir", default=None, help="Ledger data root.")
    remove_default.add_argument("--field", choices=sorted(PROFILE_DEFAULT_FIELDS), required=True)

    set_alias = subparsers.add_parser("set-alias")
    set_alias.add_argument("--data-dir", default=None, help="Ledger data root.")
    set_alias.add_argument("--field", choices=sorted(PROFILE_ALIAS_FIELDS), required=True)
    set_alias.add_argument("--alias", required=True)
    set_alias.add_argument("--value", required=True)

    remove_alias = subparsers.add_parser("remove-alias")
    remove_alias.add_argument("--data-dir", default=None, help="Ledger data root.")
    remove_alias.add_argument("--field", choices=sorted(PROFILE_ALIAS_FIELDS), required=True)
    remove_alias.add_argument("--alias", required=True)

    return parser


def main() -> int:
    configure_standard_streams()
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "show":
        result = show_command(args)
    elif args.command == "set-default":
        result = set_default_command(args)
    elif args.command == "remove-default":
        result = remove_default_command(args)
    elif args.command == "set-alias":
        result = set_alias_command(args)
    else:
        result = remove_alias_command(args)
    print(json_dump(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
