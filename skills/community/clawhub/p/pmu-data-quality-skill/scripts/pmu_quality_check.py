#!/usr/bin/env python3
"""
PMU Data Quality Checker
========================
Validates PMU (Phasor Measurement Unit) CSV data against configurable
security limits for frequency, voltage magnitude, phasor angles,
and data completeness.

Usage:
    python pmu_quality_check.py <csv_file> [--config limits_config.json] [--html] [--output output_dir]
"""

import argparse
import json
import sys
import os
from pathlib import Path
from datetime import datetime

import pandas as pd
import numpy as np


# ── Default limits (used if no config file provided) ────────────────────────
DEFAULT_LIMITS = {
    "frequency": {"min_hz": 59.95, "max_hz": 60.05, "warn_min_hz": 59.97, "warn_max_hz": 60.03},
    "voltage_magnitude": {"min_pu": 0.90, "max_pu": 1.10, "warn_min_pu": 0.95, "warn_max_pu": 1.05},
    "voltage_angle": {"min_deg": -180.0, "max_deg": 180.0, "max_rate_deg_per_sec": 30.0},
    "current_magnitude": {"min_pu": 0.0, "max_pu": 2.0, "warn_max_pu": 1.5},
    "current_angle": {"min_deg": -180.0, "max_deg": 180.0},
}

DEFAULT_COL_MAP = {
    "timestamp": "timestamp",
    "frequency": "frequency",
    "voltage_mag": "voltage_mag",
    "voltage_angle": "voltage_angle",
    "current_mag": "current_mag",
    "current_angle": "current_angle",
}


# ── Helpers ──────────────────────────────────────────────────────────────────

def load_config(config_path: str | None) -> dict:
    """Load limits configuration from JSON, or return defaults."""
    if config_path and Path(config_path).exists():
        with open(config_path) as f:
            cfg = json.load(f)
        limits = cfg.get("limits", DEFAULT_LIMITS)
        col_map = cfg.get("column_mapping", DEFAULT_COL_MAP)
        system = cfg.get("system", {})
        quality = cfg.get("quality_flags", {})
    else:
        limits = DEFAULT_LIMITS
        col_map = DEFAULT_COL_MAP
        system = {"nominal_frequency_hz": 60.0, "reporting_rate_fps": 30}
        quality = {"max_missing_pct": 5.0, "max_gap_samples": 3}
    return {"limits": limits, "column_mapping": col_map, "system": system, "quality_flags": quality}


def load_data(csv_path: str, col_map: dict) -> pd.DataFrame:
    """Load CSV and rename columns to standard names."""
    df = pd.read_csv(csv_path)

    # Build rename map (only for columns that exist)
    rename = {}
    for standard_name, csv_name in col_map.items():
        if csv_name in df.columns:
            rename[csv_name] = standard_name

    df = df.rename(columns=rename)

    # Parse timestamp
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df = df.sort_values("timestamp").reset_index(drop=True)

    return df


# ── Individual check functions ───────────────────────────────────────────────

def check_missing(df: pd.DataFrame) -> dict:
    """Check for missing / NaN values in each column."""
    results = {"total_rows": len(df), "columns": {}}
    for col in df.columns:
        n_missing = int(df[col].isna().sum())
        pct = round(n_missing / len(df) * 100, 2) if len(df) > 0 else 0
        results["columns"][col] = {"missing_count": n_missing, "missing_pct": pct}
    results["total_missing"] = int(df.isna().any(axis=1).sum())
    results["total_missing_pct"] = round(results["total_missing"] / len(df) * 100, 2) if len(df) > 0 else 0
    return results


def check_timestamp_gaps(df: pd.DataFrame, reporting_rate: int = 30, max_gap_samples: int = 3) -> dict:
    """Detect gaps in timestamp continuity."""
    results = {"gaps_found": 0, "gap_details": []}
    if "timestamp" not in df.columns or df["timestamp"].isna().all():
        results["error"] = "No valid timestamps found"
        return results

    expected_interval = pd.Timedelta(seconds=1.0 / reporting_rate)
    tolerance = expected_interval * 1.5  # allow 50% tolerance

    diffs = df["timestamp"].diff()
    gap_mask = diffs > tolerance
    gap_indices = df.index[gap_mask].tolist()

    results["gaps_found"] = len(gap_indices)
    for idx in gap_indices[:20]:  # limit reported gaps
        actual_gap = diffs.iloc[idx]
        missed_samples = int(round(actual_gap / expected_interval)) - 1
        if missed_samples >= max_gap_samples:
            results["gap_details"].append({
                "row": int(idx),
                "timestamp": str(df["timestamp"].iloc[idx]),
                "gap_seconds": round(actual_gap.total_seconds(), 4),
                "missed_samples": missed_samples,
            })

    results["significant_gaps"] = len(results["gap_details"])
    return results


