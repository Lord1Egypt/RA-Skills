#!/usr/bin/env python3
"""Small CLI for common gitcode-api SDK actions.

Deprecated: kept for backward compatibility. Prefer the package's built-in
``gitcode-api`` console entry (still experimental); see
https://gitcode-api.readthedocs.io/en/latest/sdk/cli.html
"""

import argparse
import json
import os
import sys
import warnings
from typing import Any

from gitcode_api import GitCode

_BUILTIN_CLI_DOCS = "https://gitcode-api.readthedocs.io/en/latest/sdk/cli.html"


def build_client(args: argparse.Namespace) -> GitCode:
    return GitCode(
        api_key=args.api_key or os.getenv("GITCODE_ACCESS_TOKEN"),
        owner=getattr(args, "owner", None),
        repo=getattr(args, "repo", None),
    )


def to_json(data: Any) -> str:
    if isinstance(data, list):
        payload = [item.to_dict() if hasattr(item, "to_dict") else item for item in data]
    elif hasattr(data, "to_dict"):
        payload = data.to_dict()
    else:
        payload = data
    return json.dumps(payload, indent=2, ensure_ascii=True, sort_keys=True)


def cmd_repo(args: argparse.Namespace) -> int:
    with build_client(args) as client:
        repo = client.repos.get()
    print(to_json(repo))
    return 0


def cmd_pulls(args: argparse.Namespace) -> int:
    with build_client(args) as client:
        pulls = client.pulls.list(state=args.state, per_page=args.per_page)
    print(to_json(pulls))
    return 0


def cmd_me(args: argparse.Namespace) -> int:
    with build_client(args) as client:
        user = client.users.me()
    print(to_json(user))
    return 0


def cmd_search_repos(args: argparse.Namespace) -> int:
    with build_client(args) as client:
        repos = client.search.repositories(q=args.query, per_page=args.per_page)
    print(to_json(repos))
    return 0


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run common gitcode-api SDK operations.")
    parser.add_argument("--api-key", help="GitCode access token. Defaults to GITCODE_ACCESS_TOKEN.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    repo_parser = subparsers.add_parser("repo", help="Fetch a repository using client.repos.get().")
    repo_parser.add_argument("--owner", required=True, help="Repository owner.")
    repo_parser.add_argument("--repo", required=True, help="Repository name.")
    repo_parser.set_defaults(func=cmd_repo)

    pulls_parser = subparsers.add_parser("pulls", help="List pull requests using client.pulls.list().")
    pulls_parser.add_argument("--owner", required=True, help="Repository owner.")
    pulls_parser.add_argument("--repo", required=True, help="Repository name.")
    pulls_parser.add_argument("--state", default="open", help="Pull request state filter.")
    pulls_parser.add_argument("--per-page", type=int, default=10, help="Number of items to request.")
    pulls_parser.set_defaults(func=cmd_pulls)

    me_parser = subparsers.add_parser("me", help="Fetch the authenticated user using client.users.me().")
    me_parser.set_defaults(func=cmd_me)

    search_parser = subparsers.add_parser(
        "search-repos",
        help="Search repositories using client.search.repositories().",
    )
    search_parser.add_argument("--query", required=True, help="Search query string.")
    search_parser.add_argument("--per-page", type=int, default=10, help="Number of items to request.")
    search_parser.set_defaults(func=cmd_search_repos)

    return parser


def main() -> int:
    warnings.warn(
        "This script is deprecated and retained for backward compatibility only. "
        "The gitcode-api package provides an experimental built-in CLI (`gitcode-api` / "
        f"`python -m gitcode_api`); see {_BUILTIN_CLI_DOCS}",
        DeprecationWarning,
        stacklevel=1,
    )
    parser = make_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except Exception as exc:  # pragma: no cover - standalone helper
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
