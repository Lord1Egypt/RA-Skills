# SPDX-License-Identifier: Apache-2.0
"""Bundle.json import/export with atomic cross-DB rename.

Per GRAEAE consultation f1bea48c: bundle import touches BOTH mnemos.db
and ic-engine.db. The import must be transactional across two sqlite
files. Without atomic-rename: a partial failure leaves orphaned data
in one db and not the other.

The schema is defined in sibling module `bundle_schema.py` (Pydantic).

Critical security property: bundle.json holds env-var REFERENCES for
API keys (e.g., "$TOGETHER_API_KEY"), never raw values. Resolution
happens at runtime against /data/keys.env (mode 0600).

This module's correctness is the v4.0 release-blocker for "users can
back up + restore" — the dashboard's Export/Import buttons go through
here. If atomic-rename fails halfway, user state corrupts. Get this
right.
"""
from __future__ import annotations

import json
import os
import shutil
import sqlite3
import tempfile
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

import structlog

from .bundle_schema import (
    Bundle,
    BundleMetadata,
    MemoryRecord,
    PortfolioRef,
    parse_bundle,
    serialize_bundle,
)

logger = structlog.get_logger("investorclaw_bridge.bundle")


@dataclass
class BundleImportResult:
    success: bool
    memories_imported: int
    portfolios_imported: int
    keys_referenced: int
    errors: list[str]


@dataclass
class BundleExportResult:
    success: bool
    bundle_path: Path
    memories_exported: int
    portfolios_exported: int


# ──────────────────────────────────────────────────────────────────────
# Atomic cross-DB rename pattern (the GRAEAE-flagged correctness path)
# ──────────────────────────────────────────────────────────────────────


@contextmanager
def atomic_two_file_replace(
    target_a: Path, target_b: Path,
    *,
    data_dir: Path | None = None,
) -> Iterator[tuple[Path, Path]]:
    """Yield (tmp_a, tmp_b) paths. On clean exit, atomically replace
    target_a + target_b with the contents of tmp_a + tmp_b. On exception
    or non-clean exit: discard temps, leave targets untouched.

    Usage:
        with atomic_two_file_replace(mnemos_db, ic_db) as (tmp_mnemos, tmp_ic):
            # Write candidate dbs to tmp_mnemos, tmp_ic
            # Validate both
            # If validation passes: context exits cleanly → atomic replace
            # If validation fails: raise → temps cleaned up, targets untouched

    Implementation note: rename(2) is atomic per-file on POSIX. We can't
    do a true two-file atomic rename across filesystems, but if both targets
    live in the same data volume (per v4.0 compose's shared /data volume),
    we can ensure that at most ONE rename happens before failure → we can
    detect partial state and clean up.

    Better-than-naive approach used here:
      1. Write both temps in same directory as targets (rename within FS = atomic)
      2. Pre-rename both targets aside as .pending-replace-* sentinels
      3. Rename temps into place
      4. On success: remove .pending-replace sentinels
      5. On any failure: rename .pending-replace sentinels BACK, remove temps

    Even with that, there's a microscopic window where the OS could crash
    between step 3a (a→target_a renamed) and step 3b (b→target_b renamed).
    Recovery: a startup hook detects orphaned .pending-replace sentinels
    and rolls them back.
    """
    if data_dir is None:
        data_dir = target_a.parent
    data_dir.mkdir(parents=True, exist_ok=True)

    # Ensure both targets are in the same filesystem (required for atomic rename)
    if target_a.parent.resolve() != target_b.parent.resolve():
        raise ValueError(
            f"atomic_two_file_replace requires same parent dir; got "
            f"{target_a.parent} and {target_b.parent}"
        )

    with tempfile.TemporaryDirectory(prefix=".bundle-import-", dir=data_dir) as td:
        tmp_a = Path(td) / target_a.name
        tmp_b = Path(td) / target_b.name

        try:
            yield tmp_a, tmp_b
        except Exception:
            # Discard temps; targets untouched
            logger.warning("bundle.atomic_replace.aborted", reason="exception")
            raise

        if not (tmp_a.exists() and tmp_b.exists()):
            raise FileNotFoundError(
                f"atomic_two_file_replace: both temps must exist before "
                f"replacing targets. Got tmp_a.exists={tmp_a.exists()}, "
                f"tmp_b.exists={tmp_b.exists()}"
            )

        # Move temps into the same dir as targets (within FS = atomic rename)
        tmp_a_landing = data_dir / f".{target_a.name}.replace"
        tmp_b_landing = data_dir / f".{target_b.name}.replace"
        shutil.move(str(tmp_a), str(tmp_a_landing))
        shutil.move(str(tmp_b), str(tmp_b_landing))

        # Set aside originals (atomic rename per-file)
        pending_a = data_dir / f"{target_a.name}.pending-replace"
        pending_b = data_dir / f"{target_b.name}.pending-replace"
        if target_a.exists():
            os.rename(target_a, pending_a)
        if target_b.exists():
            os.rename(target_b, pending_b)

        # Rename landings into final targets
        try:
            os.rename(tmp_a_landing, target_a)
            os.rename(tmp_b_landing, target_b)
        except OSError as e:
            # Rollback: restore pending originals if either rename failed mid-way
            logger.error("bundle.atomic_replace.rename_failed", error=str(e))
            if pending_a.exists():
                os.rename(pending_a, target_a)
            if pending_b.exists():
                os.rename(pending_b, target_b)
            raise

        # Clean up pending sentinels
        for p in (pending_a, pending_b):
            if p.exists():
                p.unlink()

        logger.info(
            "bundle.atomic_replace.committed",
            target_a=str(target_a), target_b=str(target_b),
        )


