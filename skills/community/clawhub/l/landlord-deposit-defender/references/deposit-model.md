# The Deposit Dispute Model

The complete model behind `deposit_defender.py`: condition grading, the
wear-vs-damage decision rules, useful-life proration math, jurisdiction
deadlines, the evidence checklist, and the anatomy of the generated dispute
letter.

## 1. Why this problem is structured (and mostly arithmetic)

A deposit dispute looks like an argument but decomposes into checkable
claims. The landlord asserts, for each deducted item: (a) the condition got
worse during the tenancy, (b) the worsening exceeds fair wear and tear, and
(c) the price is right. Each claim can be tested against evidence and
depreciation math. Tenants lose by arguing feelings instead of attacking (b)
and (c) item by item. This tool systematizes (a)–(c).

## 2. Condition grading rubric (0–5)

| Grade | Label | Meaning |
|---|---|---|
| 0 | new | freshly installed / unused |
| 1 | excellent | no visible wear beyond factory |
| 2 | minor wear | light scuffs, slight sheen loss — ordinary use |
| 3 | noticeable wear | visible wear spots, matted carpet paths, small marks |
| 4 | significant damage | holes, burns, stains, broken fixtures |
| 5 | destroyed / missing | item unusable or gone |

Grades are recorded per **room + item** with a free-text note and a date.
Two dated inventories (move-in, move-out) are the minimum evidence skeleton.

## 3. Wear vs damage: decision rules

The diff engine classifies each item present in both inventories:

1. **Improvement** — grade decreased (got better): never chargeable.
2. **Fair wear and tear** — grade delta ≤ 1 *over a normal-length tenancy*,
   or the defect text matches ordinary-use patterns (scuffed paint, worn
   paths, faded blinds, gently marked countertops). Not chargeable in most
   jurisdictions.
3. **Potential damage** — grade delta ≥ 2, or the defect type is outside
   ordinary use: burns, cuts, holes, missing fixtures, pet urine, broken
   appliances. Chargeable in principle — but only up to prorated value (§4).

Item age matters: a 1-grade drop on paint over 6 months looks different
from the same drop over 6 years. The engine takes tenancy length from
`--tenancy-start/--tenancy-end` and tempers classification accordingly
(short tenancy lowers the tolerance for deterioration).

Defect-type keywords in notes (burn, hole, stain, missing, crack, scratch,
fade, scuff) feed the classification; the rubric keeps it deterministic.

## 4. Useful-life proration

The core formula:

```
max_deduction = item_value × max(0, 1 − years_used / useful_life_years)
```

- `years_used` = tenancy length (or item age at move-out if known).
- If `years_used ≥ useful_life`, the item was fully depreciated — the
  maximum deduction is **zero**; the landlord received the item's full value
  as a business cost already.
- `item_value` should be like-for-like replacement of the *depreciated*
  item, not an upgrade. Charging new-for-old is double recovery.

**Typical useful-life table** (property-industry / IRS-style residential
depreciation conventions; local rules and the tenancy agreement may
override — treat as defaults):

| Item | Useful life (yr) |
|---|---|
| Interior paint | 3 |
| Wallpaper | 7 |
| Carpet | 8 |
| Vinyl flooring | 10 |
| Laminate flooring | 15 |
| Tile | 25 |
| Blinds | 5 |
| Curtains/drapes | 7 |
| Appliances (fridge, range, DW) | 12 |
| Smoke detector | 10 |
| Interior doors | 30 |
| Window seals/units | 20 |

**Worked example.** Carpet, useful life 8 yr, replacement value $1,200,
tenancy 2.5 yr:

```
max_deduction = 1200 × (1 − 2.5/8) = 1200 × 0.6875 = $825
```

A $1,200 demand over-claims by $375. After a 3-year tenancy, interior paint
(life 3 yr) is fully depreciated: max deduction $0 — the classic
"repainting charge" on a 3-year tenant's statement is rebuttable to zero.

## 5. Jurisdiction deadlines (typical — verify current law)

| Jurisdiction | Typical window to return deposit / itemize |
|---|---|
| US-CA | 21 days, itemized statement mandatory |
| US-NY | 14 days (reasonable time standard) |
| US-TX | 30 days |
| US-FL | 15–60 days per notice |
| US-IL | 30–45 days |
| US-WA | 21 days |
| US-CO | 30 days (60 if mailed) |
| US-PA | 30 days |
| US-GA | 30 days |
| US-NC | 30 days |
| UK (England/Wales) | 10 days via protection scheme |
| DE | up to 6 months for claims (BGB) |
| AU-NSW | 14 days |
| CA-ON | 30 days (interest on deposit) |

Consequences of lateness vary: some jurisdictions void deductions, some
award multiples of the deposit. The generated letter cites the deadline and
the date the itemized statement was actually received.

## 6. Evidence checklist

- Dated, room-by-room photos at move-in *and* move-out (metadata intact).
- Meter readings (utilities) at both ends, photographed.
- The signed move-in inspection report (refuse to sign blank ones).
- All deposit-related correspondence kept in writing; log dates.
- Receipts for any repairs/cleaning you paid for yourself.
- Witness or co-signature on inventories where possible.

## 7. Anatomy of the generated letter

`letter` assembles, in order:

1. **Header** — parties, tenancy address, deposit amount, date.
2. **Timeline** — tenancy start/end, notice given, move-out inspection,
   statement received date.
3. **Itemized rebuttal** — for each claimed deduction: the landlord's
   amount and reason; the classification (wear/damage/improvement); the
   prorated maximum where applicable; the disputed delta.
4. **Deadline citation** — jurisdiction window vs actual date; consequence.
5. **Demands** — corrected refund amount, itemized receipts for every
   claimed cost, like-for-like evidence.
6. **Escalation notice** — intent to pursue small-claims / scheme
   adjudication if not resolved within a stated window (default 14 days).

The letter is deliberately dry and itemized: it reads like the opening
exhibit of a court file, because that is its function.

## 8. Limitations & disclaimer

Decision support, not legal advice. Useful lives, deadline windows, and
wear-vs-damage doctrines vary by jurisdiction and change over time; the
tables here are marked "typical" for a reason. Read your tenancy agreement
(forward it into the notes if it defines its own schedules). When amounts
are material, verify current local statutes or consult a tenants' union or
attorney.

MIT © 2026 Denis Voronin
