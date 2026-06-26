"""
JOIN path discovery engine.
Three signals: FK constraints, column name matching, embedding similarity.
Plus indirect (1-hop) path inference.
"""

from __future__ import annotations

import hashlib
import re
from typing import TYPE_CHECKING

from lucid_skill.types import JoinPath

if TYPE_CHECKING:
    from lucid_skill.catalog.store import CatalogStore
    from lucid_skill.semantic.embedder import Embedder

CROSS_SOURCE_ID = "__cross__"


def compute_schema_hash(catalog: CatalogStore, source_id: str) -> str:
    """SHA256 prefix of sorted table.column:type strings."""
    tables = catalog.get_tables(source_id)
    parts: list[str] = []
    for t in tables:
        cols = catalog.get_columns(source_id, t["table_name"])
        for c in cols:
            parts.append(f"{t['table_name']}.{c['column_name']}:{c['dtype']}")
    parts.sort()
    return hashlib.sha256("|".join(parts).encode()).hexdigest()[:16]


def compute_cross_source_schema_hash(catalog: CatalogStore) -> str:
    """Compute a schema hash covering ALL sources (for cross-source cache invalidation)."""
    sources = catalog.get_sources()
    parts: list[str] = []
    for src in sources:
        tables = catalog.get_tables(src["id"])
        for t in tables:
            cols = catalog.get_columns(src["id"], t["table_name"])
            for c in cols:
                parts.append(f"{src['id']}|{t['table_name']}.{c['column_name']}:{c['dtype']}")
    parts.sort()
    return hashlib.sha256("|".join(parts).encode()).hexdigest()[:16]


def _types_compatible(a: str, b: str) -> bool:
    """Check if two column types are compatible for JOIN."""

    def norm(t: str) -> str:
        u = t.upper()
        if any(x in u for x in ("INT", "BIGINT", "SMALLINT", "TINYINT")):
            return "INT"
        if any(x in u for x in ("VARCHAR", "TEXT", "CHAR", "STRING")):
            return "STRING"
        if any(x in u for x in ("FLOAT", "DOUBLE", "DECIMAL", "NUMERIC", "REAL")):
            return "NUMERIC"
        if any(x in u for x in ("DATE", "TIMESTAMP", "TIME")):
            return "TEMPORAL"
        if "BOOL" in u:
            return "BOOL"
        return u

    return norm(a) == norm(b)


def _strip_id_suffix(name: str) -> str:
    """Strip common suffixes for fuzzy matching."""
    return re.sub(r"[_-]?(id|key|code)$", "", name, flags=re.IGNORECASE).lower()


def _path_id(source_id: str, table_a: str, table_b: str, condition: str) -> str:
    """Generate a stable path ID."""
    raw = f"{source_id}|{table_a}|{table_b}|{condition}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def _add_candidate(
    pair_candidates: dict[str, list[JoinPath]], jp: JoinPath
) -> None:
    key = "|".join(sorted([jp.table_a, jp.table_b]))
    if key not in pair_candidates:
        pair_candidates[key] = []
    pair_candidates[key].append(jp)


def _signal1_fk(
    all_table_cols: list[dict],
    catalog: CatalogStore,
    source_id: str,
    pair_candidates: dict[str, list[JoinPath]],
) -> None:
    """Signal 1: FK constraints from column comments matching 'FK -> table.column'."""
    for tc in all_table_cols:
        cols = catalog.get_columns(tc["source_id"], tc["table_name"])
        for col in cols:
            comment = col.get("comment")
            if comment and "->" in comment:
                match = re.search(r"FK\s*->\s*(\w+)\.(\w+)", comment, re.IGNORECASE)
                if match:
                    ref_table = match.group(1)
                    ref_col = match.group(2)
                    condition = f"{tc['table_name']}.{col['column_name']} = {ref_table}.{ref_col}"
                    _add_candidate(
                        pair_candidates,
                        JoinPath(
                            path_id=_path_id(source_id, tc["table_name"], ref_table, condition),
                            source_id=source_id,
                            table_a=tc["table_name"],
                            table_b=ref_table,
                            join_type="INNER",
                            join_condition=condition,
                            confidence=1.0,
                            signal_source="fk_constraint",
                            sql_template=f"SELECT * FROM {tc['table_name']} JOIN {ref_table} ON {condition}",
                            version=1,
                        ),
                    )


