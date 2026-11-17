"""Audit the Living Memory Library index (v1.2).

Pure advisor: local inspection only. No network.

Usage:
  python scripts/audit_library.py [--base <LYGO_AUTHORITY_ROOT>]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve_base(arg: str | None) -> Path:
    if arg:
        return Path(arg).expanduser().resolve()
    for key in ("LYGO_AUTHORITY_ROOT", "LYGO_WORKSPACE_ROOT"):
        val = os.environ.get(key, "").strip()
        if val:
            return Path(val).expanduser().resolve()
    # skill/scripts -> stack root -> parent = typical E Drive workspace
    stack = Path(__file__).resolve().parents[4]
    if (stack / "docs" / "LYGO_LATTICE.md").is_file():
        return stack.parent.resolve()
    return stack.resolve()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default=None, help="Authority root (default: env or stack parent)")
    args = ap.parse_args()

    base = resolve_base(args.base)
    idx_path = Path(__file__).resolve().parents[1] / "references" / "core_files_index.json"

    try:
        idx = json.loads(idx_path.read_text(encoding="utf-8"))
    except Exception as e:
        print("BAD_INDEX", e)
        raise SystemExit(2)

    items = idx.get("items") or []
    max_items = int(idx.get("maxItems") or 20)
    if len(items) > max_items:
        print("TOO_MANY_ITEMS", len(items), "max", max_items)
        raise SystemExit(2)

    missing: list[str] = []
    fragile: list[str] = []
    report: list[dict] = []

    for it in items:
        rel = it.get("path")
        role = it.get("role")
        tags = set(it.get("tags") or [])
        p = (base / rel).resolve()
        exists = p.exists()
        row: dict = {
            "path": rel,
            "role": role,
            "tags": sorted(tags),
            "exists": exists,
        }
        if not exists:
            missing.append(rel)
        else:
            st = p.stat()
            row["mtime"] = int(st.st_mtime)
            row["size"] = int(st.st_size)
            if p.is_file():
                row["sha256"] = sha256_file(p)
            else:
                row["sha256"] = None
        if "FRAGILE" in tags:
            fragile.append(rel)
        report.append(row)

    print("LIVING_MEMORY_AUDIT v1.2")
    print("base", str(base))
    print("items", len(items))
    print("missing", len(missing))
    print("fragile", len(fragile))

    if missing:
        print("\nMISSING_ITEMS:")
        for m in missing:
            print(" -", m)
    if fragile:
        print("\nFRAGILE_ITEMS (manual review before minting):")
        for f in fragile:
            print(" -", f)

    state_dir = (
        base / "LYRA_CORE" / "state"
        if (base / "LYRA_CORE").is_dir()
        else base / "state"
    )
    state_dir.mkdir(parents=True, exist_ok=True)
    out_path = state_dir / "living_memory_audit_report.json"
    out_path.write_text(
        json.dumps({"index_version": idx.get("version"), "base": str(base), "report": report}, indent=2),
        encoding="utf-8",
    )
    print("\nREPORT_JSON", str(out_path))

    if missing:
        raise SystemExit(2)
    if fragile:
        raise SystemExit(1)
    raise SystemExit(0)


if __name__ == "__main__":
    main()