#!/usr/bin/env python3
"""
Ops Detector evaluation — public, independent, dual-threshold honesty.

Operational bar (production-like): ops_score >= 0.65 OR high evasion.
Calibration bar (short suite ranking only): lower ops threshold for F1 sweep.

Never present calibration metrics as production performance.

Usage:
  python eval_ops_detector.py tests/labeled_discourse_suite.json --sweep
  python eval_ops_detector.py --operational-threshold 0.65 --calibration-threshold 0.05

Writes only under skill tests/ (least privilege). Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
TESTS = ROOT / "tests"
sys.path.insert(0, str(SCRIPTS))

import lygo_ops_detector as det  # noqa: E402

DEFAULT_SUITE = TESTS / "labeled_discourse_suite.json"
DEFAULT_OUT = TESTS / "last_eval_report.json"
OPERATIONAL_DEFAULT = 0.65
CALIBRATION_DEFAULT = 0.05


def resolve_write_path(raw: str) -> Path:
    """Constrain writes to skill tests/ only (SkillSpector least-privilege)."""
    tests = TESTS.resolve()
    candidate = Path(raw)
    if candidate.is_absolute():
        p = candidate.resolve()
    else:
        # bare name or relative → under tests/; allow "tests/foo.json" from skill root
        if candidate.parts and candidate.parts[0] == "tests":
            p = (ROOT / candidate).resolve()
        else:
            p = (tests / candidate).resolve()
    try:
        p.relative_to(tests)
    except ValueError:
        raise SystemExit(
            f"REFUSED: --out must be under skill tests/ ({tests}). Got: {p}\n"
            f"Default: {DEFAULT_OUT}"
        )
    return p


def load_suite(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    samples = data.get("samples") or data
    if not isinstance(samples, list):
        raise ValueError("suite must contain samples[]")
    return samples


def predict_binary(report: det.OpsReport, threshold: float) -> int:
    """1 = positive at *this* threshold (eval only). High evasion always positive."""
    if report.evasion_index >= det.EVASION_ACTIVE_THRESHOLD:
        return 1
    return 1 if report.ops_score >= threshold else 0


def precision_recall_fpr(y_true: list[int], y_pred: list[int]) -> dict[str, float]:
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)
    tn = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 0)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    fpr = fp / (fp + tn) if (fp + tn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "false_positive_rate": round(fpr, 4),
        "f1": round(f1, 4),
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn,
    }


def roc_auc(y_true: list[int], scores: list[float]) -> float:
    pos = [s for t, s in zip(y_true, scores) if t == 1]
    neg = [s for t, s in zip(y_true, scores) if t == 0]
    if not pos or not neg:
        return 0.0
    greater = 0.0
    for p in pos:
        for n in neg:
            if p > n:
                greater += 1.0
            elif p == n:
                greater += 0.5
    return round(greater / (len(pos) * len(neg)), 4)


def evaluate(samples: list[dict], threshold: float, *, role: str) -> dict[str, Any]:
    y_true: list[int] = []
    y_pred: list[int] = []
    y_scores: list[float] = []
    rows: list[dict] = []

    for sample in samples:
        text = sample.get("text") or ""
        label = int(sample.get("label", 0))
        report = det.analyze(
            text=text,
            public_meta=sample.get("public_meta"),
            notes=f"eval:{sample.get('id', '')}",
        )
        pred = predict_binary(report, threshold)
        score = float(report.ops_score)
        y_true.append(label)
        y_pred.append(pred)
        y_scores.append(score)
        rows.append(
            {
                "id": sample.get("id", "unknown"),
                "text": text[:120],
                "label": label,
                "predicted_at_threshold": pred,
                "ops_score": score,
                "evasion_index": report.evasion_index,
                "detector_verdict": report.overall_verdict,
                "note": (
                    "detector_verdict uses operational language rules; "
                    "predicted_at_threshold is eval-only at the stated threshold"
                ),
            }
        )

    metrics = precision_recall_fpr(y_true, y_pred)
    auc = roc_auc(y_true, y_scores)
    return {
        "role": role,
        "suite_size": len(samples),
        "threshold_ops_score": threshold,
        "prediction_rule": (
            f"predicted=1 if evasion_index>={det.EVASION_ACTIVE_THRESHOLD} "
            f"OR ops_score>={threshold}"
        ),
        "precision": metrics["precision"],
        "recall": metrics["recall"],
        "false_positive_rate": metrics["false_positive_rate"],
        "f1": metrics["f1"],
        "auc": auc,
        "confusion": {k: metrics[k] for k in ("tp", "fp", "fn", "tn")},
        "results": rows,
        "generator": "scripts/eval_ops_detector.py",
        "detector_module": "scripts/lygo_ops_detector.py",
    }


def sweep_thresholds(samples: list[dict], grid: list[float] | None = None) -> dict[str, Any]:
    grid = grid or [round(x * 0.05, 2) for x in range(0, 21)]
    best = None
    table = []
    for thr in grid:
        rep = evaluate(samples, thr, role="sweep")
        row = {
            "threshold": thr,
            "precision": rep["precision"],
            "recall": rep["recall"],
            "f1": rep["f1"],
            "fpr": rep["false_positive_rate"],
            "auc": rep["auc"],
        }
        table.append(row)
        if best is None or row["f1"] > best["f1"]:
            best = row
    return {"sweep": table, "best_f1_threshold": best}


def main() -> int:
    ap = argparse.ArgumentParser(description="Evaluate lygo-ops-detector (dual-threshold honesty)")
    ap.add_argument("suite", nargs="?", default=str(DEFAULT_SUITE))
    ap.add_argument(
        "--operational-threshold",
        type=float,
        default=OPERATIONAL_DEFAULT,
        help="Production-like bar (default 0.65). Primary metrics.",
    )
    ap.add_argument(
        "--calibration-threshold",
        type=float,
        default=CALIBRATION_DEFAULT,
        help="Short-suite ranking only (default 0.05). NOT production performance.",
    )
    ap.add_argument("--sweep", action="store_true")
    ap.add_argument(
        "--out",
        default=str(DEFAULT_OUT),
        help=f"Write JSON report under skill tests/ only (default: {DEFAULT_OUT.name})",
    )
    args = ap.parse_args()

    suite_path = Path(args.suite)
    if not suite_path.is_file():
        print(f"MISSING suite: {suite_path}", file=sys.stderr)
        return 2

    try:
        out_path = resolve_write_path(args.out)
    except SystemExit as e:
        print(str(e), file=sys.stderr)
        return 2

    samples = load_suite(suite_path)
    operational = evaluate(samples, args.operational_threshold, role="operational")
    calibration = evaluate(samples, args.calibration_threshold, role="calibration")
    # Drop nested results from secondary blocks to keep file smaller if needed
    op_metrics = {k: operational[k] for k in (
        "role", "suite_size", "threshold_ops_score", "prediction_rule",
        "precision", "recall", "false_positive_rate", "f1", "auc", "confusion",
    )}
    cal_metrics = {k: calibration[k] for k in (
        "role", "suite_size", "threshold_ops_score", "prediction_rule",
        "precision", "recall", "false_positive_rate", "f1", "auc", "confusion",
    )}

    report: dict[str, Any] = {
        "signature": "Δ9Φ963-OPS-DETECTOR-EVAL-v2.1",
        "honesty": {
            "primary": "operational_metrics (ops_score>=0.65 or high evasion)",
            "secondary": "calibration_metrics for short-suite ranking only",
            "warning": (
                "Do not advertise calibration precision/recall as production performance. "
                "Short labeled suite often needs low ops thresholds for ranking; "
                "the documented strong-pattern bar is 0.65 and may show low recall on one-liners. "
                "detector_verdict text is not the same as predicted_at_threshold."
            ),
        },
        "operational_metrics": op_metrics,
        "calibration_metrics": cal_metrics,
        # Back-compat aliases (prefer operational for headline consumers)
        "threshold_ops_score": op_metrics["threshold_ops_score"],
        "precision": op_metrics["precision"],
        "recall": op_metrics["recall"],
        "false_positive_rate": op_metrics["false_positive_rate"],
        "f1": op_metrics["f1"],
        "auc": op_metrics["auc"],
        "confusion": op_metrics["confusion"],
        "suite_size": operational["suite_size"],
        "results": operational["results"],
        "calibration_results_sample": calibration["results"][:3],
        "documented_ops_threshold": args.operational_threshold,
        "generator": "scripts/eval_ops_detector.py",
        "note": (
            "Metrics computed on the public labeled suite. "
            "Not a claim of production harm/ethics calibration. Re-run after pattern changes."
        ),
    }

    if args.sweep:
        report["threshold_sweep"] = sweep_thresholds(samples)

    # Write only under tests/ (already resolved). Never mkdir outside skill tree.
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if not str(out_path.resolve()).startswith(str(TESTS.resolve())):
        print("REFUSED: write path escaped tests/", file=sys.stderr)
        return 2
    out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "operational": {
                    "threshold": op_metrics["threshold_ops_score"],
                    "precision": op_metrics["precision"],
                    "recall": op_metrics["recall"],
                    "f1": op_metrics["f1"],
                    "auc": op_metrics["auc"],
                    "confusion": op_metrics["confusion"],
                },
                "calibration_only": {
                    "threshold": cal_metrics["threshold_ops_score"],
                    "precision": cal_metrics["precision"],
                    "recall": cal_metrics["recall"],
                    "f1": cal_metrics["f1"],
                    "warning": "NOT production performance",
                },
                "best_f1_threshold": (report.get("threshold_sweep") or {}).get("best_f1_threshold"),
                "report": str(out_path),
            },
            indent=2,
        )
    )
    print(f"\nFull report written to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