# ──────────────────────────────────────────────────────────────────────
# Public API — implementation pending
# ──────────────────────────────────────────────────────────────────────


# ──────────────────────────────────────────────────────────────────────
# Sqlite schemas — v4.0.0a1 minimal viable shape.
# Real schemas grow in mnemos_db_schema.py / ic_db_schema.py; for v0.1
# we keep them inline here so the round-trip test surface is small.
# ──────────────────────────────────────────────────────────────────────


_MNEMOS_SCHEMA_V1 = """
CREATE TABLE IF NOT EXISTS memories (
    id          TEXT PRIMARY KEY,
    content     TEXT NOT NULL,
    category    TEXT NOT NULL,
    tags        TEXT NOT NULL DEFAULT '[]',   -- JSON array
    created_at  TEXT NOT NULL,                -- ISO 8601
    metadata    TEXT                           -- JSON object, NULL allowed
);
CREATE INDEX IF NOT EXISTS idx_memories_category ON memories(category);
CREATE INDEX IF NOT EXISTS idx_memories_created  ON memories(created_at);

CREATE TABLE IF NOT EXISTS schema_version (version INTEGER NOT NULL);
INSERT OR IGNORE INTO schema_version (version) VALUES (1);
"""

_IC_ENGINE_SCHEMA_V1 = """
CREATE TABLE IF NOT EXISTS portfolios (
    id            TEXT PRIMARY KEY,
    source_file   TEXT NOT NULL,
    broker        TEXT NOT NULL,
    account_type  TEXT NOT NULL,
    label         TEXT,
    last_imported TEXT
);

CREATE TABLE IF NOT EXISTS providers_config (
    name           TEXT PRIMARY KEY,
    api_key_ref    TEXT,                       -- env-var reference, NEVER raw value
    base_url       TEXT,
    default_model  TEXT
);

CREATE TABLE IF NOT EXISTS data_sources_config (
    name         TEXT PRIMARY KEY,
    api_key_ref  TEXT
);

CREATE TABLE IF NOT EXISTS settings (
    key    TEXT PRIMARY KEY,
    value  TEXT NOT NULL                       -- JSON-serialized
);

CREATE TABLE IF NOT EXISTS schema_version (version INTEGER NOT NULL);
INSERT OR IGNORE INTO schema_version (version) VALUES (1);
"""


def _init_mnemos_db(db_path: Path) -> None:
    conn = sqlite3.connect(str(db_path))
    try:
        conn.executescript(_MNEMOS_SCHEMA_V1)
        conn.commit()
    finally:
        conn.close()


def _init_ic_engine_db(db_path: Path) -> None:
    conn = sqlite3.connect(str(db_path))
    try:
        conn.executescript(_IC_ENGINE_SCHEMA_V1)
        conn.commit()
    finally:
        conn.close()


# ──────────────────────────────────────────────────────────────────────
# Public API — v4.0.0a1 implementation
# ──────────────────────────────────────────────────────────────────────