def _signal1_fk_cross(
    all_table_cols: list[dict],
    catalog: CatalogStore,
    pair_candidates: dict[str, list[JoinPath]],
) -> None:
    """Signal 1 for cross-source: FK constraints only for same-source pairs."""
    for tc in all_table_cols:
        cols = catalog.get_columns(tc["source_id"], tc["table_name"])
        for col in cols:
            comment = col.get("comment")
            if comment and "->" in comment:
                match = re.search(r"FK\s*->\s*(\w+)\.(\w+)", comment, re.IGNORECASE)
                if match:
                    ref_table = match.group(1)
                    # Only add FK path if the referenced table is in the same source
                    ref_in_same_source = any(
                        t["source_id"] == tc["source_id"] and t["table_name"] == ref_table
                        for t in all_table_cols
                    )
                    if ref_in_same_source:
                        ref_col = match.group(2)
                        condition = f"{tc['table_name']}.{col['column_name']} = {ref_table}.{ref_col}"
                        _add_candidate(
                            pair_candidates,
                            JoinPath(
                                path_id=_path_id(CROSS_SOURCE_ID, tc["table_name"], ref_table, condition),
                                source_id=CROSS_SOURCE_ID,
                                table_a=tc["table_name"],
                                table_b=ref_table,
                                join_type="INNER",
                                join_condition=condition,
                                confidence=1.0,
                                signal_source="fk_constraint",
                                sql_template=f"SELECT * FROM {tc['table_name']} JOIN {ref_table} ON {condition}",
                                version=1,
                            ),
                        )


def _signal2_column_names(
    all_table_cols: list[dict],
    used_source_id: str,
    pair_candidates: dict[str, list[JoinPath]],
    *,
    skip_same_name: bool = False,
) -> None:
    """Signal 2: Column name matching across table pairs."""
    for i in range(len(all_table_cols)):
        for j in range(i + 1, len(all_table_cols)):
            t_a = all_table_cols[i]
            t_b = all_table_cols[j]

            # For cross-source, skip same-table
            if skip_same_name and t_a["table_name"] == t_b["table_name"]:
                continue

            for col_a in t_a["columns"]:
                for col_b in t_b["columns"]:
                    if not _types_compatible(col_a["dtype"], col_b["dtype"]):
                        continue

                    confidence = 0.0
                    signal = ""
                    col_a_lower = col_a["column_name"].lower()
                    col_b_lower = col_b["column_name"].lower()

                    # Rule 1: table_a.xxx_id = table_b.id (or vice versa)
                    t_b_singular = re.sub(r"s$", "", t_b["table_name"]).lower()
                    t_a_singular = re.sub(r"s$", "", t_a["table_name"]).lower()

                    if (
                        (col_a_lower == f"{t_b_singular}_id" and col_b_lower == "id")
                        or (col_a_lower == f"{t_b_singular}_id" and col_b_lower == f"{t_b_singular}_id")
                    ):
                        confidence = 0.85
                        signal = "name_pattern:fk_id"
                    elif (
                        (col_b_lower == f"{t_a_singular}_id" and col_a_lower == "id")
                        or (col_b_lower == f"{t_a_singular}_id" and col_a_lower == f"{t_a_singular}_id")
                    ):
                        confidence = 0.85
                        signal = "name_pattern:fk_id"
                    # Rule 2: exact column name match
                    elif col_a_lower == col_b_lower and col_a_lower != "id":
                        confidence = 0.65
                        signal = "name_pattern:exact_match"
                    # Rule 3: strip _id/_key suffix match
                    elif (
                        _strip_id_suffix(col_a["column_name"]) != ""
                        and _strip_id_suffix(col_a["column_name"]) == _strip_id_suffix(col_b["column_name"])
                        and (
                            col_a_lower.endswith("_id")
                            or col_a_lower.endswith("_key")
                            or col_b_lower.endswith("_id")
                            or col_b_lower.endswith("_key")
                        )
                    ):
                        confidence = 0.5
                        signal = "name_pattern:stripped_suffix"

                    if confidence > 0:
                        condition = (
                            f"{t_a['table_name']}.{col_a['column_name']} = "
                            f"{t_b['table_name']}.{col_b['column_name']}"
                        )
                        _add_candidate(
                            pair_candidates,
                            JoinPath(
                                path_id=_path_id(
                                    used_source_id, t_a["table_name"], t_b["table_name"], condition
                                ),
                                source_id=used_source_id,
                                table_a=t_a["table_name"],
                                table_b=t_b["table_name"],
                                join_type="INNER",
                                join_condition=condition,
                                confidence=confidence,
                                signal_source=signal,
                                sql_template=(
                                    f"SELECT * FROM {t_a['table_name']} "
                                    f"JOIN {t_b['table_name']} ON {condition}"
                                ),
                                version=1,
                            ),
                        )


