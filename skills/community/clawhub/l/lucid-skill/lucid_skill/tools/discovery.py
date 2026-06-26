"""get_join_paths / get_business_domains tool handlers."""

from __future__ import annotations

import json
from typing import Any

from lucid_skill.catalog.store import CatalogStore
from lucid_skill.discovery.domains import discover_business_domains
from lucid_skill.discovery.joins import (
    CROSS_SOURCE_ID,
    compute_cross_source_schema_hash,
    compute_schema_hash,
    discover_cross_source_join_paths,
    discover_join_paths,
)
from lucid_skill.semantic.embedder import Embedder


def handle_get_join_paths(
    params: dict[str, Any],
    catalog: CatalogStore,
    embedder: Embedder | None = None,
) -> str:
    """Discover and return JOIN paths between two tables.

    Checks cache, re-discovers if dirty, returns direct + indirect paths.
    """
    table_a: str | None = params.get("table_a")
    table_b: str | None = params.get("table_b")

    if not table_a or not table_b:
        raise ValueError("Both table_a and table_b are required")

    # Find which source(s) contain these tables
    all_tables = catalog.get_tables()
    sources_for_a = {t["source_id"] for t in all_tables if t["table_name"] == table_a}
    sources_for_b = {t["source_id"] for t in all_tables if t["table_name"] == table_b}

    # Validate both tables exist
    if not sources_for_a:
        raise ValueError(f'Table "{table_a}" not found in any connected source')
    if not sources_for_b:
        raise ValueError(f'Table "{table_b}" not found in any connected source')

    # Find common sources or all relevant sources
    relevant_sources: set[str] = sources_for_a & sources_for_b
    # If no common source, include all sources (cross-source join)
    if not relevant_sources:
        relevant_sources = sources_for_a | sources_for_b

    # For each relevant source, check cache and discover if needed (within-source paths)
    for source_id in relevant_sources:
        meta = catalog.get_cache_meta(source_id)
        current_hash = compute_schema_hash(catalog, source_id)

        needs_refresh = (
            not meta
            or meta.dirty == 1
            or meta.schema_hash != current_hash
        )

        if needs_refresh:
            catalog.clear_join_paths(source_id)
            paths = discover_join_paths(catalog, source_id, embedder)
            for p in paths:
                catalog.save_join_path(p)
            catalog.set_cache_meta(source_id, current_hash)

    # Cross-source discovery: check cache and discover if needed
    cross_meta = catalog.get_cache_meta(CROSS_SOURCE_ID)
    cross_hash = compute_cross_source_schema_hash(catalog)
    needs_cross_refresh = (
        not cross_meta
        or cross_meta.dirty == 1
        or cross_meta.schema_hash != cross_hash
    )

    if needs_cross_refresh:
        catalog.clear_join_paths(CROSS_SOURCE_ID)
        cross_paths = discover_cross_source_join_paths(catalog, embedder)
        for p in cross_paths:
            catalog.save_join_path(p)
        catalog.set_cache_meta(CROSS_SOURCE_ID, cross_hash)

    # Fetch paths for the requested table pair (includes both within-source and cross-source)
    paths = catalog.get_join_paths(table_a, table_b)

    direct_paths = [p for p in paths if not p.signal_source.startswith("indirect:")]
    indirect_paths = [p for p in paths if p.signal_source.startswith("indirect:")]

    has_low_confidence = any(p.confidence < 0.6 for p in paths)
    warning = "low confidence, manual verification recommended" if has_low_confidence else None

    return json.dumps(
        {
            "direct_paths": [
                {
                    "join_sql": p.sql_template,
                    "confidence": round(p.confidence * 100) / 100,
                    "signal": p.signal_source,
                    "join_condition": p.join_condition,
                }
                for p in direct_paths
            ],
            "indirect_paths": [
                {
                    "via": p.signal_source.replace("indirect:via_", ""),
                    "join_sql": p.sql_template,
                    "confidence": round(p.confidence * 100) / 100,
                    "signal": p.signal_source,
                    "join_condition": p.join_condition,
                }
                for p in indirect_paths
            ],
            "warning": warning,
        },
        indent=2,
    )


def handle_get_business_domains(
    params: dict[str, Any],
    catalog: CatalogStore,
    embedder: Embedder | None = None,
) -> str:
    """Discover and return business domain clusters.

    Checks cache, re-clusters if needed, returns domains.
    """
    datasource: str | None = params.get("datasource")

    # Determine which sources need refresh
    all_sources = catalog.get_sources()
    sources = (
        [s for s in all_sources if s["id"] == datasource]
        if datasource
        else all_sources
    )

    if len(sources) == 0 and datasource:
        raise ValueError(f'Data source "{datasource}" not found')

    # Check if any source is dirty or has changed schema
    needs_refresh = False
    for source in sources:
        meta = catalog.get_cache_meta(source["id"])
        current_hash = compute_schema_hash(catalog, source["id"])
        if not meta or meta.dirty == 1 or meta.schema_hash != current_hash:
            needs_refresh = True
            break

    # Also refresh if no domains exist yet
    if not needs_refresh and len(catalog.get_domains()) == 0:
        needs_refresh = True

    if needs_refresh:
        catalog.clear_domains()
        domains = discover_business_domains(catalog, embedder)
        for d in domains:
            catalog.save_domain(d)
        # Update cache for all sources
        for source in sources:
            hash_val = compute_schema_hash(catalog, source["id"])
            catalog.set_cache_meta(source["id"], hash_val)

    domains = catalog.get_domains()

    # Filter by datasource if specified
    filtered_domains = domains
    if datasource:
        source_tables = {
            t["table_name"] for t in catalog.get_tables(datasource)
        }
        filtered_domains = []
        for d in domains:
            filtered_table_names = [t for t in d.table_names if t in source_tables]
            if filtered_table_names:
                from lucid_skill.types import BusinessDomain

                filtered_domains.append(
                    BusinessDomain(
                        domain_id=d.domain_id,
                        domain_name=d.domain_name,
                        table_names=filtered_table_names,
                        keywords=d.keywords,
                        created_at=d.created_at,
                        version=d.version,
                    )
                )

    # Compute unclustered tables
    all_tables = (
        catalog.get_tables(datasource) if datasource else catalog.get_tables()
    )
    clustered_tables = {t for d in filtered_domains for t in d.table_names}
    unclustered = [
        t["table_name"] for t in all_tables if t["table_name"] not in clustered_tables
    ]

    return json.dumps(
        {
            "domains": [
                {
                    "name": d.domain_name,
                    "tables": d.table_names,
                    "keywords": d.keywords,
                    "table_count": len(d.table_names),
                }
                for d in filtered_domains
            ],
            "total_tables": len(all_tables),
            "unclustered": unclustered,
        },
        indent=2,
    )
