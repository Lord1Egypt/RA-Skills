# Hangover Recovery Planner

**The problem:** the hangover is six stacked mechanisms — dehydration, acetaldehyde, delayed methanol metabolism, gastritis, REM-destroyed sleep, and a cytokine-driven inflammatory response — and folk remedies routinely backfire: hair-of-the-dog re-pauses methanol clearance (that's *why* it "works" and why it prolongs everything), acetaminophen competes with ethanol for CYP2E1 and generates hepatotoxic NAPQI, and chugging water on suppressed ADH just makes urine. Meanwhile people want three things: can I drive, what do I do right now, and was it the whiskey?

**What this does:** stdlib-only Python from session facts (drinks by type, weight, sex, start time, water during):

- **Widmark BAC tracking** — peak and current estimate, hours-to-zero at 0.015%/h elimination
- **Fluid/sodium deficit** — 10 mL per gram ethanol net loss, 1.5× deficit over 4–6 h with sodium
- **Congener scoring** — dark-spirit detection (brandy 4, vodka 0): same gram, worse morning
- **Staged protocol** — NOW/+30-60m/+1-2h/+2-4h/sleep/avoid, food order (fructose carbs → eggs/banana/broth), 20-min nap cap, light-activity-not-exercise
- **Symptom router** — each complaint mapped to its mechanism and what actually helps it
- **Medication gates** — acetaminophen never; ibuprofen only with food after fluids
- **ER red flags** — vomiting >6 h, confusion, coffee-grounds vomit, breathing pauses
- **Mid-session mode** — `drink` verdict: STOP at ≥0.06%, LAST ONE at ≥0.04%
- **Next-time card** — personalized pacing math from this episode

```bash
python3 scripts/recovery_planner.py plan --drinks "craft-beer:4,whiskey:3" \
  --weight 80 --sex male --start 2026-10-20T21:00 --water-during 2
# est. BAC now: 0.059% — DO NOT DRIVE; rehydrate 1.1 L over 4-6 h ...
```

## Who needs this

Most adults who drink have had a hangover; workplace and exam
productivity losses are measured in the tens of billions annually. The
tool is harm-reduction: correct rehydration science, correct
medication warnings, honest evidence grades (references table: what
WORKS / HELPS / BACKFIRES), and a screening-question nudge when the
tool starts being used weekly.

Not medical advice; the red-flag list routes to emergency services
where appropriate.

## License

MIT