def check_frequency(df: pd.DataFrame, limits: dict) -> dict:
    """Check frequency against security limits."""
    col = "frequency"
    if col not in df.columns:
        return {"error": f"Column '{col}' not found"}

    freq = df[col].dropna()
    lim = limits.get("frequency", DEFAULT_LIMITS["frequency"])

    alert_low = freq < lim["min_hz"]
    alert_high = freq > lim["max_hz"]
    warn_low = (freq >= lim["min_hz"]) & (freq < lim.get("warn_min_hz", lim["min_hz"]))
    warn_high = (freq <= lim["max_hz"]) & (freq > lim.get("warn_max_hz", lim["max_hz"]))

    return {
        "total_valid": int(len(freq)),
        "alert_low_count": int(alert_low.sum()),
        "alert_high_count": int(alert_high.sum()),
        "warn_low_count": int(warn_low.sum()),
        "warn_high_count": int(warn_high.sum()),
        "min_value": round(float(freq.min()), 6),
        "max_value": round(float(freq.max()), 6),
        "mean_value": round(float(freq.mean()), 6),
        "std_value": round(float(freq.std()), 6),
        "limits_used": {"alert": [lim["min_hz"], lim["max_hz"]],
                        "warn": [lim.get("warn_min_hz"), lim.get("warn_max_hz")]},
        "alert_rows": df.index[df[col].notna() & (alert_low | alert_high)].tolist(),
    }


def check_voltage_magnitude(df: pd.DataFrame, limits: dict) -> dict:
    """Check voltage magnitude against limits."""
    col = "voltage_mag"
    if col not in df.columns:
        return {"error": f"Column '{col}' not found"}

    vmag = df[col].dropna()
    lim = limits.get("voltage_magnitude", DEFAULT_LIMITS["voltage_magnitude"])

    alert_low = vmag < lim["min_pu"]
    alert_high = vmag > lim["max_pu"]
    warn_low = (vmag >= lim["min_pu"]) & (vmag < lim.get("warn_min_pu", lim["min_pu"]))
    warn_high = (vmag <= lim["max_pu"]) & (vmag > lim.get("warn_max_pu", lim["max_pu"]))

    return {
        "total_valid": int(len(vmag)),
        "alert_low_count": int(alert_low.sum()),
        "alert_high_count": int(alert_high.sum()),
        "warn_low_count": int(warn_low.sum()),
        "warn_high_count": int(warn_high.sum()),
        "min_value": round(float(vmag.min()), 6),
        "max_value": round(float(vmag.max()), 6),
        "mean_value": round(float(vmag.mean()), 6),
        "std_value": round(float(vmag.std()), 6),
        "limits_used": {"alert": [lim["min_pu"], lim["max_pu"]],
                        "warn": [lim.get("warn_min_pu"), lim.get("warn_max_pu")]},
        "alert_rows": df.index[df[col].notna() & (alert_low | alert_high)].tolist(),
    }


