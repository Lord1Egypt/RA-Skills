# Outage Food Safety Triage

**The power just came back after 9 hours. Is the fridge food safe?**

Every extended outage ends the same way: a family standing at an open
fridge, guessing. Toss everything and you burn $300 of groceries; keep the
wrong things and you risk the food-poisoning cluster hospitals see after
every hurricane. The official FDA/USDA rules are simple — 4-hour fridge
window, 24/48-hour freezer, 40°F danger zone — but almost nobody knows the
*category* calls where the money and the safety actually live.

This skill is that triage, as an instrument:

- **Verdicts from duration + thermometer** — 4h fridge / 24h half-freezer
  / 48h full-freezer windows, with a measured-temperature override
- **Item engine** — keep/toss for the calls people get wrong: open
  mayonnaise survives (commercial mayo is acidic; the folk rule is
  backwards), deli meat does not; hard cheese yes, shredded no; cut melon
  is a named listeria vector
- **Refreeze logic** — crystals + ≤40°F = safe; thawed-warm = toss
  because toxins survive both cooking and refreezing
- **Door sign generator** — tape it inside the fridge so the *next*
  outage is a 2-minute decision instead of a guess

## Quick start

```bash
python3 scripts/triage.py verdict --hours 9
python3 scripts/triage.py verdict --hours 5 --fridge-temp 38
python3 scripts/triage.py item --name "deli turkey, opened"
python3 scripts/triage.py refreeze --state "soft and cool, no crystals"
python3 scripts/triage.py doorsign --out door-sign.md
```

Stdlib-only Python 3, offline, no dependencies.

## Example

9-hour outage, no thermometer:

```
FRIDGE (door kept closed):
  h=9.0 > 8h: FULL PERISHABLE CULL — all meat, dairy, leftovers,
    cut produce, prepared infant food OUT. Keep: condiments,
    butter, hard cheese, whole produce, bread/pantry goods.

FREEZER (door kept closed):
  h=9.0 <= 24h: 24h (half-full) / 48h (full) window — items safe
    IF still hard/crystals; verify with crystal check
```

The same 9 hours *with* a thermometer reading 38°F flips the verdict to
PASS — which is why the reference tells you to keep a $5 appliance
thermometer in the fridge and freeze jugs to fill the freezer.

Full rules, toxin biology, and preparedness notes in
`references/outage-food-rules.md`.

*Household guidance only. Never taste-test; when in doubt, throw it out.*
