#!/usr/bin/env python3
"""Priority Coach release/download monitor.

Track two things for the maintainer:
1) what changed in each iteration
2) whether downloads increased after an iteration

Default data dir: <project>/.monitoring/
The script does not require git history. It stores its own code snapshots and
computes diffs against the previous snapshot.
"""

from __future__ import annotations

import argparse
import datetime as dt
import difflib
import hashlib
import html
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MONITOR_HOME = PROJECT_ROOT / ".monitoring"
ITERATIONS_FILE = "iterations.json"
DOWNLOADS_FILE = "downloads.json"
SNAPSHOT_DIR = "snapshots"
REPORTS_DIR = "reports"
SCHEMA_VERSION = 1
MAX_TEXT_FILE_BYTES = 512 * 1024
IGNORED_DIR_NAMES = {
    ".git",
    ".monitoring",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
}
IGNORED_FILE_NAMES = {
    ".DS_Store",
}
VERSION_PATTERN = re.compile(r"^version:\s*([^\s]+)\s*$", re.MULTILINE)
HOMEPAGE_PATTERN = re.compile(r"^homepage:\s*(\S+)\s*$", re.MULTILINE)
DOWNLOAD_PATTERNS = [
    re.compile(r'"downloads"\s*:\s*(\d[\d,]*(?:\.\d+)?)', re.IGNORECASE),
    re.compile(r'"downloadCount"\s*:\s*(\d[\d,]*(?:\.\d+)?)', re.IGNORECASE),
    re.compile(r'downloads?\s*[:：]?\s*(\d[\d,]*(?:\.\d+)?[kKmM]?)', re.IGNORECASE),
    re.compile(r'(\d[\d,]*(?:\.\d+)?[kKmM]?)\s*downloads?', re.IGNORECASE),
]


def now_iso() -> str:
    return dt.datetime.now().isoformat(timespec="microseconds")


def normalize_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


class MonitorPaths:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.iterations = base_dir / ITERATIONS_FILE
        self.downloads = base_dir / DOWNLOADS_FILE
        self.snapshots = base_dir / SNAPSHOT_DIR
        self.reports = base_dir / REPORTS_DIR


class MonitorError(RuntimeError):
    pass


def resolve_monitor_home(raw: str | None) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()
    env_value = os.environ.get("PRIORITY_COACH_MONITOR_HOME")
    if env_value:
        return Path(env_value).expanduser().resolve()
    return DEFAULT_MONITOR_HOME.resolve()


def monitor_paths(args: argparse.Namespace) -> MonitorPaths:
    return MonitorPaths(resolve_monitor_home(args.store_dir))


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, data: dict[str, Any]) -> None:
    ensure_parent(path)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def write_text(path: Path, text: str) -> None:
    ensure_parent(path)
    path.write_text(text, encoding="utf-8")


def run_git(project_root: Path, args: list[str]) -> bytes:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=project_root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError as exc:
        raise MonitorError("未找到 git 命令") from exc
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.decode("utf-8", errors="replace").strip()
        command = " ".join(["git", *args])
        raise MonitorError(f"git 命令失败: {command}\n{stderr}") from exc
    return completed.stdout


def empty_iterations_store() -> dict[str, Any]:
    return {"schemaVersion": SCHEMA_VERSION, "iterations": []}


def empty_downloads_store() -> dict[str, Any]:
    return {"schemaVersion": SCHEMA_VERSION, "downloads": []}


