#!/usr/bin/env python3
"""
Score one or more finished thumbnails on objective visual metrics that
correlate with click-through rate, then optionally pick a winner.

This is NOT a real CTR prediction model. It is a deterministic, local
heuristic combining widely-cited thumbnail-design rules:

  - Punch:        global contrast (stddev of luminance)
  - Focal pop:    saliency proxy = local contrast variance over 32x32 tiles
  - Color punch:  saturation mean + saturation stddev (weighted)
  - Text impact:  presence of a high-contrast horizontal text band
                  (long horizontal runs of high local-edge density)
  - Brightness:   distance from the optimal mid-tone (penalty for too dark
                  or too washed-out)
  - Edge density: fraction of pixels above an edge-magnitude threshold
                  (proxy for visual busy-ness; mid values are best)

Each metric is normalised into [0, 100] and weighted into a final
'click_score' in [0, 100]. When given two or more thumbnails, the script
ranks them and prints which one is most likely to perform best, plus the
per-metric reasons each won or lost.

Pure standard library + Pillow. No ML, no remote calls.

Usage:
  python3 score_thumbnail.py <image1> [image2 image3 ...]
  python3 score_thumbnail.py a.png b.png c.png --json
  python3 score_thumbnail.py a.png b.png --output report.json

Exit codes:
  0 = success
  1 = unable to score any input
  2 = bad arguments / missing file / unreadable image
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    from PIL import Image, ImageFilter, ImageStat
except ImportError:
    print("error: Pillow not installed. Run: pip install Pillow", file=sys.stderr)
    sys.exit(2)


SAFE_PATH_RE = re.compile(r"^[\w./\-+ @=:%,()'\[\]]+$")


def safe_path(p: str) -> Path:
    if not SAFE_PATH_RE.match(p):
        raise ValueError(f"Refusing path with unsafe characters: {p!r}")
    return Path(p).expanduser()


def _global_contrast(luma: Image.Image) -> float:
    """Stddev of luminance, capped to a typical thumbnail range."""
    return float(ImageStat.Stat(luma).stddev[0])


def _focal_pop(luma: Image.Image, tile: int = 32) -> float:
    """Saliency proxy: variance of per-tile mean luminance.

    A thumbnail with one obvious focal area (subject brighter than the
    background) gets a high score. A flat or uniformly busy image gets a
    low score.
    """
    W, H = luma.size
    tx = max(1, W // tile)
    ty = max(1, H // tile)
    means: List[float] = []
    for j in range(ty):
        for i in range(tx):
            box = (i * tile, j * tile,
                   min((i + 1) * tile, W), min((j + 1) * tile, H))
            tile_img = luma.crop(box)
            means.append(ImageStat.Stat(tile_img).mean[0])
    if len(means) < 2:
        return 0.0
    avg = sum(means) / len(means)
    var = sum((m - avg) ** 2 for m in means) / len(means)
    return var ** 0.5  # stddev of tile means


def _color_punch(rgb: Image.Image) -> float:
    """Saturation-based punchiness via HSV stddev + mean."""
    hsv = rgb.convert("HSV")
    s_band = hsv.split()[1]
    stat = ImageStat.Stat(s_band)
    sat_mean = float(stat.mean[0])
    sat_std = float(stat.stddev[0])
    # Combined: a punchy image has both decent average saturation AND
    # variation (so it isn't a single flat colour).
    return 0.65 * sat_mean + 0.35 * sat_std


def _text_band_score(luma: Image.Image) -> float:
    """Detect a high-contrast horizontal text band.

    Compute per-row edge density. A long stretch of consecutive rows with
    above-mean edge density indicates a horizontal text strip (title bar
    or subtitle), which is a strong CTR signal.
    """
    edges = luma.filter(ImageFilter.FIND_EDGES)
    W, H = edges.size
    # Row-wise edge density.
    row_density: List[float] = []
    for y in range(H):
        row = edges.crop((0, y, W, y + 1))
        row_density.append(float(ImageStat.Stat(row).mean[0]))
    if not row_density:
        return 0.0
    avg = sum(row_density) / len(row_density)
    # Length of longest run where density > 1.4 * avg.
    longest = 0
    current = 0
    threshold = avg * 1.4
    for d in row_density:
        if d > threshold:
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    # Normalise to image height: a 6-12% band is the sweet spot.
    if H == 0:
        return 0.0
    band_frac = longest / H
    if band_frac < 0.03:
        return band_frac * 800  # 0..24
    if band_frac < 0.12:
        return 50 + (band_frac - 0.03) * 500  # 50..95
    if band_frac < 0.30:
        return 95 - (band_frac - 0.12) * 200  # taper down (too much text bar)
    return max(0.0, 60 - (band_frac - 0.30) * 100)


def _brightness_score(luma: Image.Image) -> float:
    """Penalty for being far from the ideal mid-tone (130/255)."""
    mean = float(ImageStat.Stat(luma).mean[0])
    ideal = 130.0
    dist = abs(mean - ideal) / ideal
    return max(0.0, 100.0 * (1.0 - dist))


def _edge_density_score(luma: Image.Image) -> Tuple[float, float]:
    """Fraction of high-edge pixels. Mid values are best."""
    edges = luma.filter(ImageFilter.FIND_EDGES)
    stat = ImageStat.Stat(edges)
    mean = float(stat.mean[0])
    # Heuristic: ideal mean edge magnitude is ~25-40 (bytes 0..255).
    if mean < 8:
        score = mean * 5  # too smooth, very low score
    elif mean < 25:
        score = 40 + (mean - 8) * 2.5  # 40..82
    elif mean < 45:
        score = 95 - abs(mean - 32) * 0.5  # peak near 32
    else:
        score = max(20.0, 90 - (mean - 45) * 1.5)  # too busy
    return min(100.0, max(0.0, score)), mean


def score_image(path: Path) -> Optional[Dict]:
    """Compute every metric for a single thumbnail."""
    try:
        with Image.open(path) as srcimg:
            srcimg.verify()
        with Image.open(path) as srcimg:
            rgb = srcimg.convert("RGB")
    except Exception as e:
        print(f"error: could not read {path}: {e.__class__.__name__}: {e}", file=sys.stderr)
        return None

    W, H = rgb.size
    luma = rgb.convert("L")

    # Raw metrics.
    contrast = _global_contrast(luma)
    focal = _focal_pop(luma)
    color = _color_punch(rgb)
    band = _text_band_score(luma)
    bright = _brightness_score(luma)
    edge_score, edge_mean = _edge_density_score(luma)

    # Normalise raw signals into 0-100 sub-scores.
    sub = {
        "punch":         min(100.0, contrast * 1.6),     # 0..~100
        "focal_pop":     min(100.0, focal * 2.5),         # 0..~100
        "color_punch":   min(100.0, color * 0.8),         # 0..~100
        "text_band":     band,                            # already 0..100
        "brightness":    bright,                          # already 0..100
        "edge_density":  edge_score,                      # already 0..100
    }

    # Weighted composite. Weights add to 1.0.
    weights = {
        "punch":         0.18,
        "focal_pop":     0.22,
        "color_punch":   0.15,
        "text_band":     0.20,
        "brightness":    0.12,
        "edge_density":  0.13,
    }
    click_score = sum(sub[k] * weights[k] for k in weights)
    click_score = round(min(100.0, max(0.0, click_score)), 2)

    return {
        "file": str(path),
        "size": [W, H],
        "click_score": click_score,
        "sub_scores": {k: round(v, 2) for k, v in sub.items()},
        "raw": {
            "contrast": round(contrast, 2),
            "focal_tile_stddev": round(focal, 2),
            "saturation_compound": round(color, 2),
            "edge_mean": round(edge_mean, 2),
        },
    }


def explain_winner(results: List[Dict]) -> Dict:
    """Pick the highest click_score and explain why it won vs each rival."""
    ranked = sorted(results, key=lambda r: r["click_score"], reverse=True)
    winner = ranked[0]
    others = ranked[1:]
    reasons: List[Dict] = []
    for o in others:
        diffs = []
        for k, w_v in winner["sub_scores"].items():
            o_v = o["sub_scores"][k]
            delta = round(w_v - o_v, 2)
            if abs(delta) >= 5:
                diffs.append({"metric": k, "winner": w_v, "rival": o_v, "delta": delta})
        diffs.sort(key=lambda d: abs(d["delta"]), reverse=True)
        reasons.append({
            "rival_file": o["file"],
            "rival_score": o["click_score"],
            "score_gap": round(winner["click_score"] - o["click_score"], 2),
            "top_reasons": diffs[:3],
        })
    return {
        "winner_file": winner["file"],
        "winner_score": winner["click_score"],
        "ranked": [{"file": r["file"], "click_score": r["click_score"]} for r in ranked],
        "reasons_vs_others": reasons,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("inputs", nargs="+", help="One or more thumbnail image paths")
    parser.add_argument("--output", default="", help="Optional path to write JSON report (default: stdout)")
    parser.add_argument("--json", action="store_true", help="Emit JSON to stdout instead of human-readable text")
    args = parser.parse_args()

    paths: List[Path] = []
    for raw in args.inputs:
        try:
            p = safe_path(raw).resolve()
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
        if not p.is_file():
            print(f"error: file not found: {p}", file=sys.stderr)
            return 2
        paths.append(p)

    results: List[Dict] = []
    for p in paths:
        r = score_image(p)
        if r is not None:
            results.append(r)

    if not results:
        print("error: no images could be scored", file=sys.stderr)
        return 1

    report: Dict = {
        "results": results,
    }
    if len(results) > 1:
        report["winner"] = explain_winner(results)

    if args.output:
        try:
            outp = safe_path(args.output).resolve()
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {outp}", file=sys.stderr)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for r in sorted(results, key=lambda x: x["click_score"], reverse=True):
            print(f"{r['file']}")
            print(f"  click_score: {r['click_score']:.2f} / 100")
            for k, v in r["sub_scores"].items():
                print(f"    {k:<14s} {v:>6.2f}")
        if "winner" in report:
            w = report["winner"]
            print()
            print(f"Winner: {w['winner_file']}  (score {w['winner_score']:.2f})")
            for entry in w["reasons_vs_others"]:
                print(f"  beats {entry['rival_file']} by {entry['score_gap']:+.2f}")
                for d in entry["top_reasons"]:
                    sign = "+" if d["delta"] > 0 else ""
                    print(f"    {d['metric']:<14s} winner={d['winner']:.2f} rival={d['rival']:.2f}  ({sign}{d['delta']:.2f})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
