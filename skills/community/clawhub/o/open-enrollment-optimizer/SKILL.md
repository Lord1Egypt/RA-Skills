---
name: open-enrollment-optimizer
description: "Use during fall benefits/open-enrollment window (or Medicare Oct 15-Dec 7) to choose health plans, FSA/HSA elections, and insurance elections. Models true annual cost of each plan across healthy/typical/high-use scenarios, computes FSA use-it-or-lose-it risk and optimal election, and prices HSA vs FSA vs taxable over a horizon."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [open-enrollment, health-insurance, fsa, hsa, benefits, medicare]
---

# Open-Enrollment Optimizer — Benefits Elections Without the Guesswork

## Overview

Open enrollment is a 2–6 week annual window where people lock in five-figures-worth of decisions
(premiums, deductibles, tax-advantaged accounts, life insurance multiples) from a 40-page PDF,
under deadline pressure, with no do-over until next year. The dominant mistake is premium-shopping:
picking the lowest-premium plan while ignoring that one plan's deductible changes total annual
cost by thousands for the same care. The second mistake is parking the same FSA number every year
— or forfeiting it.

This skill computes **true annual cost** of candidate plans across three utilization scenarios
(healthy year / typical year / bad-luck year), prices FSA elections against realistic spending with
rollover rules, and shows the multi-year tax advantage of HSA-eligibility when choosing a
high-deductible plan. Verdicts name the winner *per scenario* and the robust all-round pick.

## When to Use

- User mentions open enrollment, benefits election, "which health plan should I pick", FSA/HSA
  decision, or comparing employer plan tiers (bronze/silver/gold, PPO vs HDHP)
- Medicare Part D / Advantage annual election (Oct 15 – Dec 7): plan comparison method applies;
  drug-formulary specifics belong to the plan finder, but the cost math is here
- Life events outside the window (marriage, birth, job loss → special enrollment) — same math
- Don't use for: claims/billing disputes, finding specific in-network doctors (network check is a
  manual gate, see Workflow step 3), or tax filing itself

## Core Knowledge

### 1. True annual cost (the only number that matters)

```
TAC(scenario) = 12 × premium + min(max(claims, deductible) × coinsurance + claims_below_ded,
                                    claims) ...capped at out-of-pocket max + premiums
```

Precisely, per scenario with expected claims `C`:
- If `C ≤ deductible`: you pay `C` (all deductible-eligible)
- If `C > deductible`: you pay `deductible + (C − deductible) × coinsurance`
- Capped at `out-of-pocket max` (in-network)
- Always add `12 × monthly premium`
- Add copays separately if the plan is copay-based (script supports both)

A $0-deductible plan at $180/mo more can be *cheaper* than the HDHP for a pregnancy year —
and $3,000 more expensive for a healthy year. The scenarios make this visible instead of vibed.

### 2. FSA election math

- Use-it-or-lose-it with a grace-period OR carryover election (IRS allows ~$660+ carryover,
  inflation-indexed — `--fsa` uses the current figure; verify annually).
- Optimal election = min(expected qualifying spend, risk-adjusted for the chance you leave
  spending unspent). The script prices forfeiture: `election × P(underspend)` vs tax saved on
  every used dollar (marginal rate + FICA ≈ 30–40% for most).
- Dependent-care FSA has its own cap ($5,000) and different mechanics — separate line.

### 3. HSA triple advantage

Contributions dodge income tax, grow tax-free, and come out tax-free for medical spend — the only
triple-tax-advantaged account in US law. Paying medical costs out-of-pocket and saving receipts
lets the HSA act as a stealth retirement account. `--hsa` computes the N-year difference vs
taxable investing at the same gross contribution.

### 4. Elections people forget cost real money

- **Re-electing the same plan** when the plan's premium/deductible/network changed (they do change)
- **Life insurance through work beyond 1–2× salary**: portability is poor; buy term privately for
  the gap, but 1× free coverage is always take it
- **Not naming beneficiaries** (retirement, life) — defaults are wrong after marriage/divorce
- **Skipping the HSA employer seed** ($500–$1,500/yr free money on HDHP)
- **SDP/HCFSA for FEHB folks**, vision/dental only if you have planned procedures

