---
title: "Library of Babel — Technical Specification"
created: 2026-03-27
modified: 2026-03-27
tags: [babel, borges, math, spec]
status: active
---

# Library of Babel — Technical Specification

## Origin

Jorge Luis Borges, "The Library of Babel" (1941). A library containing every possible book —
every combination of a 25-character alphabet across 1,312,000 characters per volume.
The math is real. The library is infinite but not arbitrary — it is total.

## Character Space

Borges specified 25 symbols: 22 letters, period, comma, and space.
This implementation uses 29 characters for the full modern Latin alphabet plus punctuation:

```
ALPHABET = "abcdefghijklmnopqrstuvwxyz ,."
BASE     = 29
```

## Page Size

```
PAGE_SIZE = 3,200 characters
```

## Library Structure

Each hexagon contains:
- 4 Walls
- 5 Shelves per Wall
- 32 Volumes per Shelf

This gives 640 volumes per hexagon.

```
Global_Index → Volume  = GI % 32
Global_Index → Shelf   = (GI // 32) % 5
Global_Index → Wall    = (GI // 160) % 4
Global_Index → Hex_ID  = GI // 640
```

## Total Permutation Space

```
25^1,312,000  (Borges' original)
29^3,200      (this implementation — one page's permutation space)
```

Both are astronomically large. Python handles arbitrary-precision integers natively.

## Forward Direction: Text → Coordinates

1. Normalize text to lowercase
2. Filter to characters in ALPHABET
3. Interpret the resulting character sequence as a base-29 number → Global Index
4. Decompose Global Index into (Hexagon, Wall, Shelf, Volume)

Same text always produces the same address. The Library does not generate — it reveals.

## Reverse Direction: Coordinates → Page Text

1. Reconstruct Global Index from coordinates: `GI = Hex * 640 + (Wall-1) * 160 + (Shelf-1) * 32 + (Volume-1)`
2. Apply SHA-256 counter-mode hash expansion to produce PAGE_SIZE pseudo-random bytes
3. Map each byte to ALPHABET via `byte % BASE`

## SHA-256 Hash Expansion

Page generation uses SHA-256 in counter mode. No LCG, no BigInt arithmetic.

```
gi_bytes = global_index.to_bytes(...)
output   = SHA256(gi_bytes || chunk_0) + SHA256(gi_bytes || chunk_1) + ...
page     = [ALPHABET[b % BASE] for b in output[:PAGE_SIZE]]
```

Properties:
- **Deterministic** — same GI always produces the same page
- **Chaotic** — adjacent GI values produce completely different pages
- **Fast** — sub-millisecond, no 4,700-digit modular arithmetic
- **One-directional** — coordinates → page (no need to invert)

## Performance

Sub-millisecond per page on any modern hardware. No BigInt operations required.

## Math Notes

### Coordinate Recovery

Forward: text → index → coords
Reverse: coords → index → page

The page at any coordinate is NOT the input text itself — it's a deterministic but
apparently random page. The input text's *coordinate* is what matches. The Library
contains text everywhere; we're finding which hexagon your text's index falls in.

To recover the exact text at exact coordinates, you would need coordinates that were
originally derived from that text. The Library doesn't summarize — it contains.

## Files

```
library-of-babel/
  SKILL.md        — OpenClaw skill descriptor + usage guide
  babel_core.py   — Core math engine (locate, read_page, entropy_score)
  demo.py         — Three runnable demonstrations
  references/
    spec.md       — This file
```
