# Holiday Lights Load Planner

**Stop guessing how many light strings your outlets can take.**

Every December: the breaker trips with guests on the way, an extension cord
under the welcome mat runs warm, a $9 timer quietly melts because 12 amps
were pushed through a 5-amp contact. None of this is bad luck — it's
arithmetic nobody does before hanging 40 pounds of lights.

## The Problem

- A 15 A circuit honestly supports **1,440 W** (80% rule), and one 100-bulb
  incandescent mini string eats ~45 W. A 24-string roofline is 1,080 W on
  ONE plug before the inflatables even inflate.
- Incandescent strings are fused to **3–5 end-to-end** — chain more and the
  fuse blows mid-season, or the inter-string wire carries the whole run.
- Cords have gauge-vs-length limits; #16 at 100 ft drops voltage and heats.
- Timers and photocells have contact ratings almost nobody checks.

## What This Skill Does

`scripts/lights_load.py` builds a load sheet from what's actually in your
boxes:

```bash
python3 scripts/lights_load.py --breaker 15 --existing-watts 100 \
  --strings incandescent-mini:100:12 led-mini:70:3 --inflatables 1 \
  --cord-gauge 14 --cord-length-ft 80 --outdoor --timer-amps 15
```

- Circuit budget with the 80% rule and your existing always-on load
- Per-type watt/amp totals, SAFE/TIGHT/OVERLOAD verdict with margin in watts
- Daisy-chain warnings vs typical fused-plug limits (split-run advice)
- Cord gauge vs length verdict; GFCI/wet-location rules for outdoor plans
- Timer contact-rating check
- Season energy cost + LED-payback line ("swap saves 912 W = $42/season and
  frees headroom for 20 more mini-equivalents")

## Who Needs This

- Households putting up holiday displays (roofline, bushes, inflatables)
- Party/wedding planners running market lights and projectors
- Anyone whose breaker tripped "last year" and never found out why
- People deciding whether LED strings are worth it (spoiler: the capacity
  math matters more than the energy math)

## Example

24 incandescent mini strings (100-bulb) on a 15 A circuit:
1,080 W — fits the 1,440 W budget (75%), but that's ONE appliance's worth
of headroom gone and the run must split into 5-string daisy chains (5 runs
from the wall). The same circuit with LED strings carries the identical
look at ~170 W with one run. The script prints exactly this comparison
with `--compare-led`.

## Safety Notes

The math catches overloads; eyes catch failures. After hanging: 15-minute
warm-touch check on every plug, cord, and timer. Warm = re-plan, don't
reset. Outdoor displays need GFCI protection at the source, elevated
covered plugs, and outdoor-rated cords. Never staple through a wire.

## License

MIT — see LICENSE.
