# Transit Testing for Small Brands

Before cutting a 10k-unit packaging PO, run these three tests. Total cost: under $300 and two weeks.

## Test 1 — Drop test (in-house, one afternoon)

**Goal**: simulate a typical carrier handling event.

- Pack 5 units exactly as production will.
- Drop each from 30 inches onto a concrete floor, once per face (6 drops per unit).
- Also: 1 corner drop per unit from 30 inches (the worst case).
- Open each and inspect for product damage, ink transfer, and dunnage failure.

**Pass**: 5/5 units arrive undamaged. **Soft fail**: 4/5 — investigate which damage mode broke through. **Hard fail**: 3/5 or worse — redesign.

## Test 2 — Live-ship to 20 zip codes

**Goal**: see what real carriers do with the box.

- Ship 20 units to 20 different zip codes across the country (use team members, family, paid testers).
- Recipients photograph the box on arrival, before opening, from four sides. Then open, photograph again, note any damage.
- Track dwell time on the porch if relevant (rain risk).

**Outcome**: gives you damage rate and shows outer abuse patterns — crushed corners, label smudge, tape failure.

## Test 3 — ISTA-3A (third-party lab, for 10k+ unit POs)

**Goal**: industry-standard simulation including vibration, drop, compression.

- Cost: ~$800–$1,500 at a certified lab. Worth it for any PO above ~$20k packaging spend.
- Lab reports give you hard data to negotiate damage claims with carriers later.
- Deliverables: video of the test, pass/fail, recommendations.

**When to skip**: very low-fragility products (apparel, hats) where drop test + live-ship already show 0% damage.

## Damage-rate math

If your damage rate is X% and your average remedy cost is $R per damaged unit, your annual packaging-damage cost is:

```
Annual loss = Monthly volume × 12 × X × R
```

Example: 5,000 units/mo × 12 × 2% × $30 = $3,600/yr in refunds, reships, and negative-review LTV loss.

Compare to the incremental cost of better packaging. If better dunnage saves 1.5 percentage points on damage for $0.25/unit extra, the math is:

```
Savings: 5,000 × 12 × 1.5% × $30 = $2,700/yr
Cost:    5,000 × 12 × $0.25 = $15,000/yr
```

Doesn't pay back. But if the damage rate improvement is 1.5% on a $150 product:

```
Savings: 5,000 × 12 × 1.5% × $150 = $13,500/yr
Cost:    5,000 × 12 × $0.25 = $15,000/yr
```

Close, and it pays back via reviews and LTV. Always run this math before "upgrading for the unboxing feel."

## Common test mistakes

- **Dropping onto carpet**, not concrete. Carriers don't have carpet.
- **Using pre-production samples** that are slightly different from production. Test the exact production unit.
- **Only testing one way up.** Packages land on corners more than you'd think.
- **Testing with a lighter placeholder product.** The real product weight matters for shock calculations.
- **Not testing the sealed outer** — if the carrier tape comes off, the whole test is moot.
