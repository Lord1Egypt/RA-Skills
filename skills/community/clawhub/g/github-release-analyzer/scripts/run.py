#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from models import ReleaseItem, ReleaseSummary
from release_fetcher import (
    ReleaseFetchError,
    apply_limit,
    fetch_releases,
    filter_formal_releases,
    has_fast_no_update,
    pending_for_cron,
    select_manual_latest,
)
from repo_utils import RepoParseError, parse_repo
from state_store import load_state, now_iso, save_state
from summary_formatter import TemplateError, render_message


DEFAULT_LIMITS = {"manual": 1, "cron": 20}


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Prepare and commit GitHub release analysis state")
    sub = p.add_subparsers(dest="command", required=True)

    prep = sub.add_parser("prepare")
    prep.add_argument("--repo", required=True)
    prep.add_argument("--mode", choices=["manual", "cron"], required=True)
    prep.add_argument("--state-key")
    prep.add_argument("--latest-only", action="store_true")
    prep.add_argument("--limit", type=int)
    prep.add_argument("--include-prerelease", action="store_true")
    prep.add_argument("--output-template", default="default")
    prep.add_argument("--initial-cron-behavior", default="latest-only")

    render = sub.add_parser("render")
    render.add_argument("--repo", required=True)
    render.add_argument("--mode", choices=["manual", "cron"], required=True)
    render.add_argument("--output-template", default="default")

    commit = sub.add_parser("commit")
    commit.add_argument("--repo", required=True)
    commit.add_argument("--mode", choices=["cron"], required=True)
    commit.add_argument("--state-key")
    commit.add_argument("--processed-tags", required=True, help="comma-separated tags")
    commit.add_argument("--latest-release-id", type=int, required=True)
    commit.add_argument("--latest-published-at", required=True)

    return p


def default_limit(mode: str, explicit: int | None) -> int:
    if explicit is not None:
        return explicit
    return DEFAULT_LIMITS[mode]


def default_latest_only(mode: str, explicit: bool) -> bool:
    if explicit:
        return True
    return mode == "manual"


def _selection_meta(items: list[ReleaseItem]) -> dict[str, Any]:
    return {
        "selectedCount": len(items),
        "selectedTags": [item.tag_name for item in items if item.tag_name],
        "selectedReleaseIds": [item.release_id for item in items if item.release_id is not None],
    }


def _prepare_base_payload(args: argparse.Namespace, repo_slug: str, state_key: str | None, state_path: str | None) -> dict[str, Any]:
    return {
        "mode": args.mode,
        "repo": repo_slug,
        "stateKey": state_key,
        "statePath": state_path,
        "outputTemplate": args.output_template,
    }


def _prepare_result(
    args: argparse.Namespace,
    repo_slug: str,
    status: str,
    reason: str,
    releases: list[ReleaseItem],
    *,
    state_key: str | None = None,
    state_path: str | None = None,
    first_run: bool | None = None,
) -> dict[str, Any]:
    payload = _prepare_base_payload(args, repo_slug, state_key, state_path)
    if first_run is not None:
        payload["firstRun"] = first_run
    payload.update(
        {
            "status": status,
            "reason": reason,
            "releases": [item.to_dict() for item in releases],
            **_selection_meta(releases),
        }
    )
    return payload


def _load_formal_releases(repo: Any, args: argparse.Namespace) -> list[ReleaseItem]:
    releases = fetch_releases(repo)
    formal = filter_formal_releases(releases, include_prerelease=args.include_prerelease)
    return apply_limit(formal, default_limit(args.mode, args.limit))


def _prepare_manual(args: argparse.Namespace, repo: Any, formal: list[ReleaseItem]) -> dict[str, Any]:
    selected = select_manual_latest(formal) if default_latest_only(args.mode, args.latest_only) else formal
    if not selected:
        return _prepare_result(args, repo.slug, "no_release", "no formal releases after filtering", [])
    return _prepare_result(args, repo.slug, "has_updates", "manual latest formal release selected", selected)


