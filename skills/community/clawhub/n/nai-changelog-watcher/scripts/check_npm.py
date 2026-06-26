#!/usr/bin/env python3
"""
check_npm.py - Fetch version info for an npm package via the registry.

Usage:
    python3 check_npm.py <package-name>

Output: JSON object with latest version, all versions list, and dist-tags.
Exits with code 1 on error.
"""

import json
import sys
import urllib.request
import urllib.error


def fetch_package(package: str) -> dict:
    # Encode scoped packages (e.g. @org/pkg -> %40org%2Fpkg)
    encoded = urllib.request.quote(package, safe="")
    url = f"https://registry.npmjs.org/{encoded}"

    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "changelog-watcher/1.0",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(
                json.dumps({"error": "not_found", "message": f"Package '{package}' not found on npm."}),
                file=sys.stderr,
            )
            sys.exit(3)
        elif e.code == 429:
            retry_after = e.headers.get("Retry-After", "60")
            print(
                json.dumps({
                    "error": "rate_limited",
                    "message": f"npm registry rate limit hit. Retry after {retry_after}s.",
                    "retry_after": int(retry_after),
                }),
                file=sys.stderr,
            )
            sys.exit(2)
        else:
            print(
                json.dumps({"error": "http_error", "message": str(e)}),
                file=sys.stderr,
            )
            sys.exit(1)
    except urllib.error.URLError as e:
        print(
            json.dumps({"error": "network_error", "message": str(e.reason)}),
            file=sys.stderr,
        )
        sys.exit(1)

    dist_tags = raw.get("dist-tags", {})
    latest = dist_tags.get("latest", "")
    versions_map = raw.get("versions", {})

    # Collect changelogs/release notes from version objects if present
    releases = []
    latest_info = versions_map.get(latest, {})

    # Build recent version list (last 20 published)
    times = raw.get("time", {})
    # Filter to actual version entries (exclude 'created'/'modified' keys)
    version_times = {
        k: v for k, v in times.items()
        if k not in ("created", "modified") and k in versions_map
    }
    # Sort by publish date descending
    sorted_versions = sorted(version_times.items(), key=lambda x: x[1], reverse=True)[:20]

    releases = []
    for version, published_at in sorted_versions:
        v_data = versions_map.get(version, {})
        releases.append({
            "source": "npm",
            "package": package,
            "tag": version,
            "published_at": published_at,
            "description": v_data.get("description", ""),
            "url": f"https://www.npmjs.com/package/{package}/v/{version}",
        })

    result = {
        "source": "npm",
        "package": package,
        "latest": latest,
        "dist_tags": dist_tags,
        "description": raw.get("description", ""),
        "homepage": raw.get("homepage", ""),
        "repository": raw.get("repository", {}).get("url", "") if isinstance(raw.get("repository"), dict) else "",
        "recent_versions": releases,
    }

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: check_npm.py <package-name>", file=sys.stderr)
        sys.exit(1)

    package = sys.argv[1]
    result = fetch_package(package)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
