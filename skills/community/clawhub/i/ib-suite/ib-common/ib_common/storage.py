"""Local data lake: instantaneous JSON snapshots + append-only Parquet history.

Snapshots capture point-in-time state (one file per sync). Time-series
tables accumulate history and are de-duplicated on every append so repeated
syncs are idempotent.
"""
from __future__ import annotations
from pathlib import Path
import pandas as pd
from pydantic import BaseModel

from .schema import Snapshot


def write_snapshot(snap: Snapshot, root: str | Path) -> Path:
    """Write a snapshot as JSON under root/snapshots/<account_id>/<ts>.json."""
    ts_key = snap.ts.strftime("%Y%m%dT%H%M%SZ")
    out_dir = Path(root) / "snapshots" / snap.account.account_id
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{ts_key}.json"
    out.write_text(snap.model_dump_json(indent=2), encoding="utf-8")
    return out


def append_timeseries(rows: list[BaseModel], root: str | Path, name: str) -> Path:
    """Append pydantic rows to root/timeseries/<name>.parquet, deduped on all cols."""
    out_dir = Path(root) / "timeseries"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{name}.parquet"

    new_df = pd.DataFrame([r.model_dump() for r in rows])
    if out.exists():
        existing = pd.read_parquet(out)
        combined = pd.concat([existing, new_df], ignore_index=True)
    else:
        combined = new_df
    combined = combined.drop_duplicates().reset_index(drop=True)
    combined.to_parquet(out, index=False)
    return out


def read_timeseries(root: str | Path, name: str) -> pd.DataFrame:
    """Read a time-series parquet; return an empty DataFrame if it does not exist."""
    out = Path(root) / "timeseries" / f"{name}.parquet"
    if not out.exists():
        return pd.DataFrame()
    return pd.read_parquet(out)