def _prepare_cron(args: argparse.Namespace, repo: Any, formal: list[ReleaseItem]) -> dict[str, Any]:
    state, state_path, is_first_run = load_state(repo, args.state_key)
    state.last_checked_at = now_iso()
    state_key = args.state_key or repo.state_key
    path_text = str(state_path)

    if not formal:
        save_state(state_path, state)
        return _prepare_result(
            args,
            repo.slug,
            "no_release",
            "no formal releases after filtering",
            [],
            state_key=state_key,
            state_path=path_text,
            first_run=is_first_run,
        )

    if not is_first_run and has_fast_no_update(formal, state):
        save_state(state_path, state)
        return _prepare_result(
            args,
            repo.slug,
            "no_update",
            "latest formal release already matches committed state",
            [],
            state_key=state_key,
            state_path=path_text,
            first_run=False,
        )

    pending = pending_for_cron(formal, state, is_first_run=is_first_run, initial_cron_behavior=args.initial_cron_behavior)
    if not pending:
        save_state(state_path, state)
        return _prepare_result(
            args,
            repo.slug,
            "no_update",
            "no unprocessed formal releases selected",
            [],
            state_key=state_key,
            state_path=path_text,
            first_run=is_first_run,
        )

    save_state(state_path, state)
    return _prepare_result(
        args,
        repo.slug,
        "has_updates",
        "first-run latest-only selection" if is_first_run else "unprocessed formal releases selected",
        pending,
        state_key=state_key,
        state_path=path_text,
        first_run=is_first_run,
    )


def prepare(args: argparse.Namespace) -> dict[str, Any]:
    repo = parse_repo(args.repo)
    formal = _load_formal_releases(repo, args)
    if args.mode == "manual":
        return _prepare_manual(args, repo, formal)
    return _prepare_cron(args, repo, formal)


def _release_from_dict(item: dict[str, Any]) -> ReleaseItem:
    tag_name = item.get("tag_name") or ""
    html_url = item.get("html_url") or ""
    published_at = item.get("published_at")
    if not isinstance(tag_name, str) or not tag_name.strip():
        raise ValueError("each release must include a non-empty tag_name")
    if not isinstance(html_url, str) or not html_url.strip():
        raise ValueError("each release must include a non-empty html_url")
    if not isinstance(published_at, str) or not published_at.strip():
        raise ValueError("each release must include a non-empty published_at; preserve releases from prepare output unchanged")
    return ReleaseItem(
        tag_name=tag_name.strip(),
        name=item.get("name"),
        published_at=published_at.strip(),
        html_url=html_url.strip(),
        body=item.get("body") or "",
        draft=bool(item.get("draft")),
        prerelease=bool(item.get("prerelease")),
        release_id=item.get("release_id"),
    )


def _summary_from_any(item: Any) -> ReleaseSummary:
    if not isinstance(item, str) or not item.strip():
        raise ValueError("each summary must be a non-empty markdown string")
    return ReleaseSummary(markdown=item.strip())


def render(args: argparse.Namespace) -> dict[str, Any]:
    repo = parse_repo(args.repo)
    payload = json.loads(sys.stdin.read() or "{}")
    releases_raw = payload.get("releases") or []
    summaries_raw = payload.get("summaries") or []
    output_template = payload.get("outputTemplate") or args.output_template
    language = payload.get("language") or payload.get("outputLanguage") or "zh"
    if not isinstance(releases_raw, list) or not isinstance(summaries_raw, list):
        raise ValueError("render payload must contain list fields: releases and summaries")
    releases = [_release_from_dict(item) for item in releases_raw]
    summaries = [_summary_from_any(item) for item in summaries_raw]
    message = render_message(
        repo=repo,
        releases=releases,
        summaries=summaries,
        output_template=output_template,
        language=language,
    )
    return {
        "status": "rendered",
        "mode": args.mode,
        "repo": repo.slug,
        "outputTemplate": output_template,
        "language": language,
        "message": message,
        "releaseCount": len(releases),
        "renderedTags": [item.tag_name for item in releases if item.tag_name],
    }


def commit(args: argparse.Namespace) -> dict[str, Any]:
    repo = parse_repo(args.repo)
    state, state_path, _ = load_state(repo, args.state_key)
    tags = [tag.strip() for tag in args.processed_tags.split(",") if tag.strip()]
    for tag in tags:
        if tag not in state.processed_tags:
            state.processed_tags.append(tag)
    state.latest_processed_release_id = args.latest_release_id
    state.latest_processed_published_at = args.latest_published_at
    timestamp = now_iso()
    state.last_success_at = timestamp
    state.last_checked_at = timestamp
    if not state.initialized_at:
        state.initialized_at = timestamp
    save_state(state_path, state)
    return {
        "status": "committed",
        "repo": repo.slug,
        "stateKey": args.state_key or repo.state_key,
        "statePath": str(state_path),
        "processedTags": state.processed_tags,
        "latestProcessedReleaseId": state.latest_processed_release_id,
        "latestProcessedPublishedAt": state.latest_processed_published_at,
        "committedAt": timestamp,
    }


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == "prepare":
            payload = prepare(args)
        elif args.command == "render":
            payload = render(args)
        else:
            payload = commit(args)
    except (RepoParseError, ReleaseFetchError, TemplateError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=False))
        return 1

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
