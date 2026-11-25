---
name: india-income-tax
description: Compare India's new vs old income tax regime for Tax Year 2026-27 (Income-tax Act, 2025) and work out exact tax, rebate, surcharge, cess, HRA exemption, monthly TDS and break-even deductions. Use when someone in India asks how much income tax they will pay, which regime to choose, whether to switch, how much to invest in 80C/NPS to save tax, or what their salary means after tax.
version: 1.0.0
tags: [india, tax, income-tax, finance, salary, itr]
---

# India Income Tax: New vs Old Regime (Tax Year 2026-27)

Gives an exact, side-by-side tax estimate for a **resident individual in India** under both regimes, using a deterministic calculator. Never do the slab arithmetic in your head: always run the script.

## When to use
- "How much tax will I pay on ₹18 lakh?"
- "Old or new regime for me?" / "Should I switch regimes?"
- "How much should I put in 80C / NPS to make the old regime worth it?"
- "What will my monthly TDS be?"
- "Is ₹12.75 lakh really tax-free?"

## Steps

1. **Collect inputs.** Ask only for what's missing, in one short message. Yearly amounts in rupees.
   - Required: gross `salary` (or 0), `age`.
   - Helpful: `other_income` (FD/savings interest, rent after 30% deduction), `basic_da`, `hra_received`, `rent_paid`, `city`, `sec_80c`, `sec_80ccd_1b` (own extra NPS), `employer_nps`, `health_insurance_self`, `health_insurance_parents`, `parents_senior`, `home_loan_interest` (self-occupied), `professional_tax`, `other_old_deductions` (80E, 80G, 80TTA…).
   - If the person gives a monthly figure or CTC, convert it and state your assumption (e.g. "taking ₹1.5L/month × 12 = ₹18L gross; employer PF excluded").
   - If they don't know their deductions, run once with zero deductions and show the break-even figure.

2. **Run the calculator** (from this skill's folder):
   ```bash
   python3 scripts/tax.py '{"salary": 1800000, "age": 30, "sec_80c": 150000}'
   ```
   `python3 scripts/tax.py --example` prints every supported field.

3. **Present the result** briefly:
   - A two-column table: taxable income, slab tax, rebate/relief, surcharge, cess, **total tax**, monthly TDS.
   - One line: which regime is cheaper and by how much.
   - If old regime is costlier, use `extra_old_deductions_to_break_even`: "You'd need about ₹X more in deductions for the old regime to win."
   - Suggest specific next steps only where the numbers support them (e.g. employer NPS works in both regimes; 80C only helps in the old regime).

4. **Always end with the caveat**: this is an estimate, not tax advice; confirm on incometax.gov.in's calculator or with a CA.

## Rules built into the script (Tax Year 2026-27)
- **New regime (default):** 0–4L nil, 4–8L 5%, 8–12L 10%, 12–16L 15%, 16–20L 20%, 20–24L 25%, above 24L 30%. Standard deduction ₹75,000. Rebate (s.156, formerly 87A) up to ₹60,000 when taxable income ≤ ₹12L, with marginal relief just above ₹12L. Surcharge 10% / 15% / 25% above ₹50L / ₹1Cr / ₹2Cr (max 25%). Employer NPS allowed up to 14% of basic+DA.
- **Old regime:** 0–2.5L nil (3L if 60–79, 5L if 80+), then 5% / 20% / 30%. Standard deduction ₹50,000. Rebate up to ₹12,500 when taxable income ≤ ₹5L. Surcharge up to 37%. Caps: 80C ₹1.5L, 80CCD(1B) ₹50k, home-loan interest ₹2L, 80D ₹25k/₹50k (senior), professional tax ₹2,500. HRA = least of HRA received, rent − 10% of basic, 50% of basic (Delhi, Mumbai, Kolkata, Chennai, Bengaluru, Hyderabad, Pune, Ahmedabad) or 40% elsewhere.
- Health & education cess 4% on tax + surcharge in both. Marginal relief on surcharge is applied.

## Out of scope (say so if asked)
Capital gains at special rates (STCG/LTCG on shares, property), business/presumptive income, non-residents, HUFs, arrears relief, and advance-tax interest. For those, recommend a CA.

## Updating for a new year
All numbers live in the `RULES` dictionary at the top of `scripts/tax.py`. Change them there after each Union Budget.
