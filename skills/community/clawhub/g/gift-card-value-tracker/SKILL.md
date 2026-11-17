---
name: gift-card-value-tracker
description: Use when managing a drawer of gift cards, deciding whether to spend or sell one, checking dormancy fees and expiry law (US CARD Act), or when a card's retailer files bankruptcy — balance registry, decay math, resale cash-out verdicts.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [gift-cards, personal-finance, resale, bankruptcy, CARD-Act]
---

# Gift Card Value Tracker

## Overview
Americans hold roughly **$15–23 billion in unused gift cards**, averaging ~$180 per household — money that silently decays. It dies four ways: the card is lost, the retailer goes bankrupt (your balance becomes an unsecured claim worth cents), state escheat laws swallow "abandoned" balances, or dormancy/inactivity fees nibble it away where allowed. Meanwhile every card you'll never use has a cash value today of 60–92% on resale exchanges — but people don't sell because they don't know what they hold.

This skill is a **gift-card portfolio instrument**: a registry of balances (card numbers optional, last-4 fine), decay math (dormancy fees, CARD Act 2009 protections, 5-year validity floor), bankruptcy risk response (spend-first doctrine), and per-card verdicts — **BURN** (spend it, full value), **SELL** (cash out at the best resale %), **CONVERT** (exchange for a merchant you actually use), or **AT RISK** (retailer distress → act this week).

## When to Use
- Post-holidays/birthdays: "I have a stack of gift cards, what should I do with them?"
- Cleaning out a wallet or a parent's estate; consolidating before a move
- A retailer you hold cards for announced store closures or Chapter 11
- Deciding between "spend $50 at a store I hate" vs "sell for $38 cash"
- Checking whether an old card can legally expire or be fee'd down

**Don't use for:** prepaid debit/payroll cards (different fee structures), store credit from returns (often certificate-law-exempt, but usually no resale market), or scam "balance check" calls — never read a card number to anyone who called *you*.

## Quick Start
```bash
# Add cards to the registry (balance + when you got it; last-4 optional)
python3 scripts/gift_card_tracker.py add --store "Home Depot" --balance 50 --received 2024-12-25
python3 scripts/gift_card_tracker.py add --store "Bloomin Brands" --balance 75 --received 2025-06-01 --last4 4417

# Portfolio status: decay risk, dormancy clock, verdicts
python3 scripts/gift_card_tracker.py status

# A resale exchange offered 82% of face value for a card you'll never use
python3 scripts/gift_card_tracker.py sell-advice --store "Home Depot" --offer-pct 82

# Retailer distress: re-score everything for that brand
python3 scripts/gift_card_tracker.py distress --store "Bloomin Brands"
```

## The Decay Model (what the script computes)
1. **Dormancy clock.** US CARD Act 2009: no inactivity fee until **12 months of no activity**, then at most ~$1/month, and only if disclosed on the card. Cards idle 12+ months get a DORMANCY WATCH flag; 24+ months an ACT flag.
2. **Validity floor.** Funds must remain usable at least **5 years from last load/activity**. A card older than that isn't automatically dead — reload/refresh the clock with any purchase, even $1.
3. **Escheat shadow.** State unclaimed-property laws can pull balances after ~3–5 years of no activity (state-dependent). The practical defense is the same: *any activity resets clocks* — buy a $1 item, or consolidate.
4. **Bankruptcy haircut.** In Chapter 11 the retailer *may* honor cards temporarily (court decides; typical window: stop accepting within days–weeks of filing). Treat balance as worth **$0.10–$0.25 on the $1** in liquidation. Doctrine: the moment distress news breaks, cards for that brand convert to SPEND-NOW, highest priority.
5. **Resale reality.** Exchanges (CardCash, Raise, etc.) pay ~60–92% depending on brand liquidity: big-box/electronics high, restaurants mid, niche/fashion low. Selling beats letting a $75 card for a store you never visit decay to zero.

## Verdict Logic
| Situation | Verdict | Action |
|---|---|---|
| You shop there anyway | BURN | Spend like cash; nothing to decide |
| Won't use, resale ≥ 70% | SELL | Cash out; list card, keep proof of sale |
| Won't use, resale < 70% | CONVERT | Exchange kiosk/marketplace swap to a brand you use |
| Retailer distress/bankruptcy | AT RISK | Spend immediately (essentials first) or sell before the market reprices |
| Idle 12+ months, small balance | REFRESH | $1 purchase resets dormancy + escheat clocks |
| Lost physical card | RECOVER | Receipt + last-4 + store call; many can reissue |

## Bankruptcy Playbook (the highest-dollar feature)
1. **News triggers action, not hope.** Chapter 11 filing, "going out of business" sales, or delisting → all that brand's cards = spend this week.
2. **Spend order:** essentials/consumables first (things you'd buy anyway), then resale-friendly goods (buy items that hold value, sell privately) — never gift cards for others, never high-markup "going out of business" junk.
3. **If they stop accepting:** file a claim in the bankruptcy (proof of purchase/card), expect pennies — and count the loss as the tuition that makes you sell future cards from shaky retailers early.
4. **Watch the gift-card promotions** from distressed retailers ("20% bonus on gift cards!") — buying them is lending money to a distressed debtor.

## Security Rules
- Balance-check only at the retailer's own site/app, typing the URL yourself. "Gift card balance check" is a top phishing lure; OTA/refund scams ask victims to read card numbers over the phone.
- A card + PIN is **cash**. Store the registry file like one (no photos of cards in shared albums).
- Never buy discounted cards from marketplaces without buyer protection; stolen-card balances get zeroed.

## Common Pitfalls
1. **Hoarding restaurant cards** "for a special occasion" until the chain files Chapter 11 (a recurring US pattern among casual-dining brands).
2. **Assuming expiry is illegal everywhere** — the 5-year floor is US federal law; other countries differ (EU: 2-year minimum in several states; UK: expiry only if clearly disclosed).
3. **Selling at the first offer** — resale % varies 15+ points between exchanges for the same brand; compare two.
4. **Ignoring digital wallets** — adding cards to Apple/Google Wallet makes the balance usable at checkout you'd otherwise skip.
5. **Confusing store credit with gift cards** after a return: expiry rules and resale value differ.

## Verification Checklist
- [ ] Registry saved (`gift_cards.json`) with received dates, not just balances
- [ ] Every card has a verdict (BURN/SELL/CONVERT/AT RISK/REFRESH)
- [ ] Dormancy clock checked for 12-month-idle cards
- [ ] No full card numbers + PINs stored together in plaintext notes
- [ ] Distress brands re-scored and spent or sold

## Example Session
```
$ python3 scripts/gift_card_tracker.py status
Portfolio: 2 cards, $125.00 total
  Home Depot        $50.00  idle 10.4 mo  -> BURN (you shop here; resale floor 85%)
  Bloomin Brands    $75.00  idle 17.2 mo  -> DORMANCY WATCH; casual-dining distress
       risk: high. SELL or spend this month; resale ~70% ≈ $52.50 cash today.
```
