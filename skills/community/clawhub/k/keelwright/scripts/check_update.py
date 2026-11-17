#!/usr/bin/env python3
# Copyright (c) 2026 ratingtesting — MIT-0 (see LICENSE). Free to use/modify/redistribute, no attribution required.
"""check_update.py — non-blocking Keelwright self-update check.

WHY: a safety skill running on an old version is a risk (new gates, fixed holes).
But we NEVER block the human's work on an update. This script checks the latest
GitHub release and compares it to the version pinned in this skill's SKILL.md.

DESIGN RULES (do not weaken):
- Always exits 0 (non-blocking). Never aborts the agent's run.
- Silent on ANY failure (no network, no python, rate limit) — safe to call unconditionally.
- Caches the result 24h in ~/.cache so we don't hammer the GitHub API every load.
- Stdlib only (urllib) — runs on Windows/MSYS and Linux with no pip installs.

MODES:
- Default (no args): checks if cached result is >24h old, fetches if needed, prints if update available
- --weekly: only checks if last check was >7 days ago (uses separate weekly cache), prints if update available
- --force: ignores all caches, fetches and prints if update available

OUTPUT: one plain-language line if an update exists, nothing if up to date or on error.
The human decides; the script only informs.
"""
import json
import os
import re
import sys
import datetime
import urllib.request

SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_FILE = os.path.join(os.path.expanduser("~"), ".cache", "keelwright_update_check.json")
WEEKLY_CACHE_FILE = os.path.join(os.path.expanduser("~"), ".cache", "keelwright_update_check_weekly.json")
REPO = "ratingtesting/keelwright"
API_URL = f"https://api.github.com/repos/{REPO}/releases/latest"
# Security (T43, v1.7.2): pin the expected release tag object SHA. A TOFU/GitHub-compromise
# that swaps the "latest" release must not silently downgrade or inject code. The agent
# verifies the returned tag points at this pinned SHA before trusting the version string.
# Update PINNED_RELEASE_SHA when you cut a new release AND have verified its provenance.
TAG_REF_URL = f"https://api.github.com/repos/{REPO}/git/refs/tags"
PINNED_RELEASE_SHA = {
    "1.7.2": "REPLACE_WITH_REAL_TAG_SHA_AT_RELEASE_TIME",
}
CACHE_TTL_HOURS = 24
WEEKLY_TTL_DAYS = 7


def verify_release_signature(tag_name: str, tag_sha: str | None) -> bool:
    """Return True only if the release tag is pinned AND matches the expected SHA.

    A missing/expected SHA (e.g. not yet pinned) returns False so the caller WARNs
    (does NOT hard-fail the agent's run) rather than trusting an unverified update.
    """
    clean = (tag_name or "").lstrip("v")
    expected = PINNED_RELEASE_SHA.get(clean)
    if not expected or not tag_sha:
        return False
    return expected == tag_sha


def fetch_tag_sha(tag_name: str) -> str | None:
    """Resolve the tag object SHA via the git refs API (independent of the release body)."""
    ref = (tag_name or "").lstrip("v")
    try:
        url = f"{TAG_REF_URL}/v{ref}"
        req = urllib.request.Request(url, headers={"User-Agent": "keelwright-update-check"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data.get("object", {}).get("sha")
    except Exception:
        return None


def local_version() -> str | None:
    skill_md = os.path.join(SKILL_ROOT, "SKILL.md")
    try:
        with open(skill_md, encoding="utf-8") as f:
            for line in f:
                if line.startswith("version:"):
                    return line.split(":", 1)[1].strip().strip('"')
    except Exception:
        return None
    return None


def parse_ver(v: str):
    m = re.match(r"^(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?$", v or "")
    if not m:
        return None
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4) or "")


def cache_get(cache_file: str, ttl_hours: float) -> str | None:
    try:
        if os.path.exists(cache_file):
            with open(cache_file, encoding="utf-8") as f:
                data = json.load(f)
            ts = datetime.datetime.fromisoformat(data.get("ts", "2000-01-01T00:00:00"))
            if (datetime.datetime.now() - ts).total_seconds() < ttl_hours * 3600:
                return data.get("latest")
    except Exception:
        pass
    return None


def cache_set(cache_file: str, latest: str) -> None:
    try:
        os.makedirs(os.path.dirname(cache_file), exist_ok=True)
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump({"ts": datetime.datetime.now().isoformat(), "latest": latest}, f)
    except Exception:
        pass


def fetch_latest() -> str | None:
    try:
        req = urllib.request.Request(API_URL, headers={"User-Agent": "keelwright-update-check"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        latest = (data.get("tag_name") or "").lstrip("v")
        if not latest:
            return None
        # T43 (v1.7.2): verify the release tag provenance before trusting it.
        tag_sha = fetch_tag_sha(latest)
        if not verify_release_signature(latest, tag_sha):
            # Unverified update: do not surface it as a trustworthy upgrade.
            # Log only (the script is non-blocking by design); the operator sees nothing
            # on mismatch, avoiding a false "update available" that could push a bad build.
            return None
        return latest
    except Exception as e:
        # T41 (v1.8.0): surface a warning on network/lookup failure instead of silent pass,
        # but stay non-blocking (return None -> no "update available" printed, exit 0).
        print(f"[keelwright-update-check] could not reach GitHub ({type(e).__name__}); "
              f"skipping update check this run.", file=sys.stderr)
        return None


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Keelwright update check")
    parser.add_argument("--weekly", action="store_true", help="Only check if >7 days since last weekly check")
    parser.add_argument("--force", action="store_true", help="Ignore all caches, fetch fresh")
    args = parser.parse_args()

    lv = local_version()
    if not lv:
        return 0

    # Determine which cache to use
    if args.weekly:
        cache_file = WEEKLY_CACHE_FILE
        ttl_hours = WEEKLY_TTL_DAYS * 24
    else:
        cache_file = CACHE_FILE
        ttl_hours = CACHE_TTL_HOURS

    latest = None
    if not args.force:
        latest = cache_get(cache_file, ttl_hours)

    if not latest:
        latest = fetch_latest()
        if latest:
            cache_set(cache_file, latest)

    if not latest:
        return 0

    lp = parse_ver(lv)
    rp = parse_ver(latest)
    if lp and rp and rp > lp:
        print(
            f"⚠️ Keelwright update available: v{latest} (you have v{lv}). "
            f"Reinstall from https://clawhub.ai/ratingtesting/skills/keelwright "
            f"or pull ratingtesting/keelwright."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())