def check_phasor_angle(df: pd.DataFrame, col_name: str, limits: dict, limit_key: str,
                        reporting_rate: int = 30) -> dict:
    """Check phasor angle for range violations and excessive rate-of-change."""
    if col_name not in df.columns:
        return {"error": f"Column '{col_name}' not found"}

    angles = df[col_name].dropna()
    lim = limits.get(limit_key, DEFAULT_LIMITS.get(limit_key, {}))

    out_of_range = (angles < lim.get("min_deg", -180)) | (angles > lim.get("max_deg", 180))

    # Rate of change (degrees per second)
    max_rate = lim.get("max_rate_deg_per_sec", None)
    roc_violations = 0
    roc_rows = []
    if max_rate and len(angles) > 1:
        angle_diff = angles.diff().abs()
        # Handle wraparound (e.g., 179 -> -179 is only 2 degrees, not 358)
        angle_diff = angle_diff.where(angle_diff <= 180, 360 - angle_diff)
        roc = angle_diff * reporting_rate  # deg/sample * samples/sec = deg/sec
        roc_mask = roc > max_rate
        roc_violations = int(roc_mask.sum())
        roc_rows = angles.index[roc_mask].tolist()

    return {
        "total_valid": int(len(angles)),
        "out_of_range_count": int(out_of_range.sum()),
        "rate_of_change_violations": roc_violations,
        "min_value": round(float(angles.min()), 4),
        "max_value": round(float(angles.max()), 4),
        "mean_value": round(float(angles.mean()), 4),
        "out_of_range_rows": df.index[df[col_name].notna() & out_of_range].tolist(),
        "roc_violation_rows": roc_rows[:20],
    }


def check_current_magnitude(df: pd.DataFrame, limits: dict) -> dict:
    """Check current magnitude against limits."""
    col = "current_mag"
    if col not in df.columns:
        return {"error": f"Column '{col}' not found"}

    cmag = df[col].dropna()
    lim = limits.get("current_magnitude", DEFAULT_LIMITS["current_magnitude"])

    alert_high = cmag > lim["max_pu"]
    warn_high = (cmag <= lim["max_pu"]) & (cmag > lim.get("warn_max_pu", lim["max_pu"]))

    return {
        "total_valid": int(len(cmag)),
        "alert_high_count": int(alert_high.sum()),
        "warn_high_count": int(warn_high.sum()),
        "min_value": round(float(cmag.min()), 6),
        "max_value": round(float(cmag.max()), 6),
        "mean_value": round(float(cmag.mean()), 6),
        "limits_used": {"alert_max": lim["max_pu"], "warn_max": lim.get("warn_max_pu")},
        "alert_rows": df.index[df[col].notna() & alert_high].tolist(),
    }


# ── Flagged rows export ─────────────────────────────────────────────────────

def build_flagged_df(df: pd.DataFrame, all_results: dict) -> pd.DataFrame:
    """Create a copy of df with a 'flags' column summarizing all issues per row."""
    flags = pd.Series([""] * len(df), index=df.index)

    # Missing data
    for idx in df.index[df.isna().any(axis=1)]:
        missing_cols = df.columns[df.loc[idx].isna()].tolist()
        flags.iloc[idx] += f"MISSING({','.join(missing_cols)}); "

    # Frequency alerts
    for idx in all_results.get("frequency", {}).get("alert_rows", []):
        flags.iloc[idx] += "FREQ_ALERT; "

    # Voltage magnitude alerts
    for idx in all_results.get("voltage_magnitude", {}).get("alert_rows", []):
        flags.iloc[idx] += "VMAG_ALERT; "

    # Current magnitude alerts
    for idx in all_results.get("current_magnitude", {}).get("alert_rows", []):
        flags.iloc[idx] += "IMAG_ALERT; "

    # Voltage angle issues
    for idx in all_results.get("voltage_angle", {}).get("out_of_range_rows", []):
        flags.iloc[idx] += "VANG_RANGE; "
    for idx in all_results.get("voltage_angle", {}).get("roc_violation_rows", []):
        flags.iloc[idx] += "VANG_ROC; "

    # Current angle issues
    for idx in all_results.get("current_angle", {}).get("out_of_range_rows", []):
        flags.iloc[idx] += "IANG_RANGE; "

    flagged = df.copy()
    flagged["flags"] = flags.str.strip("; ")
    return flagged[flagged["flags"] != ""]


# ── Report printing ──────────────────────────────────────────────────────────