def _signal3_embedding(
    all_table_cols: list[dict],
    catalog: CatalogStore,
    embedder: Embedder,
    used_source_id: str,
    pair_candidates: dict[str, list[JoinPath]],
    *,
    skip_same_name: bool = False,
) -> None:
    """Signal 3: Embedding similarity (soft signal)."""
    from lucid_skill.semantic.embedder import Embedder as EmbedderClass

    for i in range(len(all_table_cols)):
        for j in range(i + 1, len(all_table_cols)):
            t_a = all_table_cols[i]
            t_b = all_table_cols[j]

            if skip_same_name and t_a["table_name"] == t_b["table_name"]:
                continue

            emb_a = catalog.get_embedding(t_a["source_id"], t_a["table_name"])
            emb_b = catalog.get_embedding(t_b["source_id"], t_b["table_name"])

            if emb_a and emb_b:
                cosine = EmbedderClass.cosine_similarity(emb_a["vector"], emb_b["vector"])
                if cosine > 0.7:
                    emb_score = cosine * 0.6
                    key = "|".join(sorted([t_a["table_name"], t_b["table_name"]]))
                    existing = pair_candidates.get(key, [])
                    # Boost existing candidates with embedding score
                    for c in existing:
                        if c.signal_source.startswith("name_pattern"):
                            col_score = c.confidence
                            c.confidence = 0.6 * col_score + 0.4 * emb_score
                            c.signal_source += "+embedding"
                    # If no column-based candidate exists, add a pure embedding candidate
                    if len(existing) == 0:
                        _add_candidate(
                            pair_candidates,
                            JoinPath(
                                path_id=_path_id(
                                    used_source_id,
                                    t_a["table_name"],
                                    t_b["table_name"],
                                    f"embedding:{cosine:.3f}",
                                ),
                                source_id=used_source_id,
                                table_a=t_a["table_name"],
                                table_b=t_b["table_name"],
                                join_type="INNER",
                                join_condition=f"-- embedding similarity {cosine:.3f}, manual verification needed",
                                confidence=emb_score,
                                signal_source="embedding",
                                sql_template=(
                                    f"-- No auto-generated JOIN: tables are semantically related "
                                    f"(cosine={cosine:.3f}) but no matching columns found"
                                ),
                                version=1,
                            ),
                        )


def _fuse_candidates(pair_candidates: dict[str, list[JoinPath]]) -> list[JoinPath]:
    """Fusion: FK wins, filter >= 0.4 confidence, top 3 per pair."""
    direct_paths: list[JoinPath] = []
    for _key, candidates in pair_candidates.items():
        # FK constraints always win
        fk_paths = [c for c in candidates if c.signal_source == "fk_constraint"]
        if fk_paths:
            direct_paths.extend(fk_paths)
            continue

        # Filter by minimum threshold
        valid = [c for c in candidates if c.confidence >= 0.4]
        # Sort by confidence desc, take top 3
        valid.sort(key=lambda c: c.confidence, reverse=True)
        direct_paths.extend(valid[:3])
    return direct_paths


def _find_indirect_paths(
    direct_paths: list[JoinPath],
    table_names: list[str],
    used_source_id: str,
) -> list[JoinPath]:
    """Find indirect (1-hop) paths via adjacency graph."""
    direct_pair_set: set[str] = set()
    for p in direct_paths:
        direct_pair_set.add("|".join(sorted([p.table_a, p.table_b])))

    # Build adjacency map from direct paths
    adjacency: dict[str, dict[str, JoinPath]] = {}
    for p in direct_paths:
        if p.table_a not in adjacency:
            adjacency[p.table_a] = {}
        if p.table_b not in adjacency:
            adjacency[p.table_b] = {}
        # Keep highest-confidence path per direction
        exist_ab = adjacency[p.table_a].get(p.table_b)
        if not exist_ab or p.confidence > exist_ab.confidence:
            adjacency[p.table_a][p.table_b] = p
        exist_ba = adjacency[p.table_b].get(p.table_a)
        if not exist_ba or p.confidence > exist_ba.confidence:
            adjacency[p.table_b][p.table_a] = p

    indirect_paths: list[JoinPath] = []
    unique_table_names = list(dict.fromkeys(table_names))

    for i in range(len(unique_table_names)):
        for j in range(i + 1, len(unique_table_names)):
            t_a = unique_table_names[i]
            t_b = unique_table_names[j]
            pair_key = "|".join(sorted([t_a, t_b]))

            # Skip if direct path exists
            if pair_key in direct_pair_set:
                continue

            neighbors_a = adjacency.get(t_a)
            if not neighbors_a:
                continue

            for mid, path_am in neighbors_a.items():
                if mid == t_b:
                    continue
                neighbors_m = adjacency.get(mid)
                if not neighbors_m:
                    continue
                path_mb = neighbors_m.get(t_b)
                if not path_mb:
                    continue

                conf = min(path_am.confidence, path_mb.confidence) * 0.8
                if conf < 0.4:
                    continue

                condition = f"{path_am.join_condition} AND {path_mb.join_condition}"
                sql_template = (
                    f"SELECT * FROM {t_a} JOIN {mid} ON {path_am.join_condition} "
                    f"JOIN {t_b} ON {path_mb.join_condition}"
                )

                indirect_paths.append(
                    JoinPath(
                        path_id=_path_id(used_source_id, t_a, t_b, f"via:{mid}"),
                        source_id=used_source_id,
                        table_a=t_a,
                        table_b=t_b,
                        join_type="INNER",
                        join_condition=condition,
                        confidence=conf,
                        signal_source=f"indirect:via_{mid}",
                        sql_template=sql_template,
                        version=1,
                    )
                )

    return indirect_paths


