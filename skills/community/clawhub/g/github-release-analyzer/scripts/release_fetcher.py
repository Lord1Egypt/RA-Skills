from __future__ import annotations

import json
import urllib.error
import urllib.request

from models import ReleaseItem, RepoSpec, StateData


class ReleaseFetchError(RuntimeError):
    pass


def fetch_releases(repo: RepoSpec, timeout: int = 20) -> list[ReleaseItem]:
    request = urllib.request.Request(
        repo.api_url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "openclaw-github-release-analyzer/1.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="ignore")
        raise ReleaseFetchError(f"GitHub API HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise ReleaseFetchError(f"GitHub API request failed: {exc.reason}") from exc

    if not isinstance(payload, list):
        raise ReleaseFetchError("GitHub API did not return a release array")

    items: list[ReleaseItem] = []
    for item in payload:
        items.append(
            ReleaseItem(
                tag_name=item.get("tag_name") or "",
                name=item.get("name"),
                published_at=item.get("published_at"),
                html_url=item.get("html_url") or "",
                body=item.get("body") or "",
                draft=bool(item.get("draft")),
                prerelease=bool(item.get("prerelease")),
                release_id=item.get("id"),
            )
        )
    return items


def filter_formal_releases(releases: list[ReleaseItem], include_prerelease: bool = False) -> list[ReleaseItem]:
    return [
        release
        for release in releases
        if not release.draft and (include_prerelease or not release.prerelease)
    ]


def apply_limit(releases: list[ReleaseItem], limit: int) -> list[ReleaseItem]:
    return releases[: max(limit, 0)]


def select_manual_latest(releases: list[ReleaseItem]) -> list[ReleaseItem]:
    return releases[:1]


def has_fast_no_update(releases: list[ReleaseItem], state: StateData) -> bool:
    if not releases:
        return False
    latest = releases[0]
    if state.latest_processed_release_id and latest.release_id == state.latest_processed_release_id:
        return True
    if state.latest_processed_published_at and latest.published_at and latest.published_at <= state.latest_processed_published_at:
        return True
    return False


def pending_for_cron(
    releases: list[ReleaseItem],
    state: StateData,
    is_first_run: bool,
    initial_cron_behavior: str = "latest-only",
) -> list[ReleaseItem]:
    if not releases:
        return []
    if is_first_run and initial_cron_behavior == "latest-only":
        return releases[:1]

    # 先用 latest_processed_published_at 做时间切分，再用 processed_tags 去重兜底
    cutoff = state.latest_processed_published_at
    processed = set(state.processed_tags)

    pending: list[ReleaseItem] = []
    for release in releases:
        if release.tag_name and release.tag_name in processed:
            continue
        if cutoff and release.published_at and release.published_at <= cutoff:
            continue
        pending.append(release)

    pending.sort(key=lambda item: item.published_at or "")
    return pending
