# Traveling with Medications — Rule Book

This reference backs `scripts/medtravel.py`. It is compiled from public
regulatory guidance (TSA, US DEA scheduling, FDA drug stability labels,
national import rules) and is intentionally conservative: when in doubt the
script says STOP and points at the embassy. It is not medical advice.

## 1. Airport security (TSA-style rules)

- **Medications in pill form**: allowed in carry-on in any quantity. No
  prescription needed at the checkpoint itself — but border/immigration is a
  different check (below).
- **Medically necessary liquids** (syrups, injectables, insulin): exempt from
  the 100 mL / one-bag limit, **but must be declared** to the officer and are
  subject to additional screening. Frozen gel packs used to keep medicine cold
  are allowed — say so at the start, not after the X-ray flags it.
- **Syringes/needles**: allowed with the injectable medication they support.
  Keep them together with the labeled box.
- **Checked baggage**: never pack critical or temperature-sensitive medicine
  there. Checked holds routinely drop below 0°C and are delayed/lost.
- **Rule of two**: split the supply — half in your personal item, half in a
  companion's bag or a second carry-on, plus 2–3 extra days of buffer.

## 2. US controlled-substance schedules (for the letter/container rule)

| Schedule | Examples (keyword hits in the script) | Travel rule |
|---|---|---|
| II | Adderall/amphetamine, methylphenidate (Ritalin/Concerta), oxycodone, morphine, fentanyl | Original container + doctor letter; declare at borders; count must match Rx |
| III | Testosterone, ketamine, codeine combinations (<90mg/dose in some countries) | Letter recommended |
| IV | Alprazolam, lorazepam, diazepam, tramadol, zolpidem | Letter recommended; some countries restrict |
| V | Low-dose codeine cough syrups, pregabalin (in some jurisdictions) | Original container |

Prescription-checkpoint reality: domestic TSA does not verify prescriptions;
**immigration and foreign customs do**, and they can and do confiscate.

## 3. Destination gates (KB shipped with the script)

- **Japan**: amphetamine/methylphenidate-class stimulants are prohibited
  narcotics; import needs a Yakkan Shoumei certificate applied ~2 months ahead
  via MHLW. Some OTC allergy meds (pseudoephedrine) also restricted.
- **UAE / Saudi Arabia / Qatar**: many psychotropics (incl. stimulants,
  alprazolam) require pre-approval from the national health authority; carry
  the original + a doctor letter + sometimes an attested Arabic translation.
- **Singapore**: sleeping pills and anxiolytics need a license (HSA approval);
  codeine restrictions.
- **Greece**: codeine and tramadol controlled — prescription + letter required.
- **China**: strictly controlled psychotropics; requires certificate.
- **Schengen area**: for >90-day supply of some controlled drugs a Schengen
  certificate (Article 75) applies.
- **Anywhere not listed**: embassy check is the default for Schedule II/III.

## 4. Cold-chain drugs and stability windows

| Drug | Unopened | In use (room temp) | Notes |
|---|---|---|---|
| Insulin (all: glargine/Lantus, lispro, aspart, degludec) | 2–8°C until expiry | **28 days** ≤25–30°C | Never freeze, never car glovebox, never checked hold |
| Semaglutide (Ozempic) | 2–8°C until expiry | 28 days ≤30°C (pen in use) | Preflight: verify hotel fridge temperature — some freeze |
| Tirzepatide (Mounjaro) | 2–8°C | 21 days ≤30°C | |
| Insulin degludec (Tresiba) | 2–8°C | 56 days (in use) | Longest in-use window — good for long trips |
| Biologics generally (adalimumab etc.) | 2–8°C | 14 days ≤25°C typical | |
| EpiPen | 15–30°C (NOT a fridge drug) | — | Thermal pouch, not cold chain |

**Packing protocol (cold chain)**: Frio evaporative pouch (activated with
water) or insulated pouch + 1 frozen gel pack wrapped in cloth (never direct
contact — local freezing destroys protein drugs). Voltage abroad differs —
most hotel mini-fridges run too cold: put pens in the door shelf or wrap in a
sock, and carry a small liquid thermometer.

## 5. Supply math and early refills

```
pills_needed = days × doses_per_day
deficit = pills_needed − pills_on_hand
```
- Deficit > 0 → call the prescriber now. For controlled substances say the
  words "vacation supply" / "early refill with vacation override" — insurers
  have a standard override code for travel.
- Insurance typically allows up to a 90-day fill for maintenance drugs
  specifically for travel; ask before the trip, not after.

## 6. Doctor's letter — required elements

1. Doctor's letterhead + license number + contact
2. Patient full name (as in passport) and date of birth
3. Each medication: brand + generic name, dose, form, frequency
4. Statement "prescribed for the patient's ongoing medical condition"
5. Signature and date (issued within ~30 days of travel)

The `letter` subcommand prints this as a checklist + a ready-to-send request
email so the doctor's office can produce it in one pass.

## 7. Timezone shift doctrine (summary)

| Regimen | Zone shift ≤4 h | Zone shift >4 h / long-haul |
|---|---|---|
| Once daily, wide window | Take at new local time immediately | ±1 h per day ladder, or single early/late dose within 18–30 h gap — never double |
| Twice daily | Keep home clock, shift on return | Travel-day interval may stretch to 8–14 h once, then local time |
| Basal insulin | Home clock if trip ≤3 days | Shift 2–3 h/day toward local; check glucose more often |
| Fixed-interval (birth control, some antibiotics) | Home clock entire trip | Alarm on home-clock time for the whole trip is simplest and safe |
| Levothyroxine | Any consistent time; a missed-timing day is absorbed with negligible harm — but do not skip | |
