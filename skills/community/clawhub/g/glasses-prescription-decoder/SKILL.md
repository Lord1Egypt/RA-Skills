---
name: glasses-prescription-decoder
description: "Use when you get an eye exam and need to understand the paper prescription, compare it to your old one, or buy glasses online: decodes OD/OS/SPH/CYL/AXIS/ADD/PRISM into plain vision language, computes your exact lens type (single/progressive/bifocal), analyzes what CHANGED between two prescriptions, verifies online-order entry, and explains PD (pupillary distance) rules. Solves the 'this paper is a code and the optical shop wants $400' problem."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [eyewear, prescription, vision, glasses, health, shopping, pd]
---

# Glasses Prescription Decoder

## Overview

An eyeglass prescription is a dense, error-prone shorthand — `OD -2.75 -1.25 x 175 / OS -3.00 SPH / ADD +2.25 / PD 62` — that opticians read fluently and everyone else pretends to understand. The consequences of not understanding it are real: entering `-1.25` where `-1.75` belongs when ordering online produces lenses that strain your eyes for months; ignoring the difference between `SPH` and `CYL` signs (plus vs minus cylinder convention) can invert your astigmatism correction entirely; not knowing your PD forces you into a $400 in-store markup because "we can't fill a prescription without it."

This skill decodes every field of the prescription into plain language ("right eye, moderately nearsighted with meaningful astigmatism at nearly-horizontal angle"), tells you what changed versus your last prescription and whether adaptation difficulty is expected, checks the numbers for entry errors, and states exactly which lens type your prescription implies (single vision vs progressive vs reading glasses) — the determination that drives 80% of the price.

The right to your prescription is federal law in the US (FTC Eyeglass Rule: the exam must be released to you immediately, whether you ask or not, at no charge) — and PD requirements vary. This is the knowledge asymmetry killer for the ~$40B optical retail industry.

## When to Use

- Just got an exam: decode the paper before it goes in a drawer and gets lost
- Ordering glasses online (Zenni, EyeBuyDirect, Liingo...) — verify your typed-in values match
- Comparing old vs new prescriptions: "is this really a change, or within measurement noise?"
- Deciding lens type: single vision vs progressive vs computer glasses from the ADD value
- Kid's first prescription: what does it mean, is it serious, how fast will it change
- Contact lens prescription (different powers — conversion awareness)

**Don't use for:** contact lens fitting (a CL prescription has a base curve/diameter and different effective power at the eye — needs a fitter), or medical eye concerns (sudden vision changes, flashes/floaters → eye doctor now).

## The Fields, Decoded

1. **OD / OS / OU** — right eye (oculus dexter) / left eye (oculus sinister) / both. On your prescription, OD is by convention written first/left on the page. **Transposition trap:** some countries and some Rx swap this — check the legend.
2. **SPH (sphere)** — the main correction, in diopters (D).
   - **Minus (−):** myopia (nearsighted) — clear near, blurry far. −0.25 to −3.00 mild/moderate; −3.00 to −6.00 moderate/high; −6.00+ high myopia.
   - **Plus (+):** hyperopia (farsighted) — the eye must focus to compensate; in young people often无症状 until accommodation fatigue. + values above +3.00 in children deserve prompt follow-up.
   - 0.25-D steps are the standard; smaller increments exist but rarely matter.
3. **CYL (cylinder) + AXIS** — astigmatism (cornea/lens shaped more like a rugby ball than a sphere). CYL is the amount (0.25–3.00+), AXIS the orientation (0–180°, pure numbers, no sign). AXIS without CYL is meaningless; CYL 0 or blank = no astigmatism.
   - **Plus-cylinder vs minus-cylinder:** same eye, two notations. Optometrists (ODs) usually write minus cylinder; ophthalmologists (MDs) often plus cylinder. Transposition formula: `new_SPH = SPH + CYL; new_CYL = -CYL; new_AXIS = 90 ± AXIS`. Ordering with the wrong convention inverts your correction — the #1 online-order disaster.
