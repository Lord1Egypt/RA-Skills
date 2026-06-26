#!/usr/bin/env python3
"""
Generate four A/B-testable variants of the same thumbnail using different
color schemes and text positions. All variants share the same source frame
and title; only style choices differ. Useful for split-testing click rate.

Usage:
  python3 make_variants.py <source_frame> <output_dir> --title TEXT
                                                       [--subtitle TEXT]
                                                       [--font PATH]
                                                       [--logo PATH]
                                                       [--logo-corner CORNER]
                                                       [--logo-scale FLOAT]

Writes:
  variant_a_bold_yellow_bottom.png
  variant_b_clean_white_top.png
  variant_c_red_alert_center.png
  variant_d_cool_blue_bottom.png

Optional auto-pick (added v0.3.0):
  --auto-pick    Score every produced variant with score_thumbnail.py and copy
                 the winner to <output_dir>/winner.png. Also writes a small
                 winner.json with the ranking.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

SAFE_PATH_RE = re.compile(r"^[\w./\-+ @=:%,()'\[\]]+$")

VARIANTS = [
    ("a", "bold-yellow", "bottom"),
    ("b", "clean-white", "top"),
    ("c", "red-alert", "center"),
    ("d", "cool-blue", "bottom"),
]


def safe_path(p: str) -> Path:
    if not SAFE_PATH_RE.match(p):
        raise ValueError(f"Refusing path with unsafe characters: {p!r}")
    return Path(p).expanduser()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("input", help="Source frame image")
    parser.add_argument("output_dir", help="Output directory for variants")
    parser.add_argument("--title", required=True, help="Main title text")
    parser.add_argument("--subtitle", default="", help="Optional subtitle text")
    parser.add_argument("--font", default="", help="Path to a TTF/OTF font")
    parser.add_argument("--logo", default="", help="Optional logo image path")
    parser.add_argument("--logo-corner", default="top-right",
                        help="Logo corner (top-left, top-right, bottom-left, bottom-right)")
    parser.add_argument("--logo-scale", type=float, default=0.12,
                        help="Logo width as a fraction of image width")
    parser.add_argument("--auto-pick", action="store_true",
                        help="Score variants with score_thumbnail.py and copy "
                             "the winner to <output_dir>/winner.png")
    args = parser.parse_args()

    try:
        src = safe_path(args.input).resolve()
        out_dir = safe_path(args.output_dir).resolve()
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if not src.exists():
        print(f"error: input not found: {src}", file=sys.stderr)
        return 2
    if not args.title or not args.title.strip():
        print("error: --title must be a non-empty string", file=sys.stderr)
        return 2

    out_dir.mkdir(parents=True, exist_ok=True)

    # Locate compose_thumbnail.py next to this script
    here = Path(__file__).resolve().parent
    compose = here / "compose_thumbnail.py"
    if not compose.is_file():
        print(f"error: compose_thumbnail.py not found next to make_variants.py at {compose}",
              file=sys.stderr)
        return 1

    written = 0
    for letter, scheme, position in VARIANTS:
        out_name = f"variant_{letter}_{scheme.replace('-', '_')}_{position}.png"
        out_path = out_dir / out_name

        cmd = [
            sys.executable, str(compose),
            str(src), str(out_path),
            "--title", args.title,
            "--color-scheme", scheme,
            "--position", position,
        ]
        if args.subtitle:
            cmd += ["--subtitle", args.subtitle]
        if args.font:
            cmd += ["--font", args.font]
        if args.logo:
            cmd += ["--logo", args.logo, "--logo-corner", args.logo_corner,
                    "--logo-scale", str(args.logo_scale)]

        res = subprocess.run(cmd, check=False, text=True, stderr=subprocess.PIPE)
        if res.returncode != 0:
            print(f"  variant {letter} failed: {res.stderr.strip()}", file=sys.stderr)
            continue
        print(f"  wrote {out_path}  ({scheme}, {position})", file=sys.stderr)
        written += 1

    if written == 0:
        print("error: no variants produced", file=sys.stderr)
        return 1

    print(f"Wrote {written} variant(s) to {out_dir}", file=sys.stderr)

    if args.auto_pick:
        scorer = here / "score_thumbnail.py"
        if not scorer.is_file():
            print("warning: --auto-pick requested but score_thumbnail.py "
                  "is not next to make_variants.py; skipping.",
                  file=sys.stderr)
            return 0
        produced = sorted(out_dir.glob("variant_*.png"))
        if not produced:
            print("warning: --auto-pick found no variant_*.png files",
                  file=sys.stderr)
            return 0
        cmd = [sys.executable, str(scorer), "--json"] + [str(p) for p in produced]
        res = subprocess.run(cmd, check=False, text=True, capture_output=True)
        if res.returncode != 0:
            print(f"warning: scorer failed: {res.stderr.strip()}",
                  file=sys.stderr)
            return 0
        try:
            import json
            payload = json.loads(res.stdout)
        except Exception as e:
            print(f"warning: could not parse scorer output: {e}",
                  file=sys.stderr)
            return 0
        winner_path = None
        winner_block = payload.get("winner")
        if isinstance(winner_block, dict):
            winner_path = winner_block.get("winner_file") or winner_block.get("file")
            ranked = winner_block.get("ranked") or []
            if not winner_path and ranked:
                winner_path = ranked[0].get("file")
        elif isinstance(winner_block, str):
            winner_path = winner_block
        if not winner_path:
            results = payload.get("results") or []
            if results:
                best = max(results,
                           key=lambda r: r.get("click_score", 0))
                winner_path = best.get("file")
        if not winner_path:
            print("warning: scorer did not return a winner file",
                  file=sys.stderr)
            return 0
        winner_src = Path(winner_path)
        winner_dst = out_dir / "winner.png"
        try:
            import shutil
            shutil.copyfile(winner_src, winner_dst)
        except Exception as e:
            print(f"warning: could not copy winner: {e}", file=sys.stderr)
            return 0
        ranking_path = out_dir / "winner.json"
        ranking_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"Auto-pick: winner = {winner_src.name} -> {winner_dst}",
              file=sys.stderr)
        print(f"  ranking written to {ranking_path}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