def print_report(all_results: dict, cfg: dict):
    """Print a human-readable summary report to stdout."""
    sep = "=" * 70
    thin = "-" * 70

    print(f"\n{sep}")
    print("  PMU DATA QUALITY REPORT")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(sep)

    # ── Missing data ──
    missing = all_results.get("missing", {})
    print(f"\n{'[1] MISSING DATA':─<70}")
    print(f"  Total rows:      {missing.get('total_rows', '?')}")
    print(f"  Rows w/ missing: {missing.get('total_missing', '?')} ({missing.get('total_missing_pct', '?')}%)")
    for col, info in missing.get("columns", {}).items():
        if info["missing_count"] > 0:
            print(f"    - {col}: {info['missing_count']} missing ({info['missing_pct']}%)")

    # ── Timestamp gaps ──
    gaps = all_results.get("timestamp_gaps", {})
    print(f"\n{'[2] TIMESTAMP CONTINUITY':─<70}")
    print(f"  Total gaps detected:     {gaps.get('gaps_found', '?')}")
    print(f"  Significant gaps (≥{cfg['quality_flags'].get('max_gap_samples', 3)} samples): {gaps.get('significant_gaps', '?')}")
    for g in gaps.get("gap_details", []):
        print(f"    - Row {g['row']}: gap={g['gap_seconds']}s ({g['missed_samples']} missed samples) at {g['timestamp']}")

    # ── Frequency ──
    freq = all_results.get("frequency", {})
    if "error" not in freq:
        print(f"\n{'[3] FREQUENCY CHECK':─<70}")
        lim = freq.get("limits_used", {})
        print(f"  Limits — Alert: {lim.get('alert')},  Warn: {lim.get('warn')}")
        print(f"  Range:   {freq['min_value']} – {freq['max_value']} Hz")
        print(f"  Mean:    {freq['mean_value']} Hz  (σ = {freq['std_value']})")
        total_alerts = freq["alert_low_count"] + freq["alert_high_count"]
        total_warns = freq["warn_low_count"] + freq["warn_high_count"]
        status = "✅ PASS" if total_alerts == 0 else f"❌ FAIL ({total_alerts} alerts)"
        print(f"  Alerts:  {total_alerts}  (low={freq['alert_low_count']}, high={freq['alert_high_count']})")
        print(f"  Warns:   {total_warns}  (low={freq['warn_low_count']}, high={freq['warn_high_count']})")
        print(f"  Status:  {status}")

    # ── Voltage magnitude ──
    vmag = all_results.get("voltage_magnitude", {})
    if "error" not in vmag:
        print(f"\n{'[4] VOLTAGE MAGNITUDE CHECK':─<70}")
        lim = vmag.get("limits_used", {})
        print(f"  Limits — Alert: {lim.get('alert')},  Warn: {lim.get('warn')}")
        print(f"  Range:   {vmag['min_value']} – {vmag['max_value']} pu")
        print(f"  Mean:    {vmag['mean_value']} pu  (σ = {vmag['std_value']})")
        total_alerts = vmag["alert_low_count"] + vmag["alert_high_count"]
        total_warns = vmag["warn_low_count"] + vmag["warn_high_count"]
        status = "✅ PASS" if total_alerts == 0 else f"❌ FAIL ({total_alerts} alerts)"
        print(f"  Alerts:  {total_alerts}  (low={vmag['alert_low_count']}, high={vmag['alert_high_count']})")
        print(f"  Warns:   {total_warns}  (low={vmag['warn_low_count']}, high={vmag['warn_high_count']})")
        print(f"  Status:  {status}")

    # ── Voltage angle ──
    vang = all_results.get("voltage_angle", {})
    if "error" not in vang:
        print(f"\n{'[5] VOLTAGE ANGLE CHECK':─<70}")
        print(f"  Range:   {vang['min_value']}° – {vang['max_value']}°")
        print(f"  Mean:    {vang['mean_value']}°")
        print(f"  Out of range:   {vang['out_of_range_count']}")
        print(f"  ROC violations: {vang['rate_of_change_violations']}")
        oor = vang["out_of_range_count"] + vang["rate_of_change_violations"]
        status = "✅ PASS" if oor == 0 else f"❌ FAIL ({oor} issues)"
        print(f"  Status:  {status}")

    # ── Current magnitude ──
    cmag = all_results.get("current_magnitude", {})
    if "error" not in cmag:
        print(f"\n{'[6] CURRENT MAGNITUDE CHECK':─<70}")
        lim = cmag.get("limits_used", {})
        print(f"  Limits — Alert max: {lim.get('alert_max')},  Warn max: {lim.get('warn_max')}")
        print(f"  Range:   {cmag['min_value']} – {cmag['max_value']} pu")
        print(f"  Mean:    {cmag['mean_value']} pu")
        status = "✅ PASS" if cmag["alert_high_count"] == 0 else f"❌ FAIL ({cmag['alert_high_count']} alerts)"
        print(f"  Alerts:  {cmag['alert_high_count']}")
        print(f"  Warns:   {cmag['warn_high_count']}")
        print(f"  Status:  {status}")

    # ── Current angle ──
    iang = all_results.get("current_angle", {})
    if "error" not in iang:
        print(f"\n{'[7] CURRENT ANGLE CHECK':─<70}")
        print(f"  Range:   {iang['min_value']}° – {iang['max_value']}°")
        print(f"  Out of range: {iang['out_of_range_count']}")
        status = "✅ PASS" if iang["out_of_range_count"] == 0 else f"❌ FAIL"
        print(f"  Status:  {status}")

    # ── Overall ──
    print(f"\n{sep}")
    has_any_fail = any([
        freq.get("alert_low_count", 0) + freq.get("alert_high_count", 0) > 0,
        vmag.get("alert_low_count", 0) + vmag.get("alert_high_count", 0) > 0,
        cmag.get("alert_high_count", 0) > 0,
        vang.get("out_of_range_count", 0) + vang.get("rate_of_change_violations", 0) > 0,
        missing.get("total_missing_pct", 0) > cfg["quality_flags"].get("max_missing_pct", 5.0),
    ])
    overall = "❌ DATA QUALITY ISSUES FOUND" if has_any_fail else "✅ ALL CHECKS PASSED"
    print(f"  OVERALL: {overall}")
    print(f"{sep}\n")


