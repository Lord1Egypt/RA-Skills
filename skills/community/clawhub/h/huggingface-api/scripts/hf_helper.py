#!/usr/bin/env python3
"""
Hugging Face Hub helper — programmatic CLI over the huggingface_hub Python API.

Reads HF_TOKEN from environment automatically; no token needed for public repos.

Usage:
    python hf_helper.py whoami
    python hf_helper.py info   <org/repo>  [--type model|dataset|space]
    python hf_helper.py files  <org/repo>  [--type model|dataset|space] [--revision REV]
    python hf_helper.py search <query>     [--type model|dataset|space] [--limit N]
    python hf_helper.py cache
    python hf_helper.py spaces <org>
"""

import argparse
import os
import sys


def _require_hub():
    try:
        import huggingface_hub  # noqa: F401
    except ImportError:
        sys.exit("huggingface_hub not installed. Run: pip install huggingface_hub")


def _api():
    from huggingface_hub import HfApi
    return HfApi(token=os.environ.get("HF_TOKEN"))


def cmd_whoami(_args):
    _require_hub()
    api = _api()
    try:
        info = api.whoami()
        print(f"User    : {info['name']}")
        print(f"Email   : {info.get('email', '(not set)')}")
        orgs = [o['name'] for o in info.get('orgs', [])]
        print(f"Orgs    : {', '.join(orgs) if orgs else '(none)'}")
    except Exception as e:
        sys.exit(f"Auth error: {e}\nSet HF_TOKEN or run: huggingface-cli login")


def cmd_info(args):
    _require_hub()
    api = _api()
    repo_type = args.type or "model"
    try:
        info = api.repo_info(repo_id=args.repo, repo_type=repo_type)
    except Exception as e:
        sys.exit(f"Error: {e}")

    print(f"ID          : {info.id}")
    print(f"Type        : {repo_type}")
    print(f"Private     : {info.private}")
    print(f"SHA         : {info.sha}")
    if hasattr(info, 'downloads') and info.downloads is not None:
        print(f"Downloads   : {info.downloads:,}")
    if hasattr(info, 'likes') and info.likes is not None:
        print(f"Likes       : {info.likes:,}")
    if hasattr(info, 'pipeline_tag') and info.pipeline_tag:
        print(f"Pipeline    : {info.pipeline_tag}")
    if hasattr(info, 'library_name') and info.library_name:
        print(f"Library     : {info.library_name}")
    tags = getattr(info, 'tags', []) or []
    if tags:
        print(f"Tags        : {', '.join(tags[:10])}{'...' if len(tags) > 10 else ''}")
    if hasattr(info, 'last_modified') and info.last_modified:
        print(f"Last modified: {info.last_modified}")


def cmd_files(args):
    _require_hub()
    api = _api()
    repo_type = args.type or "model"
    revision = args.revision or "main"
    try:
        items = list(api.list_repo_tree(
            repo_id=args.repo,
            repo_type=repo_type,
            revision=revision,
            recursive=True,
        ))
    except Exception as e:
        sys.exit(f"Error: {e}")

    from huggingface_hub.hf_api import RepoFile
    files = [i for i in items if isinstance(i, RepoFile)]
    total = sum(f.size or 0 for f in files)
    print(f"{len(files)} files  ({_human_size(total)} total)\n")
    for f in sorted(files, key=lambda x: x.path):
        size_str = _human_size(f.size or 0).rjust(9)
        print(f"  {size_str}  {f.path}")


def cmd_search(args):
    _require_hub()
    api = _api()
    repo_type = args.type or "model"
    limit = args.limit or 10
    try:
        if repo_type == "model":
            results = list(api.list_models(search=args.query, limit=limit, sort="downloads", direction=-1))
            for r in results:
                dl = f"  {r.downloads:>10,} dl" if r.downloads else ""
                print(f"{r.id}{dl}")
        elif repo_type == "dataset":
            results = list(api.list_datasets(search=args.query, limit=limit))
            for r in results:
                print(r.id)
        elif repo_type == "space":
            results = list(api.list_spaces(search=args.query, limit=limit))
            for r in results:
                print(r.id)
        else:
            sys.exit(f"Unknown type: {repo_type}")
    except Exception as e:
        sys.exit(f"Error: {e}")
    if not results:
        print(f"No {repo_type}s found for '{args.query}'.")


def cmd_cache(_args):
    _require_hub()
    from huggingface_hub import scan_cache_dir
    try:
        info = scan_cache_dir()
    except Exception as e:
        sys.exit(f"Error scanning cache: {e}")

    print(f"Cache dir : {info.cache_dir}")
    print(f"Total size: {info.size_on_disk_str}")
    print(f"Repos     : {len(info.repos)}\n")
    for repo in sorted(info.repos, key=lambda r: r.size_on_disk, reverse=True):
        rev_count = len(repo.revisions)
        print(f"  {repo.size_on_disk_str:>9}  {repo.repo_type}/{repo.repo_id}  ({rev_count} revision{'s' if rev_count != 1 else ''})")


def cmd_spaces(args):
    _require_hub()
    api = _api()
    try:
        spaces = list(api.list_spaces(author=args.org, limit=args.limit or 20))
    except Exception as e:
        sys.exit(f"Error: {e}")
    if not spaces:
        print(f"No spaces found for '{args.org}'.")
        return
    print(f"{len(spaces)} space(s) for '{args.org}':\n")
    for s in spaces:
        sdk = getattr(s, 'sdk', '') or ''
        print(f"  {s.id}  [{sdk}]")


def _human_size(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


def main():
    parser = argparse.ArgumentParser(
        description="Hugging Face Hub helper (uses HF_TOKEN env var for auth)"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("whoami", help="Print current authenticated user")

    p_info = sub.add_parser("info", help="Show repo metadata")
    p_info.add_argument("repo", help="org/repo")
    p_info.add_argument("--type", choices=["model", "dataset", "space"], default="model")

    p_files = sub.add_parser("files", help="List files in a repo")
    p_files.add_argument("repo", help="org/repo")
    p_files.add_argument("--type", choices=["model", "dataset", "space"], default="model")
    p_files.add_argument("--revision", default="main")

    p_search = sub.add_parser("search", help="Search the Hub")
    p_search.add_argument("query")
    p_search.add_argument("--type", choices=["model", "dataset", "space"], default="model")
    p_search.add_argument("--limit", type=int, default=10)

    sub.add_parser("cache", help="Show local cache summary")

    p_spaces = sub.add_parser("spaces", help="List Spaces for an org/user")
    p_spaces.add_argument("org")
    p_spaces.add_argument("--limit", type=int, default=20)

    args = parser.parse_args()
    dispatch = {
        "whoami": cmd_whoami,
        "info":   cmd_info,
        "files":  cmd_files,
        "search": cmd_search,
        "cache":  cmd_cache,
        "spaces": cmd_spaces,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
