from __future__ import annotations

from urllib.parse import urlparse

from models import RepoSpec


class RepoParseError(ValueError):
    pass


ALLOWED_HOSTS = {"github.com", "www.github.com"}


def parse_repo(value: str) -> RepoSpec:
    raw = (value or "").strip()
    if not raw:
        raise RepoParseError("repo is required")

    if raw.startswith("http://") or raw.startswith("https://"):
        return _parse_repo_url(raw)

    return _parse_repo_slug(raw)


def _parse_repo_slug(value: str) -> RepoSpec:
    cleaned = value.strip().strip("/")
    parts = [p for p in cleaned.split("/") if p]
    if len(parts) != 2:
        raise RepoParseError(f"invalid repo slug: {value}")
    owner, repo = parts
    return RepoSpec(owner=owner, repo=repo)


def _parse_repo_url(value: str) -> RepoSpec:
    parsed = urlparse(value)
    if parsed.netloc not in ALLOWED_HOSTS:
        raise RepoParseError(f"unsupported repo host: {parsed.netloc}")

    parts = [p for p in parsed.path.split("/") if p]
    if len(parts) < 2:
        raise RepoParseError(f"invalid repo url: {value}")

    owner, repo = parts[0], parts[1]
    return RepoSpec(owner=owner, repo=repo)
