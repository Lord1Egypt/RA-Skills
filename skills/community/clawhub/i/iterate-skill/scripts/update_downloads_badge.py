#!/usr/bin/env python3
"""Fetch cross-platform download counts and write badges/downloads.json.

Aggregates the all-time download counts of the skill from three sources:

* ClawHub     -- https://clawhub.ai/api/skill?slug=iterate-skill
* SkillHub    -- https://api.skillhub.tencent.com/api/v1/skills/iterate-skill
* npm         -- https://api.npmjs.org/downloads/point/<range>/iterate-skill-installer

The resulting `badges/downloads.json` is consumed by the README "Downloads"
badge via shields.io's dynamic/json endpoint.

Only writes the file when a full set of three counts can be resolved. When an
upstream API is unavailable, the previously committed value is reused (with a
warning) so the badge never shows a misleading partial sum.
"""

from __future__ import annotations

import http.client
import json
import os
import ssl
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Protocol

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BADGES_FILE = os.path.join(REPO_ROOT, "badges", "downloads.json")

USER_AGENT = "iterate-skill-downloads-badge/1.0 (+https://github.com/jingzhao-l/iterate-skill)"
TIMEOUT_SECONDS = 20

# source -> (API url, JSON path to the all-time download count)
SOURCES = {
    "clawhub": (
        "https://clawhub.ai/api/skill?slug=iterate-skill",
        ("skill", "stats", "downloads"),
    ),
    "skillhub": (
        "https://api.skillhub.tencent.com/api/v1/skills/iterate-skill",
        ("skill", "stats", "downloads"),
    ),
    "npm": (
        "https://api.npmjs.org/downloads/point/2000-01-01:2100-01-01/iterate-skill-installer",
        ("downloads",),
    ),
}


def _nested_get(payload: object, path: tuple[str, ...]) -> object | None:
    """Walk a JSON payload along `path`, returning None when any step is missing."""
    current = payload
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def extract_count(source: str, payload: object) -> int | None:
    """Extract a non-negative int download count from a raw API payload."""
    if not isinstance(payload, dict):
        return None
    value = _nested_get(payload, SOURCES[source][1])
    if isinstance(value, bool) or not isinstance(value, int):
        return None
    return value if value >= 0 else None


# Referer header is required only by the Tencent SkillHub API; sending it to
# other hosts (ClawHub, npm) can trip their anti-abuse checks and bloat the
# request. It is therefore attached based on the request host, not globally.
#
# SkillHub exposes two distinct host families, both under ``*.tencent.com``:
#   * ``skillhub.tencent.com``          -- the API host (see SOURCES)
#   * ``skillhub.cloud.tencent.com``    -- the console / asset host
# Each is matched exactly as a host or as a ``.``-prefixed suffix of a sub-host.
_REFERER_HOSTS = (
    "skillhub.tencent.com",
    "skillhub.cloud.tencent.com",
)
_REFERER_HEADER = "https://skillhub.cloud.tencent.com/"

_MAX_RESPONSE_BYTES = 5 * 1024 * 1024  # 5 MiB cap on a JSON download-count payload


def _is_skillhub_url(url: str) -> bool:
    """Return True when a URL targets the Tencent SkillHub API.

    Matching is suffix-safe: only a bare host or a ``.``-prefixed sub-host of
    one of the recognised SkillHub hosts qualifies, so
    ``evilskillhub.tencent.com.evil.com`` (and similar lookalikes) is excluded.
    """
    try:
        host = urllib.parse.urlsplit(url).hostname or ""
    except ValueError:
        return False
    return any(
        host == known or host.endswith("." + known) for known in _REFERER_HOSTS
    )


class _FileLikeRead(Protocol):
    """Minimal readable-file protocol for bounded response reading.

    Matches the ``read(amt: int) -> bytes`` interface exposed by ``urllib`` /
    ``http.client`` response objects, so callers may pass any of them.
    """

    def read(self, amt: int = ...) -> bytes: ...


def _read_bounded(resp: _FileLikeRead) -> bytes:
    """Read a bounded-size response body to avoid unbounded memory use.

    ``resp`` must expose a ``read(amt: int) -> bytes``-style interface (any
    ``urllib``/``http.client`` response object). Reads repeatedly until EOF so
    a response that delivers less than the requested amount per ``read()``
    call is still fully capped (a single fixed-size read is not enough to
    enforce the limit). Raises ``ValueError`` when the payload exceeds the cap.
    """
    chunks: list[bytes] = []
    total = 0
    while True:
        if total > _MAX_RESPONSE_BYTES:
            raise ValueError(
                f"response body exceeds {_MAX_RESPONSE_BYTES} byte safety cap"
            )
        chunk = resp.read(min(_MAX_RESPONSE_BYTES + 1 - total, 1 << 16))
        if not chunk:
            break
        total += len(chunk)
        chunks.append(chunk)
    return b"".join(chunks)


