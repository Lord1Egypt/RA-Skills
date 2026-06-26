---
name: library-of-babel
description: "Bidirectional mathematical engine for Borges' Library of Babel. Finds the permanent hexagon address of any text, reads any page at any coordinate, and scores pages by Shannon entropy. No database, no randomness — same input always produces identical output. Use when asked to locate text in the Library of Babel, generate a page at given coordinates, explore Borges' infinite library concept, or analyze page entropy. Triggers on: find this in the Library of Babel, what is the address of, read a page at coordinates, entropy heatmap, Borges library."
---

# Library of Babel

A bidirectional mathematical engine for Borges' infinite library.

No database. No storage. No randomness. Same input always produces identical output — across machines, across time.

---

## What It Does

**Forward:** Paste any text → get its permanent address (Hexagon, Wall, Shelf, Volume).

**Reverse:** Give coordinates → get the 3,200-character page that has always lived there.

The Library doesn't generate text. It reveals what was always there.

---

## Usage

### Forward lookup — find where your text lives

```python
from babel_core import format_locate

print(format_locate("call me ishmael"))
```

Output:
```
📍 Hexagon 936,177,732,035,491,926 · Wall 3 · Shelf 4 · Volume 21
(Global index: 936177732...)

This text has always existed here. It is not generated — it is found.
```

### Reverse lookup — read a page at any coordinate

```python
from babel_core import format_read_page

print(format_read_page(hexagon=1, wall=1, shelf=1, volume=1))
```

Output:
```
📖 Hexagon 1 · Wall 1 · Shelf 1 · Volume 1

sw,quamqysyjnki.eog,u,gl.b.u uuejbadqcfwmbegfeljp.toqwpq... (3200 chars total)
```

### Entropy analysis — how noise-like is a page?

```python
from babel_core import index_to_page, shannon_entropy, space_frequency, classify_page

page = index_to_page(12345)
h = shannon_entropy(page)
sp = space_frequency(page)
tag = classify_page(h, sp)
print(f"H={h:.2f} bits | space={sp:.1f}% | {tag}")
```

Shannon entropy thresholds (theoretical max for 29-char alphabet: log₂(29) ≈ 4.86 bits):
- `🟢 coherent` — H < 3.8 and space > 14% (almost never random — that's the point)
- `🟡 interesting` — H 3.8–4.5 or space 6–14%
- `🔴 noise` — H > 4.5 or space < 6%

---

## The Codex

`codex.json` ships with 7 pre-mapped passages from literature and culture.
Zero tokens to browse — it's a static JSON read.
The coordinates are permanent and independently verifiable.

```python
from demo import show_codex, add_to_codex

# Display all pre-mapped passages
show_codex()

# Add your own — coordinates computed and persisted immediately
add_to_codex("the medium is the message", "Understanding Media — Marshall McLuhan")
```

Pre-mapped passages:
- "call me ishmael" — Moby Dick
- "it was a bright cold day in april..." — 1984
- "the library of babel" — Borges
- "in the beginning god created the heavens and the earth" — Genesis 1:1
- "to be or not to be that is the question" — Hamlet
- "it was the best of times it was the worst of times" — A Tale of Two Cities
- "attention is a currency" — High Noon Office

---

## Three Demo Scripts

Run all four demos at once:

```bash
python3 demo.py
```

Or call individually:

```python
from demo import locate, read_page_demo, entropy_heatmap, show_codex, add_to_codex

# Demo 1: Locate any text
locate("the library of babel")

# Demo 2: Read a page at coordinates
read_page_demo(hexagon=1, wall=1, shelf=1, volume=1)

# Demo 3: Entropy heatmap — 5 random coordinates, ranked by Shannon entropy + space frequency
entropy_heatmap(n=5)

# Demo 4: Codex — browse pre-mapped passages
show_codex()
```

---

## The Math

**Alphabet:** `abcdefghijklmnopqrstuvwxyz ,. ` — 29 characters (Borges' 25-char set extended to full Latin alphabet)

**Forward (text → index):** Interpret the filtered character sequence as a base-29 integer.

**Coordinates:**
```
Volume  = index % 32
Shelf   = (index // 32) % 5
Wall    = (index // 160) % 4
Hexagon = index // 640
```

**Page generation:** SHA-256 counter-mode hash expansion. `SHA256(gi_bytes || chunk_id)` repeated to fill 3,200 bytes, each mapped to the alphabet via `byte % 29`. Deterministic, chaotic, sub-millisecond.

Note on the LCG approach: A Linear Congruential Generator with `a=30, m=29^3200` maps small indices (e.g. `640`) to tiny values like `19201`, which decode as 3,197 leading 'a' characters when expanded to 3,200 base-29 digits. Hash expansion solves the distribution problem correctly.

---

## Files

```
library-of-babel/
  SKILL.md          — This file
  babel_core.py     — Core math engine
  demo.py           — Four runnable demonstrations + codex functions
  codex.json        — Pre-mapped passages (add your own with add_to_codex())
  references/
    spec.md         — Full technical specification
```

---

## Setup

Pure Python 3 standard library — no external dependencies required.

```bash
cd library-of-babel
python3 demo.py
```
