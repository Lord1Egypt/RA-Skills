#!/usr/bin/env python3

import argparse
import json
import os
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Generate OpenClaw growth charts from analytics summary JSON.")
    parser.add_argument("--analytics", required=True, help="Path to analytics summary JSON")
    parser.add_argument("--out-dir", required=True, help="Directory for generated PNG files")
    parser.add_argument("--manifest", required=True, help="Output chart manifest JSON path")
    return parser.parse_args()


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def sanitize_slug(value: str) -> str:
    safe = []
    for ch in value.lower():
        if ch.isalnum():
            safe.append(ch)
        elif ch in ("-", "_"):
            safe.append(ch)
        else:
            safe.append("_")
    return "".join(safe).strip("_") or "signal"


def to_float(value):
    try:
        number = float(value)
        if number != number:  # NaN check
            return None
        return number
    except (TypeError, ValueError):
        return None


def render_signal_chart(signal, out_file: Path):
    try:
        import matplotlib.pyplot as plt
    except Exception as exc:
        raise RuntimeError(
            "matplotlib is required. Install with: python3 -m pip install matplotlib"
        ) from exc

    current = to_float(signal.get("current_value") or signal.get("currentValue"))
    baseline = to_float(signal.get("baseline_value") or signal.get("baselineValue"))
    metric_name = str(signal.get("metric") or "metric")
    title = str(signal.get("title") or "Signal")
    delta = to_float(signal.get("delta_percent") or signal.get("deltaPercent"))

    labels = []
    values = []
    if baseline is not None:
        labels.append("baseline")
        values.append(baseline)
    if current is not None:
        labels.append("current")
        values.append(current)

    if not values:
        return False

    colors = ["#9ca3af" if label == "baseline" else "#2563eb" for label in labels]
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    bars = ax.bar(labels, values, color=colors)
    ax.set_title(title)
    ax.set_ylabel(metric_name)

    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value:.3g}",
            ha="center",
            va="bottom",
            fontsize=9,
        )

    if delta is not None:
        ax.text(
            0.99,
            0.95,
            f"delta: {delta:.1f}%",
            transform=ax.transAxes,
            ha="right",
            va="top",
            fontsize=10,
            color="#b91c1c" if delta < 0 else "#166534",
        )

    fig.tight_layout()
    fig.savefig(out_file, dpi=160)
    plt.close(fig)
    return True


def main():
    args = parse_args()
    analytics_path = Path(args.analytics).resolve()
    out_dir = Path(args.out_dir).resolve()
    manifest_path = Path(args.manifest).resolve()

    payload = load_json(analytics_path)
    signals = payload.get("signals", [])
    if not isinstance(signals, list):
        raise RuntimeError("analytics summary must contain an array at `signals`")

    out_dir.mkdir(parents=True, exist_ok=True)
    charts = []
    for idx, signal in enumerate(signals):
        if not isinstance(signal, dict):
            continue
        signal_id = str(signal.get("id") or f"signal_{idx + 1}")
        slug = sanitize_slug(signal_id)
        title = str(signal.get("title") or signal_id)
        file_path = out_dir / f"{slug}.png"
        rendered = render_signal_chart(signal, file_path)
        if not rendered:
            continue
        charts.append(
            {
                "signal_id": signal_id,
                "file_path": str(file_path),
                "caption": f"{title} ({signal.get('metric') or 'metric'})",
            }
        )

    manifest = {
        "generated_at": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "source_file": str(analytics_path),
        "chart_count": len(charts),
        "charts": charts,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)

    print(str(manifest_path))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
