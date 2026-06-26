---
name: Groupon
slug: groupon
version: 1.0.0
homepage: https://clawic.com/skills/groupon
description: Find, compare, and vet Groupon vouchers with fine-print checks, refund rules, and redemption planning.
changelog: Initial release with SAVE deal screening, merchant risk checks, and voucher recovery workflows.
metadata: {"clawdbot":{"emoji":"🎟️","requires":{"bins":[],"config":["~/groupon/"]},"os":["linux","darwin","win32"],"configPaths":["~/groupon/"]}}
---

## When to Use

Use this skill when the user wants help with Groupon deals, vouchers, or local offers and needs more than a headline discount.

Use it for discovery, shortlist building, merchant validation, fine-print review, booking friction checks, post-purchase triage, and refund or support recovery planning.

## Architecture

Memory lives in `~/groupon/`. If `~/groupon/` does not exist, run `setup.md`. See `memory-template.md` for structure and status values.

```text
~/groupon/
├── memory.md       # City, budget posture, category preferences, and hard no rules
├── shortlists.md   # Ranked deals with verdicts and caveats
├── purchases.md    # Bought, gifted, or expiring vouchers with next actions
└── incidents.md    # Booking failures, merchant disputes, refund attempts, support notes
```

## Quick Reference

Use the smallest file needed for the current task.

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory structure and status model | `memory-template.md` |
| SAVE scorecard and output format | `deal-qualification.md` |
| Merchant trust and fine-print checks | `merchant-checks.md` |
| Category-specific watchouts | `category-playbook.md` |
| Refund, booking, and support recovery | `recovery.md` |

## Core Rules

### 1. Start with intent, not the discount badge
- Capture the real job first: category, city, date window, party size, budget, and travel tolerance.
- Distinguish "find something fun under budget" from "check whether this exact voucher is worth buying."
- A 70% headline discount is irrelevant if the user cannot redeem it on the needed day or for the needed group size.

### 2. Run the SAVE screen before recommending anything
Use the SAVE workflow from `deal-qualification.md`:
- **Scope** the real use case and deal type.
- **Assess** merchant quality and booking friction.
- **Verify** every restriction in the fine print.
- **Estimate** the true out-of-pocket cost and redemption effort.

No recommendation is complete until SAVE ends with a clear verdict.

### 3. Treat fine print as blocking data
- Always read the restriction block, not just the title and hero price.
- Check validity windows, excluded days, one-per-person rules, "new customers only" language, auto-gratuity, add-ons, taxes, paid value vs promo value, and required booking channels.
- If any critical term is missing or ambiguous, say so plainly and downgrade confidence.

### 4. Optimize for redeemability, not theoretical savings
- Prefer deals the user can actually book this week, in the right neighborhood, with acceptable scheduling friction.
- Penalize phone-only booking, narrow redemption windows, poor recent reviews, and merchants that seem hard to reach.
- If the merchant fit is weak, recommend a better option even when the headline discount is smaller.

### 5. Separate deal types before making policy claims
- Local services, goods, getaways, and ticketed offers behave differently on booking, shipping, expiration, and refunds.
- Do not promise refund outcomes from memory alone. Confirm the live deal type, voucher status, and current Groupon policy before giving a final answer.
- In post-purchase workflows, document whether the voucher is unused, booked, redeemed, shipped, or disputed.

### 6. Keep money-impacting actions user-approved
- The agent may search, compare, shortlist, draft support messages, and guide checkout or redemption.
- Buying, gifting, booking, marking redeemed, or submitting a refund request needs explicit user confirmation.
- Never store payment details, login secrets, full voucher barcodes, or claim codes in local files.

### 7. Leave a decision-ready output every time
Return the final recommendation in this structure:

```text
Verdict: Recommend | Recommend with caveats | Skip
Best fit: [deal or category]
Why it wins: [up to 3 bullets]
Blocking terms: [if any]
True cost: [price + known extras]
Next step: [buy now, hold, compare, contact merchant, request support]
```

## Common Traps

| Trap | Why It Fails | Better Move |
|------|--------------|-------------|
| Ranking by discount percent alone | Inflated list prices make weak offers look amazing | Compare true cost, merchant quality, and redemption friction |
| Ignoring neighborhood and timing | A cheap deal two neighborhoods away at the wrong hour is not value | Score location, travel time, and usable dates early |
| Skimming past "restrictions apply" | The deal can become unusable for weekends, groups, or repeat visits | Read the full fine print before any recommendation |
| Assuming every voucher refunds the same way | Groupon rules vary by deal type and current status | Classify the deal first, then use `recovery.md` |
| Treating service deals like retail products | Trust, availability, and upsells dominate the real outcome | Run merchant checks and booking friction checks |
| Recommending merchants with stale or weak signals | Closed, overloaded, or badly rated merchants create support pain | Use recent reviews and direct booking clues, not score alone |
| Jumping to checkout without extras | Mandatory gratuity, taxes, parking, drinks, or upgrades erase savings | Estimate true cost before telling the user to buy |
| Logging sensitive voucher details | Local notes can become a privacy or fraud problem | Store only what is needed to follow up safely |

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| `https://www.groupon.com/*` | search terms, city or ZIP, deal URLs, and normal browser navigation signals | discovery, fine-print review, and support page lookup |
| `https://help.groupon.com/*` | issue categories, deal type references, and support navigation | refund, booking, and policy verification |

No other data is sent externally.

## Security & Privacy

**Data that leaves your machine:**
- Search terms, location context, and deal URLs sent to Groupon pages during discovery and verification.
- Optional support or booking context the user explicitly asks to submit.

**Data that stays local:**
- Preferences, shortlist decisions, and follow-up notes in `~/groupon/`.

**This skill does NOT:**
- Access files outside `~/groupon/`
- Store payment cards, login secrets, or full voucher codes
- Buy, redeem, or request refunds without explicit user approval
- Claim merchant quality or refund certainty when the evidence is weak

## Trust

By using this skill, deal-search context may be sent to Groupon and, when the user chooses to proceed, to the merchant tied to a specific offer.
Only install if you trust Groupon and the selected merchant with that context.

## Scope

This skill ONLY:
- Finds and compares Groupon offers
- Screens merchants, restrictions, and usable value
- Guides checkout, booking, and recovery workflows with explicit approval boundaries

This skill NEVER:
- Guarantee availability, savings, or refund outcomes
- Hide uncertainty about fine print or merchant quality
- Spend money or reveal voucher secrets without the user's instruction

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `buy` — evaluate real value, compare alternatives, and avoid bad purchases
- `shopping` — broaden the search when Groupon is not the best channel
- `booking` — plan reservations and compare travel or stay options
- `tripadvisor` — validate hospitality and attraction quality with broader review signals
- `travel` — connect local offers with larger trip planning decisions

## Feedback

- If useful: `clawhub star groupon`
- Stay updated: `clawhub sync`
