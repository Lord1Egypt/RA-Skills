# Glasses Prescription Decoder

**The problem.** Your eye exam ends, you're handed a slip of paper covered in `OD -2.75 -1.25 x175 / ADD +2.25`, and the optical shop immediately tries to convert your ignorance into a $400 sale. Meanwhile buying the same lenses online costs $30 — if you can read the code, avoid the sign-convention traps, and know your PD. Most people can't, and the paper goes in a drawer.

**What this does.** Decodes every field of an eyeglass prescription into plain vision language ("right eye: low-moderate nearsightedness, moderate astigmatism at a near-horizontal axis, mature presbyopia ADD — full readers would be −0.50"). Then goes further:

- **Change analysis**: compares old vs new prescriptions per field, with felt-vs-noise verdicts (Δ ≥ 0.50 D = you'll feel it; 0.25 = measurement noise) and OD/OS-swap detection
- **Plus↔minus cylinder transposition** — the #1 silent killer when switching between an optometrist (minus cyl) and an ophthalmologist (plus cyl): entering plus-cylinder numbers into an online form inverts your astigmatism correction entirely
- **Lens-type verdict**: single vision vs progressive vs two-pairs from the ADD value, with the honest note that two online pairs often beat one progressive
- **Computer-glasses derivation**: intermediate ADD fraction from your actual monitor distance (65 cm → ~38% of ADD), ordered as cheap single-vision
- **PD self-measurement**: mirror/photo/old-glasses protocols — US shops withhold PD (it's a "fitting measurement," not part of the legal Rx) to force in-store fills
- **Material tiers**: when 1.67/1.74 index actually matters (combined power > 4 D), when it's an upsell

**Example.** New exam says `-2.75 -1.25 x175` where last year said `-2.50 -1.00 x180`: the diff command shows −0.25 borderline changes (noise-level, don't pay for new lenses yet) — while the swap-detector would catch a data-entry error that flips the eyes' difference sign. First-time progressive wearer gets adaptation expectations (3–14 days of peripheral swim, return at 2 weeks).

## Quick start

```bash
python3 scripts/rx_decode.py decode --od "-2.75 -1.25 x175" --os "-3.00" --add 2.25 --pd 62
python3 scripts/rx_decode.py diff --old "-2.50 -1.00 x180 | -2.75" --new "-2.75 -1.25 x175 | -3.00"
python3 scripts/rx_decode.py computer --rx "-2.75 -1.25 x175 | -3.00" --add 2.25 --distance-cm 65
python3 scripts/rx_decode.py pd --method mirror
```

## Files

- `SKILL.md` — field-by-field decoder guide, pitfalls, verification checklist
- `references/rx-science.md` — severity bands, transposition math, PD tolerances, FTC Eyeglass Rule, material tiers, adaptation timelines
- `scripts/rx_decode.py` — decoder/differ/PD assistant (stdlib only)

## Not for

Contact lens prescriptions (different powers at the eye, plus base curve/diameter — needs a fitter), or medical eye symptoms (flashes, floaters, sudden changes → eye doctor now).

## License

MIT © 2026 Denis Voronin
