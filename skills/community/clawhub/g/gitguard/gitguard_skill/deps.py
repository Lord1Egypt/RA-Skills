"""
Dependency freshness checker.

Parses package.json (npm) and requirements.txt (pip) to extract pinned
versions, then queries the public registries for the latest release.
Network calls are best-effort: if there is no connectivity, versions_behind
stays None and is_stale is left False rather than raising -- this keeps
the health scan usable fully offline.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from .models import DependencyStatus

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


def _parse_semver(v: str) -> tuple[int, ...]:
    v = v.lstrip("^~=v")
    parts = re.findall(r"\d+", v)
    return tuple(int(p) for p in parts[:3]) if parts else (0,)


def _versions_behind(current: str, latest: str) -> int:
    c, l = _parse_semver(current), _parse_semver(latest)
    # pad to equal length
    length = max(len(c), len(l))
    c = c + (0,) * (length - len(c))
    l = l + (0,) * (length - len(l))
    if c >= l:
        return 0
    # crude "distance" proxy: difference in major*10000+minor*100+patch
    def score(t):
        s = 0
        for i, x in enumerate(t):
            s += x * (100 ** (length - i - 1))
        return s
    diff = score(l) - score(c)
    return max(1, min(diff, 999))  # clamp for sanity


def parse_package_json(path: Path) -> dict[str, str]:
    try:
        data = json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return {}
    deps = {}
    for key in ("dependencies", "devDependencies"):
        deps.update(data.get(key, {}) or {})
    return deps


def parse_requirements_txt(path: Path) -> dict[str, str]:
    deps: dict[str, str] = {}
    try:
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("-"):
                continue
            m = re.match(r"^([A-Za-z0-9_.\-]+)\s*==\s*([\w.\-]+)", line)
            if m:
                deps[m.group(1)] = m.group(2)
    except OSError:
        pass
    return deps


def _fetch_latest_npm(name: str, timeout: float = 4.0) -> str | None:
    if not HAS_REQUESTS:
        return None
    try:
        r = requests.get(f"https://registry.npmjs.org/{name}/latest", timeout=timeout)
        if r.status_code == 200:
            return r.json().get("version")
    except requests.RequestException:
        pass
    return None


def _fetch_latest_pypi(name: str, timeout: float = 4.0) -> str | None:
    if not HAS_REQUESTS:
        return None
    try:
        r = requests.get(f"https://pypi.org/pypi/{name}/json", timeout=timeout)
        if r.status_code == 200:
            return r.json().get("info", {}).get("version")
    except requests.RequestException:
        pass
    return None


def check_dependencies(repo_path: str, staleness_threshold: int = 5,
                        max_checks: int = 40) -> list[DependencyStatus]:
    """Scan package.json / requirements.txt and report stale dependencies.

    staleness_threshold: a dependency is flagged stale if it is behind by
    this many "version points" (see _versions_behind) -- a lightweight
    proxy for "several releases old", not a precise semver distance.
    """
    root = Path(repo_path)
    results: list[DependencyStatus] = []
    checked = 0

    npm_file = root / "package.json"
    if npm_file.exists():
        for name, current in parse_package_json(npm_file).items():
            if checked >= max_checks:
                break
            checked += 1
            latest = _fetch_latest_npm(name)
            behind = _versions_behind(current, latest) if latest else None
            results.append(DependencyStatus(
                name=name, current_version=current, latest_version=latest,
                versions_behind=behind, ecosystem="npm",
                is_stale=bool(behind and behind >= staleness_threshold),
            ))

    req_file = root / "requirements.txt"
    if req_file.exists():
        for name, current in parse_requirements_txt(req_file).items():
            if checked >= max_checks:
                break
            checked += 1
            latest = _fetch_latest_pypi(name)
            behind = _versions_behind(current, latest) if latest else None
            results.append(DependencyStatus(
                name=name, current_version=current, latest_version=latest,
                versions_behind=behind, ecosystem="pypi",
                is_stale=bool(behind and behind >= staleness_threshold),
            ))

    return results
