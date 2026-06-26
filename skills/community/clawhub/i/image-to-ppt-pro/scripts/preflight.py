#!/usr/bin/env python3
"""
preflight.py — Pre-execution coordinate check tool for PPT scripts
Usage: python scripts/preflight.py create_slide.js

Checks three types of issues:
  ❌ Out of bounds    Elements with x+w > 10 or y+h > 5.625 (must fix)
  ⚠️  Overlap    Non-parent-child rectangle intersections (manual confirmation needed)
  📋 Summary    All elements sorted by y coordinate, compare region proportions with original image

Note: Uses regex to parse x/y/w/h literals from JS, covers most writing styles.
      Dynamic coordinates (for loops, variable operations) need manual verification.
"""

import re
import sys
from itertools import combinations

SLIDE_W      = 10.0
SLIDE_H      = 5.625
SAFE_MARGIN  = 0.01   # Float error tolerance


def parse_elements(js_path):
    """Parse all addShape / addText coordinates from JS file."""
    with open(js_path, encoding="utf-8") as f:
        content = f.read()

    elements = []

    # Match addShape/addText call blocks (greedy capture until first }); )
    call_pat = re.compile(
        r'(addShape|addText)\s*\('
        r'(.*?)'          # Call content
        r'\)\s*;',
        re.DOTALL
    )
    coord_pat = re.compile(
        r'\bx\s*:\s*(-?[\d.]+).*?'
        r'\by\s*:\s*(-?[\d.]+).*?'
        r'\bw\s*:\s*(-?[\d.]+).*?'
        r'\bh\s*:\s*(-?[\d.]+)',
        re.DOTALL
    )
    comment_pat = re.compile(r'//\s*(.+)')

    for i, m in enumerate(call_pat.finditer(content)):
        body = m.group(2)
        cm = coord_pat.search(body)
        if not cm:
            continue

        x = float(cm.group(1))
        y = float(cm.group(2))
        w = abs(float(cm.group(3)))
        h = abs(float(cm.group(4)))

        # Get nearest line comment before call as label
        snippet = content[max(0, m.start() - 300):m.start()]
        comments = comment_pat.findall(snippet)
        label = comments[-1].strip()[:50] if comments else f"#{i+1} {m.group(1)}"

        elements.append({
            "id":    i + 1,
            "type":  m.group(1),
            "label": label,
            "x": x,  "y": y,
            "w": w,  "h": h,
            "x2": x + w,
            "y2": y + h,
        })

    return elements


def check_boundary(elements):
    """Check A: Out of bounds detection."""
    violations = []
    for el in elements:
        issues = []
        if el["x2"] > SLIDE_W + SAFE_MARGIN:
            issues.append(f"Right overflow  x+w = {el['x2']:.3f}\"  (limit {SLIDE_W}\")")
        if el["y2"] > SLIDE_H + SAFE_MARGIN:
            issues.append(f"Bottom overflow  y+h = {el['y2']:.3f}\"  (limit {SLIDE_H}\")")
        if el["x"] < -SAFE_MARGIN:
            issues.append(f"Left overflow  x = {el['x']:.3f}\"")
        if el["y"] < -SAFE_MARGIN:
            issues.append(f"Top overflow  y = {el['y']:.3f}\"")
        if issues:
            violations.append((el, issues))
    return violations


def rect_overlap_area(a, b):
    """Calculate overlap area of two rectangles, return 0 if no overlap."""
    ox = min(a["x2"], b["x2"]) - max(a["x"], b["x"])
    oy = min(a["y2"], b["y2"]) - max(a["y"], b["y"])
    return ox * oy if ox > 0 and oy > 0 else 0


def contains(a, b):
    """Determine if rectangle a completely contains b (parent-child relationship)."""
    return (a["x"] - SAFE_MARGIN <= b["x"] and
            a["x2"] + SAFE_MARGIN >= b["x2"] and
            a["y"] - SAFE_MARGIN <= b["y"] and
            a["y2"] + SAFE_MARGIN >= b["y2"])


