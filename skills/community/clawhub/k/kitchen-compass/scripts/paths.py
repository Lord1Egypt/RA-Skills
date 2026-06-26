#!/usr/bin/env python3
from __future__ import annotations

import fcntl
import json
import os
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DATA_ROOT_ENV = "KITCHEN_COMPASS_DATA_ROOT"
LEGACY_DATA_ROOT_ENV = "FOOD_BRAIN_DATA_ROOT"
VERBOSE_ENV = "KITCHEN_COMPASS_VERBOSE"

_LOGGED_ROOTS: set[Path] = set()
_LEGACY_ENV_WARNED = False


def write_atomic(path: Path, content: str, encoding: str = "utf-8") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
    )
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding=encoding) as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_path, path)
    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise


def append_jsonl(path: Path, event: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(event, sort_keys=True) + "\n"
    with path.open("a", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            handle.write(line)
            handle.flush()
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


@dataclass(frozen=True)
class KitchenCompassPaths:
    data_root: Path
    household_dir: Path
    recipes_dir: Path
    inventory_dir: Path
    inventory_items_file: Path
    inventory_transactions_file: Path
    inventory_freezer_notes_file: Path
    deals_dir: Path
    deal_brief_input_file: Path
    deal_store_briefs_dir: Path
    history_dir: Path
    history_file: Path
    generated_dir: Path
    generated_query_dir: Path
    generated_planner_dir: Path
    generated_deals_dir: Path
    generated_deal_scan_file: Path
    generated_deal_scan_markdown_file: Path
    generated_combined_deal_sheet_file: Path
    generated_combined_deal_sheet_markdown_file: Path
    query_planning_dir: Path
    planner_views_dir: Path
    inbox_dir: Path
    raw_recipes_dir: Path

    @classmethod
    def from_root(cls, data_root: Path) -> "KitchenCompassPaths":
        root = data_root.expanduser().resolve()
        generated_dir = root / "generated"
        return cls(
            data_root=root,
            household_dir=root / "household",
            recipes_dir=root / "recipes",
            inventory_dir=root / "inventory",
            inventory_items_file=root / "inventory" / "items.json",
            inventory_transactions_file=root / "inventory" / "transactions.jsonl",
            inventory_freezer_notes_file=root / "inventory" / "freezer.md",
            deals_dir=root / "deals",
            deal_brief_input_file=root / "deals" / "weekly-deal-brief-input.json",
            deal_store_briefs_dir=root / "deals" / "store-briefs",
            history_dir=root / "history",
            history_file=root / "history" / "events.jsonl",
            generated_dir=generated_dir,
            generated_query_dir=generated_dir / "query",
            generated_planner_dir=generated_dir / "planner",
            generated_deals_dir=generated_dir / "deals",
            generated_deal_scan_file=generated_dir / "deals" / "weekly-deal-scan-latest.json",
            generated_deal_scan_markdown_file=generated_dir / "deals" / "weekly-deal-scan-latest.md",
            generated_combined_deal_sheet_file=generated_dir / "deals" / "combined-weekly-deal-sheet-latest.json",
            generated_combined_deal_sheet_markdown_file=generated_dir / "deals" / "combined-weekly-deal-sheet-latest.md",
            query_planning_dir=generated_dir / "query" / "planning-views",
            planner_views_dir=generated_dir / "planner" / "planning-views",
            inbox_dir=root / "inbox",
            raw_recipes_dir=root / "inbox" / "raw-recipes",
        )

    def ensure_runtime_dirs(self) -> None:
        for path in [
            self.household_dir,
            self.recipes_dir,
            self.inventory_dir,
            self.deals_dir,
            self.deal_store_briefs_dir,
            self.history_dir,
            self.generated_query_dir,
            self.generated_planner_dir,
            self.generated_deals_dir,
            self.query_planning_dir,
            self.planner_views_dir,
            self.raw_recipes_dir,
        ]:
            path.mkdir(parents=True, exist_ok=True)


# DEPRECATED: retained for backwards compatibility with code that imported
# the old name. New code should use KitchenCompassPaths.
FoodBrainPaths = KitchenCompassPaths


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def looks_like_data_root(path: Path) -> bool:
    return (path / "recipes").is_dir() and (path / "household").is_dir()


def looks_like_skill_root(path: Path) -> bool:
    return (path / "SKILL.md").is_file() and (path / "scripts").is_dir() and (path / "assets").is_dir()


def resolve_data_root(raw: str | None = None, *, verbose: bool = False) -> Path:
    resolved = _resolve_data_root(raw)
    if (verbose or os.environ.get(VERBOSE_ENV)) and resolved not in _LOGGED_ROOTS:
        _LOGGED_ROOTS.add(resolved)
        print(f"[kitchen-compass] data root: {resolved}", file=sys.stderr)
    return resolved


def _resolve_data_root(raw: str | None) -> Path:
    if raw:
        return Path(raw).expanduser().resolve()

    new_env = os.environ.get(DATA_ROOT_ENV)
    legacy_env = os.environ.get(LEGACY_DATA_ROOT_ENV)
    if legacy_env and not new_env:
        _warn_legacy_env_once()
        return Path(legacy_env).expanduser().resolve()
    if new_env and legacy_env:
        _warn_legacy_env_once()
    if new_env:
        return Path(new_env).expanduser().resolve()

    cwd = Path.cwd().resolve()
    if looks_like_data_root(cwd):
        return cwd

    default_child = cwd / "kitchen-compass-data"
    if looks_like_data_root(default_child):
        return default_child

    if looks_like_skill_root(cwd):
        sibling_root = cwd.parent / "kitchen-compass-data"
        if looks_like_data_root(sibling_root):
            return sibling_root
        return sibling_root

    return default_child


def _warn_legacy_env_once() -> None:
    global _LEGACY_ENV_WARNED
    if _LEGACY_ENV_WARNED:
        return
    _LEGACY_ENV_WARNED = True
    print(
        f"[kitchen-compass] {LEGACY_DATA_ROOT_ENV} is deprecated; use {DATA_ROOT_ENV} instead.",
        file=sys.stderr,
    )
