"""
demo.py — Library of Babel: Three Demonstrations
=================================================
Run: python3 demo.py

Demo 1: Locate a text string — find its permanent address in the Library
Demo 2: Read a page at given coordinates — show what lives there
Demo 3: Entropy heatmap — 5 random coordinates, ranked by Shannon entropy + space frequency
"""

import json
import os
import random
import time
from babel_core import (
    format_locate,
    format_read_page,
    locate as babel_locate,
    read_page,
    shannon_entropy,
    space_frequency,
    classify_page,
)

_CODEX_PATH = os.path.join(os.path.dirname(__file__), "codex.json")

# ---------------------------------------------------------------------------
# Demo 1: Locate text
# ---------------------------------------------------------------------------

def locate(text: str):
    """Find the permanent coordinates of any text in the Library of Babel."""
    print(f'\n{"=" * 60}')
    print(f'DEMO 1: Locating text')
    print(f'Input: "{text}"')
    print(f'{"=" * 60}')
    print(format_locate(text))
    print()

# ---------------------------------------------------------------------------
# Demo 2: Read a page
# ---------------------------------------------------------------------------

def read_page_demo(hexagon: int = 1, wall: int = 1, shelf: int = 1, volume: int = 1):
    """Read the page at given Library coordinates."""
    print(f'\n{"=" * 60}')
    print(f'DEMO 2: Reading a page')
    print(f'Coordinates: Hex {hexagon:,} · Wall {wall} · Shelf {shelf} · Vol {volume}')
    print(f'{"=" * 60}')
    print("(Computing — may take a few seconds for BigInt ops...)")
    t0 = time.time()
    result = format_read_page(hexagon, wall, shelf, volume)
    elapsed = time.time() - t0
    print(result)
    print(f'\n[Generated in {elapsed:.2f}s]')
    print()

# ---------------------------------------------------------------------------
# Demo 3: Entropy heatmap
# ---------------------------------------------------------------------------

def entropy_heatmap(n: int = 5, seed: int = 42):
    """
    Generate n random coordinates, compute Shannon entropy + space frequency for each.
    Rank from lowest entropy (most structured) to highest entropy (most noise-like).

    Shannon entropy reference:
      Human English  : ~3.8 – 4.2 bits
      Interesting    : ~4.2 – 4.5 bits
      Pure noise     : ~4.5 – 4.61 bits  (log2(29) ≈ 4.86 theoretical max)
    Space frequency:
      BASE-29 noise  : ~3.4%
      English text   : ~18%
    """
    print(f'\n{"=" * 72}')
    print(f'DEMO 3: Entropy Heatmap ({n} random coordinates)')
    print(f'Shannon entropy (bits/char) + space frequency  →  noise / interesting / coherent')
    print(f'{"=" * 72}')

    rng = random.Random(seed)

    entries = []
    for i in range(n):
        coords = {
            "hexagon": rng.randint(0, 10_000_000),
            "wall":    rng.randint(1, 4),
            "shelf":   rng.randint(1, 5),
            "volume":  rng.randint(1, 32),
        }
        label = (
            f"Hexagon {coords['hexagon']:,} · Wall {coords['wall']} · "
            f"Shelf {coords['shelf']} · Volume {coords['volume']}"
        )
        print(f"  [{i+1}/{n}] Reading {label}...")
        t0 = time.time()
        page = read_page(coords["hexagon"], coords["wall"], coords["shelf"], coords["volume"])
        elapsed = time.time() - t0
        h = shannon_entropy(page)
        sp = space_frequency(page)
        tag = classify_page(h, sp)
        entries.append({
            "label": label,
            "entropy": h,
            "space_pct": sp,
            "tag": tag,
            "page_preview": page[:60],
            "time": elapsed,
        })

    # Rank by entropy ascending (lower = more structured = more interesting)
    ranked = sorted(entries, key=lambda e: e["entropy"])

    print(f'\n{"─" * 72}')
    print(f'RANKED LOWEST → HIGHEST ENTROPY (most structured first)\n')
    for rank, entry in enumerate(ranked, 1):
        print(
            f"  #{rank} {entry['label']}  |  "
            f"H={entry['entropy']:.2f} bits  |  "
            f"space={entry['space_pct']:.1f}%  |  {entry['tag']}"
        )
        print(f"       Preview: {entry['page_preview']!r}")
        print()

# ---------------------------------------------------------------------------
# Codex: pre-mapped passages
# ---------------------------------------------------------------------------

def show_codex():
    """Display all pre-mapped locations in the Library of Babel."""
    print(f'\n{"=" * 66}')
    print(f'CODEX: Pre-Mapped Passages')
    print(f'These addresses are permanent. The Library has always held them.')
    print(f'{"=" * 66}')

    with open(_CODEX_PATH, "r") as f:
        data = json.load(f)

    for entry in data["codex"]:
        hex_fmt = f"{entry['hexagon']:,}"
        print(f'\n  📍 "{entry["text"]}"')
        print(f'     Source: {entry["source"]}')
        print(
            f'     Hexagon {hex_fmt} · Wall {entry["wall"]} · '
            f'Shelf {entry["shelf"]} · Volume {entry["volume"]}'
        )
    print()


def add_to_codex(text: str, source: str):
    """
    Compute coordinates for new text and append to codex.json.
    Prints confirmation with full coordinates.
    """
    result = babel_locate(text)
    hex_fmt = f"{result['hexagon']:,}"

    with open(_CODEX_PATH, "r") as f:
        data = json.load(f)

    # Avoid duplicate entries for the same text
    existing_texts = [e["text"] for e in data["codex"]]
    if text.lower() in existing_texts:
        result = babel_locate(text)
        hex_fmt = f"{result['hexagon']:,}"
        print(f'  Already in codex: "{text}"')
        print(f'  Hexagon {hex_fmt} · Wall {result["wall"]} · Shelf {result["shelf"]} · Volume {result["volume"]}')
        return

    entry = {
        "text": text,
        "source": source,
        "hexagon": result["hexagon"],
        "wall": result["wall"],
        "shelf": result["shelf"],
        "volume": result["volume"],
    }
    data["codex"].append(entry)

    with open(_CODEX_PATH, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f'\n  ✅ Added to codex: "{text}"')
    print(f'     Source: {source}')
    print(f'     Hexagon {hex_fmt} · Wall {result["wall"]} · Shelf {result["shelf"]} · Volume {result["volume"]}')
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("\n╔══════════════════════════════════════════════════════════╗")
    print("║          THE LIBRARY OF BABEL — Mathematical Engine       ║")
    print("║  Every text that exists already has a permanent address.  ║")
    print("╚══════════════════════════════════════════════════════════╝")

    # Demo 1: Locate a famous text
    locate("the library of babel")

    # Demo 2: Read a page at fixed coordinates
    read_page_demo(hexagon=1, wall=1, shelf=1, volume=1)

    # Demo 3: Entropy heatmap
    entropy_heatmap(n=5)

    # Demo 4: Codex — pre-mapped passages
    show_codex()

    print("=" * 60)
    print("Done. The Library has always contained these pages.")
    print("=" * 60)
