#!/usr/bin/env python3
"""Configure reusable OData service profiles without storing credentials."""

from __future__ import annotations

import argparse
import json
import sys

from odata_profiles import config_path, load_config, public_profile, save_config, validate_profile


def output(value) -> None:  # noqa: ANN001
    json.dump(value, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def parse_headers(values: list[str]) -> dict[str, str]:
    result = {}
    for item in values:
        if "=" not in item:
            raise ValueError("--header-env must be HEADER=ENV_VAR")
        header, env_name = item.split("=", 1)
        result[header] = env_name
    return result


def command_set(args: argparse.Namespace) -> None:
    path = config_path(args.config)
    value = load_config(path)
    profile = {
        "service_root": args.service_root,
        "odata_version": args.odata_version,
        "headers_from_env": parse_headers(args.header_env),
    }
    for field in ("bearer_env", "basic_user_env", "basic_password_env"):
        option = getattr(args, field)
        if option:
            profile[field] = option
    value["profiles"][args.name] = validate_profile(args.name, profile)
    if args.default or not value.get("default_profile"):
        value["default_profile"] = args.name
    save_config(path, value)
    output({"saved": args.name, "default_profile": value["default_profile"], "config": str(path)})


def command_list(args: argparse.Namespace) -> None:
    path = config_path(args.config)
    value = load_config(path)
    output({"config": str(path), "default_profile": value["default_profile"], "profiles": sorted(value["profiles"])})


def command_show(args: argparse.Namespace) -> None:
    path = config_path(args.config)
    value = load_config(path, require=True)
    profile = value["profiles"].get(args.name)
    if profile is None:
        raise ValueError(f"OData profile {args.name!r} does not exist in {path}")
    output({"name": args.name, "default": value["default_profile"] == args.name, **public_profile(profile)})


def command_default(args: argparse.Namespace) -> None:
    path = config_path(args.config)
    value = load_config(path, require=True)
    if args.name not in value["profiles"]:
        raise ValueError(f"OData profile {args.name!r} does not exist in {path}")
    value["default_profile"] = args.name
    save_config(path, value)
    output({"default_profile": args.name, "config": str(path)})


def command_remove(args: argparse.Namespace) -> None:
    path = config_path(args.config)
    value = load_config(path, require=True)
    if args.name not in value["profiles"]:
        raise ValueError(f"OData profile {args.name!r} does not exist in {path}")
    del value["profiles"][args.name]
    if value["default_profile"] == args.name:
        value["default_profile"] = sorted(value["profiles"])[0] if value["profiles"] else None
    save_config(path, value)
    output({"removed": args.name, "default_profile": value["default_profile"], "config": str(path)})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", help="config path; defaults to ODATA_SKILL_CONFIG or ~/.config/odata-skill/services.json")
    subparsers = parser.add_subparsers(dest="command", required=True)

    set_parser = subparsers.add_parser("set", help="create or replace a profile")
    set_parser.add_argument("name")
    set_parser.add_argument("--service-root", required=True)
    set_parser.add_argument("--odata-version", choices=("4.0", "4.01"), default="4.0")
    set_parser.add_argument("--bearer-env", metavar="ENV_VAR")
    set_parser.add_argument("--basic-user-env", metavar="ENV_VAR")
    set_parser.add_argument("--basic-password-env", metavar="ENV_VAR")
    set_parser.add_argument("--header-env", action="append", default=[], metavar="HEADER=ENV_VAR")
    set_parser.add_argument("--default", action="store_true")
    set_parser.set_defaults(handler=command_set)

    list_parser = subparsers.add_parser("list", help="list profile names")
    list_parser.set_defaults(handler=command_list)
    show = subparsers.add_parser("show", help="show one profile without resolving secret values")
    show.add_argument("name")
    show.set_defaults(handler=command_show)
    default = subparsers.add_parser("default", help="select the default profile")
    default.add_argument("name")
    default.set_defaults(handler=command_default)
    remove = subparsers.add_parser("remove", help="remove a profile")
    remove.add_argument("name")
    remove.set_defaults(handler=command_remove)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        args.handler(args)
    except (ValueError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
