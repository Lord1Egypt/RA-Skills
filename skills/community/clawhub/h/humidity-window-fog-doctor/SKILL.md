---
name: humidity-window-fog-doctor
description: "Use when windows fog/weep/frost on the inside in winter: computes the inner-pane surface temperature for your glazing (U-value + film coefficients), finds the condensation RH threshold for each window class, diagnoses cause (too humid / too cold glass / thermal bridging / lifestyle moisture sources), and gives the target indoor RH + ventilation fix with mold-risk timing."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [condensation, window-fog, humidity, mold-prevention, indoor-air, glazing, winter, dew-point]
---

# Humidity & Window Fog Doctor

## Overview
Winter window condensation is a **dew-point collision on a cold surface**:
warm moist indoor air meets an inner pane chilled below that air's dew
point. Whether a window fogs is fully computable from indoor temp, indoor
RH, outdoor temp, and the glazing's thermal resistance — which means the fix
is computable too (either raise glass temperature or lower RH; which one is
cheaper depends on the numbers).

This skill:

- Computes **inner-pane surface temperature** for single / double / triple
  glazing (U-value + indoor/outdoor film coefficients, with night-radiation
  and curtain-cavity effects)
- Finds the **condensation threshold RH** — the indoor humidity above which
  THAT window starts collecting water at tonight's outdoor temp
- Converts complaint → cause: "weeping at 60% RH but only on the north
  windows" = glazing class difference, "fog every morning only in the
  bedroom" = overnight moisture load (2 sleeping people ≈ 40–80 g/h water)
- Sizing the moisture sources: shower, cooking, plants, drying laundry,
  aquariums, unflued gas heaters (≈ 1.6 kg water per kg of gas!)
- Mold-risk framing: liquid water on organic frames/drywall paper above
  0 °C for hours = mold in 24–48 h at the corner; below 0 °C = frost, less
  biological risk but worse on thaw
- The **fix ladder**: target RH for your coldest window → ventilation
  strategy (intermittent vs trickle vs HRV) → warm-edge spacers /
  low-e storm panes as the glass-side fix

## When to Use
- "My windows are wet every morning / have black spots on the frames"
- Setting a humidifier in winter: what RH can this house actually carry
  without weeping windows? (Higher than people fear with good glass;
  lower with single pane.)
- Bedroom/bathroom/kitchen condensation pattern diagnosis
- Renters documenting a landlord conversation: glazing class vs indoor RH,
  who owns the fix
- **Don't use for:** summer condensation on AC supply grilles (different
  mechanism), whole-building HVAC design, or already-established large mold
  (>1 m² — remediation, see references).

## Steps
1. Measure/know: indoor temp, indoor RH (any hygrometer), outdoor min temp,
   glazing class (single/double/double-low-e/triple), window location notes
   (curtains closed at night? north wall? bay window?).
   ```bash
   python3 scripts/windowfog.py --tin 21 --rh 55 --tout -8 --glazing double
   python3 scripts/windowfog.py --tin 21 --rh 55 --tout -8 --glazing double --curtains
   ```
2. Read the verdict: glass surface temp vs dew point, margin in °C/RH
   points, whether curtains made it worse (closed curtains chill the pane —
   the classic self-inflicted fog).
3. Fix ladder: target RH for tonight's temps (e.g. "hold ≤45% and the
   double glazing stays dry; ventilate bedroom 10 min at 7:00 and 22:00").
4. If target RH < 35% (comfort floor), the glass is the problem — the
   ladder says so and switches to glazing-side fixes.

## The Model (summary — full in references/condensation-physics.md)
- Pane surface temp: `T_s ≈ T_in − (T_in − T_out) · R_film_in / R_total`
  with R_total from U-value, R_film_in ≈ 0.13 m²K/W (still air; less with
  curtains trapping a cold pocket → colder pane).
- Dew point from Magnus formula; condensation iff `T_s ≤ T_dp`.
- Threshold RH: invert Magnus at T_s → the RH where dew point reaches the
  pane. Each glazing class has a characteristic threshold curve vs outdoor
  temp (single ≈ 30–35% at −10 °C; double ≈ 45–52%; triple ≈ 60%+).
- Moisture balance: sources (g/h) vs ventilation removal
  (air changes × humidity capacity difference).

## Output
Verdict + threshold table across outdoor temps (0/−5/−10/−15/−20) for your
glazing, moisture-source audit checklist, fix ladder ordered by cost.
`--json` for machine use.

## Common Pitfalls
1. **Treating all windows the same.** Single-pane kitchen vs triple bedroom
   differ by 25+ RH points of threshold; fix each or accept gradient.
2. **Closing curtains "to keep warm"** — the cavity between curtain and
   glass goes colder than the room, the pane drops several degrees, and fog
   appears exactly behind the curtains where you can't see it. Leave a 2–3
   cm gap at top/bottom for convective washing, or accept the fog.
3. **Wiping instead of ventilating.** Removing liquid does nothing to the
   vapor supply; the water returns nightly. Ventilation first (dry incoming
   winter air holds a huge absorption margin).
4. **Humidifier chasing "healthy 50%" folklore.** With single glazing at
   −15 °C outside, 50% RH turns windows into nightly rivers and frames into
      mold farms. The correct target is the threshold of your *coldest*
      window minus a 5-point safety margin.
5. **Ignoring hidden sources**: unflued gas heaters and indoor drying racks
   each add kilograms per day — the audit table converts to RH points.
6. **Frost ≠ safe.** Sub-zero panes deposit frost (no liquid for mold) but
   thaw into running water every morning; treat as condensation.

## Verification Checklist
- [ ] Glass surface temp computed from the actual glazing class (not assumed double)
- [ ] Dew point and threshold RH both shown with margin (RH points and °C)
- [ ] Curtain/cavity effect flagged if user has night curtains
- [ ] Fix ladder starts with the free options (ventilation timing, source removal)
- [ ] If threshold < 35% RH → glazing-side fix recommended, not "dry the house more"
