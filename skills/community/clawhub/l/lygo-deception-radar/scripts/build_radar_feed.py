#!/usr/bin/env python3
"""
Build public Deception Radar feed from the public labeled discourse suite.

- PUBLIC samples only (ops-detector suite or bundled samples)
- Anonymized: sample ids + text snippets only (no PII)
- Dual thresholds documented (operational 0.65 vs calibration)
- No network, no subprocess

Signature: Delta9Phi963-DECEPTION-RADAR-v1.0.0
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SIG = "Delta9Phi963-DECEPTION-RADAR-v1.0.0"
VERSION = "1.0.0"
HERE = Path(__file__).resolve().parent
SKILL = HERE.parent


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def find_ops_detector() -> Path | None:
    candidates = [
        SKILL.parent / "lygo-ops-detector" / "scripts" / "lygo_ops_detector.py",
        Path(r"I:\E Drive\.grok\skills\lygo-ops-detector\scripts\lygo_ops_detector.py"),
        Path(r"D:\lygo-protocol-stack\clawhub\mirrors\lygo-ops-detector\scripts\lygo_ops_detector.py"),
    ]
    env = __import__("os").environ.get("LYGO_STACK_ROOT", "").strip()
    if env:
        candidates.append(
            Path(env) / "clawhub" / "mirrors" / "lygo-ops-detector" / "scripts" / "lygo_ops_detector.py"
        )
    for p in candidates:
        if p.is_file():
            return p
    return None


def load_suite(path: Path | None) -> list[dict[str, Any]]:
    if path and path.is_file():
        data = json.loads(path.read_text(encoding="utf-8"))
        return list(data.get("samples") or data)
    # bundled fallback (minimal public samples)
    fallback = SKILL / "tests" / "public_samples.json"
    if fallback.is_file():
        data = json.loads(fallback.read_text(encoding="utf-8"))
        return list(data.get("samples") or [])
    return []


def build_feed(samples: list[dict], operational: float = 0.65) -> dict[str, Any]:
    det_path = find_ops_detector()
    if not det_path:
        return {"ok": False, "error": "ops_detector_missing", "signature": SIG}
    sys.path.insert(0, str(det_path.parent))
    import lygo_ops_detector as det  # noqa: E402

    rows = []
    strong = 0
    weak = 0
    clear = 0
    for s in samples:
        text = (s.get("text") or "")[:500]
        sid = s.get("id") or f"sample_{len(rows)}"
        label = s.get("label")
        report = det.analyze(text=text, notes=f"radar:{sid}")
        ops = float(report.ops_score)
        ev = float(report.evasion_index)
        if ev > 0.7 or ops >= operational:
            band = "strong"
            strong += 1
        elif ops >= 0.05:
            band = "weak_calibration"
            weak += 1
        else:
            band = "clear"
            clear += 1
        rows.append(
            {
                "id": sid,
                "public_label": label,
                "text_preview": text[:160],
                "ops_score": ops,
                "evasion_index": ev,
                "band": band,
                "verdict": report.overall_verdict,
            }
        )

    # sort: strong first
    order = {"strong": 0, "weak_calibration": 1, "clear": 2}
    rows.sort(key=lambda r: (order.get(r["band"], 9), -r["ops_score"]))

    return {
        "ok": True,
        "signature": SIG,
        "version": VERSION,
        "generated_utc": utc_now(),
        "source": "public labeled discourse suite only — no private mail/logs",
        "ethics": {
            "not_for_doxing": True,
            "not_person_verdicts": True,
            "public_samples_only": True,
            "operational_threshold": operational,
            "note": "weak_calibration is ranking-only; do not treat as production alerts",
        },
        "stats": {
            "samples": len(rows),
            "strong": strong,
            "weak_calibration": weak,
            "clear": clear,
            "strong_rate": round(strong / max(len(rows), 1), 4),
        },
        "signals": rows,
        "detector": str(det_path),
    }


def write_html(feed: dict[str, Any], out_html: Path) -> None:
    stats = feed.get("stats") or {}
    ethics = feed.get("ethics") or {}
    rows_html = []
    for r in feed.get("signals") or []:
        band = r.get("band")
        color = {"strong": "#e94560", "weak_calibration": "#ffcc00", "clear": "#00ff88"}.get(band, "#aaa")
        preview = (r.get("text_preview") or "").replace("<", "&lt;").replace(">", "&gt;")
        rows_html.append(
            f"<tr><td><code>{r.get('id')}</code></td>"
            f"<td style='color:{color};font-weight:600'>{band}</td>"
            f"<td>{r.get('ops_score')}</td><td>{r.get('evasion_index')}</td>"
            f"<td class='prev'>{preview}</td></tr>"
        )
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>LYGO Deception Radar — public discourse signals</title>
  <meta name="description" content="Public, anonymized Ops Detector radar on labeled discourse samples. Not for doxing. Operational threshold 0.65." />
  <style>
    :root {{ --bg:#0b0b12; --card:#141422; --fg:#e8e8f0; --muted:#889; --line:#2a2a40; --accent:#7d00ff; }}
    * {{ box-sizing: border-box; }}
    body {{ margin:0; font-family: ui-sans-serif, system-ui, sans-serif; background:var(--bg); color:var(--fg); line-height:1.45; }}
    header {{ padding:1.5rem 1.25rem; border-bottom:1px solid var(--line); background:linear-gradient(180deg,#1a1030,#0b0b12); }}
    h1 {{ margin:0 0 .35rem; font-size:1.45rem; }}
    .sub {{ color:var(--muted); font-size:.95rem; max-width:52rem; }}
    main {{ padding:1.25rem; max-width:1100px; margin:0 auto; }}
    .cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(140px,1fr)); gap:.75rem; margin:1rem 0 1.5rem; }}
    .card {{ background:var(--card); border:1px solid var(--line); border-radius:12px; padding:1rem; }}
    .card b {{ display:block; font-size:1.5rem; }}
    .warn {{ background:#2a1a10; border:1px solid #664400; color:#ffcc99; padding:.85rem 1rem; border-radius:10px; margin-bottom:1rem; font-size:.9rem; }}
    table {{ width:100%; border-collapse:collapse; font-size:.88rem; }}
    th, td {{ border-bottom:1px solid var(--line); padding:.55rem .4rem; text-align:left; vertical-align:top; }}
    th {{ color:var(--muted); font-weight:600; }}
    .prev {{ color:#ccc; max-width:28rem; }}
    footer {{ padding:1.5rem 1.25rem; color:var(--muted); font-size:.85rem; border-top:1px solid var(--line); margin-top:2rem; }}
    a {{ color:#b388ff; }}
    code {{ background:#222; padding:.1rem .3rem; border-radius:4px; }}
  </style>
</head>
<body>
  <header>
    <h1>LYGO Deception Radar</h1>
    <p class="sub">Public discourse-signal feed from the labeled Ops Detector suite.
    <strong>Not a person profiler.</strong> Operational bar: ops ≥ {ethics.get('operational_threshold', 0.65)} or high evasion.</p>
  </header>
  <main>
    <div class="warn">
      <strong>Ethics:</strong> Public sample texts only. Scores are heuristic discourse patterns — not guilt, identity, or legal findings.
      Weak/calibration bands are for ranking short samples, not production alerts.
    </div>
    <div class="cards">
      <div class="card"><span>Samples</span><b>{stats.get('samples', 0)}</b></div>
      <div class="card"><span>Strong</span><b style="color:#e94560">{stats.get('strong', 0)}</b></div>
      <div class="card"><span>Weak (cal)</span><b style="color:#ffcc00">{stats.get('weak_calibration', 0)}</b></div>
      <div class="card"><span>Clear</span><b style="color:#00ff88">{stats.get('clear', 0)}</b></div>
    </div>
    <p class="sub">Generated: <code>{feed.get('generated_utc')}</code> · Signature: <code>{feed.get('signature')}</code></p>
    <table>
      <thead><tr><th>ID</th><th>Band</th><th>Ops</th><th>Evasion</th><th>Preview</th></tr></thead>
      <tbody>
        {''.join(rows_html)}
      </tbody>
    </table>
  </main>
  <footer>
    Part of the LYGO lattice ·
    <a href="https://clawhub.ai/deepseekoracle/lygo-ops-detector">Ops Detector</a> ·
    <a href="https://clawhub.ai/deepseekoracle/lygo-kickstart-wizard">Kickstart</a> ·
    <a href="https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChart.html">Star Chart</a><br/>
    Feed JSON: <code>radar_feed.json</code> · Rebuild: <code>python scripts/build_radar_feed.py --write-html</code>
  </footer>
</body>
</html>
"""
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text(html, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Build LYGO Deception Radar public feed")
    ap.add_argument("--suite", default="", help="Path to labeled_discourse_suite.json")
    ap.add_argument("--out-json", default="", help="Write radar_feed.json")
    ap.add_argument("--write-html", action="store_true", help="Also write index.html next to JSON")
    ap.add_argument("--out-html", default="", help="HTML path (default beside JSON)")
    ap.add_argument("--operational-threshold", type=float, default=0.65)
    args = ap.parse_args()

    suite = Path(args.suite) if args.suite else None
    if suite is None:
        for cand in (
            SKILL.parent / "lygo-ops-detector" / "tests" / "labeled_discourse_suite.json",
            Path(r"I:\E Drive\.grok\skills\lygo-ops-detector\tests\labeled_discourse_suite.json"),
            Path(r"D:\lygo-protocol-stack\clawhub\mirrors\lygo-ops-detector\tests\labeled_discourse_suite.json"),
            SKILL / "tests" / "public_samples.json",
        ):
            if cand.is_file():
                suite = cand
                break

    samples = load_suite(suite)
    if not samples:
        print(json.dumps({"ok": False, "error": "no_samples"}))
        return 2

    feed = build_feed(samples, operational=args.operational_threshold)
    if not feed.get("ok"):
        print(json.dumps(feed, indent=2))
        return 1

    out_json = Path(args.out_json) if args.out_json else (SKILL / "data" / "radar_feed.json")
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(feed, indent=2) + "\n", encoding="utf-8")

    if args.write_html or args.out_html:
        out_html = Path(args.out_html) if args.out_html else (out_json.parent / "index.html")
        write_html(feed, out_html)
        print(json.dumps({"ok": True, "json": str(out_json), "html": str(out_html), "stats": feed["stats"]}, indent=2))
    else:
        print(json.dumps({"ok": True, "json": str(out_json), "stats": feed["stats"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
