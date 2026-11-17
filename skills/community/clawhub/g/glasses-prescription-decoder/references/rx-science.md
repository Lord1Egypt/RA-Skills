# Eyeglass Prescription Reference

## 1. Anatomy of the prescription

```
  Rx  Dr. Someone, OD          Date: 2026-10-30
  ┌──────────────────────────────────────┐
  │        SPH     CYL     AXIS    ADD   │
  │ OD    -2.75   -1.25   175    +2.25   │   PD: 62  (sometimes separate)
  │ OS    -3.00   ---      --    +2.25   │
  └──────────────────────────────────────┘
```

- Values in diopters (D), 0.25 steps. AXIS in degrees 1–180 (NOT diopters).
- "SPH" or "DS" written in the CYL cell = zero cylinder (explicitly none).
- Balance "BAL" = non-seeing eye, lens ground to match weight/appearance only.

## 2. Severity bands (population context)

| Metric | Band | Meaning |
|---|---|---|
| SPH −0.25..−1.00 | mild myopia | drive-legal without correction in most jurisdictions; board/school blur |
| SPH −1.00..−3.00 | low-moderate | daily wear zone; clear at ~30–100 cm uncorrected |
| SPH −3.00..−6.00 | moderate-high | uncorrected clear zone ~10–30 cm; constant wear |
| SPH > −6.00 | high myopia | index-1.74 + small frames; retinal-check cadence ↑ |
| SPH +0.25..+2.00 | low hyperopia | often asymptomatic young; strain with screens |
| SPH > +3.00 | high hyperopia | children: urgent-ish follow-up (amblyopia risk) |
| CYL 0.25..0.75 | trace/mild astig | often ignored or left uncorrected |
| CYL 1.00..2.00 | moderate | night starbursts, edge-of-screen skew |
| CYL > 2.00 | high | lens choice matters; axis accuracy critical |
| ADD +0.75..+1.25 | early presbyopia | holding phone farther; push the light up |
| ADD +1.50..+2.00 | established | progressive or dedicated readers |
| ADD +2.25..+2.75 | mature | reading distance locked ~33–40 cm |

## 3. Transposition (plus ↔ minus cylinder)

Optometry convention: **minus cylinder**. Ophthalmology often **plus cylinder**.
Same eye, three-step conversion:

```
SPH'  = SPH + CYL
CYL'  = −CYL
AXIS' = AXIS ± 90   (if AXIS ≤ 90 add 90, else subtract 90)
```

Example: `−2.75 −1.25 × 175` ≡ `−4.00 +1.25 × 85`.
An online form has ONE convention (almost always minus). Entering plus-cylinder values into a minus-cylinder form produces a lens that is wrong in both power and axis → instant "adaptation headache" that never resolves. If two prescriptions from different prescribers look wildly different for the same year, transpose before concluding anything changed.

## 4. PD (pupillary distance)

- Distance PD (far): 54–74 mm, avg ~63. Near PD (reading): subtract 3–4 mm.
- Binocular single number vs monocular (R 31 / L 31.5) — monocular is better for high Rx and progressives; most forms accept either.
- **US:** PD is a *fitting* measurement, not part of the legal Rx → shops keep it to force retail fill. Ask anyway; many will measure for free/small fee. Or self-measure:
  1. Mirror method: stand 50 cm from mirror, marker dot on lens over each pupil center (looking at your OWN reflection's eye), measure between dots. Repeat 3×, average.
  2. Phone-flash "red-eye" selfie at arm's length, scale from a credit card held at temple plane. Free apps do the scaling; accuracy ±1 mm when done carefully.
  3. From old glasses: hold at 90° edge, marker over pupil-center reflection of a small light source, ruler in mm.
- PD error tolerance: ±2 mm fine for low Rx; ±1 mm for |SPH|+|CYL| > 4; progressive channel alignment uses monocular PDs — labs require them for best result.

## 5. Reading/computer glasses derivation

- Full readers SPH = distance SPH + ADD (per eye), CYL/AXIS unchanged.
- Computer glasses (monitor ~65 cm): intermediate power ≈ distance SPH + 0.6 × ADD (rule of thumb; true intermediate is set by your measured working distance):
  `intermediate_ADD ≈ ADD × (1 − (65cm⁻¹ − 40cm⁻¹)/(∞ − 40cm⁻¹))` — the script computes from your working distance in cm.
- Never wear full ADD at monitor distance through a fixed reader bought at a pharmacy (they're set to 40 cm) — you'll lean back and crane.

## 6. Lens material & tier honest guide

| Combined power (max meridian) | Material | Why |
|---|---|---|
| ≤ 2.00 | CR-39 / poly / any | all thin enough |
| 2.00–4.00 | polycarbonate or 1.59 | impact resistance, UV, cheap |
| 4.00–6.00 | 1.67 | visible thinning step |
| 6.00–8.00 | 1.74 | best available; small-frame choice matters more than index beyond here |
| > 8.00 | 1.74 + smallest eye-size frame + ask lab | edge thickness is frame-geometry-limited |

- Anti-reflective coating: highest comfort-per-dollar upgrade for screen users.
- "Blue-light" tint: weak evidence for eye strain; free or cheap = fine, don't pay tiers.
- Photochromic: convenience feature, not vision correction — price accordingly.

## 7. Legal notes (US-centric)

- **FTC Eyeglass Rule (16 CFR 456):** prescriber MUST give you your complete eyeglass prescription immediately after the exam, free, whether or not you ask. Withholding = violation, reportable to FTC. It does NOT have to include PD.
- **Contact Lens Rule:** CL prescription released after fitting (you pay for the fit; the paper is yours).
- Rx validity: state-set, typically 1 year (minors often less), 1–2 years adults; expiration must be on the Rx.
- Verification: online sellers may verify with your prescriber (8 business hours to respond) — that's normal, not a scam.

## 8. Adaptation expectations after change

- New Rx Δ ≤ 0.50 D: minutes to a day.
- First progressive ever: 3–14 days of peripheral swim; return if > 2 weeks.
- Large axis rotation (>15°) with CYL > 1.00: up to a week of tilted-world.
- Anisometropia (inter-eye difference > 1.00 D, or > 1.5 D meridian-wise): ground-in prism or contact lenses often beat glasses (image-size difference, spectacles magnify unequally).
- Any "adaptation" still failing at 3 weeks = go back; labs do remake errors, and one recheck of the ordered values against the paper catches most.
