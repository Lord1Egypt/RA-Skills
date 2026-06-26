#!/usr/bin/env python3
# SECURITY MANIFEST:
# Environment variables accessed: none
# External endpoints called: none
# Local files read: none
# Local files written: output JSON spec file
"""
Generate a starter JSON spec for building editable PPTX slides.

Usage examples:
  python scripts/generate_spec_template.py --title "Sample" --output sample_spec.json
  python scripts/generate_spec_template.py --title "Deck" --slides 3 --output deck_spec.json
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def make_slide(index: int, title: str) -> dict:
    return {
        "background": "F8F8FA",
        "items": [
            {
                "kind": "textbox",
                "x": 0.0,
                "y": 0.4,
                "w": 13.333,
                "h": 0.55,
                "text": f"{title}" if index == 1 else f"{title} — Slide {index}",
                "size": 32,
                "color": "1B3460",
                "align": "center",
            },
            {
                "kind": "shape",
                "shape": "round_rect",
                "x": 0.8,
                "y": 1.4,
                "w": 4.0,
                "h": 0.9,
                "fill": "E9EBF1",
                "text": "Replace with reconstructed section",
                "size": 18,
                "color": "1B3460",
                "align": "center",
            },
            {
                "kind": "textbox",
                "x": 0.9,
                "y": 2.55,
                "w": 4.4,
                "h": 0.45,
                "text": "Use shapes and text to match the source image.",
                "size": 16,
                "color": "243A5C",
                "align": "left",
            }
        ]
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", default="Editable Slide")
    parser.add_argument("--slides", type=int, default=1)
    parser.add_argument("--width", type=float, default=13.333)
    parser.add_argument("--height", type=float, default=7.5)
    parser.add_argument("--background", default="F8F8FA")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    spec = {
        "presentation": {
            "width": args.width,
            "height": args.height,
            "background": args.background,
        },
        "slides": [make_slide(i + 1, args.title) for i in range(args.slides)],
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(spec, indent=2) + "\n")
    print(out)


if __name__ == "__main__":
    main()