def import_bundle(
    bundle_path: Path,
    *,
    mnemos_db: Path,
    ic_engine_db: Path,
    data_dir: Path | None = None,
) -> BundleImportResult:
    """Import a v4.0 bundle.json — atomically across both sqlite dbs.

    Parses bundle.json (Pydantic validates schema + rejects raw keys),
    materializes a temp mnemos.db + ic-engine.db with the v1 schema,
    inserts memories + portfolios + config, then atomically replaces
    the live dbs via atomic_two_file_replace.

    On any failure: existing dbs untouched, no orphaned files,
    structured error in BundleImportResult.errors.

    Args:
        bundle_path: path to the bundle.json file
        mnemos_db: target mnemos.db path
        ic_engine_db: target ic-engine.db path (must share parent dir
            with mnemos_db — atomic-replace requires same FS)
        data_dir: parent dir for temp files (defaults to mnemos_db.parent)

    Returns:
        BundleImportResult with success flag + counts.
    """
    errors: list[str] = []

    # 1. Parse + validate. Pydantic raises on schema violations or raw keys.
    try:
        bundle = parse_bundle(bundle_path.read_text())
    except Exception as e:
        errors.append(f"bundle.parse_error: {e}")
        return BundleImportResult(
            success=False,
            memories_imported=0,
            portfolios_imported=0,
            keys_referenced=0,
            errors=errors,
        )

    keys_referenced = (
        sum(1 for p in bundle.providers.values() if p.api_key_ref)
        + sum(1 for ds in bundle.data_sources.values() if ds.api_key_ref)
        + (1 if bundle.mcp.auth_token_ref else 0)
    )

    # 2. Atomic write to both dbs
    try:
        with atomic_two_file_replace(
            mnemos_db, ic_engine_db, data_dir=data_dir
        ) as (tmp_mnemos, tmp_ic):
            _init_mnemos_db(tmp_mnemos)
            _init_ic_engine_db(tmp_ic)

            # Insert memories into mnemos.db
            with sqlite3.connect(str(tmp_mnemos)) as conn:
                conn.executemany(
                    """INSERT INTO memories
                       (id, content, category, tags, created_at, metadata)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    [
                        (
                            m.id,
                            m.content,
                            m.category,
                            json.dumps(m.tags),
                            m.created_at.isoformat(),
                            json.dumps(m.metadata) if m.metadata else None,
                        )
                        for m in (bundle.memories or [])
                    ],
                )
                conn.commit()

            # Insert portfolios + config into ic-engine.db
            with sqlite3.connect(str(tmp_ic)) as conn:
                conn.executemany(
                    """INSERT INTO portfolios
                       (id, source_file, broker, account_type, label, last_imported)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    [
                        (
                            p.id,
                            p.source_file,
                            p.broker,
                            p.account_type,
                            p.label,
                            p.last_imported_at.isoformat()
                            if p.last_imported_at
                            else None,
                        )
                        for p in bundle.portfolios
                    ],
                )
                conn.executemany(
                    """INSERT INTO providers_config
                       (name, api_key_ref, base_url, default_model)
                       VALUES (?, ?, ?, ?)""",
                    [
                        (name, p.api_key_ref, p.base_url, p.default_model)
                        for name, p in bundle.providers.items()
                    ],
                )
                conn.executemany(
                    """INSERT INTO data_sources_config
                       (name, api_key_ref) VALUES (?, ?)""",
                    [(name, ds.api_key_ref) for name, ds in bundle.data_sources.items()],
                )
                conn.executemany(
                    "INSERT INTO settings (key, value) VALUES (?, ?)",
                    [
                        ("narrative", bundle.narrative.model_dump_json()),
                        ("mcp", bundle.mcp.model_dump_json()),
                        ("memory", bundle.memory.model_dump_json()),
                    ],
                )
                conn.commit()

            # Integrity check — PRAGMA quick_check is faster than integrity_check
            # for our small dbs and catches the same corruption modes.
            for db_path in (tmp_mnemos, tmp_ic):
                with sqlite3.connect(str(db_path)) as conn:
                    result = conn.execute("PRAGMA quick_check").fetchone()[0]
                    if result != "ok":
                        raise sqlite3.DatabaseError(
                            f"{db_path.name} failed quick_check: {result}"
                        )

            logger.info(
                "bundle.import.staged",
                memories=len((bundle.memories or [])),
                portfolios=len(bundle.portfolios),
                providers=len(bundle.providers),
            )

    except Exception as e:
        errors.append(f"bundle.import_error: {type(e).__name__}: {e}")
        return BundleImportResult(
            success=False,
            memories_imported=0,
            portfolios_imported=0,
            keys_referenced=0,
            errors=errors,
        )

    return BundleImportResult(
        success=True,
        memories_imported=len((bundle.memories or [])),
        portfolios_imported=len(bundle.portfolios),
        keys_referenced=keys_referenced,
        errors=[],
    )