4. **ADD** — the reading/bifocal addition, always **plus**, always the same number for both eyes (a mismatch is an entry error worth querying). ADD +1.00 to +1.50 typical emerging presbyopia (age ~40+); +2.00 to +2.75 mature. ADD on the paper = the whole bottom segment of a progressive/bifocal, or the full power of reading glasses.
5. **PRISM + BASE** (rare) — correction for eye alignment (double vision, strain). Must be entered separately on orders; get the optician to verify online-entry of prism — many labs handle it badly.
6. **PD (pupillary distance)** — the distance between pupil centers, 54–74 mm adults (near PD is 3–4 mm less; measure for reading glasses separately). In the US, PD is often *not* on the prescription (it's treated as a fitting measurement, not part of the Rx). You can measure it yourself with a mirror + ruler, or from an existing pair of glasses (see script).

## Lens-Type Decision from the Numbers

- **No ADD, SPH/CYL only → single vision** (distance if minus, near if reading-only prescription). Cheapest: online from ~$15.
- **ADD present + SPH = distance Rx → progressive (PAL)**, bifocal, or **two pairs** (distance + readers). Two pairs from an online discounter often total less than one progressive and give better wide-field vision at each distance — the trade is swapping glasses.
- **Computer/office glasses:** SPH adjusted for ~60–70 cm working distance + full ADD, or a "office progressive" with intermediate/near zones. Massive comfort win for desk work if you're presbyopic and staring at screens.
- **High-index material guide (by strongest meridian, |SPH|+|CYL| combined power):** ≤ ±4.00 standard plastic/CR-39 or polycarbonate; 4–6 → 1.67; 6+ → 1.74. Above ±6, ask about lens diameter/frame size — edge thickness is geometry.
- **Kids/teens:** ask about myopia-control options (special lenses, ortho-K, atropine) — standard single-vision correction is no longer the only path for progressing myopia.

## Comparing Two Prescriptions (the "did it really change" test)

- Per-eye, per-field: delta = new − old. |ΔSPH| or |ΔCYL| ≥ 0.50 D = a change you will feel; 0.25 = measurement noise / borderline.
- AXIS shifts ≥ 10° with meaningful CYL (>0.75) will be felt; small axis shifts with weak cylinder don't matter.
- First ADD appearance = presbyopia announcement, usually between 40–45.
- Sudden large jumps (>1.00 D) at any age, or any change with symptoms (headaches, diplopia) → recheck, not just reorder.

## Common Pitfalls

1. **Minus vs plus cylinder confusion** when the prescriber changes (OD→MD). Always ask "is this minus cylinder?" or let the script normalize; entering both Rx's as-if-same yields a "new" axis 90° off.
2. **OD/OS swap when typing online** — the classic silent error. Both eyes similar? You won't feel it for days. Script checks: a swap makes the new order's inter-eye difference flip sign.
3. **Entering the ADD into the SPH field** for reading glasses. Reading-glasses SPH = distance SPH + ADD. If the site has an ADD field, leave SPH alone.
4. **Guessing PD.** Average is 63; using it off by ≥4 mm induces prism — eye strain. Measure (script's `pd` command) or ask; many online stores will request a selfie-measure app.
5. **Believing "we can't release the prescription."** US FTC Eyeglass Rule: you get it immediately, free, after the exam (with pupil distance in many other countries; PD separately in the US). A shop refusing is a rule violation — reportable.
6. **Over-buying lens tiers.** Above 1.67 the marginal thinness is small; coatings (anti-reflective) matter more for comfort than another 0.1 of index for most prescriptions under ±6.
7. **Expired prescription.** Most US states: eyeglass Rx valid 1–2 years (often 2 for adults); contacts typically 1. Online retailers verify — reordering old Rx's past expiry will be blocked.

## Verification Checklist

- [ ] Every field decoded with plain-language meaning + severity band
- [ ] Both eyes compared; any inter-eye difference > 1.00 D flagged (anisometropia — adaptation note)
- [ ] If old Rx supplied: per-field deltas with felt/not-felt verdicts
- [ ] Lens-type verdict + honest cheapest-compliant-material suggestion
- [ ] Cylinder convention identified (or normalized to minus)
- [ ] PD guidance given (measure or obtain) if ordering online

## One-Shot Recipe: decode + compare + order check

```bash
# decode this exam's paper
python3 scripts/rx_decode.py decode --od "-2.75 -1.25 x175" --os "-3.00" --add 2.25 --pd 62
# compare to last year's pair — did it really change?
python3 scripts/rx_decode.py diff --old "-2.50 -1.00 x180 | -2.75 SPH" \
  --new "-2.75 -1.25 x175 | -3.00 SPH"
# measure PD from an existing pair of glasses (ruler + marker method)
python3 scripts/rx_decode.py pd --method mirror
```
