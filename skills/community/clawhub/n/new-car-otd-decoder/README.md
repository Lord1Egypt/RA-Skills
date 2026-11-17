# new-car-otd-decoder

**Out-the-door quote forensics for new-car buyers.** Audits every line of a purchase
worksheet or lease deal: classifies fees as FAIR / STATE-CAPPED / PADDED / REFUSE,
finds the total dealer padding, computes a corrected OTD, decodes lease money factor
into real APR, and compares dealer financing against a pre-approved loan.

## The real-world problem

The average new-car deal contains **$500–$2,500 of dealer-installed padding** — VIN
etching at 75× cost, "surface protection" that's a $15 bottle of sealant, nitrogen
fills of ordinary air, gap insurance marked up 30× over your auto insurer's price.
Sales tax treatment of rebates varies by state (Texas taxes them), doc fees are
capped at $85 in California but uncapped in Ohio, and lease deals hide their interest
rate behind a "money factor" that almost no buyer converts to APR.

Buyers see none of this because it arrives as a single confusing worksheet at the
moment of maximum fatigue — 45 minutes before driving home in the car they've
already mentally bought.

## What it does

| Capability | Detail |
|---|---|
| Line-item audit | Every quote line classified FAIR / STATE-CAPPED / OVER-CAP / PADDED / REFUSE with the reason |
| Add-on catalog | 25+ classic dealer add-ons with real fair values (VIN etch = $0, mats = OEM list, gap = $20–30/yr via your insurer) |
| State rules | Doc-fee caps, rebate taxation (TX/NM tax rebates), trade-in tax credit (CA/DC/HI/MI/VA give none) |
| Lease decode | Money factor × 2400 = effective APR; payment re-derived from cap cost/residual/MF; markup cost of a bumped MF |
| Financing check | Amortization comparison — dealer rate bump vs pre-approval, total interest delta |
| Negotiation playbook | The 4-email OTD sequence, F&I office defense, lease counters, walking rules |

## Quick start

```bash
# see what a padded deal looks like, audited
python3 scripts/otd_decoder.py --demo

# audit your own quote
python3 scripts/otd_decoder.py --quote scripts/quote.example.json

# decode a lease offer
python3 scripts/otd_decoder.py --lease 0.00145 41500 58 36 7.5

# what a 0.0004 money-factor markup costs you over 36 months
python3 scripts/otd_decoder.py --lease-markup 0.0004 41500 58 36

# dealer 7.9% vs bank 5.5% on $32,356 / 60mo
python3 scripts/otd_decoder.py --finance 32356 5.5 60 7.9
```

Stdlib only — no dependencies.

## Example

A Texas worksheet shows $41,995 "OTD" including VIN etching $1,495, surface
protection $495, nitrogen $210, all-weather mats $495, gap insurance $795. The audit
refuses $2,200 outright (etch/protection/nitrogen/gap → your insurer charges
$25/yr), counters mats at $200 — **corrected OTD ≈ $39,900, padding found ≈ $2,100.**
It also flags that Texas taxes the $3,000 rebate, so the rebate is worth $3,000, not
$3,000 + $248 of tax savings.

## Why it matters

Cars are the second-largest purchase most people make, 5–8 times per lifetime, against
a professional counterpart whose entire craft is worksheet fog. This skill turns a
confusing worksheet into a short refuse-list and one honest number to negotiate.