## Workflow

1. **Gather** for each candidate plan: monthly premium (all tiers: employee / +spouse / +family),
   deductible, coinsurance %, out-of-pocket max, copays, HSA-eligibility + employer seed.
2. **Estimate scenarios** (script defaults are sane; adjust to the user):
   - healthy: ~$500 claims (a physical + a couple sick visits)
   - typical: ~$3,000 (a managed condition, one procedure, meds)
   - bad-luck: ~$15,000+ (surgery, ER, imaging — this tests the OOP max)
3. **Gate manually BEFORE math**: is your doctor/medication in-network/formulary? A cheap plan that
   drops your specialist has TAC = ∞. No script can do this — ask the user.
4. **Run:**
   ```bash
   python3 scripts/enrollment_optimizer.py --demo
   python3 scripts/enrollment_optimizer.py --plans plans.json
   python3 scripts/enrollment_optimizer.py --fsa 1400 --spend 1200 --taxrate 32
   python3 scripts/enrollment_optimizer.py --hsa 4300 8 25
   ```
5. **Read verdicts**: per-scenario winner, robust winner, the premium-vs-deductible crossover
   claims amount ("below $X/yr in claims, Plan A wins; above, Plan B").
6. **FSA/HSA**: election + expected forfeiture vs tax saved; HDHP premium savings + seed added to
   the HSA column before declaring an HDHP winner.
7. **Lock the calendar**: elections deadline, FSA claims deadline + grace period dates.

## Verdicts

| Output | Meaning |
|---|---|
| `WINS: <plan> (<$X TAC)` | lowest true annual cost for that scenario |
| ROBUST PICK | wins or near-ties across all three scenarios |
| CROSSOVER | claims $/yr where the ranking flips — the honest answer to "which is cheaper" |
| FORFEIT RISK | FSA dollars at risk if spending comes in low |

## Common Pitfalls

1. **Premium-shopping.** Lowest premium ≠ lowest cost; the deductible and coinsurance dominate
   any year you actually use care. Always compare TAC at your scenario, not the paycheck delta.
2. **Assuming last year's plan is unchanged.** Networks shrink silently; premiums rise 5–10%.
   Re-verify doctor + drug every year even if you re-elect.
3. **FSA parking / round numbers.** Electing "what I did last year" or a round $2,000 forfeits
   real dollars. Elect expected spend minus carryover headroom.
4. **Ignoring the OOP max in the bad-luck scenario.** A low premium/high-max plan can expose you
   to $2–4k more in a surgery year. The bad-luck scenario exists to surface exactly this.
5. **HSA-eligible + not funding the HSA.** HDHP without HSA funding is just a high deductible.
6. **Missing the deadline.** Nov/Dec deadlines are hard; missing them locks defaults (often the
   most expensive option or no FSA at all).

## Verification Checklist

- [ ] All candidate plans entered with premium/deductible/coinsurance/OOP-max
- [ ] TAC computed for healthy / typical / bad-luck scenarios for every plan
- [ ] Manual gate done: doctors in-network, meds on formulary
- [ ] Crossover claims number stated
- [ ] FSA election justified vs expected spend + forfeiture risk priced
- [ ] HDHP candidates include employer seed + premium savings in the comparison
- [ ] Deadlines (election + FSA claims + grace) written down

## One-Shot Recipe: PPO vs HDHP for a family

PPO $520/mo, $1,500 ded, 20% coins, $6k OOP max vs HDHP $360/mo, $3,000 ded, 20% coins, $8k OOP
max, employer seeds $1,000 to HSA. Healthy year: HDHP wins by ~$2,400 (premiums + seed).
Typical year ($6k claims): PPO ≈ $6,240 + $500 = total ~$8,900; HDHP ≈ $3,000 + $600 = $3,600
capped math + premiums − seed ≈ $7,920 — HDHP still wins. Bad-luck ($20k claims): PPO caps at
$6,000 + $6,240 ≈ $12,240; HDHP caps at $8,000 + $4,320 − $1,000 ≈ $11,320 — closer. Verdict:
HDHP robust, fund the HSA with the premium difference, copays for meds confirmed on formulary.
