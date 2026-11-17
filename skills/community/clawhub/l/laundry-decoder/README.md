# Laundry Decoder 🧺

**What does that symbol mean? Can these be washed together? How do I save
this shirt from the wine?**

Care labels use a pictographic language most people can't read — consumer
surveys repeatedly show the majority misinterpret the symbols, and "my
whites came out pink" / "the sweater is now a crop top" are preventable
disasters. This tool reads symbols (from text descriptions), plans safe
wash loads with real textile rules, and gives stain-specific first aid
ordered least-destructive-first.

## What it does

- **`decode`** — 30+ care symbols (ISO 37500/GINETEX families) described in
  words → meaning + how-to + what happens if you ignore it
- **`plan`** — partition a pile of garments into the fewest *safe* loads:
  color-bleed separation, whites-vs-darks, delicates vs heavy, wool/terry
  conflicts, temperature ceilings (load temp = min of members)
- **`stain`** — 21 protocols (wine, blood, ink, wax, pet urine, dye
  transfer…) each ordered least→most aggressive, with a hard 🚫 NEVER rule
  per stain and protein-fiber warnings
- **`list`** — full printable symbol reference

## Quick start

```bash
# What does the label say?
python3 scripts/laundry_decoder.py decode "tub 40 with bar" "square circle 1 dot" "iron crossed"

# Can I wash these together?
python3 scripts/laundry_decoder.py plan \
  --item "white towels;white;90;cotton" \
  --item "red tee;new;40;cotton" \
  --item "jeans;dark;40;denim" \
  --item "silk blouse;light;30;silk;delicate"
# → 4 loads, each with temperature, cycle, and the rule that forced the split

# Emergency: red wine on cotton
python3 scripts/laundry_decoder.py stain "red wine" --fabric cotton
```

Item format: `name;color;maxTempC;fabric[;flags]` — color ∈
white/light/dark/red/new · flags: `delicate`, `hot-only`.

## Why it matters

Laundry mistakes cost real money — one shrunken wool sweater or a dyed-pink
load of whites easily exceeds $100. The knowledge exists (textile science
is settled); the problem is it lives in care-label PDFs nobody reads. This
puts the rules where the decision happens.

## Files

- `SKILL.md` — agent-facing usage guide
- `scripts/laundry_decoder.py` — decoder + planner + stain aid (stdlib only)
- `scripts/test_laundry_decoder.py` — self-tests
- `references/care-and-stains.md` — textile science behind every rule

## Test

```bash
python3 scripts/test_laundry_decoder.py
```

MIT © 2026 Denis Voronin
