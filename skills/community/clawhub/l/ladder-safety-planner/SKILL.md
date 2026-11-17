---
name: ladder-safety-planner
description: Use when setting up any ladder for home DIY — gutter cleaning, roof access, painting, light bulbs — and unsure what size or type you need. Computes correct stepladder/extension size from working height, 4:1 lean-angle geometry, duty rating (Type III–IAA) with gear allowance, roof-access overlap math, power-line clearances, and a pre-climb checklist. Fights the ~500k/yr US ER-treated ladder injuries with engineering rules, not vibes.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [ladder-safety, diy, home-improvement, fall-prevention, roof-work, gutters, painter-safety]
---

# Ladder Safety Planner

## Overview

Ladders are the most dangerous tool most people own: roughly **500,000
ER-treated injuries and ~300 deaths per year in the US alone**, almost all
from falls under 12 feet. The failure is almost never the ladder — it is the
*setup*: a stepladder two sizes too short (standing on the top cap), an
extension ladder leaned at 30° instead of 75°, a Type III household ladder
loaded with a 220 lb roofer plus a bundle of shingles, or aluminum set up
under the service drop.

This skill replaces guessing with arithmetic:

1. **Size selection** — from the height you need to *touch*, pick the right
   stepladder size (stand no higher than 2 steps from the top; max reach ≈
   size + 4 ft) or extension ladder length (3 ft above the roof line, minus
   section overlap).
2. **4:1 angle geometry** — base distance = working height ÷ 4, plus a
   no-tape-measure phone check.
3. **Duty rating** — Type III (200 lb) → IAA (350 lb), computed from body +
   clothes + tools + materials actually carried.
4. **Roof access** — extension above roof edge, walk-up sequence, and the
   re-securing move people get wrong.
5. **Power lines & material** — clearance ladders by voltage; fiberglass
   near electricity, never metal.
6. **Pre-climb checklist** — the 60-second ritual.

## When to Use

- Buying or borrowing a ladder for a specific job ("what size do I need to
  clean my gutters on a 2-story house?")
- Setting up an extension ladder against a wall or roof edge
- Deciding whether your old household stepladder is rated for you + gear
- Any work near overhead service drops or overhead lines
- Choosing between stepladder / extension ladder / ladder+platform for a task

**Don't use for:** scaffolding design, rope access, boom lifts or anything
professional rigging — hire it out. Not a substitute for OSHA-compliant
training on job sites.

## Quick Start

```bash
python3 scripts/ladder.py setup --reach 16 --type extension --purpose roof
python3 scripts/ladder.py setup --reach 9  --type step
python3 scripts/ladder.py angle --height 14
python3 scripts/ladder.py duty --weight 205 --gear 25
python3 scripts/ladder.py powerline --kv 0.4
python3 scripts/ladder.py checklist
```

Stdlib-only, no network.

## Core Rules (what the math encodes)

| Rule | Value | Why |
|---|---|---|
| Stepladder max standing | top 2 steps OFF-limits | Standing there removes handholds and inverts the tripod |
| Stepladder max reach | ≈ ladder size + 4 ft | Assumes ~5'9" person with 12" vertical reach |
| Extension lean angle | 4:1 (75°) | base out = climb height ÷ 4; shallower = slide-out, steeper = tip-back |
| Extension above roof edge | ≥ 3 ft | A handhold rail when you step off/on the roof |
| Usable vs nominal length | 16→13, 20→17, 24→21, 28→25, 32→29, 36→33, 40→37 ft | Sections overlap in the middle — the fly section doesn't add net length |
| Duty ratings | III 200 / II 225 / I 250 / IA 300 / IAA 350 lb | Rated load = you + clothes + tool belt + materials, all at once |
| Power lines | ≥10 ft to 50 kV, more above | Aluminum and wet wood both conduct |
| 3 points of contact | always | One hand or two feet — never carry loads up |

## Workflow

1. **Define the reach** — the highest point you must comfortably *touch*
   with your hands (for gutters: gutter height; for roof work: roof edge).
2. `setup --reach H --type step|extension [--purpose roof]` → recommended
   size, standing platform, and the setup geometry if extension.
3. **Check the load path**: `duty --weight W --gear G` → minimum duty type.
   Budget honestly: a drill + shingle bundle + bucket is 20–50 lb.
4. `angle --height H` for extension ladders → print the base distance and
   verify with the standing-toes / straight-arm check (below).
5. **Scan overhead**: `powerline --kv V` (residential service drop is
   usually 0.12–0.48 kV, but treat unknown as high). 10 ft minimum — that
   includes the ladder while it's being carried upright.
6. `checklist` — run the 60-second pre-climb ritual. For roof work, tie off
   or have a helper foot the ladder for the step-across.
7. For anything involving steep pitch, wet roof, or >24 ft reach: **stop —
   rent a lift or hire a pro**. This skill is for setup arithmetic, not
   risk appetite.

### No-tape-measure angle check
Stand with your toes against the ladder rails, reach straight out parallel
to the ground: your palm should just touch the rungs. Too far / can't touch
= wrong angle; adjust the base.

### Roof access sequence
1. Set ladder with 3 ft above the roof edge, base at height÷4.
2. Climb to just below roof level; check footing and roof condition.
3. Keep 3 points of contact; shift weight slowly to the roof, then grab the
   rail ABOVE the roof edge before fully stepping off.
4. Coming back: grab the rail above the edge BEFORE stepping back on —
   the ladder below you is now unsupported against your momentum.

## Common Pitfalls

1. **Buying by "house height" instead of reach.** A 24 ft wall needs an
   extension ladder rated ~27+ ft usable (24 + 3 above roof edge if you step
   off) — not a "24-footer" whose usable length is only 21 ft.
2. **Ignoring section overlap.** A nominal 16 ft extension ladder extends
   to about 13 ft of safe length. The table in `setup` encodes this.
3. **Standing on the top cap / top step of a stepladder** because "I just
   need 6 more inches." That 6 inches is where half the injuries live —
   take the bigger ladder.
4. **Lean angle by eye.** Most people set ~60–65°, which slides out under
   dynamic load. Measure height÷4 or use the toes/straight-arm check.
5. **Duty rating = "my weight."** It's your weight plus everything on you.
   200 lb person + 30 lb of paint + tools on a Type III is over.
6. **Aluminum under the service drop.** Fiberglass rails are the only
   non-conductive option near electrical; wet/fiberglass-dirty still needs
   distance. `powerline` gives the clearance table.
7. **Leaning a stepladder closed against a wall.** Stepladders are built to
   be self-supporting and spread; leaning one closed is an uncontrolled
   slide. Use the right tool.
8. **Ladder feet on dirt/mulch/snow.** Level, firm footing with both feet
   flat and levelers if needed; soft soil swallows one foot and rotates the
   whole setup.

## Verification Checklist

- [ ] Reach defined as "highest point I touch", not wall height
- [ ] Recommended size accounts for standing-level limits (stepladder) or
      3-ft extension + overlap (extension)
- [ ] Duty rating ≥ body + clothes + gear + materials
- [ ] Base at height÷4 (extension), verified with toes/straight-arm check
- [ ] Overhead lines checked with 10 ft+ clearance, fiberglass near power
- [ ] Feet level and on firm surface; 3 points of contact planned
- [ ] Helper informed or ladder secured/tied for roof step-off

## Safety Disclaimer

Fall height is not a proxy for injury severity — most fatal ladder falls
are under 10 feet. When the math says the setup is marginal, the correct
tool is a rental lift or a professional, not confidence. Local codes and
OSHA rules govern workplaces; this skill is for homeowner planning.
