# Plan Comparison Method — True Annual Cost Modeling

## Why premiums lie

Two plans can differ by $100/month in premium and by $4,000 in deductible. Over a year, the
premium difference is $1,200 — but a single knee MRI + orthopedist year blows past the deductible
difference in one claim. The only honest comparison is **total annual cost under stated
assumptions about care use**.

## The model

For each plan and each utilization scenario with deductible-eligible claims `C`:

```
medical_spend(C):
    if C <= deductible:        C                          # everything is deductible
    else:                      deductible + (C − deductible) × coinsurance
    cap at:                    out_of_pocket_max

TRUE ANNUAL COST = 12 × monthly_premium + medical_spend(C) − employer_HSA_seed (if HDHP)
```

Rules that matter for correctness:

1. **Premiums are post-tax or pre-tax** — employer premiums are usually pre-tax (×(1−marginal))
   if paid by payroll deduction; Marketplace/COBRA are post-tax. The script has `--pretax-premium`.
2. **Copay plans**: fixed copays ($25 primary, $50 specialist, $ urgent care) apply *before*
   deductible in most plans; the script takes `copays` dict and adds them per scenario visit counts.
3. **OOP max includes deductible** (in-network, ACA-compliant plans). Old plans and some
   grandmothered ones exclude it — check the SBC (Summary of Benefits, page 1).
4. **Out-of-network is a different planet**: separate deductible, 40–50% coinsurance, balance
   billing. This method compares in-network care only.
5. **Embedded vs aggregate deductibles** (family plans): embedded = each person has own ded;
   aggregate = whole family must hit one number. Huge for one-sick-person families.

## Choosing scenarios

| Scenario | Claims | Represents |
|---|---|---|
| healthy | $400–$800 | physical + 1–2 sick visits + labs |
| typical | $2,500–$4,000 | a managed condition, one procedure, generic meds |
| bad-luck | $15,000–$30,000 | surgery/ER/pregnancy — exercises the OOP max |

Adjust from the user's actual last-year spend (claims EOB summary or insurer app history) — last
year's numbers are the best prior for next year absent known events.

## The crossover number

Between two plans there is a claims amount where the winner flips:

```
crossover = solve  12·(P₁ − P₂) + spend₁(C) − spend₂(C) = 0
```

Report it as: "Under ~$X/yr of claims, Plan A is cheaper; above, Plan B." This is the honest
answer to "which is cheaper" — it depends on use, and now the user knows their own threshold.
(With flat coinsurance the solve is closed-form; the script bisects numerically to be safe with
deductible kinks and caps.)

## Medicare application (Oct 15 – Dec 7)

Same TAC method with Part D specifics:
- Premiums: Part B (income-IRMAA-adjusted) + Part D/MA-PD premium
- "Deductible" = Part D deductible; "coinsurance" = tier copays/coins through initial coverage
- "OOP max" = Part D true out-of-pocket (TrOOP) — includes what the *plan* paid? No — your spend +
  what would have been your discount (yes, the 70% manufacturer discount era detail is gone;
  current law counts patient payments). Use the plan finder's modeled annual cost for each drug
  list — then add premiums here. Don't hand-model formulary tiers.
- MA vs Medigap+Original: MA networks are HMO/PPO-tight — the network gate is decisive for MA.

## Life-event special enrollments (any time of year)

Marriage/birth/adoption/job loss trigger 60-day windows. Same math applies, plus:
- New baby → family-tier premium switch + immediately elect dependent-care FSA (permitted
  mid-year with qualifying event even though it's usually annual)
- Job loss → COBRA (102% of premium) vs Marketplace (subsidy on income drop) — compare post-tax
  totals with the subsidy included.

## Data-entry checklist per plan

- [ ] Monthly premium (your tier)
- [ ] In-network deductible (individual AND family if covering others)
- [ ] Coinsurance % after deductible
- [ ] Out-of-pocket max (in-network)
- [ ] Copays (primary/specialist/urgent/ER) — ER copay often waived if admitted
- [ ] HSA-eligible? Employer seed amount?
- [ ] Your doctor in-network? (call the office, don't trust the directory)
- [ ] Your meds on formulary and at what tier?