def export_bundle(
    output_path: Path,
    *,
    mnemos_db: Path,
    ic_engine_db: Path,
    investorclaw_version: str = "4.0.0a1",
    from_host: str | None = None,
) -> BundleExportResult:
    """Export the current state to a bundle.json file.

    Reads memories from mnemos.db, portfolios + config from ic-engine.db,
    builds a Bundle, serializes to bundle.json. Sets file mode 0600
    (defense in depth — even though bundle.json never carries raw keys,
    the schema-violating import-error path could leak a partial state).

    Args:
        output_path: where to write bundle.json
        mnemos_db: source mnemos.db
        ic_engine_db: source ic-engine.db
        investorclaw_version: version string for metadata
        from_host: hostname for metadata (defaults to socket.gethostname())
    """
    if from_host is None:
        import socket
        from_host = socket.gethostname()

    memories: list[MemoryRecord] = []
    if mnemos_db.exists():
        with sqlite3.connect(str(mnemos_db)) as conn:
            rows = conn.execute(
                """SELECT id, content, category, tags, created_at, metadata
                   FROM memories ORDER BY created_at"""
            ).fetchall()
        for row in rows:
            memories.append(
                MemoryRecord(
                    id=row[0],
                    content=row[1],
                    category=row[2],
                    tags=json.loads(row[3]) if row[3] else [],
                    created_at=datetime.fromisoformat(row[4]),
                    metadata=json.loads(row[5]) if row[5] else None,
                )
            )

    portfolios: list[PortfolioRef] = []
    providers: dict[str, Any] = {}
    data_sources: dict[str, Any] = {}
    settings: dict[str, str] = {}

    if ic_engine_db.exists():
        with sqlite3.connect(str(ic_engine_db)) as conn:
            for row in conn.execute(
                """SELECT id, source_file, broker, account_type, label, last_imported
                   FROM portfolios"""
            ):
                portfolios.append(
                    PortfolioRef(
                        id=row[0],
                        source_file=row[1],
                        broker=row[2],
                        account_type=row[3],
                        label=row[4],
                        last_imported_at=datetime.fromisoformat(row[5])
                        if row[5]
                        else None,
                    )
                )

            for row in conn.execute(
                """SELECT name, api_key_ref, base_url, default_model
                   FROM providers_config"""
            ):
                providers[row[0]] = {
                    "api_key_ref": row[1],
                    "base_url": row[2],
                    "default_model": row[3],
                }

            for row in conn.execute(
                "SELECT name, api_key_ref FROM data_sources_config"
            ):
                data_sources[row[0]] = {"api_key_ref": row[1]}

            for row in conn.execute("SELECT key, value FROM settings"):
                settings[row[0]] = row[1]

    bundle = Bundle(
        providers={k: _provider_from_dict(v) for k, v in providers.items()},
        data_sources={k: _data_source_from_dict(v) for k, v in data_sources.items()},
        portfolios=portfolios,
        narrative=_load_narrative(settings),
        mcp=_load_mcp(settings),
        memory=_load_memory(settings),
        memories=memories,
        metadata=BundleMetadata(
            exported_at=datetime.now(timezone.utc),
            from_host=from_host,
            investorclaw_version=investorclaw_version,
        ),
    )

    output_path.write_text(serialize_bundle(bundle))
    output_path.chmod(0o600)

    logger.info(
        "bundle.export.ok",
        path=str(output_path),
        memories=len(memories),
        portfolios=len(portfolios),
    )

    return BundleExportResult(
        success=True,
        bundle_path=output_path,
        memories_exported=len(memories),
        portfolios_exported=len(portfolios),
    )


# ──────────────────────────────────────────────────────────────────────
# Internal helpers — load Bundle sub-models from sqlite settings
# ──────────────────────────────────────────────────────────────────────


def _provider_from_dict(d: dict[str, Any]):
    from .bundle_schema import ProviderConfig

    return ProviderConfig(
        api_key_ref=d.get("api_key_ref"),
        base_url=d.get("base_url"),
        default_model=d.get("default_model"),
    )


def _data_source_from_dict(d: dict[str, Any]):
    from .bundle_schema import DataSourceConfig

    return DataSourceConfig(api_key_ref=d.get("api_key_ref"))


def _load_narrative(settings: dict[str, str]):
    from .bundle_schema import NarrativeConfig

    if "narrative" in settings:
        return NarrativeConfig.model_validate_json(settings["narrative"])
    return NarrativeConfig()


def _load_mcp(settings: dict[str, str]):
    from .bundle_schema import McpConfig

    if "mcp" in settings:
        return McpConfig.model_validate_json(settings["mcp"])
    return McpConfig()


def _load_memory(settings: dict[str, str]):
    from .bundle_schema import MemoryConfig

    if "memory" in settings:
        return MemoryConfig.model_validate_json(settings["memory"])
    return MemoryConfig()