def check_overlap(elements):
    """Check B: Suspected overlap (exclude parent-child containment, only report intersections with area > 0.01)."""
    warnings = []
    for a, b in combinations(elements, 2):
        area = rect_overlap_area(a, b)
        if area < 0.01:
            continue
        if contains(a, b) or contains(b, a):
            continue      # Parent-child relationship, normal overlay
        warnings.append((a, b, area))
    # Sort by overlap area descending, only return top 15
    warnings.sort(key=lambda x: -x[2])
    return warnings[:15]


def print_summary(elements):
    """Output coordinate summary table sorted by y coordinate."""
    sorted_els = sorted(elements, key=lambda e: (round(e["y"], 2), e["x"]))
    print("\n📋 Coordinate Summary (sorted by y)")
    print(f"  {'ID':>3}  {'Type':<10}  {'x':>5}  {'y':>5}  {'w':>5}  {'h':>5}  {'x+w':>5}  {'y+h':>5}  {'Height%':>5}  Label")
    print("  " + "─" * 80)
    for el in sorted_els:
        pct = el["h"] / SLIDE_H * 100
        flag = "❌" if (el["x2"] > SLIDE_W + SAFE_MARGIN or
                        el["y2"] > SLIDE_H + SAFE_MARGIN) else "  "
        print(f"  {flag}{el['id']:>3}  {el['type']:<10}  "
              f"{el['x']:>5.2f}  {el['y']:>5.2f}  "
              f"{el['w']:>5.2f}  {el['h']:>5.2f}  "
              f"{el['x2']:>5.2f}  {el['y2']:>5.2f}  "
              f"{pct:>4.1f}%  {el['label']}")


def main():
    js_path = sys.argv[1] if len(sys.argv) > 1 else "create_slide.js"

    try:
        elements = parse_elements(js_path)
    except FileNotFoundError:
        print(f"❌ File not found: {js_path}")
        sys.exit(1)

    if not elements:
        print("⚠️  No addShape/addText elements parsed, please check script format")
        sys.exit(1)

    print(f"\n🔍 Pre-flight Check: {js_path}")
    print(f"   Parsed {len(elements)} elements   Slide size: {SLIDE_W}\" × {SLIDE_H}\"\n")

    has_error = False

    # ── Check A: Out of bounds ──────────────────────────────────────────────────────────
    violations = check_boundary(elements)
    if violations:
        print(f"❌ Check A: Found {len(violations)} out of bounds elements (must fix before execution)")
        for el, issues in violations:
            print(f"\n   [{el['id']}] {el['label']}")
            print(f"        x={el['x']:.3f}  y={el['y']:.3f}  w={el['w']:.3f}  h={el['h']:.3f}")
            for iss in issues:
                print(f"        → {iss}")
        has_error = True
    else:
        print("✅ Check A: No out of bounds elements")

    # ── Check B: Overlap ──────────────────────────────────────────────────────────
    overlaps = check_overlap(elements)
    if overlaps:
        print(f"\n⚠️  Check B: Found {len(overlaps)} suspected overlaps (please confirm if expected overlay)")
        for a, b, area in overlaps:
            print(f"\n   [{a['id']}] {a['label']}")
            print(f"   [{b['id']}] {b['label']}")
            print(f"        Overlap area: {area:.3f} square inches")
    else:
        print("✅ Check B: No suspected overlaps")

    # ── Coordinate Summary ──────────────────────────────────────────────────────────────
    print_summary(elements)

    # ── Conclusion ──────────────────────────────────────────────────────────────────
    print("\n" + "═" * 55)
    if has_error:
        print("❌ Pre-flight Check failed — Please fix out of bounds issues and re-run before executing script")
        sys.exit(1)
    elif overlaps:
        print("⚠️  Pre-flight Check has warnings — Confirm all overlaps are reasonable before executing script")
    else:
        print("✅ Pre-flight Check passed — Script can be executed")


if __name__ == "__main__":
    main()
