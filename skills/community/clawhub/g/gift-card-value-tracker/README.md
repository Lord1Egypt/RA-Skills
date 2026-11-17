# Gift Card Value Tracker

Roughly **$15–23 billion in gift cards sits unused** in the US — about $180 per household — dying quietly four ways: lost plastic, retailer bankruptcy (your $75 becomes an unsecured claim worth pennies), state escheat laws swallowing "abandoned" balances, and dormancy fees where allowed. Meanwhile a card you'll never use has cash value **today** at 60–92% on resale exchanges. People don't act because they don't know what they hold or what it's worth.

This skill turns a drawer of gift cards into a managed portfolio:

- **Registry** with received dates and last-4 (never full numbers+PIN together)
- **Decay math** — CARD Act 2009 rules encoded: no inactivity fee before 12 months idle, ~$1/month after, 5-year validity floor, escheat window watch
- **Verdicts per card**: BURN (spend like cash) / SELL (cash out) / CONVERT (swap to a brand you use) / REFRESH ($1 purchase resets the clocks) / **AT RISK** (retailer distress → spend this week)
- **Bankruptcy playbook** — distress news triggers spend-first doctrine, not hope; spend order and claim-filing if the chain stops accepting
- **Resale judge** — feed it a live exchange offer, get SELL / SELL-IF / LOWBALL against brand-class fair bands

## Real problem it solves
"I got $185 in gift cards for stores I don't shop at" is a recurring post-holiday reality. Without structure, those cards sit until the casual-dining chain files Chapter 11 (a recurring US pattern) or the balance escheats to the state. This instrument forces a dated decision per card and prices the sell-vs-hoard trade honestly.

## Quick start
```bash
python3 scripts/gift_card_tracker.py add --store "Bloomin Brands" --balance 75 --received 2025-06-01
python3 scripts/gift_card_tracker.py status
python3 scripts/gift_card_tracker.py sell-advice --store "Sephora" --offer-pct 72
python3 scripts/gift_card_tracker.py distress --store "Bloomin Brands"   # news broke
```

## Example output
```
[2] Bloomin Brands  $75.00 -> AT RISK
    marked distressed: SPEND this week (essentials first) or sell before
    the market reprices. Bankruptcy haircut 75-90%.
```

## Contents
- `SKILL.md` — verdict logic, CARD Act rules, bankruptcy playbook, security rules
- `references/decay-bankruptcy-resale.md` — law, escheat mechanics, resale economics, non-US notes
- `scripts/gift_card_tracker.py` — stdlib-only CLI (add/list/status/sell-advice/distress/spend)

## License
MIT
