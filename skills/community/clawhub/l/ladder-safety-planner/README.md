# Ladder Safety Planner

**What size ladder do I need — and how do I set it up so it doesn't kill me?**

~500,000 Americans visit the ER each year after ladder falls; ~300 die, most
from falls under 12 feet during routine homeowner jobs. The ladder is rarely
defective — the *setup* is: two sizes too short, leaned at the wrong angle,
overloaded past its duty rating, or parked under the service drop.

This skill does the arithmetic for you:

- **Size** — from the highest point you need to *touch*, pick the correct
  stepladder size (with the top-two-steps rule) or extension ladder length
  (with section-overlap losses and the 3-ft roof-edge rule).
- **Angle** — the 4:1 rule computed for your wall, plus a no-tape-measure
  field check (toes + straight arm).
- **Duty rating** — Type III…IAA minimum from body + clothes + tools +
  materials you'll actually carry.
- **Power lines** — clearance table by voltage; when fiberglass is mandatory.
- **Checklist** — the 60-second pre-climb ritual, with abort triggers.

## Quick start

```bash
python3 scripts/ladder.py setup --reach 16 --type extension --purpose roof
python3 scripts/ladder.py setup --reach 9 --type step
python3 scripts/ladder.py angle --height 14
python3 scripts/ladder.py duty --weight 205 --gear 25
python3 scripts/ladder.py powerline --kv 0.4
python3 scripts/ladder.py checklist
```

Stdlib-only Python 3, no dependencies, works offline.

## Example

Gutter cleaning on a two-story house, roof edge at 16 ft, you weigh 205 lb
with a 25 lb bucket:

```
EXTENSION LADDER plan:
  Ladder must span 19.0 ft (roof edge + 3 ft rail above)
  → 24-ft extension ladder (usable 21 ft ≥ 19.0 ft)
  - Base set 4.8 ft out from the wall (4:1 rule, 76°)
  - Helper foots the base or tie top to an anchor

Load: 205 lb body + 25 lb gear = 230 lb
  → MINIMUM: Type I (250 lb)
```

The two classic mistakes this prevents: buying a "24-footer" for a 24-ft
wall (usable length is only 21 ft), and standing on a stepladder's top step
because "six more inches" — exactly where the injuries cluster.

See `references/ladder-engineering.md` for the full tables and reasoning.

*Planning aid for homeowner work — not OSHA training. When the math says
marginal, rent a lift or hire a pro.*
