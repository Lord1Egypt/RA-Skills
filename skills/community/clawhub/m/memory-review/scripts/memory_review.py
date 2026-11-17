#!/usr/bin/env python3
"""Deterministic helpers for memory-review scan state and decision validation."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DAILY_RE = re.compile(r"^memory/daily/(\d{4}-\d{2})/(\d{4}-\d{2}-\d{2})\.md$")
DATE_IN_NAME_RE = re.compile(r"(?:^|[-_])20\d{2}(?:[-_]\d{2})?(?:[-_]\d{2})?(?:[-_]|$)")
ALLOWED_ACTIONS = {
    "update_existing",
    "create_new",
    "skip_duplicate",
    "review_merge",
    "defer",
}
PROTECTED_TOP_LEVEL = {
    "AGENTS.md",
    "MEMORY.md",
    "TOOLS.md",
    "USER.md",
    "SOUL.md",
    "IDENTITY.md",
    "ENVIRONMENT.md",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def md5(path: Path) -> str:
    digest = hashlib.md5()  # noqa: S324 - required only for legacy-state migration
    digest.update(path.read_bytes())
    return digest.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    temporary.replace(path)


def relative(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def daily_files(root: Path) -> list[tuple[str, Path]]:
    found: list[tuple[str, Path]] = []
    daily_root = root / "memory" / "daily"
    if not daily_root.exists():
        return found
    for path in daily_root.glob("????-??/????-??-??.md"):
        rel = relative(root, path)
        match = DAILY_RE.fullmatch(rel)
        if match:
            found.append((match.group(2), path))
    return sorted(found)


def load_v2_state(path: Path) -> dict[str, str] | None:
    if not path.exists():
        return None
    raw = json.loads(path.read_text())
    if raw.get("schema_version") != 2 or not isinstance(raw.get("sources"), dict):
        raise ValueError(f"unsupported state schema: {path}")
    return {str(k): str(v) for k, v in raw["sources"].items()}


@dataclass(frozen=True)
class LegacyCursor:
    date: str
    md5: str
    source: str


def find_legacy_cursor(root: Path) -> LegacyCursor | None:
    log_dir = root / "data" / "exec-logs" / "memory-review"
    if not log_dir.exists():
        return None
    pattern = re.compile(
        r'"date"\s*:\s*"(?P<date>\d{4}-\d{2}-\d{2})".*?'
        r'"md5"\s*:\s*"(?P<md5>[a-fA-F0-9]{32})"',
        re.S,
    )
    for path in sorted(log_dir.glob("????-??-??*.md"), reverse=True):
        match = pattern.search(path.read_text(errors="replace"))
        if match:
            return LegacyCursor(
                date=match.group("date"),
                md5=match.group("md5").lower(),
                source=relative(root, path),
            )
    return None


def build_scan(root: Path, state_path: Path, lookback: int) -> dict[str, Any]:
    files = daily_files(root)
    current = {relative(root, path): sha256(path) for _, path in files}
    state = load_v2_state(state_path)
    changed: list[dict[str, str]] = []
    bootstrap: dict[str, Any]

    if state is not None:
        bootstrap = {"mode": "state_v2"}
        for date, path in files:
            rel = relative(root, path)
            if rel not in state:
                changed.append({"date": date, "path": rel, "reason": "new", "sha256": current[rel]})
            elif state[rel] != current[rel]:
                changed.append({"date": date, "path": rel, "reason": "changed", "sha256": current[rel]})
    else:
        legacy = find_legacy_cursor(root)
        if legacy:
            bootstrap = {"mode": "legacy_cursor", "date": legacy.date, "source": legacy.source}
            for date, path in files:
                rel = relative(root, path)
                if date > legacy.date:
                    changed.append({"date": date, "path": rel, "reason": "new", "sha256": current[rel]})
                elif date == legacy.date and md5(path) != legacy.md5:
                    changed.append({"date": date, "path": rel, "reason": "changed", "sha256": current[rel]})
        else:
            selected = files[-max(lookback, 0) :] if lookback else []
            selected_paths = {path for _, path in selected}
            bootstrap = {"mode": "lookback", "count": len(selected)}
            for date, path in files:
                if path in selected_paths:
                    rel = relative(root, path)
                    changed.append(
                        {"date": date, "path": rel, "reason": "initial_lookback", "sha256": current[rel]}
                    )

    removed = sorted(set(state or {}) - set(current))
    return {
        "schema_version": 2,
        "state_path": relative(root, state_path),
        "bootstrap": bootstrap,
        "changed_sources": changed,
        "unchanged_count": len(files) - len(changed),
        "removed_sources": removed,
        "state_after": {"schema_version": 2, "sources": current},
    }


def normalized_ngrams(value: str) -> set[str]:
    normalized = "".join(ch.lower() for ch in value if ch.isalnum())
    if len(normalized) < 2:
        return {normalized} if normalized else set()
    return {normalized[i : i + 2] for i in range(len(normalized) - 1)}


def similarity(left: str, right: str) -> float:
    a = normalized_ngrams(left)
    b = normalized_ngrams(right)
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def first_heading(text: str) -> str:
    match = re.search(r"^#\s+(.+)$", text, re.M)
    return match.group(1).strip() if match else ""


def headings(text: str) -> str:
    return " ".join(re.findall(r"^#{1,4}\s+(.+)$", text, re.M))


def corpus_files(root: Path) -> list[Path]:
    paths = list((root / "memory" / "knowledge").glob("**/*.md"))
    paths.extend((root / "memory" / "projects").glob("**/*.md"))
    paths.extend([root / "memory" / "glossary.md", root / "memory" / "post-mortems.md"])
    return sorted(path for path in paths if path.is_file())


def candidate_rows(root: Path, query: str, limit: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in corpus_files(root):
        text = path.read_text(errors="replace")
        title = first_heading(text)
        stem = path.stem.replace("-", " ").replace("_", " ")
        header_text = headings(text[:20000])
        score = (
            0.45 * similarity(query, title)
            + 0.25 * similarity(query, stem)
            + 0.20 * similarity(query, header_text)
            + 0.10 * similarity(query, text[:20000])
        )
        normalized_query = "".join(ch.lower() for ch in query if ch.isalnum())
        normalized_title = "".join(ch.lower() for ch in title if ch.isalnum())
        if normalized_query and normalized_query in normalized_title:
            score += 0.25
        if score > 0:
            rows.append(
                {
                    "path": relative(root, path),
                    "title": title,
                    "score": round(min(score, 1.0), 4),
                }
            )
    return sorted(rows, key=lambda item: (-item["score"], item["path"]))[:limit]


def safe_relative_path(value: str) -> bool:
    path = Path(value)
    return not path.is_absolute() and ".." not in path.parts


def is_allowed_destination(value: str) -> bool:
    if not safe_relative_path(value):
        return False
    path = Path(value)
    if value in {"memory/glossary.md", "memory/post-mortems.md"}:
        return True
    return len(path.parts) >= 3 and path.parts[:2] in {
        ("memory", "knowledge"),
        ("memory", "projects"),
    } and path.suffix == ".md"


def validate_decision_plan(root: Path, plan: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if plan.get("schema_version") != 2:
        errors.append("schema_version must be 2")
    decisions = plan.get("decisions")
    if not isinstance(decisions, list):
        return errors + ["decisions must be a list"]
    source_files = plan.get("source_files")
    valid_sources: set[str] = set()
    if not isinstance(source_files, list) or not source_files:
        errors.append("source_files must be a non-empty list")
    else:
        for source in source_files:
            if not isinstance(source, str) or not DAILY_RE.fullmatch(source):
                errors.append(f"source_files contains non-daily path: {source!r}")
            elif not (root / source).is_file():
                errors.append(f"source_files path does not exist: {source}")
            else:
                valid_sources.add(source)
    seen_signals: set[str] = set()
    created_destinations: set[str] = set()

    for index, decision in enumerate(decisions):
        prefix = f"decisions[{index}]"
        if not isinstance(decision, dict):
            errors.append(f"{prefix} must be an object")
            continue
        signal = str(decision.get("signal", "")).strip()
        action = decision.get("action")
        reason = str(decision.get("reason", "")).strip()
        source_refs = decision.get("source_refs")
        destination = decision.get("destination")
        candidates = decision.get("candidates_checked")
        searches = decision.get("searches_performed")
        if not signal:
            errors.append(f"{prefix}.signal is required")
        elif signal.casefold() in seen_signals:
            errors.append(f"{prefix}.signal duplicates another decision")
        else:
            seen_signals.add(signal.casefold())
        if action not in ALLOWED_ACTIONS:
            errors.append(f"{prefix}.action must be one of {sorted(ALLOWED_ACTIONS)}")
        if not reason:
            errors.append(f"{prefix}.reason is required")
        if not isinstance(source_refs, list) or not source_refs:
            errors.append(f"{prefix}.source_refs must be a non-empty list")
        else:
            for source in source_refs:
                if not isinstance(source, str) or not DAILY_RE.fullmatch(source):
                    errors.append(f"{prefix}.source_refs contains non-daily path: {source!r}")
                elif source not in valid_sources:
                    errors.append(f"{prefix}.source_refs is not declared in source_files: {source}")

        if candidates is not None:
            if not isinstance(candidates, list):
                errors.append(f"{prefix}.candidates_checked must be a list")
            else:
                for candidate in candidates:
                    if not isinstance(candidate, str) or not safe_relative_path(candidate):
                        errors.append(f"{prefix}.candidates_checked contains an invalid path: {candidate!r}")
                    elif not (root / candidate).is_file():
                        errors.append(f"{prefix}.candidates_checked path does not exist: {candidate}")

        if destination is not None:
            if not isinstance(destination, str) or not is_allowed_destination(destination):
                errors.append(f"{prefix}.destination is outside automatic write targets")
            elif Path(destination).name in PROTECTED_TOP_LEVEL:
                errors.append(f"{prefix}.destination is protected")

        if action == "update_existing":
            if not isinstance(destination, str) or not (root / destination).is_file():
                errors.append(f"{prefix}.destination must be an existing file")
        elif action == "create_new":
            if not isinstance(destination, str):
                errors.append(f"{prefix}.destination is required")
            else:
                if (root / destination).exists():
                    errors.append(f"{prefix}.destination already exists")
                if destination.startswith("memory/knowledge/") and DATE_IN_NAME_RE.search(Path(destination).stem):
                    errors.append(f"{prefix}.destination must use a date-free knowledge filename")
                if destination in created_destinations:
                    errors.append(f"{prefix}.destination is created more than once")
                created_destinations.add(destination)
            if not isinstance(searches, list) or not searches or not all(
                isinstance(search, str) and search.strip() for search in searches
            ):
                errors.append(f"{prefix}.searches_performed is required for create_new")
        elif action == "skip_duplicate" and destination is not None:
            if not isinstance(destination, str) or not (root / destination).is_file():
                errors.append(f"{prefix}.destination must identify an existing canonical file")
        elif action == "review_merge":
            if not isinstance(candidates, list) or len(candidates) < 2:
                errors.append(f"{prefix}.candidates_checked must list at least two files")
    return errors


def cmd_scan(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    state = root / args.state
    plan = build_scan(root, state, args.lookback)
    if args.output:
        output = Path(args.output)
        atomic_json(output, plan)
        print(
            json.dumps(
                {
                    "output": str(output),
                    "bootstrap": plan["bootstrap"],
                    "changed_sources": plan["changed_sources"],
                    "unchanged_count": plan["unchanged_count"],
                    "removed_sources": plan["removed_sources"],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        sys.stdout.write(json.dumps(plan, ensure_ascii=False, indent=2) + "\n")
    return 0


def cmd_commit_state(args: argparse.Namespace) -> int:
    root = args.root.resolve()
    scan = json.loads(Path(args.scan).read_text())
    state_after = scan.get("state_after")
    if not isinstance(state_after, dict) or not isinstance(state_after.get("sources"), dict):
        raise SystemExit("scan plan does not contain state_after.sources")
    for rel, expected in state_after["sources"].items():
        path = root / rel
        if not path.is_file() or sha256(path) != expected:
            raise SystemExit(f"stale scan plan; source changed or disappeared: {rel}")
    state_path = root / str(scan.get("state_path", args.state))
    atomic_json(state_path, state_after)
    print(state_path)
    return 0


def cmd_candidates(args: argparse.Namespace) -> int:
    result = {"query": args.query, "candidates": candidate_rows(args.root.resolve(), args.query, args.limit)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_validate_plan(args: argparse.Namespace) -> int:
    plan = json.loads(Path(args.plan).read_text())
    errors = validate_decision_plan(args.root.resolve(), plan)
    if errors:
        print(json.dumps({"valid": False, "errors": errors}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps({"valid": True, "decisions": len(plan.get("decisions", []))}, ensure_ascii=False, indent=2))
    return 0


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    sub = result.add_subparsers(dest="command", required=True)

    scan = sub.add_parser("scan", help="build a deterministic daily-log scan plan")
    scan.add_argument("--root", type=Path, default=Path.cwd())
    scan.add_argument("--state", default="data/exec-logs/memory-review/state.json")
    scan.add_argument("--lookback", type=int, default=5)
    scan.add_argument("--output")
    scan.set_defaults(func=cmd_scan)

    commit = sub.add_parser("commit-state", help="commit state after a successful review")
    commit.add_argument("--root", type=Path, default=Path.cwd())
    commit.add_argument("--state", default="data/exec-logs/memory-review/state.json")
    commit.add_argument("--scan", required=True)
    commit.set_defaults(func=cmd_commit_state)

    candidates = sub.add_parser("candidates", help="rank existing memory documents for a topic")
    candidates.add_argument("--root", type=Path, default=Path.cwd())
    candidates.add_argument("--query", required=True)
    candidates.add_argument("--limit", type=int, default=8)
    candidates.set_defaults(func=cmd_candidates)

    validate = sub.add_parser("validate-plan", help="validate a review decision plan")
    validate.add_argument("--root", type=Path, default=Path.cwd())
    validate.add_argument("--plan", required=True)
    validate.set_defaults(func=cmd_validate_plan)
    return result


def main() -> int:
    args = parser().parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
