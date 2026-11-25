#!/usr/bin/env python3
"""Source reliability scoring for Scout tools (stdlib-only).

Computes precision / recall / F1 / false-positive rate for a tool against a
LABELED corpus, so tiered verification (invariant 8) and the tier assignments
can rest on measured accuracy instead of assumption.

Input is a corpus of labeled observations:

    [
      {"tool": "sherlock", "site": "github", "handle": "someone",
       "predicted": true,  "actual": true},
      {"tool": "sherlock", "site": "github", "handle": "zzz_no_such",
       "predicted": true,  "actual": false}
    ]

Metrics are reported PER TOOL and PER (tool, site), because a tool's aggregate
figure hides the sites that carry it — a tool that is 0.9 precise overall may
be 0.4 on the handful of sites that produce most of its hits.

There are no shipped numbers here on purpose. A reliability figure that was not
measured on a labeled corpus is a fabrication, so this script reports nothing
until you give it real labels. Build the corpus first (label known-real and
known-fake handles per site), then run this.

Usage:

    python3 source_reliability.py --corpus corpus.json
    python3 source_reliability.py --corpus corpus.json --tool sherlock
    python3 source_reliability.py --corpus corpus.json --format detailed
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _envelope import add_format_arg, emit, fail, main_guard  # noqa: E402

# Below this many labeled observations a metric is reported but flagged, because
# a precision of 1.0 over three examples is not evidence.
MIN_N_FOR_CONFIDENCE = 20


def _metrics(tp: int, fp: int, fn: int, tn: int) -> dict:
    precision = tp / (tp + fp) if (tp + fp) else None
    recall = tp / (tp + fn) if (tp + fn) else None
    f1 = (2 * precision * recall / (precision + recall)
          if precision and recall else None)
    fpr = fp / (fp + tn) if (fp + tn) else None
    return {
        "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "n": tp + fp + fn + tn,
        "precision": round(precision, 3) if precision is not None else None,
        "recall": round(recall, 3) if recall is not None else None,
        "f1": round(f1, 3) if f1 is not None else None,
        "fpr": round(fpr, 3) if fpr is not None else None,
    }


def score(rows: list[dict], min_n: int = MIN_N_FOR_CONFIDENCE) -> dict:
    per_tool: dict[str, list[int]] = {}
    per_site: dict[tuple[str, str], list[int]] = {}

    def _tally(bucket, key, pred, actual):
        tp, fp, fn, tn = bucket.setdefault(key, [0, 0, 0, 0])
        if pred and actual:
            bucket[key][0] = tp + 1
        elif pred and not actual:
            bucket[key][1] = fp + 1
        elif not pred and actual:
            bucket[key][2] = fn + 1
        else:
            bucket[key][3] = tn + 1

    for row in rows:
        tool = str(row.get("tool", "")).lower()
        site = str(row.get("site", "")).lower()
        pred = bool(row.get("predicted"))
        actual = bool(row.get("actual"))
        if not tool:
            continue
        _tally(per_tool, tool, pred, actual)
        _tally(per_site, (tool, site), pred, actual)

    def _build(bucket):
        out = {}
        for key, counts in bucket.items():
            m = _metrics(*counts)
            m["reliable"] = m["n"] >= min_n
            out[key] = m
        return out

    tools = _build(per_tool)
    sites = {f"{t}:{s}": m for (t, s), m in _build(per_site).items()}

    ranked = sorted(
        ({"tool": t, **m} for t, m in tools.items()),
        key=lambda r: (-(r["f1"] or 0), -r["n"]),
    )
    return {
        "tools": tools,
        "sites": sites,
        "ranked": ranked,
        "min_n_for_confidence": min_n,
        "labeled_observations": len(rows),
    }


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--corpus", required=True,
                    help="Labeled corpus JSON (list of {tool, site, predicted, actual})")
    ap.add_argument("--tool", default="", help="Restrict to one tool")
    ap.add_argument("--min-n", type=int, default=MIN_N_FOR_CONFIDENCE,
                    help="Labeled observations below which a metric is flagged")
    add_format_arg(ap)
    a = ap.parse_args()

    try:
        rows = json.loads(Path(a.corpus).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return fail(f"cannot read {a.corpus}: {exc}", a.format,
                    guidance=("Pass a JSON list of labeled observations: "
                              "[{tool, site, predicted, actual}, ...]. Build it "
                              "by scanning handles you know are real and handles "
                              "you know are fake."),
                    code="bad_input")
    if not isinstance(rows, list):
        return fail("corpus must be a JSON list", a.format,
                    guidance="Wrap the observations in a JSON array.",
                    code="bad_input")
    if a.tool:
        rows = [r for r in rows if str(r.get("tool", "")).lower() == a.tool.lower()]
    if not rows:
        return fail("no labeled observations", a.format,
                    guidance=("The corpus held no observations (or none for this "
                              "tool). Label at least a few real and fake handles "
                              "per site before scoring."),
                    code="no_data")

    res = score(rows, a.min_n)
    res["ok"] = True
    res["count"] = len(res["ranked"])

    if a.tool:
        res["ranked"] = [r for r in res["ranked"] if r["tool"] == a.tool.lower()]

    lines = []
    for r in res["ranked"]:
        flag = "" if r["reliable"] else "  [LOW N — not yet evidence]"
        lines.append(
            f"{r['tool']}: P={r['precision']} R={r['recall']} "
            f"F1={r['f1']} FPR={r['fpr']} (n={r['n']}){flag}")

    emit(
        res, a.format,
        summary=("Source reliability over %d labeled observation(s):\n  %s"
                 % (res["labeled_observations"], "\n  ".join(lines))),
        concise_keys=("tool", "precision", "recall", "f1", "fpr", "n",
                      "reliable"),
    )
    print(json.dumps({"actionable_guidance": (
        "Use these figures to set the tiered-verification sampling (invariant "
        "8): a tool with low precision needs more of its hits verified before "
        "it can feed synthesis; a low-recall tool should be paired with a "
        "second source. Metrics flagged LOW N must not be cited as measured "
        "accuracy — they are provisional.")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main_guard(main))
