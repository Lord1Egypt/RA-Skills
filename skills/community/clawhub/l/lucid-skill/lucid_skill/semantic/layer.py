"""YAML-based semantic layer for reading/writing table semantics."""

from __future__ import annotations

import re
from dataclasses import asdict, fields
from datetime import datetime, timezone
from pathlib import Path

import yaml

from lucid_skill.config import get_config
from lucid_skill.types import (
    ColumnSemantic,
    MetricDefinition,
    RelationSemantic,
    TableSemantic,
)


def sanitize_source_id(source_id: str) -> str:
    """Replace non-alphanumeric/underscore/chinese/hyphen characters with '_'."""
    return re.sub(r"[^\w\u4e00-\u9fff\-]", "_", source_id)


def get_semantic_file_path(source_id: str, table_name: str) -> Path:
    """Return the path to the YAML file for a given source and table."""
    config = get_config()
    store_path = Path(config.semantic.store_path)
    return store_path / sanitize_source_id(source_id) / f"{table_name}.yaml"


def _dict_to_table_semantic(data: dict) -> TableSemantic:
    """Convert a raw dict (from YAML) to a TableSemantic dataclass."""
    columns = [
        ColumnSemantic(**col) for col in (data.get("columns") or [])
    ]
    relations = [
        RelationSemantic(**rel) for rel in (data.get("relations") or [])
    ] if data.get("relations") else None
    metrics = [
        MetricDefinition(**m) for m in (data.get("metrics") or [])
    ] if data.get("metrics") else None

    return TableSemantic(
        source=data.get("source", ""),
        table=data.get("table", ""),
        confirmed=data.get("confirmed", False),
        updated_at=data.get("updated_at", ""),
        columns=columns,
        description=data.get("description"),
        business_domain=data.get("business_domain"),
        tags=data.get("tags"),
        relations=relations,
        metrics=metrics,
    )


def _table_semantic_to_dict(semantic: TableSemantic) -> dict:
    """Convert a TableSemantic dataclass to a dict suitable for YAML output."""
    data = asdict(semantic)
    # Remove None values for cleaner YAML
    return {k: v for k, v in data.items() if v is not None}


def read_table_semantic(source_id: str, table_name: str) -> TableSemantic | None:
    """Read a TableSemantic from the YAML file. Returns None if not found."""
    path = get_semantic_file_path(source_id, table_name)
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not data:
            return None
        return _dict_to_table_semantic(data)
    except Exception:
        return None


def write_table_semantic(source_id: str, table_name: str, semantic: TableSemantic) -> None:
    """Write a TableSemantic to the YAML file, creating directories as needed."""
    path = get_semantic_file_path(source_id, table_name)
    path.parent.mkdir(parents=True, exist_ok=True)

    # Update the timestamp
    semantic.updated_at = datetime.now(timezone.utc).isoformat()

    data = _table_semantic_to_dict(semantic)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def list_semantics(source_id: str) -> list[TableSemantic]:
    """List all TableSemantic entries for a given source."""
    config = get_config()
    source_dir = Path(config.semantic.store_path) / sanitize_source_id(source_id)
    if not source_dir.exists():
        return []
    results = []
    for yaml_file in sorted(source_dir.glob("*.yaml")):
        try:
            with open(yaml_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if data:
                results.append(_dict_to_table_semantic(data))
        except Exception:
            continue
    return results


def list_all_semantics() -> list[TableSemantic]:
    """List all TableSemantic entries across all sources."""
    config = get_config()
    store_path = Path(config.semantic.store_path)
    if not store_path.exists():
        return []
    results = []
    for source_dir in sorted(store_path.iterdir()):
        if not source_dir.is_dir():
            continue
        for yaml_file in sorted(source_dir.glob("*.yaml")):
            try:
                with open(yaml_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                if data:
                    results.append(_dict_to_table_semantic(data))
            except Exception:
                continue
    return results


def delete_table_semantic(source_id: str, table_name: str) -> bool:
    """Delete a TableSemantic YAML file. Returns True if deleted, False if not found."""
    path = get_semantic_file_path(source_id, table_name)
    if not path.exists():
        return False
    path.unlink()
    return True
