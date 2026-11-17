# The Compensation Model

This document defines every formula `offer_compare.py` uses, with a fully
worked example whose numbers match the tool's `example` output.

## 1. Why salary alone lies

Two offers, headline numbers $95,000 and $115,000 — a $20k gap. But the
offers differ in:

- **Bonus**: 10% target vs 15% target — +$7,750 for the big offer
- **Retirement match**: 4% uncapped-up-to-$10k vs 6% capped at $4k
- **Equity**: $12k/yr of private-company grants vs none
- **Health premiums**: $150/mo vs $600/mo employee share — −$5,400/yr
- **Commute**: 0 vs 30 km × 5 days — cost AND ~10.7 h/week of life
- **Overtime norm**: 40 h vs 45 h weeks
- **Cost of living**: index 100 vs 115

Each of these is knowable from the offer documents. None of them is in the
headline number. The model's job is to line them up.

## 2. Formulas

### 2.1 Gross compensation

```
bonus            = base × bonus_pct
retirement_match = min(base × retirement_match_pct, retirement_match_cap)
equity_ev        = equity_annual_value × (1 − equity_risk)
other_annual     = other_benefits_monthly × 12
gross            = base + bonus + retirement_match + equity_ev
                 + other_annual + relocation_bonus   (one-time, flagged)
```

`bonus_pct` is the **expected** payout. If the letter says "up to 20%" and
historical payout is ~60% of max, enter 0.12. Entering the max systematically
inflates bonus-heavy offers.

`equity_risk` is the probability the grant is worth ~nothing when it vests.
Sensible defaults: 0.0–0.2 for liquid public RSUs, 0.5 for late-stage
private, 0.8–0.95 for early startup. A $12k/yr grant at 0.5 risk is a $6k/yr
expected value — still real, no longer dominant.

### 2.2 Commute

```
annual km      = commute_km_each_way × 2 × commute_days_per_week × 52
transport cost = annual km × commute_cost_per_km
parking        = monthly_parking_or_transit × 12
commute cost   = transport + parking
commute h/week = 2 × commute_days_per_week × (km_each_way ÷ 28)
```

The 28 km/h door-to-door average includes lights, transfers, and parking
walks. `commute_cost_per_km` default $0.30 is an all-in car rate (fuel,
tires, service, depreciation) — broadly in line with motoring-club and
tax-authority per-km figures; adjust to your actual car or transit fare.

### 2.3 True compensation

```
risk_adjusted = gross − health_premium_monthly×12 − commute_cost
true_comp     = risk_adjusted ÷ (col_index ÷ 100)
```

`col_index = 100` is your baseline (usually your current city, so the
comparison answers "am I better off?"). 115 = 15% pricier city. This is a
blown-goods approximation: it adjusts everything, though taxes and housing
move differently from the general index.

### 2.4 Real hours and effective hourly

```
work h/week  = hours_per_week + overtime_hours_per_week
real h/week  = work h/week + commute h/week
effective_hourly = true_comp ÷ (52 × real h/week)
```

This is the single most clarifying metric in the model: it converts
everything into "dollars per hour of my life, in my city's prices."

### 2.5 PTO value

```
true_daily_rate = true_comp ÷ 260        (52 weeks × 5 days)
pto_value       = pto_days × true_daily_rate
```

PTO is already paid inside base — this valuation exists to **price the
difference** between offers (25 days vs 15 days at a $437 daily rate is a
$4,373/yr difference in time-for-money).

### 2.6 Break-even base

Find base B for the losing offer L such that:

```
true_comp(L | base = B) = true_comp(winner)
```

Solved by bisection (200 iterations, tolerance ≪ $1). Bisection is used
instead of algebra because the retirement-match cap introduces a kink: below
the cap, base increases true comp at rate (1+bonus_pct+match_pct)/col; above
it, only at (1+bonus_pct)/col. The target is expressed **in the loser's
city's dollars** (its own COL index applied), holding its bonus %, match
%/cap, and deductions constant.

