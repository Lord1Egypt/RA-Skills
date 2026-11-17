---
name: laundry-decoder
description: "Decode laundry care symbols from text descriptions (tub, triangle, iron, circle, square shapes with dots/bars), build a safe wash plan for a mixed load (color bleeding risk, temperature ceilings, fabric conflicts), and give evidence-based stain removal protocols by stain type. Use when the user asks what a care label means, whether clothes can be washed together, what temperature is safe, or how to remove a specific stain without ruining the fabric."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [laundry, care-symbols, washing, stains, household, clothing, textiles]
---

# Laundry Decoder 🧺

Care labels are a pictographic language most people can't read — surveys
consistently show **the majority of consumers misinterpret care symbols**,
which is why shrinking sweaters and pink-white laundry are universal
experiences. This skill translates symbols to plain instructions, tells you
whether today's pile can be **one load or must be several**, and gives
stain-specific first aid ordered by least-destructive-first.

## Overview

Three jobs, one tool (`scripts/laundry_decoder.py`):

1. **Symbol decode** — describe a symbol in words (`tub 40`, `triangle
   crossed`, `iron 2 dots`, `circle p`, `square circle 1 dot`) and get the
   meaning, the risk if ignored, and the safe-action phrasing. Covers the
   ISO 37500 / GINETEX families: washtub (wash), triangle (bleach), square
   with circle (dry), iron (iron), circle (professional care).
2. **Load planner** — enter garments with color class, max temperature,
   fabric, and delicates flag; the planner partitions them into the fewest
   safe loads using real rules:
   - temperature = min of the load's ceilings
   - new/dark cottons bleed onto lights (hot water worsens it)
   - delicates never mix with heavy cottons/towels (abrasion)
   - wool/silk never mix with cotton terry (felting + snagging)
   - items flagged "hot wash only" (bad towels, workout synthetics) can't go
     cold
3. **Stain first aid** — 20+ common stains, each with a protocol ordered
   from least to most aggressive for the stated fabric, plus the one thing
   you must NOT do (heat-set proteins! bleach on wool!).

Everything is stdlib-only and offline — the data lives in the script.

## When to Use

- "What does this symbol on my shirt mean?" (user describes it in words)
- "Can I wash these together?" — jeans + new red tee + white towels
- "What temperature should this load be?"
- "How do I get [red wine/blood/coffee] out of [cotton/wool/silk]?"
- "I washed a red shirt with whites — now what?" → reversal advice for
   dye-transfer accidents (in references)

**Don't use for:** dry-cleaning chemical handling (that's professional
territory), leather/suede care (different domain entirely).

## How It Works — Steps

1. **Decode a label** — user reads the symbols aloud:
   ```bash
   python3 scripts/laundry_decoder.py decode "tub 30" "triangle crossed" "iron 1 dot" "circle p"
   ```
2. **Plan loads** — one garment per `--item` (format: `name;color;temp;fabric[;flags]`,
   color ∈ white/light/dark/red/new, temp = max °C, flags: delicate, hot-only):
   ```bash
   python3 scripts/laundry_decoder.py plan \
     --item "white towels,white,90,cotton" \
     --item "red tee,new,40,cotton" \
     --item "jeans,dark,40,denim" \
     --item "silk blouse,light,30,silk,delicate"
   ```
3. **Get the partition**: which loads, what temperature, what cycle, and the
   specific rule that forced each split.
4. **Stain help**:
   ```bash
   python3 scripts/laundry_decoder.py stain "red wine" --fabric cotton
   ```
5. **Browse all symbols** (`--list`) when the user wants a reference sheet.

## Conflict Rules (the load-planner brain)

| Rule | Effect |
|---|---|
| `bleeder` (new/red) + non-bleeder | separate load — no exceptions |
| delicate + heavy fabric | separate (delicates cycle protects both) |
| wool/silk + terry/towels | separate (felting, snagging) |
| hot-only + cold-max item | separate (can't satisfy both temps) |
| load temperature | min of members' ceilings |
| mixed colors without bleeders | allowed, cold/warm |

## Worked Example

Items: white towels (90°C), new red tee (40°C), jeans (40°C), silk blouse
(delicate, 30°C) →

```
Load 1: white towels — 90°C, cotton/heavy cycle
Load 2: red tee — 40°C, first wash alone (color-set: cold + salt/vinegar soak)
Load 3: jeans — 40°C, turned inside-out
Load 4: silk blouse — 30°C, delicates cycle, mesh bag
```
4 loads, each split justified by a rule — the planner names the rule.

## Common Pitfalls

1. **Heat-setting protein stains** (blood, egg, milk). Hot water cooks the
   protein into fibers permanently. Always cold first — the stain table
   enforces this ordering.
2. **Bleach on wool/silk/lycra** — dissolves the fibers. Chlorine bleach is
   whites-cotton-only; oxygen bleach is the safer general choice.
3. **Overloading detergent** "for extra clean" — excess traps soil back into
   fabric and wreks machines (yes, the residue myth is real: it's called
   redeposition).
4. **Assuming "dry clean" means dry clean ONLY.** The circle means the
   manufacturer chose not to test home care; many silks and wools handle
   careful hand-washing — see references for the risk framework.
5. **Tumble-drying what says "dry flat"** — wool knits stretch under their
   own weight + tumble; the shape never comes back.
6. **Mixing a bleeder "just once, cold"** — new red/black cottons bleed even
   cold. Two solo washes first, then they join the family.

## Verification Checklist

- [ ] Every load's temperature ≤ min of member ceilings
- [ ] No bleeder shares a load with a non-bleeder
- [ ] No delicate shares with heavy cotton/terry
- [ ] Stain protocol starts with the least aggressive step
- [ ] Protein stains never meet hot water in step 1

## One-Shot Recipes

**"Translate this whole label":**
```bash
python3 scripts/laundry_decoder.py decode "tub 40 with bar" "square circle 1 dot" "triangle" "iron crossed" "circle p"
```

**Weekly load plan for the family pile:**
```bash
python3 scripts/laundry_decoder.py plan --item ... (one per garment) --json
```

**Emergency stain card (print & keep by the washer):**
```bash
python3 scripts/laundry_decoder.py stain --fabric cotton | a2ps
```
