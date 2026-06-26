#!/usr/bin/env python3
"""HyperMemory-4D Micro-Index Builder
MVP: build thin index + shard latest records from memory master index.
"""
from __future__ import annotations

from pathlib import Path
import os
import argparse
import json
from typing import Any, Dict, List

WORKSPACE = Path(os.environ.get('OPENCLAW_WORKSPACE', str(Path.home() / '.openclaw' / 'workspace')))
DEFAULT_INPUT = WORKSPACE / "memory" / "index" / "memory-master-index.json"
DEFAULT_OUTPUT_DIR = WORKSPACE / "memory" / "index" / "shards"
DEFAULT_THIN_INDEX = WORKSPACE / "memory" / "index" / "thin-index.json"


class MicroIndexBuilder:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_master_index(self, path: Path) -> Dict[str, Any]:
        if not path.exists():
            raise FileNotFoundError(f"missing master index: {path}")
        return json.loads(path.read_text(encoding="utf-8"))

    def latest_records(self, payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        items = payload.get("latest_records", [])
        if not isinstance(items, list):
            return []
        return items

    def create_thin_index(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        thin: List[Dict[str, Any]] = []
        for r in records:
            thin.append({
                "id": r.get("id"),
                "type": r.get("type"),
                "title": (r.get("title") or "")[:100],
                "source_path": r.get("source_path"),
                "record_class": r.get("record_class"),
                "sync_policy": r.get("sync_policy"),
                "vector_profile": r.get("vector_profile"),
                "salience_level": r.get("salience_level"),
                "retention_tier": r.get("retention_tier"),
                "priority": r.get("priority", 5),
            })
        return thin

    def save_thin_index(self, thin: List[Dict[str, Any]], path: Path) -> None:
        path.write_text(json.dumps(thin, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def save_shards(self, records: List[Dict[str, Any]], prefix: str, shard_size: int) -> List[str]:
        shard_files: List[str] = []
        if not records:
            return shard_files
        for start in range(0, len(records), shard_size):
            shard = records[start:start + shard_size]
            shard_idx = start // shard_size
            shard_path = self.output_dir / f"{prefix}.shard-{shard_idx:04d}.json"
            shard_path.write_text(json.dumps(shard, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            shard_files.append(str(shard_path))
        return shard_files

    def build(self, input_path: Path, thin_index_path: Path, shard_size: int) -> Dict[str, Any]:
        payload = self.load_master_index(input_path)
        records = self.latest_records(payload)
        thin = self.create_thin_index(records)
        self.save_thin_index(thin, thin_index_path)
        shard_files = self.save_shards(records, input_path.stem, shard_size)
        return {
            "input": str(input_path),
            "total_records": payload.get("total_records", 0),
            "latest_records": len(records),
            "thin_index": str(thin_index_path),
            "shard_count": len(shard_files),
            "shards": shard_files,
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build HM4D micro index")
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--thin-index", default=str(DEFAULT_THIN_INDEX))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--shard-size", type=int, default=100)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    builder = MicroIndexBuilder(Path(args.output_dir))
    result = builder.build(Path(args.input), Path(args.thin_index), args.shard_size)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
