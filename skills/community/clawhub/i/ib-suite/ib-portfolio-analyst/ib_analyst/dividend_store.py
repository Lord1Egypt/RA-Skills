# skills/ib-portfolio-analyst/ib_analyst/dividend_store.py
"""Normalize parsed dividends into the append-only Parquet lake.

Thin wrapper over ib_common.storage so dividends share the same dedup and
read semantics as every other time-series table. Dates round-trip through
Parquet as native date objects and are re-validated by the Dividend model.
"""
from __future__ import annotations
from pathlib import Path
from ib_common.schema import Dividend
from ib_common.storage import append_timeseries, read_timeseries

_TABLE = "dividends"


def store_dividends(dividends: list[Dividend], root: str | Path) -> Path:
    """Append dividend rows to the lake (deduped); return the parquet path."""
    return append_timeseries(dividends, root, _TABLE)


def load_dividends(root: str | Path) -> list[Dividend]:
    """Read stored dividends back into typed Dividend rows (empty if none)."""
    df = read_timeseries(root, _TABLE)
    if df.empty:
        return []
    out: list[Dividend] = []
    for rec in df.to_dict(orient="records"):
        out.append(Dividend.model_validate(rec))
    return out