def fetch_json(url: str) -> object:
    """GET a JSON endpoint, raising on any network/decode failure.

    Raises:
        OSError: ``urllib`` errors — connection refused, DNS, TLS, timeout.
        ValueError: malformed JSON in the body.
        http.client.HTTPException: HTTP framing problems
            (``IncompleteRead``, ``BadStatusLine``, ``LineTooLong``) when the
            server's response is truncated or garbled. Callers must catch this
            alongside the two above if they intend to fall back to the
            previously committed value — it is not an ``OSError``.
    """
    context = ssl.create_default_context()
    headers = {"User-Agent": USER_AGENT}
    if _is_skillhub_url(url):
        headers["Referer"] = _REFERER_HEADER
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS, context=context) as resp:
        return json.loads(_read_bounded(resp).decode("utf-8"))


def resolve_counts(
    fetched: dict[str, object], previous: dict[str, object] | None
) -> tuple[dict[str, int], list[str]]:
    """Resolve one count per source, falling back to the previous committed value.

    Returns (resolved, warnings). Raises ValueError when a source has neither a
    fresh value nor a usable previous value, so the caller keeps the old file.
    """
    resolved: dict[str, int] = {}
    warnings: list[str] = []
    for source in SOURCES:
        value = extract_count(source, fetched.get(source))
        if value is None:
            prev = previous.get(source) if previous else None
            if isinstance(prev, int) and not isinstance(prev, bool) and prev >= 0:
                value = prev
                warnings.append(
                    f"{source}: upstream unavailable/invalid, reused previous value {prev}"
                )
            else:
                warnings.append(
                    f"{source}: no value available (upstream down and no previous)"
                )
                resolved[source] = -1
                continue
        resolved[source] = value
    missing = [name for name, count in resolved.items() if count < 0]
    if missing:
        raise ValueError(
            "cannot resolve download counts for: " + ", ".join(missing)
        )
    return resolved, warnings


def build_output(resolved: dict[str, int], warnings: list[str]) -> dict[str, object]:
    """Build the JSON document consumed by the README badge."""
    output: dict[str, object] = dict(resolved)
    output["total"] = sum(resolved.values())
    output["updatedAt"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    if warnings:
        output["warnings"] = warnings
    return output


def read_previous(path: str) -> dict[str, object]:
    """Read the previously committed JSON, tolerating a missing/corrupt file."""
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def write_output(path: str, data: dict[str, object]) -> None:
    """Write the JSON atomically so a crash never leaves a truncated file."""
    tmp_path = path + ".tmp"
    try:
        with open(tmp_path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(tmp_path, path)
    except BaseException:
        # Never leave a partial temp file behind on failure.
        try:
            os.remove(tmp_path)
        except OSError:
            pass
        raise


def main() -> int:
    previous = read_previous(BADGES_FILE)
    fetched: dict[str, object] = {}
    for source, (url, _) in SOURCES.items():
        try:
            fetched[source] = fetch_json(url)
        # http.client.HTTPException (IncompleteRead, BadStatusLine, LineTooLong)
        # is neither OSError nor ValueError: a truncated or garbled response
        # escaped this guard as a raw traceback and killed the whole run,
        # forfeiting the very fallback below. The point of catching here is to
        # keep the last good badge instead.
        except (OSError, ValueError, http.client.HTTPException) as exc:
            print(f"warning: {source} fetch failed: {exc}")
            fetched[source] = None

    try:
        resolved, warnings = resolve_counts(fetched, previous)
    except ValueError as exc:
        # A source has neither a fresh value nor a usable previous value, so
        # writing a partial sum would mislead the badge. Keep the last good
        # file and signal failure to the caller (e.g. the hourly workflow).
        print(f"error: {exc}; keeping previously committed {BADGES_FILE}")
        return 1
    output = build_output(resolved, warnings)
    write_output(BADGES_FILE, output)
    for warning in warnings:
        print("warning: " + warning)
    print(
        "wrote " + BADGES_FILE + ": " + json.dumps(output, ensure_ascii=False)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