def discover_join_paths(
    catalog: CatalogStore,
    source_id: str,
    embedder: Embedder | None = None,
) -> list[JoinPath]:
    """
    Discover all JOIN paths for a given source.
    Returns direct paths from three signals + indirect 1-hop paths.
    """
    tables = catalog.get_tables(source_id)
    all_table_cols: list[dict] = []
    for t in tables:
        cols = catalog.get_columns(source_id, t["table_name"])
        all_table_cols.append(
            {
                "source_id": source_id,
                "table_name": t["table_name"],
                "columns": [
                    {"column_name": c["column_name"], "dtype": c["dtype"]} for c in cols
                ],
            }
        )

    pair_candidates: dict[str, list[JoinPath]] = {}

    # Signal 1: FK constraints
    _signal1_fk(all_table_cols, catalog, source_id, pair_candidates)

    # Signal 2: Column name matching
    _signal2_column_names(all_table_cols, source_id, pair_candidates)

    # Signal 3: Embedding similarity
    if embedder and embedder.is_ready():
        _signal3_embedding(all_table_cols, catalog, embedder, source_id, pair_candidates)

    # Fusion
    direct_paths = _fuse_candidates(pair_candidates)

    # Indirect paths
    table_names = [tc["table_name"] for tc in all_table_cols]
    indirect_paths = _find_indirect_paths(direct_paths, table_names, source_id)

    return direct_paths + indirect_paths


def discover_cross_source_join_paths(
    catalog: CatalogStore,
    embedder: Embedder | None = None,
) -> list[JoinPath]:
    """
    Discover JOIN paths across ALL sources.
    Gathers tables from every source and runs column-name matching (Signal 2) + embedding (Signal 3)
    across source boundaries. FK constraints (Signal 1) are only added for same-source pairs.
    """
    sources = catalog.get_sources()
    all_table_cols: list[dict] = []

    for src in sources:
        tables = catalog.get_tables(src["id"])
        for t in tables:
            cols = catalog.get_columns(src["id"], t["table_name"])
            all_table_cols.append(
                {
                    "source_id": src["id"],
                    "table_name": t["table_name"],
                    "columns": [
                        {"column_name": c["column_name"], "dtype": c["dtype"]} for c in cols
                    ],
                }
            )

    if len(all_table_cols) < 2:
        return []

    pair_candidates: dict[str, list[JoinPath]] = {}

    # Signal 1: FK constraints (only for same-source pairs)
    _signal1_fk_cross(all_table_cols, catalog, pair_candidates)

    # Signal 2: Column name matching (across all tables)
    _signal2_column_names(
        all_table_cols, CROSS_SOURCE_ID, pair_candidates, skip_same_name=True
    )

    # Signal 3: Embedding similarity
    if embedder and embedder.is_ready():
        _signal3_embedding(
            all_table_cols,
            catalog,
            embedder,
            CROSS_SOURCE_ID,
            pair_candidates,
            skip_same_name=True,
        )

    # Fusion
    direct_paths = _fuse_candidates(pair_candidates)

    # Indirect paths
    table_names = [tc["table_name"] for tc in all_table_cols]
    indirect_paths = _find_indirect_paths(direct_paths, table_names, CROSS_SOURCE_ID)

    return direct_paths + indirect_paths
