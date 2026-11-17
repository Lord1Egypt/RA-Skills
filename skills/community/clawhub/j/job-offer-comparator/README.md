# Job Offer Comparator ⚖️

**Which job offer is actually better? Not which one has the bigger headline salary — which one is better for your life.**

## The problem

Job offers are deliberately hard to compare. The headline number is base salary, and everything that actually moves your standard of living hides elsewhere: bonus targets written as "up to", retirement match caps in benefits PDFs, $600/month health premiums, 30 km commutes that cost both money and 10 hours a week of your life, equity in a company that may never liquify, and a cost of living that isn't your city's.

The result: people routinely leave $5,000–$25,000 a year (plus 5–15 hours a week) on the table because they compared two numbers that were never comparable — and then negotiate against the wrong one.

## What this skill does

`offer_compare.py` turns any two (or more) offers into an apples-to-apples comparison:

- **True total compensation** — base + expected bonus + capped retirement match + risk-discounted equity + other benefits − health premiums − commute cost, adjusted for cost of living
- **Effective hourly rate on real hours** — contracted hours + overtime + commute time, all priced
- **PTO valuation** — what those 25 vs 15 vacation days are actually worth
- **A plain-language verdict** — who wins on money, who wins on hours/life, and the marginal $/hour of the extra hours the money-rich offer demands
- **Break-even base salary** — the exact number to say in negotiation: *"My other offer is worth $113,700/yr to me. I need $116,204 base to say yes."*

Every assumption is printed above the results — never hidden.

## Example

```
$ python3 scripts/offer_compare.py compare --file offers.json

                       RemoteRocket  BigCityBank
Base salary                $95,000     $115,000
Bonus (expected)            $9,500      $17,250
Retirement match            $3,800      $4,000*
Equity (risk-adjusted)      $6,000           $0
...
TRUE COMP (COL-adjusted)  $113,700     $112,496
Real h/week                   40.0        55.7
Effective hourly           $54.66/h    $38.83/h

=== Verdict ===
Money (true comp): RemoteRocket — $113,700/yr (+$1,204 vs best alternative)
Hours/life: RemoteRocket — real h/week ranked: RemoteRocket 40.0, BigCityBank 55.7
The trade: RemoteRocket leads on true comp, hours, and effective hourly — ...
```

The $115k offer loses. The tool also tells you exactly what base would flip it (`breakeven`).

## Install & usage

Requires Python 3. No third-party dependencies.

```bash
python3 scripts/offer_compare.py example > offers.json   # copy & edit
python3 scripts/offer_compare.py compare --file offers.json
python3 scripts/offer_compare.py breakeven --file offers.json
python3 scripts/offer_compare.py annotate                # field-by-field help
python3 scripts/test_offer_compare.py                    # verify the math
```

## What's inside

```
SKILL.md                          # agent-facing instructions
references/compensation-model.md  # every formula, worked examples, assumptions
scripts/offer_compare.py          # the comparison engine
scripts/test_offer_compare.py     # 36-assertion test suite
```

## Honest limitations

Gross-of-tax model (taxes depend on filing status and jurisdiction). Equity is risk-discounted, not valued. Benefits quality (parental leave, WFH stipend, learning budget) isn't priced — judge it separately. Decision support, not financial advice.

## License

MIT © 2026 Denis Voronin