# ── Main ─────────────────────────────────────────────────────────────────────

def run_quality_check(csv_path: str, config_path: str | None = None,
                      output_dir: str | None = None) -> dict:
    """Run all quality checks and return results dict."""
    cfg = load_config(config_path)
    limits = cfg["limits"]
    col_map = cfg["column_mapping"]
    system = cfg["system"]
    quality = cfg["quality_flags"]
    reporting_rate = system.get("reporting_rate_fps", 30)

    df = load_data(csv_path, col_map)

    all_results = {}
    all_results["missing"] = check_missing(df)
    all_results["timestamp_gaps"] = check_timestamp_gaps(
        df, reporting_rate, quality.get("max_gap_samples", 3)
    )
    all_results["frequency"] = check_frequency(df, limits)
    all_results["voltage_magnitude"] = check_voltage_magnitude(df, limits)
    all_results["voltage_angle"] = check_phasor_angle(
        df, "voltage_angle", limits, "voltage_angle", reporting_rate
    )
    all_results["current_magnitude"] = check_current_magnitude(df, limits)
    all_results["current_angle"] = check_phasor_angle(
        df, "current_angle", limits, "current_angle", reporting_rate
    )

    # Print report
    print_report(all_results, cfg)

    # Export flagged rows
    flagged = build_flagged_df(df, all_results)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        out_path = Path(output_dir) / (Path(csv_path).stem + "_flagged.csv")
    else:
        out_path = Path(csv_path).with_name(Path(csv_path).stem + "_flagged.csv")

    if len(flagged) > 0:
        flagged.to_csv(out_path, index=False)
        print(f"  Flagged rows exported to: {out_path}")
        print(f"  Total flagged: {len(flagged)} / {len(df)} rows\n")
    else:
        print("  No flagged rows to export — data looks clean!\n")

    return all_results


def main():
    parser = argparse.ArgumentParser(description="PMU Data Quality Checker")
    parser.add_argument("csv_file", help="Path to the PMU data CSV file")
    parser.add_argument("--config", "-c", help="Path to limits config JSON", default=None)
    parser.add_argument("--output", "-o", help="Output directory for flagged CSV", default=None)
    parser.add_argument("--html", action="store_true", help="Generate HTML report (requires matplotlib)")
    args = parser.parse_args()

    if not Path(args.csv_file).exists():
        print(f"Error: File not found: {args.csv_file}", file=sys.stderr)
        sys.exit(1)

    results = run_quality_check(args.csv_file, args.config, args.output)

    if args.html:
        try:
            from pmu_quality_html_report import generate_html_report
            generate_html_report(args.csv_file, results, args.output)
        except ImportError:
            print("  Note: HTML report requires matplotlib. Install with: pip install matplotlib")


if __name__ == "__main__":
    main()