## 3. Worked example (matches `example` output)

Offer A "RemoteRocket": base 95,000; bonus 10%; equity 12,000 @ risk 0.5;
match 4% cap 10,000; health 150/mo; other benefits 100/mo; 40 h; no commute;
COL 100; PTO 25.

```
bonus      = 95,000 × 0.10            =  9,500
match      = min(95,000×0.04, 10,000) =  3,800   (uncapped)
equity EV  = 12,000 × 0.5             =  6,000
other      = 100 × 12                 =  1,200
gross      = 95,000+9,500+3,800+6,000+1,200 = 115,500
health     = 150 × 12                 =  1,800
commute    = 0
risk_adj   = 115,500 − 1,800          = 113,700
true comp  = 113,700 ÷ 1.00           = 113,700
real hours = 40
eff. hourly= 113,700 ÷ (52×40)        = $54.66/h
```

Offer B "BigCityBank": base 115,000; bonus 15%; match 6% cap 4,000; health
600/mo; 30 km × 5 days @ $0.30/km; parking 250/mo; COL 115; 45 h; PTO 15;
relo 8,000.

```
bonus      = 115,000 × 0.15           = 17,250
match      = min(115,000×0.06, 4,000) =  4,000  ← CAP BINDS (6% would be 6,900)
gross      = 115,000+17,250+4,000+0+8,000 = 144,250
health     = 600 × 12                 =  7,200
commute km = 30×2×5×52                = 15,600 km/yr
transport  = 15,600 × 0.30            =  4,680
parking    = 250 × 12                 =  3,000
risk_adj   = 144,250 − 7,200 − 7,680  = 129,370
true comp  = 129,370 ÷ 1.15           = 112,496
real hours = 45 + 2×5×(30/28)         = 55.7
eff. hourly= 112,496 ÷ (52×55.7)      = $38.83/h
```

**Verdict**: the $95k remote offer wins on money ($113,700 vs $112,496),
on hours (40 vs 55.7 h/week), and on effective hourly ($54.66 vs $38.83).
The headline $20k gap was an illusion created by uncapped-vs-capped match,
premiums, commute, overtime, and COL.

**Breakeven**: BigCityBank needs base ≈ **$116,204** (+1.0%) to match
RemoteRocket's true comp — that is the counter-offer number. Conversely,
RemoteRocket could drop to $93,944 and still win.

## 4. Assumptions table

| Assumption | Value | Why |
|---|---|---|
| Working year | 52 weeks, 260 days | standard paid-year convention |
| Commute speed | 28 km/h door-to-door | urban average incl. stops |
| Car cost | $0.30/km | all-in motoring rate (adjust!) |
| Equity risk default | 0.50 | illiquid private grant |
| Taxes | ignored | filing-status dependent; compare gross first |
| Relocation | year-one only | flagged in table |
| Benefits quality | not modeled | parental leave, WFH stipends — judge separately |

## 5. Limitations

- **Gross-of-tax.** Two offers with equal true comp can differ thousands in
  after-tax value (equity timing, pre-tax deductions). Consult a tax
  professional for final decisions.
- **COL index is blunt.** It scales everything by one number; if you would
  rent vs buy differently across the two cities, model housing separately.
- **Bonus persistence not modeled.** A 15% target in a bad year pays 0.
- **Equity upside beyond EV ignored.** A lottery ticket's expected value
  isn't its whole story — but decisions should rest on EV, not hope.

## 6. Negotiation notes

- The breakeven number is a **floor for the loser to become acceptable**, in
  the loser's own city terms. Ask for a bit more than breakeven.
- The reverse number (how far the winner could drop) tells you how much
  margin you have when the winner lowballs after you decline the loser.
- Negotiate the **cap**, not just base: lifting BigCityBank's match cap from
  $4k to uncapped is worth $2,900/yr — often easier for HR to approve than
  $2,900 of base.
- Every revised offer → update JSON → re-run `compare` + `breakeven`.
