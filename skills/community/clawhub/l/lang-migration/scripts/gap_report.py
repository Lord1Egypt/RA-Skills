#!/usr/bin/env python3
"""
gap_report.py — Migration Completeness Audit for lang-migration skill.

Usage:
    python gap_report.py --workspace migration_workspace/ \
                         --source genericagent/ \
                         --target go-GenericAgent/

Reads: migration-state.yaml, asset-inventory.yaml, ipo-registry.yaml
Walks: source and target directory trees
Outputs: gap-report.md + gap-report.yaml in migration_workspace/
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml --break-system-packages")
    sys.exit(1)


# ─── Loaders ──────────────────────────────────────────────────────────────────

def load_yaml(path: Path) -> dict:
    if not path.exists():
        print(f"WARNING: {path} not found — returning empty dict")
        return {}
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def walk_dirs(root: Path) -> set:
    """Return all subdirectory paths relative to root."""
    result = set()
    for dirpath, dirnames, _ in os.walk(root):
        # Skip hidden and build dirs
        dirnames[:] = [d for d in dirnames if not d.startswith(".")
                       and d not in ("__pycache__", "node_modules", ".git",
                                     "target", "dist", "build", "_build")]
        rel = Path(dirpath).relative_to(root)
        if rel != Path("."):
            result.add(str(rel).replace("\\", "/"))
    return result


def walk_files(root: Path) -> set:
    """Return all file paths relative to root."""
    result = set()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")
                       and d not in ("__pycache__", "node_modules", ".git",
                                     "target", "dist", "build", "_build")]
        for fname in filenames:
            rel = (Path(dirpath) / fname).relative_to(root)
            result.add(str(rel).replace("\\", "/"))
    return result


# ─── Dimension Analysers ──────────────────────────────────────────────────────

def dim1_file_coverage(assets: list, target_root: Path, target_files: set) -> dict:
    """Dimension 1: Source → Target file coverage."""
    result = {
        "translate": {"total": 0, "present": 0, "missing": []},
        "adapt":     {"total": 0, "present": 0, "missing": []},
        "direct_use":{"total": 0, "present": 0, "missing": []},
        "preserve":  {"total": 0, "present": 0, "missing": []},
    }

    for asset in assets:
        strategy = asset.get("migration_strategy", "")
        src_path  = asset.get("path", "")
        tgt_path  = asset.get("target_path", "").strip()

        if strategy not in result:
            continue

        bucket = result[strategy]
        bucket["total"] += 1

        # Determine where to look in target
        if strategy in ("translate", "adapt") and tgt_path:
            exists = tgt_path in target_files
        elif strategy == "direct_use":
            # Check if source filename appears anywhere in target tree
            fname = Path(src_path).name
            exists = any(Path(f).name == fname for f in target_files)
        elif strategy == "preserve":
            fname = Path(src_path).name
            exists = any(Path(f).name == fname for f in target_files)
        else:
            exists = True  # reference_only, generated — no check needed

        if exists:
            bucket["present"] += 1
        else:
            bucket["missing"].append({
                "source": src_path,
                "target_expected": tgt_path or f"(filename: {Path(src_path).name})"
            })

    return result


def dim2_function_coverage(functions: list) -> dict:
    """Dimension 2: Function translation coverage."""
    total = len(functions)
    done_with_lines = []
    done_no_lines   = []
    todo            = []
    blocked         = []

    for fn in functions:
        status = fn.get("translation_status", "TODO")
        target_lines = str(fn.get("target_lines", "")).strip()
        target_file  = str(fn.get("target_impl_file", "")).strip()

        if status == "DONE":
            if target_lines and target_lines != "0":
                done_with_lines.append(fn["id"])
            else:
                done_no_lines.append({
                    "id": fn["id"],
                    "target_impl_file": target_file
                })
        elif status == "BLOCKED":
            blocked.append(fn["id"])
        else:
            todo.append(fn["id"])

    true_pct = round(len(done_with_lines) / total * 100, 1) if total else 0
    todo_cap = 20

    return {
        "total":                total,
        "done_with_lines":      len(done_with_lines),
        "done_no_lines":        len(done_no_lines),
        "done_no_lines_list":   done_no_lines,
        "todo":                 len(todo),
        "todo_list":            todo[:todo_cap],
        "todo_list_truncated":  len(todo) > todo_cap,  # D-4: 明确标注截断
        "blocked":              len(blocked),
        "blocked_list":         blocked,
        "true_completion_pct":  true_pct,
    }


def dim3_directory_coverage(source_root: Path, target_root: Path,
                             src_dirs: set, tgt_dirs: set) -> dict:
    """Dimension 3: Directory structure gap."""

    # Flatten dir names for fuzzy matching
    tgt_leaves = {Path(d).name.lower() for d in tgt_dirs}
    tgt_parts  = set()
    for d in tgt_dirs:
        for part in Path(d).parts:
            tgt_parts.add(part.lower())

    unmapped = []
    for src_dir in sorted(src_dirs):
        parts = [p.lower() for p in Path(src_dir).parts]
        # Check if any part of source path appears in target tree
        matched = any(p in tgt_parts for p in parts)
        if not matched:
            unmapped.append(src_dir)

    # Target dirs not obviously derived from source
    src_parts = set()
    for d in src_dirs:
        for part in Path(d).parts:
            src_parts.add(part.lower())

    unexpected = []
    for tgt_dir in sorted(tgt_dirs):
        parts = [p.lower() for p in Path(tgt_dir).parts]
        matched = any(p in src_parts for p in parts)
        if not matched:
            unexpected.append(tgt_dir)

    return {
        "source_dirs_total":          len(src_dirs),
        "source_dirs_unmapped":       len(unmapped),
        "unmapped_source_dirs":       unmapped[:30],
        "target_dirs_unexpected":     len(unexpected),
        "unexpected_target_dirs":     unexpected[:20],
    }


def dim4_non_code_assets(assets: list, functions: list, target_files: set) -> dict:
    """Dimension 4: Non-code asset coverage."""
    fixtures_total     = 0
    fixtures_present   = 0
    fixtures_missing   = []

    p3_required_total  = 0
    p3_referenced      = 0
    p3_unreferenced    = []

    # Build set of all process.reference values in IPO registry
    ipo_references = set()
    for fn in functions:
        proc = fn.get("process", {}) or {}
        ref  = (proc.get("reference", "") or "").strip()
        if ref:
            ipo_references.add(ref)
        # Also check translation_notes
        notes = (fn.get("translation_notes", "") or "").strip()
        if notes:
            ipo_references.add(notes)

    for asset in assets:
        strategy = asset.get("migration_strategy", "")
        src_path = asset.get("path", "")
        p3_req   = bool(asset.get("p3_required", False))

        if strategy == "direct_use":
            fixtures_total += 1
            fname = Path(src_path).name
            exists = any(Path(f).name == fname for f in target_files)
            if exists:
                fixtures_present += 1
            else:
                fixtures_missing.append(src_path)

        if p3_req:
            p3_required_total += 1
            # Check if this file appears in any IPO reference
            referenced = any(src_path in ref for ref in ipo_references)
            if referenced:
                p3_referenced += 1
            else:
                p3_unreferenced.append(src_path)

    return {
        "fixtures_total":        fixtures_total,
        "fixtures_present":      fixtures_present,
        "fixtures_missing":      fixtures_missing,
        "p3_required_total":     p3_required_total,
        "p3_referenced":         p3_referenced,
        "p3_unreferenced":       p3_unreferenced,
    }


def dim5_skip_classification(assets: list, decisions_log: list,
                              target_files: set, target_lang: str = "target") -> dict:
    """Dimension 5: Intentional skips vs accidental gaps."""

    # Build set of intentionally skipped files from decisions_log
    intentional_ids = set()
    intentional_detail = []
    for entry in decisions_log:
        item_id  = str(entry.get("item_id", ""))
        decision = str(entry.get("decision", ""))
        rat      = str(entry.get("rationale", ""))
        intentional_detail.append({
            "item_id":  item_id,
            "decision": decision,
            "rationale": rat,
        })
        intentional_ids.add(item_id)

    accidental = []
    platform_specific = []
    PLATFORM_KEYWORDS = ("streamlit", "pyqt", "tkinter", "pygame", "pywebview",
                         "stapp", "qtapp", "desktop_pet", "ultralytics", "yolo",
                         "rapidocr", "wechatapp", "ilink", "pyobjc")

    for asset in assets:
        strategy  = asset.get("migration_strategy", "")
        src_path  = asset.get("path", "")
        tgt_path  = asset.get("target_path", "").strip()
        status    = asset.get("status", "")
        notes_raw = (asset.get("notes", "") or "").lower()

        if strategy not in ("translate", "adapt"):
            continue

        # Check if file is in decisions_log
        if any(src_path in iid for iid in intentional_ids):
            continue

        # Check if target actually exists
        if tgt_path and tgt_path in target_files:
            continue
        fname = Path(src_path).name
        if any(Path(f).name == fname for f in target_files):
            continue

        # Classify: platform-specific or accidental?
        is_platform = any(kw in src_path.lower() or kw in notes_raw
                          for kw in PLATFORM_KEYWORDS)
        if is_platform:
            platform_specific.append({
                "source": src_path,
                "reason": f"source-only framework/library — no {target_lang} equivalent"
            })
        else:
            accidental.append({
                "source": src_path,
                "target_expected": tgt_path or "(unknown)",
                "status_in_inventory": status,
            })

    return {
        "intentional_documented":  len(intentional_detail),
        "intentional_detail":      intentional_detail,
        "platform_specific":       len(platform_specific),
        "platform_specific_list":  platform_specific,
        "accidental_gaps":         len(accidental),
        "accidental_list":         accidental,
    }


# ─── True Completion Rate ──────────────────────────────────────────────────────

def compute_true_completion(d1, d2, d4) -> float:
    """Weighted true 1:1 completion rate."""
    # Files: translate + adapt
    files_expected = d1["translate"]["total"] + d1["adapt"]["total"]
    files_done     = d1["translate"]["present"] + d1["adapt"]["present"]

    # Functions
    fn_expected = d2["total"]
    fn_done     = d2["done_with_lines"]

    # Fixtures
    fix_expected = d4["fixtures_total"]
    fix_done     = d4["fixtures_present"]

    total_expected = files_expected + fn_expected + fix_expected
    total_done     = files_done + fn_done + fix_done

    if total_expected == 0:
        return 0.0
    return round(total_done / total_expected * 100, 1)


# ─── Report Rendering ──────────────────────────────────────────────────────────

def render_markdown(state: dict, d1, d2, d3, d4, d5, true_pct: float,
                    source_dir: str, target_dir: str, target_exists: bool = True) -> str:
    meta = state.get("meta", {})
    now  = datetime.now().strftime("%Y-%m-%d %H:%M")

    def pct(a, b):
        return f"{round(a/b*100,1)}%" if b else "N/A"

    target_label = f"`{target_dir}`" if target_exists else f"`{target_dir}` ⚠️ **DIRECTORY NOT FOUND — all coverage metrics reflect missing target**"
    lines = [
        "# Migration Completeness Audit",
        f"**Project**: {meta.get('project_name', '?')}  ",
        f"**Generated**: {now}  ",
        f"**Source**: `{source_dir}`  **Target**: {target_label}  ",
        f"**Language pair**: {meta.get('source_lang','?')} → {meta.get('target_lang','?')}",
        "",
        "---",
        "",
        "## Summary",
        "",
        "| Dimension | Metric | Value |",
        "|---|---|---|",
        f"| File Coverage | translate files present | {d1['translate']['present']}/{d1['translate']['total']} ({pct(d1['translate']['present'], d1['translate']['total'])}) |",
        f"| File Coverage | adapt files present | {d1['adapt']['present']}/{d1['adapt']['total']} ({pct(d1['adapt']['present'], d1['adapt']['total'])}) |",
        f"| File Coverage | direct_use present | {d1['direct_use']['present']}/{d1['direct_use']['total']} ({pct(d1['direct_use']['present'], d1['direct_use']['total'])}) |",
        f"| Function Coverage | genuinely DONE (with target_lines) | {d2['done_with_lines']}/{d2['total']} ({pct(d2['done_with_lines'], d2['total'])}) |",
        f"| Function Coverage | ⚠️ DONE but no evidence | {d2['done_no_lines']} |",
        f"| Function Coverage | TODO/BLOCKED | {d2['todo'] + d2['blocked']} |",
        f"| Directory Coverage | unmapped source dirs | {d3['source_dirs_unmapped']}/{d3['source_dirs_total']} |",
        f"| Non-code Assets | fixtures in target | {d4['fixtures_present']}/{d4['fixtures_total']} |",
        f"| Non-code Assets | p3-required docs referenced | {d4['p3_referenced']}/{d4['p3_required_total']} |",
        f"| Skip Classification | intentional (documented) | {d5['intentional_documented']} |",
        f"| Skip Classification | platform-specific Python | {d5['platform_specific']} |",
        f"| Skip Classification | ⚠️ accidental gaps | {d5['accidental_gaps']} |",
        "",
        f"### TRUE 1:1 COMPLETION: **{true_pct}%**",
        "",
        "---",
        "",
    ]

    # Priority action items
    actions = []
    if d2["done_no_lines"] > 0:
        actions.append(("🔴", f"CRITICAL: {d2['done_no_lines']} functions marked DONE but have no target_lines — re-verify"))
    if d5["accidental_gaps"] > 0:
        actions.append(("🔴", f"CRITICAL: {d5['accidental_gaps']} source files have no target equivalent and no documented skip reason"))
    if d1["translate"]["missing"]:
        actions.append(("🟡", f"IMPORTANT: {len(d1['translate']['missing'])} translate-strategy files not yet created in target"))
    if d1["direct_use"]["missing"]:
        actions.append(("🟡", f"IMPORTANT: {len(d1['direct_use']['missing'])} test fixtures/data files not copied to target"))
    if d3["source_dirs_unmapped"] > 0:
        actions.append(("🟡", f"IMPORTANT: {d3['source_dirs_unmapped']} source directories have no obvious target equivalent"))
    if d4["p3_unreferenced"]:
        actions.append(("🟢", f"MINOR: {len(d4['p3_unreferenced'])} p3-required docs were never cited in IPO registry"))
    if d3["target_dirs_unexpected"] > 0:
        actions.append(("🟢", f"MINOR: {d3['target_dirs_unexpected']} target directories don't obviously derive from source"))

    if actions:
        lines.append("## Priority Action Items")
        lines.append("")
        for emoji, msg in actions:
            lines.append(f"- {emoji} {msg}")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Detail sections
    if d1["translate"]["missing"] or d1["adapt"]["missing"]:
        lines.append("## Missing Translation/Adapt Files")
        lines.append("")
        for item in d1["translate"]["missing"][:50]:
            lines.append(f"- `{item['source']}` → expected `{item['target_expected']}`")
        for item in d1["adapt"]["missing"][:20]:
            lines.append(f"- `{item['source']}` (adapt) → expected `{item['target_expected']}`")
        lines.append("")

    if d2["done_no_lines_list"]:
        lines.append("## ⚠️ Functions: DONE Status but No target_lines (Suspicious)")
        lines.append("")
        for item in d2["done_no_lines_list"][:30]:
            lines.append(f"- `{item['id']}` (target: `{item['target_impl_file']}`)")
        lines.append("")

    if d3["unmapped_source_dirs"]:
        lines.append("## Unmapped Source Directories")
        lines.append("")
        for d in d3["unmapped_source_dirs"]:
            lines.append(f"- `{d}`")
        lines.append("")

    if d4["fixtures_missing"]:
        lines.append("## Missing Test Fixtures / Direct-Use Files")
        lines.append("")
        for f in d4["fixtures_missing"][:30]:
            lines.append(f"- `{f}`")
        lines.append("")

    if d4["p3_unreferenced"]:
        lines.append("## P3-Required Docs Never Referenced in IPO")
        lines.append("")
        for f in d4["p3_unreferenced"]:
            lines.append(f"- `{f}`")
        lines.append("")

    if d5["accidental_list"]:
        lines.append("## ⚠️ Accidental Gaps (No Target, No Documented Skip)")
        lines.append("")
        for item in d5["accidental_list"]:
            lines.append(f"- `{item['source']}` → expected `{item['target_expected']}` (inventory status: {item['status_in_inventory']})")
        lines.append("")

    if d5["platform_specific_list"]:
        lines.append("## Intentional Platform-Specific Skips")
        lines.append("")
        for item in d5["platform_specific_list"]:
            lines.append(f"- `{item['source']}` — {item['reason']}")
        lines.append("")

    if d5["intentional_detail"]:
        lines.append("## Documented Decision Skips")
        lines.append("")
        for item in d5["intentional_detail"]:
            lines.append(f"- **{item['item_id']}**: {item['decision']}")
            if item["rationale"]:
                lines.append(f"  - Rationale: {item['rationale']}")
        lines.append("")

    return "\n".join(lines)


# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="lang-migration gap reporter")
    parser.add_argument("--workspace", required=True, help="Path to migration_workspace/")
    parser.add_argument("--source",    required=True, help="Path to source project root")
    parser.add_argument("--target",    required=True, help="Path to target project root")
    args = parser.parse_args()

    ws  = Path(args.workspace).resolve()
    src = Path(args.source).resolve()
    tgt = Path(args.target).resolve()

    if not ws.exists():
        print(f"ERROR: workspace not found: {ws}")
        sys.exit(1)

    print(f"Loading workspace from {ws}...")
    state     = load_yaml(ws / "migration-state.yaml")
    inventory = load_yaml(ws / "asset-inventory.yaml")
    ipo       = load_yaml(ws / "ipo-registry.yaml")

    assets    = inventory.get("assets", [])
    functions = ipo.get("functions", [])
    decisions = state.get("decisions_log", []) or []

    target_lang = state.get("meta", {}).get("target_lang", "target")

    print(f"Scanning directories...")
    src_exists = src.exists()
    tgt_exists = tgt.exists()

    # D-3: 目标目录不存在时给出明确警告，避免误读为"0%完成"
    if not tgt_exists:
        print(f"WARNING: target directory does not exist: {tgt}")
        print("WARNING: All file coverage will show as missing. This reflects a missing target, not a 0% migration.")
        print()

    src_files = walk_files(src) if src_exists else set()
    tgt_files = walk_files(tgt) if tgt_exists else set()
    src_dirs  = walk_dirs(src)  if src_exists else set()
    tgt_dirs  = walk_dirs(tgt)  if tgt_exists else set()

    print(f"Source: {len(src_files)} files, {len(src_dirs)} dirs")
    print(f"Target: {len(tgt_files)} files, {len(tgt_dirs)} dirs" + (" (DIRECTORY NOT FOUND)" if not tgt_exists else ""))
    print(f"IPO functions: {len(functions)}")
    print(f"Asset entries: {len(assets)}")
    print()

    print("Running analysis...")
    d1 = dim1_file_coverage(assets, tgt, tgt_files)
    d2 = dim2_function_coverage(functions)
    d3 = dim3_directory_coverage(src, tgt, src_dirs, tgt_dirs)
    d4 = dim4_non_code_assets(assets, functions, tgt_files)
    d5 = dim5_skip_classification(assets, decisions, tgt_files, target_lang)

    true_pct = compute_true_completion(d1, d2, d4)

    # Render markdown
    md = render_markdown(state, d1, d2, d3, d4, d5, true_pct,
                         args.source, args.target, tgt_exists)

    md_path   = ws / "gap-report.md"
    yaml_path = ws / "gap-report.yaml"

    md_path.write_text(md, encoding="utf-8")

    gap_data = {
        "generated_at":        datetime.now().isoformat(),
        "true_completion_pct": true_pct,
        "dimension_1_file_coverage": d1,
        "dimension_2_function_coverage": d2,
        "dimension_3_directory_coverage": d3,
        "dimension_4_non_code_assets": d4,
        "dimension_5_skip_classification": d5,
    }
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(gap_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    print(md)
    print(f"\nReports written to:")
    print(f"  {md_path}")
    print(f"  {yaml_path}")


if __name__ == "__main__":
    main()
