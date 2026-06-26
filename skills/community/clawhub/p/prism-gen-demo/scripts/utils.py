"""
PRISM-Gen Skill — Shared Utilities
Pure Python, no shell commands, no hardcoded paths.
"""

import os
import sys
import csv
import json

# --------------- Data directory detection ---------------

def get_data_dir():
    """Return the absolute path to the data/ directory."""
    skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(skill_root, "data")
    if not os.path.isdir(data_dir):
        print(f"ERROR: data directory not found at {data_dir}", file=sys.stderr)
        sys.exit(1)
    return data_dir


# --------------- CSV registry ---------------

STAGE_FILES = {
    "step3a":       "step3a_optimized_molecules.csv",
    "step3a_top":   "step3a_top200.csv",
    "step3b":       "step3b_dft_results.csv",
    "step3c":       "step3c_dft_refined.csv",
    "step4a":       "step4a_admet_final.csv",
    "step4b":       "step4b_top_molecules_pyscf.csv",
    "step4c":       "step4c_master_summary.csv",
    "step5a":       "step5a_broadspectrum_docking.csv",
    "step5b":       "step5b_final_candidates.csv",
    "step5b_master":"step5b_master_summary.csv",
}

STAGE_DESCRIPTIONS = {
    "step3a":       "RL-optimized molecules (top 200, generation + surrogate scoring)",
    "step3a_top":   "Top 200 molecules by Reward",
    "step3b":       "GFN2-xTB electronic structure results (HOMO, LUMO, gap, ESP)",
    "step3c":       "xTB-refined ranking with GEM scoring (R_DFT, R_total)",
    "step4a":       "ADMET filtering (Lipinski, hERG, QED, R_ADMET, R_global)",
    "step4b":       "B3LYP/6-31G* DFT validation (PySCF, top candidates)",
    "step4c":       "Master summary (all stages merged, 200 molecules)",
    "step5a":       "Broad-spectrum docking results (36 candidates, 3 targets)",
    "step5b":       "Final candidates with all annotations (36 molecules)",
    "step5b_master":"Master summary with docking (200 molecules)",
}


def resolve_stage(stage_key):
    """Resolve a stage key to a file path. Returns (path, description) or exits."""
    key = stage_key.strip().lower()
    if key not in STAGE_FILES:
        print(f"ERROR: Unknown stage '{stage_key}'.", file=sys.stderr)
        print(f"Available stages: {', '.join(sorted(STAGE_FILES.keys()))}", file=sys.stderr)
        sys.exit(1)
    path = os.path.join(get_data_dir(), STAGE_FILES[key])
    if not os.path.isfile(path):
        print(f"ERROR: File not found: {path}", file=sys.stderr)
        sys.exit(1)
    return path, STAGE_DESCRIPTIONS[key]


# --------------- Lightweight CSV reader (no pandas dependency) ---------------

def read_csv(filepath, max_rows=None):
    """Read a CSV file and return (headers, rows) where rows are list of dicts."""
    rows = []
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        for i, row in enumerate(reader):
            if max_rows is not None and i >= max_rows:
                break
            rows.append(row)
    return headers, rows


def to_float(value, default=None):
    """Safely convert a string to float."""
    if value is None or value == "":
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def to_bool(value):
    """Convert string to bool."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in ("true", "1", "yes")
    return False


# --------------- Output formatting ---------------

def print_table(headers, rows, max_col_width=30, max_rows=50):
    """Print a formatted ASCII table."""
    if not rows:
        print("(no data)")
        return

    display_rows = rows[:max_rows]
    col_widths = {}
    for h in headers:
        col_widths[h] = min(max_col_width, max(len(h), max(len(str(r.get(h, ""))[:max_col_width]) for r in display_rows)))

    # Header
    header_line = " | ".join(h.ljust(col_widths[h])[:col_widths[h]] for h in headers)
    print(header_line)
    print("-+-".join("-" * col_widths[h] for h in headers))

    # Rows
    for r in display_rows:
        line = " | ".join(str(r.get(h, "")).ljust(col_widths[h])[:col_widths[h]] for h in headers)
        print(line)

    if len(rows) > max_rows:
        print(f"\n... showing {max_rows} of {len(rows)} rows. Use --max_rows to see more.")


def print_json(data):
    """Print data as formatted JSON."""
    print(json.dumps(data, indent=2, default=str))