def load_json_store(path: Path, fallback: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return fallback
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return fallback
    if not isinstance(data, dict):
        return fallback
    data["schemaVersion"] = SCHEMA_VERSION
    return data


def load_iterations_store(paths: MonitorPaths) -> dict[str, Any]:
    data = load_json_store(paths.iterations, empty_iterations_store())
    if not isinstance(data.get("iterations"), list):
        data["iterations"] = []
    return data


def load_downloads_store(paths: MonitorPaths) -> dict[str, Any]:
    data = load_json_store(paths.downloads, empty_downloads_store())
    if not isinstance(data.get("downloads"), list):
        data["downloads"] = []
    return data


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def iter_project_text_files(project_root: Path):
    for path in sorted(project_root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(project_root)
        if any(part in IGNORED_DIR_NAMES for part in rel.parts):
            continue
        if path.name in IGNORED_FILE_NAMES:
            continue
        try:
            size = path.stat().st_size
        except OSError:
            continue
        if size > MAX_TEXT_FILE_BYTES:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        yield rel.as_posix(), content, size


def iter_git_ref_text_files(project_root: Path, git_ref: str):
    raw = run_git(project_root, ["ls-tree", "-r", "-z", "--name-only", git_ref])
    for rel_raw in raw.split(b"\x00"):
        if not rel_raw:
            continue
        rel_path = rel_raw.decode("utf-8", errors="replace")
        rel = Path(rel_path)
        if any(part in IGNORED_DIR_NAMES for part in rel.parts):
            continue
        if rel.name in IGNORED_FILE_NAMES:
            continue

        blob = run_git(project_root, ["show", f"{git_ref}:{rel_path}"])
        if len(blob) > MAX_TEXT_FILE_BYTES:
            continue
        try:
            content = blob.decode("utf-8")
        except UnicodeDecodeError:
            continue
        yield rel_path, content, len(blob)


def git_resolve_ref(project_root: Path, git_ref: str) -> str:
    return run_git(project_root, ["rev-parse", git_ref]).decode("utf-8", errors="replace").strip()


def build_snapshot(project_root: Path, *, git_ref: str = "") -> dict[str, Any]:
    files: dict[str, Any] = {}
    if git_ref:
        iterator = iter_git_ref_text_files(project_root, git_ref)
        source = "git-ref"
    else:
        iterator = iter_project_text_files(project_root)
        source = "worktree"

    for rel_path, content, size in iterator:
        files[rel_path] = {
            "sha256": sha256_text(content),
            "bytes": size,
            "content": content,
        }
    return {
        "schemaVersion": SCHEMA_VERSION,
        "projectRoot": str(project_root),
        "createdAt": now_iso(),
        "source": source,
        "gitRef": git_ref,
        "files": files,
    }


def load_snapshot(paths: MonitorPaths, snapshot_id: str) -> dict[str, Any] | None:
    target = paths.snapshots / f"{snapshot_id}.json"
    if not target.exists():
        return None
    try:
        with target.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    files = data.get("files")
    if not isinstance(files, dict):
        return None
    return data


def save_snapshot(paths: MonitorPaths, snapshot_id: str, snapshot: dict[str, Any]) -> Path:
    target = paths.snapshots / f"{snapshot_id}.json"
    write_json(target, snapshot)
    return target


def diff_line_counts(before: str, after: str) -> tuple[int, int]:
    before_lines = before.splitlines()
    after_lines = after.splitlines()
    matcher = difflib.SequenceMatcher(a=before_lines, b=after_lines)
    added = 0
    removed = 0
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "insert":
            added += j2 - j1
        elif tag == "delete":
            removed += i2 - i1
        elif tag == "replace":
            removed += i2 - i1
            added += j2 - j1
    return added, removed


def diff_excerpt(before: str, after: str, *, limit: int = 6) -> list[str]:
    excerpt: list[str] = []
    for line in difflib.unified_diff(
        before.splitlines(),
        after.splitlines(),
        fromfile="before",
        tofile="after",
        lineterm="",
    ):
        if line.startswith(("---", "+++", "@@")):
            continue
        if line.startswith(("+", "-")):
            excerpt.append(line)
        if len(excerpt) >= limit:
            break
    return excerpt


def compare_snapshots(previous: dict[str, Any] | None, current: dict[str, Any]) -> list[dict[str, Any]]:
    previous_files = previous.get("files", {}) if isinstance(previous, dict) else {}
    current_files = current.get("files", {}) if isinstance(current, dict) else {}

    all_paths = sorted(set(previous_files) | set(current_files))
    changes: list[dict[str, Any]] = []

    for rel_path in all_paths:
        before_entry = previous_files.get(rel_path)
        after_entry = current_files.get(rel_path)

        if before_entry is None and after_entry is not None:
            after_content = normalize_string(after_entry.get("content"))
            changes.append(
                {
                    "path": rel_path,
                    "status": "added",
                    "addedLines": len(after_content.splitlines()),
                    "removedLines": 0,
                    "beforeHash": "",
                    "afterHash": normalize_string(after_entry.get("sha256")),
                    "excerpt": diff_excerpt("", after_content),
                }
            )
            continue

        if before_entry is not None and after_entry is None:
            before_content = normalize_string(before_entry.get("content"))
            changes.append(
                {
                    "path": rel_path,
                    "status": "removed",
                    "addedLines": 0,
                    "removedLines": len(before_content.splitlines()),
                    "beforeHash": normalize_string(before_entry.get("sha256")),
                    "afterHash": "",
                    "excerpt": diff_excerpt(before_content, ""),
                }
            )
            continue

        before_hash = normalize_string(before_entry.get("sha256"))
        after_hash = normalize_string(after_entry.get("sha256"))
        if before_hash == after_hash:
            continue

        before_content = normalize_string(before_entry.get("content"))
        after_content = normalize_string(after_entry.get("content"))
        added, removed = diff_line_counts(before_content, after_content)
        changes.append(
            {
                "path": rel_path,
                "status": "modified",
                "addedLines": added,
                "removedLines": removed,
                "beforeHash": before_hash,
                "afterHash": after_hash,
                "excerpt": diff_excerpt(before_content, after_content),
            }
        )

    return changes


def detect_skill_metadata(project_root: Path) -> dict[str, str]:
    meta_version = ""
    skill_version = ""
    homepage = ""

    meta_path = project_root / "_meta.json"
    if meta_path.exists():
        try:
            with meta_path.open("r", encoding="utf-8") as f:
                meta_data = json.load(f)
            if isinstance(meta_data, dict):
                meta_version = normalize_string(meta_data.get("version"))
        except Exception:
            meta_version = ""

    skill_path = project_root / "SKILL.md"
    if skill_path.exists():
        try:
            text = skill_path.read_text(encoding="utf-8")
        except Exception:
            text = ""
        version_match = VERSION_PATTERN.search(text)
        if version_match:
            skill_version = normalize_string(version_match.group(1))
        homepage_match = HOMEPAGE_PATTERN.search(text)
        if homepage_match:
            homepage = normalize_string(homepage_match.group(1))

    version = meta_version or skill_version
    return {
        "version": version,
        "metaVersion": meta_version,
        "skillVersion": skill_version,
        "homepage": homepage,
    }


def make_iteration_id(version: str) -> str:
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    suffix = version or "no-version"
    safe_suffix = re.sub(r"[^0-9A-Za-z._-]+", "-", suffix)
    return f"{stamp}-{safe_suffix}"


def sort_by_captured_at(items: list[dict[str, Any]], *, reverse: bool = False) -> list[dict[str, Any]]:
    return sorted(items, key=lambda item: normalize_string(item.get("capturedAt")), reverse=reverse)


def parse_iso_datetime(raw: Any) -> dt.datetime | None:
    text = normalize_string(raw)
    if not text:
        return None
    try:
        return dt.datetime.fromisoformat(text)
    except ValueError:
        return None


def parse_anchor_date(raw: str | None) -> dt.date:
    text = normalize_string(raw)
    if not text:
        return dt.date.today()
    try:
        return dt.date.fromisoformat(text)
    except ValueError as exc:
        raise MonitorError(f"日期格式无效: {raw}，请使用 YYYY-MM-DD") from exc


def period_bounds(anchor_date: dt.date, days: int) -> tuple[dt.datetime, dt.datetime]:
    if days <= 0:
        raise MonitorError("days 必须大于 0")
    start_date = anchor_date - dt.timedelta(days=days - 1)
    end_date = anchor_date + dt.timedelta(days=1)
    return (
        dt.datetime.combine(start_date, dt.time.min),
        dt.datetime.combine(end_date, dt.time.min),
    )


def format_date(value: dt.date) -> str:
    return value.isoformat()


def format_period(start_at: dt.datetime, end_at: dt.datetime) -> str:
    end_inclusive = (end_at - dt.timedelta(days=1)).date()
    return f"{format_date(start_at.date())} ~ {format_date(end_inclusive)}"


def within_period(captured_at: Any, start_at: dt.datetime, end_at: dt.datetime) -> bool:
    ts = parse_iso_datetime(captured_at)
    if ts is None:
        return False
    return start_at <= ts < end_at


def first_download_after_or_at(
    downloads: list[dict[str, Any]],
    captured_at: str,
) -> dict[str, Any] | None:
    for item in sort_by_captured_at(downloads):
        ts = normalize_string(item.get("capturedAt"))
        if ts >= captured_at:
            return item
    return None


def parse_human_number(raw: str) -> int:
    text = normalize_string(raw).lower().replace(",", "")
    if not text:
        raise MonitorError("下载量不能为空")
    multiplier = 1
    if text.endswith("k"):
        multiplier = 1000
        text = text[:-1]
    elif text.endswith("m"):
        multiplier = 1000000
        text = text[:-1]
    try:
        value = float(text)
    except ValueError as exc:
        raise MonitorError(f"无法解析数字: {raw}") from exc
    return int(round(value * multiplier))


def format_number(value: int | None) -> str:
    if value is None:
        return "N/A"
    return f"{value:,}"


def fetch_text(url: str, timeout: float) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (PriorityCoachMonitor/1.0)",
            "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset, errors="replace")
    except URLError as exc:
        raise MonitorError(f"抓取失败: {exc}") from exc


def find_download_match(raw_text: str) -> tuple[int, str] | None:
    plain_text = html.unescape(re.sub(r"<[^>]+>", " ", raw_text))
    candidates = [raw_text, plain_text]
    for candidate in candidates:
        for pattern in DOWNLOAD_PATTERNS:
            match = pattern.search(candidate)
            if not match:
                continue
            raw_value = normalize_string(match.group(1))
            return parse_human_number(raw_value), raw_value
    return None


def append_download_snapshot(
    paths: MonitorPaths,
    *,
    downloads: int,
    source: str,
    url: str,
    raw_value: str,
    note: str,
    captured_at: str | None = None,
) -> dict[str, Any]:
    store = load_downloads_store(paths)
    entry = {
        "capturedAt": normalize_string(captured_at) or now_iso(),
        "downloads": downloads,
        "source": normalize_string(source) or "manual",
        "url": normalize_string(url),
        "rawValue": normalize_string(raw_value),
        "note": normalize_string(note),
    }
    store["downloads"].append(entry)
    store["downloads"] = sort_by_captured_at(store["downloads"])
    write_json(paths.downloads, store)
    return entry


def latest_download_before_or_at(
    downloads: list[dict[str, Any]],
    captured_at: str,
) -> dict[str, Any] | None:
    result = None
    for item in sort_by_captured_at(downloads):
        ts = normalize_string(item.get("capturedAt"))
        if ts <= captured_at:
            result = item
        else:
            break
    return result


def latest_download_after_or_at(
    downloads: list[dict[str, Any]],
    captured_at: str,
) -> dict[str, Any] | None:
    result = None
    for item in sort_by_captured_at(downloads):
        ts = normalize_string(item.get("capturedAt"))
        if ts >= captured_at:
            result = item
    return result


def download_delta_for_iteration(
    iteration: dict[str, Any],
    downloads: list[dict[str, Any]],
) -> dict[str, Any]:
    captured_at = normalize_string(iteration.get("capturedAt"))
    before = latest_download_before_or_at(downloads, captured_at)
    latest_after = latest_download_after_or_at(downloads, captured_at)

    baseline = before.get("downloads") if isinstance(before, dict) else None
    current = latest_after.get("downloads") if isinstance(latest_after, dict) else None
    delta = None
    if isinstance(baseline, int) and isinstance(current, int):
        delta = current - baseline

    return {
        "baseline": before,
        "latestAfter": latest_after,
        "delta": delta,
    }


def summarize_top_paths(
    iterations: list[dict[str, Any]],
    *,
    limit: int,
) -> list[dict[str, Any]]:
    path_map: dict[str, dict[str, Any]] = {}

    for record in iterations:
        for item in record.get("changedFiles", []) or []:
            path = normalize_string(item.get("path"))
            if not path:
                continue
            summary = path_map.setdefault(
                path,
                {
                    "path": path,
                    "count": 0,
                    "addedLines": 0,
                    "removedLines": 0,
                    "lastStatus": "",
                },
            )
            summary["count"] += 1
            summary["addedLines"] += int(item.get("addedLines", 0))
            summary["removedLines"] += int(item.get("removedLines", 0))
            summary["lastStatus"] = normalize_string(item.get("status"))

    ranked = sorted(
        path_map.values(),
        key=lambda item: (
            int(item.get("count", 0)),
            int(item.get("addedLines", 0)) + int(item.get("removedLines", 0)),
            normalize_string(item.get("path")),
        ),
        reverse=True,
    )
    return ranked[:limit]


def summarize_period(
    iterations: list[dict[str, Any]],
    downloads: list[dict[str, Any]],
    *,
    start_at: dt.datetime,
    end_at: dt.datetime,
    top_files_limit: int,
) -> dict[str, Any]:
    iterations_in_period = [
        record for record in sort_by_captured_at(iterations)
        if within_period(record.get("capturedAt"), start_at, end_at)
    ]
    download_snapshots = [
        item for item in sort_by_captured_at(downloads)
        if within_period(item.get("capturedAt"), start_at, end_at)
    ]

    changed_files_total = 0
    added_lines_total = 0
    removed_lines_total = 0
    notes: list[dict[str, str]] = []

    for record in iterations_in_period:
        totals = record.get("totals", {}) or {}
        changed_files_total += int(totals.get("changedFiles", 0))
        added_lines_total += int(totals.get("addedLines", 0))
        removed_lines_total += int(totals.get("removedLines", 0))
        note = normalize_string(record.get("note"))
        if note:
            notes.append(
                {
                    "capturedAt": normalize_string(record.get("capturedAt")),
                    "label": normalize_string(record.get("label")) or normalize_string(record.get("version")),
                    "note": note,
                }
            )

    period_start_iso = start_at.isoformat(timespec="microseconds")
    period_end_iso = (end_at - dt.timedelta(microseconds=1)).isoformat(timespec="microseconds")
    baseline = latest_download_before_or_at(downloads, period_start_iso)
    if baseline is None:
        baseline = first_download_after_or_at(downloads, period_start_iso)
    current = latest_download_before_or_at(downloads, period_end_iso)
    if current is None and download_snapshots:
        current = download_snapshots[-1]

    baseline_value = baseline.get("downloads") if isinstance(baseline, dict) else None
    current_value = current.get("downloads") if isinstance(current, dict) else None
    download_delta = None
    if isinstance(baseline_value, int) and isinstance(current_value, int):
        download_delta = current_value - baseline_value

    return {
        "period": {
            "startAt": start_at.isoformat(timespec="microseconds"),
            "endAtExclusive": end_at.isoformat(timespec="microseconds"),
            "label": format_period(start_at, end_at),
            "days": (end_at.date() - start_at.date()).days,
        },
        "iterationCount": len(iterations_in_period),
        "changedFilesTotal": changed_files_total,
        "addedLinesTotal": added_lines_total,
        "removedLinesTotal": removed_lines_total,
        "downloadSnapshotCount": len(download_snapshots),
        "downloadBaseline": baseline,
        "downloadCurrent": current,
        "downloadDelta": download_delta,
        "iterations": iterations_in_period,
        "downloadSnapshots": download_snapshots,
        "topChangedPaths": summarize_top_paths(iterations_in_period, limit=top_files_limit),
        "notes": notes,
    }


def compare_periods(current: dict[str, Any], previous: dict[str, Any]) -> dict[str, Any]:
    def diff_int(key: str) -> int | None:
        current_value = current.get(key)
        previous_value = previous.get(key)
        if not isinstance(current_value, int) or not isinstance(previous_value, int):
            return None
        return current_value - previous_value

    return {
        "iterationCountDelta": diff_int("iterationCount"),
        "changedFilesTotalDelta": diff_int("changedFilesTotal"),
        "addedLinesTotalDelta": diff_int("addedLinesTotal"),
        "removedLinesTotalDelta": diff_int("removedLinesTotal"),
        "downloadSnapshotCountDelta": diff_int("downloadSnapshotCount"),
        "downloadDeltaDelta": diff_int("downloadDelta"),
    }


def format_optional_delta(value: int | None) -> str:
    if value is None:
        return "N/A"
    return f"{value:+d}"


def build_weekly_report_markdown(
    *,
    generated_at: str,
    current_summary: dict[str, Any],
    previous_summary: dict[str, Any],
    comparison: dict[str, Any],
    max_iterations: int,
    max_files: int,
) -> str:
    current_period = current_summary.get("period", {}) or {}
    previous_period = previous_summary.get("period", {}) or {}
    baseline = current_summary.get("downloadBaseline") or {}
    current_download = current_summary.get("downloadCurrent") or {}
    previous_baseline = previous_summary.get("downloadBaseline") or {}
    previous_download = previous_summary.get("downloadCurrent") or {}

    lines = [
        "# Priority Coach 监控周报",
        "",
        f"- 生成时间：{generated_at}",
        f"- 统计周期：{current_period.get('label', 'N/A')}",
        f"- 对比周期：{previous_period.get('label', 'N/A')}",
        "",
        "## 本周期概览",
        f"- 迭代次数：{current_summary.get('iterationCount', 0)}",
        f"- 变更文件总数：{current_summary.get('changedFilesTotal', 0)}",
        f"- 代码行变化：+{current_summary.get('addedLinesTotal', 0)} / -{current_summary.get('removedLinesTotal', 0)}",
        (
            f"- 下载量：{format_number(baseline.get('downloads'))} -> "
            f"{format_number(current_download.get('downloads'))}"
            f"（增量 {format_optional_delta(current_summary.get('downloadDelta'))}）"
        ),
        f"- 下载量快照数：{current_summary.get('downloadSnapshotCount', 0)}",
        "",
        "## 与上一周期对比",
        (
            f"- 迭代次数：{current_summary.get('iterationCount', 0)} vs {previous_summary.get('iterationCount', 0)} "
            f"({format_optional_delta(comparison.get('iterationCountDelta'))})"
        ),
        (
            f"- 变更文件总数：{current_summary.get('changedFilesTotal', 0)} vs {previous_summary.get('changedFilesTotal', 0)} "
            f"({format_optional_delta(comparison.get('changedFilesTotalDelta'))})"
        ),
        (
            f"- 代码新增行数：{current_summary.get('addedLinesTotal', 0)} vs {previous_summary.get('addedLinesTotal', 0)} "
            f"({format_optional_delta(comparison.get('addedLinesTotalDelta'))})"
        ),
        (
            f"- 下载增量：{format_optional_delta(current_summary.get('downloadDelta'))} vs "
            f"{format_optional_delta(previous_summary.get('downloadDelta'))} "
            f"({format_optional_delta(comparison.get('downloadDeltaDelta'))})"
        ),
        "",
        "## 上一周期概览",
        f"- 周期：{previous_period.get('label', 'N/A')}",
        f"- 迭代次数：{previous_summary.get('iterationCount', 0)}",
        f"- 变更文件总数：{previous_summary.get('changedFilesTotal', 0)}",
        f"- 代码行变化：+{previous_summary.get('addedLinesTotal', 0)} / -{previous_summary.get('removedLinesTotal', 0)}",
        (
            f"- 下载量：{format_number(previous_baseline.get('downloads'))} -> "
            f"{format_number(previous_download.get('downloads'))}"
            f"（增量 {format_optional_delta(previous_summary.get('downloadDelta'))}）"
        ),
        "",
        "## 本周期主要改动文件",
    ]

    top_paths = current_summary.get("topChangedPaths", []) or []
    if not top_paths:
        lines.append("- （本周期暂无迭代）")
    else:
        for item in top_paths[:max_files]:
            lines.append(
                f"- `{item.get('path')}`：{item.get('count', 0)} 次，"
                f"+{item.get('addedLines', 0)} / -{item.get('removedLines', 0)}"
            )

    lines.extend([
        "",
        "## 本周期迭代详情",
    ])

    iterations = current_summary.get("iterations", []) or []
    if not iterations:
        lines.append("- （本周期暂无迭代）")
    else:
        for record in iterations[-max_iterations:]:
            totals = record.get("totals", {}) or {}
            lines.append(
                f"### {record.get('capturedAt')} | {record.get('label') or record.get('version') or '未命名迭代'}"
            )
            if record.get("gitCommit"):
                lines.append(f"- Commit：{str(record.get('gitCommit'))[:12]}")
            if record.get("note"):
                lines.append(f"- 说明：{record.get('note')}")
            lines.append(
                f"- 变化：{totals.get('changedFiles', 0)} 文件 (+{totals.get('addedLines', 0)} / -{totals.get('removedLines', 0)})"
            )
            changed_files = record.get("changedFiles", []) or []
            for item in changed_files[:max_files]:
                lines.append(
                    f"  - `{item.get('path')}` [{item.get('status')}] +{item.get('addedLines', 0)} / -{item.get('removedLines', 0)}"
                )
            if len(changed_files) > max_files:
                lines.append(f"  - ... 还有 {len(changed_files) - max_files} 个文件")
            lines.append("")

    lines.append("## 本周期下载量快照")
    download_snapshots = current_summary.get("downloadSnapshots", []) or []
    if not download_snapshots:
        lines.append("- （本周期暂无下载量快照）")
    else:
        for item in download_snapshots:
            note = normalize_string(item.get("note"))
            suffix = f" | {note}" if note else ""
            lines.append(
                f"- {item.get('capturedAt')} | {format_number(item.get('downloads'))} | {item.get('source') or 'manual'}{suffix}"
            )

    lines.append("")
    return "\n".join(lines)


def summarize_change_counts(changes: list[dict[str, Any]]) -> dict[str, int]:
    changed_files = len(changes)
    added_lines = sum(int(item.get("addedLines", 0)) for item in changes)
    removed_lines = sum(int(item.get("removedLines", 0)) for item in changes)
    return {
        "changedFiles": changed_files,
        "addedLines": added_lines,
        "removedLines": removed_lines,
    }


def print_iteration_summary(record: dict[str, Any], delta_info: dict[str, Any] | None = None) -> None:
    version = normalize_string(record.get("version")) or "(no version)"
    label = normalize_string(record.get("label")) or "未命名迭代"
    note = normalize_string(record.get("note"))
    git_commit = normalize_string(record.get("gitCommit"))
    totals = record.get("totals", {}) or {}
    print(f"已记录迭代：{record.get('id')}")
    print(f"- 版本：{version}")
    print(f"- 标签：{label}")
    if git_commit:
        print(f"- Commit：{git_commit[:12]}")
    if note:
        print(f"- 说明：{note}")
    print(
        "- 代码变化："
        f"{totals.get('changedFiles', 0)} 个文件，"
        f"+{totals.get('addedLines', 0)} / -{totals.get('removedLines', 0)}"
    )
    changed_files = record.get("changedFiles", []) or []
    for item in changed_files[:8]:
        print(
            f"  - {item.get('path')} [{item.get('status')}] "
            f"+{item.get('addedLines', 0)} / -{item.get('removedLines', 0)}"
        )
    if len(changed_files) > 8:
        print(f"  - ... 还有 {len(changed_files) - 8} 个文件")

    if delta_info:
        baseline = delta_info.get("baseline") or {}
        latest_after = delta_info.get("latestAfter") or {}
        delta = delta_info.get("delta")
        baseline_value = baseline.get("downloads") if isinstance(baseline, dict) else None
        current_value = latest_after.get("downloads") if isinstance(latest_after, dict) else None
        print(
            f"- 下载量：基线 {format_number(baseline_value)} -> 当前 {format_number(current_value)}"
            + (f"（增量 {delta:+d}）" if isinstance(delta, int) else "")
        )


def cmd_path(args: argparse.Namespace) -> int:
    paths = monitor_paths(args)
    print(json.dumps({
        "monitorHome": str(paths.base_dir),
        "iterations": str(paths.iterations),
        "downloads": str(paths.downloads),
        "snapshots": str(paths.snapshots),
        "reports": str(paths.reports),
    }, ensure_ascii=False, indent=2))
    return 0


def cmd_capture_iteration(args: argparse.Namespace) -> int:
    paths = monitor_paths(args)
    iteration_store = load_iterations_store(paths)
    git_ref = normalize_string(getattr(args, "git_ref", "") or getattr(args, "commit_sha", ""))
    git_commit = ""
    if git_ref:
        git_commit = git_resolve_ref(PROJECT_ROOT, git_ref)
        for item in iteration_store["iterations"]:
            if normalize_string(item.get("gitCommit")) == git_commit:
                print(f"该 commit 已记录：{git_commit}")
                return 0

    previous_iterations = sort_by_captured_at(iteration_store["iterations"])
    previous_snapshot = None
    if previous_iterations:
        latest = previous_iterations[-1]
        snapshot_id = normalize_string(latest.get("snapshotId"))
        if snapshot_id:
            previous_snapshot = load_snapshot(paths, snapshot_id)

    current_snapshot = build_snapshot(PROJECT_ROOT, git_ref=git_ref)
    changes = compare_snapshots(previous_snapshot, current_snapshot)
    if not changes and not args.allow_empty:
        print("没有检测到文件变化；未记录新迭代。若仍需记录，可加 --allow-empty。")
        return 0

    metadata = detect_skill_metadata(PROJECT_ROOT)
    version = normalize_string(args.version) or metadata.get("version", "")
    label = normalize_string(args.label) or version or "priority-coach"
    iteration_id = make_iteration_id(version)
    save_snapshot(paths, iteration_id, current_snapshot)
    commit_subject = normalize_string(getattr(args, "commit_subject", ""))
    note = normalize_string(args.note)
    if not note and commit_subject:
        short_commit = git_commit[:7] if git_commit else ""
        note = f"[{short_commit}] {commit_subject}" if short_commit else commit_subject

    record = {
        "id": iteration_id,
        "capturedAt": now_iso(),
        "label": label,
        "version": version,
        "metaVersion": metadata.get("metaVersion", ""),
        "skillVersion": metadata.get("skillVersion", ""),
        "homepage": metadata.get("homepage", ""),
        "note": note,
        "captureSource": "git-ref" if git_ref else "worktree",
        "gitRef": git_ref,
        "gitCommit": git_commit,
        "gitCommitSubject": commit_subject,
        "snapshotId": iteration_id,
        "changedFiles": changes,
        "totals": summarize_change_counts(changes),
    }
    iteration_store["iterations"].append(record)
    iteration_store["iterations"] = sort_by_captured_at(iteration_store["iterations"])
    write_json(paths.iterations, iteration_store)

    delta_info = None
    if args.downloads:
        downloads_value = parse_human_number(args.downloads)
        append_download_snapshot(
            paths,
            downloads=downloads_value,
            source="capture-iteration",
            url=metadata.get("homepage", ""),
            raw_value=args.downloads,
            note=f"baseline for {iteration_id}",
            captured_at=record["capturedAt"],
        )
        downloads_store = load_downloads_store(paths)
        delta_info = download_delta_for_iteration(record, downloads_store["downloads"])

    print_iteration_summary(record, delta_info)
    return 0


def cmd_capture_downloads(args: argparse.Namespace) -> int:
    paths = monitor_paths(args)
    metadata = detect_skill_metadata(PROJECT_ROOT)
    url = normalize_string(args.url) or metadata.get("homepage", "")
    note = normalize_string(args.note)
    source = normalize_string(args.source)

    if args.count:
        downloads = parse_human_number(args.count)
        raw_value = args.count
        if not source:
            source = "manual"
    else:
        if not url:
            raise MonitorError("缺少 --url，且未能从 SKILL.md 自动识别 homepage")
        raw_text = fetch_text(url, timeout=float(args.timeout))
        parsed = find_download_match(raw_text)
        if not parsed:
            raise MonitorError(
                "自动抓取成功，但没在页面里识别到 downloads。可改用 --count 手动记一笔。"
            )
        downloads, raw_value = parsed
        if not source:
            source = "fetched"

    entry = append_download_snapshot(
        paths,
        downloads=downloads,
        source=source,
        url=url,
        raw_value=raw_value,
        note=note,
    )

    print("已记录下载量快照：")
    print(json.dumps(entry, ensure_ascii=False, indent=2))
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    paths = monitor_paths(args)
    iteration_store = load_iterations_store(paths)
    downloads_store = load_downloads_store(paths)
    iterations = sort_by_captured_at(iteration_store["iterations"], reverse=True)
    downloads = sort_by_captured_at(downloads_store["downloads"])

    if args.json:
        payload = []
        for record in iterations[: args.limit]:
            item = dict(record)
            item["downloadDelta"] = download_delta_for_iteration(record, downloads)
            payload.append(item)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print(f"监控目录：{paths.base_dir}")
    print(f"迭代记录：{len(iterations)} 条 | 下载快照：{len(downloads)} 条")

    if not iterations:
        print("（暂无迭代记录）")
        return 0

    for index, record in enumerate(iterations[: args.limit], start=1):
        delta_info = download_delta_for_iteration(record, downloads)
        baseline = delta_info.get("baseline") or {}
        latest_after = delta_info.get("latestAfter") or {}
        delta = delta_info.get("delta")
        totals = record.get("totals", {}) or {}
        print()
        print(f"{index}. {record.get('capturedAt')} | {record.get('label') or record.get('version') or '未命名迭代'}")
        print(
            f"   版本: {record.get('version') or 'N/A'} | 变化: {totals.get('changedFiles', 0)} 文件 "
            f"(+{totals.get('addedLines', 0)} / -{totals.get('removedLines', 0)})"
        )
        if record.get("gitCommit"):
            print(f"   Commit: {str(record.get('gitCommit'))[:12]}")
        if record.get("note"):
            print(f"   说明: {record.get('note')}")
        changed_files = record.get("changedFiles", []) or []
        for item in changed_files[: args.max_files]:
            print(
                f"   - {item.get('path')} [{item.get('status')}] "
                f"+{item.get('addedLines', 0)} / -{item.get('removedLines', 0)}"
            )
            if args.verbose:
                excerpt = item.get("excerpt", []) or []
                for line in excerpt[:6]:
                    print(f"     {line}")
        if len(changed_files) > args.max_files:
            print(f"   - ... 还有 {len(changed_files) - args.max_files} 个文件")

        baseline_value = baseline.get("downloads") if isinstance(baseline, dict) else None
        latest_value = latest_after.get("downloads") if isinstance(latest_after, dict) else None
        baseline_at = baseline.get("capturedAt") if isinstance(baseline, dict) else ""
        latest_at = latest_after.get("capturedAt") if isinstance(latest_after, dict) else ""
        if baseline_value is None and latest_value is None:
            print("   下载量: 暂无快照")
        else:
            delta_text = f" | 增量 {delta:+d}" if isinstance(delta, int) else ""
            print(
                f"   下载量: {format_number(baseline_value)} ({baseline_at or 'N/A'})"
                f" -> {format_number(latest_value)} ({latest_at or 'N/A'}){delta_text}"
            )
    return 0


def cmd_weekly_report(args: argparse.Namespace) -> int:
    paths = monitor_paths(args)
    iteration_store = load_iterations_store(paths)
    downloads_store = load_downloads_store(paths)
    iterations = sort_by_captured_at(iteration_store["iterations"])
    downloads = sort_by_captured_at(downloads_store["downloads"])

    anchor_date = parse_anchor_date(args.anchor_date)
    current_start, current_end = period_bounds(anchor_date, args.days)
    previous_end = current_start
    previous_start = previous_end - dt.timedelta(days=args.days)

    current_summary = summarize_period(
        iterations,
        downloads,
        start_at=current_start,
        end_at=current_end,
        top_files_limit=args.max_files,
    )
    previous_summary = summarize_period(
        iterations,
        downloads,
        start_at=previous_start,
        end_at=previous_end,
        top_files_limit=args.max_files,
    )
    comparison = compare_periods(current_summary, previous_summary)

    if args.json:
        payload = {
            "generatedAt": now_iso(),
            "current": current_summary,
            "previous": previous_summary,
            "comparison": comparison,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    markdown = build_weekly_report_markdown(
        generated_at=now_iso(),
        current_summary=current_summary,
        previous_summary=previous_summary,
        comparison=comparison,
        max_iterations=args.max_iterations,
        max_files=args.max_files,
    )

    output_path = ""
    if args.out:
        output_path = str(Path(args.out).expanduser())
    elif args.save:
        label = current_summary.get("period", {}).get("label", "period")
        safe_label = label.replace(" ", "").replace("~", "_to_")
        output_path = str(paths.reports / f"weekly-{safe_label}.md")

    if output_path:
        target = Path(output_path).expanduser()
        write_text(target, markdown)
        print(f"已生成周报：{target}")
        print(f"- 本周期：{current_summary.get('period', {}).get('label', 'N/A')}")
        print(
            f"- 下载增量：{format_optional_delta(current_summary.get('downloadDelta'))} | "
            f"上一周期：{format_optional_delta(previous_summary.get('downloadDelta'))}"
        )
        return 0

    print(markdown)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Priority Coach 迭代/下载量监控")
    parser.add_argument(
        "--store-dir",
        help="监控数据目录；默认使用项目根目录下的 .monitoring/",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    path_parser = subparsers.add_parser("path", help="查看监控数据路径")
    path_parser.set_defaults(func=cmd_path)

    capture_iteration_parser = subparsers.add_parser(
        "capture-iteration",
        help="记录一次迭代，并自动比较与上次快照的差异",
    )
    capture_iteration_parser.add_argument("--version", help="手动覆盖版本号")
    capture_iteration_parser.add_argument("--label", help="给本次迭代起一个标签")
    capture_iteration_parser.add_argument("--note", help="补充本次迭代说明")
    capture_iteration_parser.add_argument(
        "--git-ref",
        help="按指定 git ref/commit 做快照，例如 HEAD 或具体 commit sha",
    )
    capture_iteration_parser.add_argument(
        "--commit-sha",
        help="--git-ref 的别名，便于 git hook 传入",
    )
    capture_iteration_parser.add_argument(
        "--commit-subject",
        help="可选：记录 commit subject，若未显式传 --note，会自动写入 note",
    )
    capture_iteration_parser.add_argument(
        "--downloads",
        help="可选：同时记录当前下载量基线，例如 42 或 1.2k",
    )
    capture_iteration_parser.add_argument(
        "--allow-empty",
        action="store_true",
        help="即使没有文件变化，也强制记一条迭代记录",
    )
    capture_iteration_parser.set_defaults(func=cmd_capture_iteration)

    capture_downloads_parser = subparsers.add_parser(
        "capture-downloads",
        help="记录当前下载量，可手动输入，也可尝试自动抓取 homepage",
    )
    source_group = capture_downloads_parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--count", help="手动输入下载量，例如 37 或 2.4k")
    source_group.add_argument(
        "--fetch",
        action="store_true",
        help="从 skill homepage 自动抓取下载量",
    )
    capture_downloads_parser.add_argument("--url", help="抓取地址，默认取 SKILL.md 中的 homepage")
    capture_downloads_parser.add_argument("--source", help="来源说明，例如 manual / fetched / clawhub")
    capture_downloads_parser.add_argument("--note", help="本次快照说明")
    capture_downloads_parser.add_argument(
        "--timeout",
        default="10",
        help="自动抓取超时秒数，默认 10",
    )
    capture_downloads_parser.set_defaults(func=cmd_capture_downloads)

    report_parser = subparsers.add_parser("report", help="查看迭代与下载量增量报告")
    report_parser.add_argument("--limit", type=int, default=10, help="最多展示多少条迭代记录")
    report_parser.add_argument(
        "--max-files",
        type=int,
        default=6,
        help="每条迭代最多展示多少个变化文件",
    )
    report_parser.add_argument(
        "--verbose",
        action="store_true",
        help="额外显示每个文件的差异摘录",
    )
    report_parser.add_argument("--json", action="store_true", help="输出 JSON")
    report_parser.set_defaults(func=cmd_report)

    weekly_report_parser = subparsers.add_parser(
        "weekly-report",
        help="生成监控周报与增长对比",
    )
    weekly_report_parser.add_argument(
        "--anchor-date",
        help="统计截止日期（YYYY-MM-DD），默认今天；统计区间为截止日往前数 days 天",
    )
    weekly_report_parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="统计周期天数，默认 7",
    )
    weekly_report_parser.add_argument(
        "--max-iterations",
        type=int,
        default=10,
        help="周报中最多展示多少条迭代详情",
    )
    weekly_report_parser.add_argument(
        "--max-files",
        type=int,
        default=8,
        help="每部分最多展示多少个文件",
    )
    weekly_report_parser.add_argument(
        "--save",
        action="store_true",
        help="将 Markdown 周报保存到 .monitoring/reports/ 下",
    )
    weekly_report_parser.add_argument(
        "--out",
        help="将 Markdown 周报保存到指定路径",
    )
    weekly_report_parser.add_argument(
        "--json",
        action="store_true",
        help="输出 JSON 结构化周报",
    )
    weekly_report_parser.set_defaults(func=cmd_weekly_report)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except MonitorError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("已取消", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
