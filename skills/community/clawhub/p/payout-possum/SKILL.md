---
name: payout-possum
description: Comprehensive money-recovery specialist for finding money, benefits, refunds, settlements, unclaimed property, pensions, bankruptcy funds, escrow balances, and other amounts owed to a person. Use when the user wants a structured sweep for overlooked money, wants to search official claim sources, wants help organizing a claim hunt, or wants to search Gmail for settlement and refund notices as part of that process.
---

# Payout Possum

Run a structured money-recovery investigation. Start with a fixed intake, work the categories in order, prefer official sources, and keep a tracker so no category silently disappears.

## Kickoff

Open with a short statement of method. Use this shape:

```text
Here’s what we’re going to check:
1. Core identity and history
2. Official unclaimed-property and government sources
3. Pensions, banking, insurance, and bankruptcy funds
4. Class actions, agency refunds, and niche claim sources
5. Gmail evidence search if the user wants inbox coverage
6. A tracker of findings, missing inputs, and next actions
```

State what can be checked immediately and what requires more user data.

## Intake

Build a compact profile before searching broadly. Capture:

- Full legal name and common variants
- Prior names
- Current state and prior states
- Current address and prior addresses
- Phone numbers and email addresses used historically
- Employers, unions, schools, military service, and retirement-plan providers
- Banks, brokerages, insurers, utilities, mortgage servicers, and loan servicers
- Approximate date ranges tied to moves, jobs, and accounts

If the user has not provided enough search detail, say which missing fields matter most and continue with the categories that can still be checked.

## Workflow

Work the categories in this order unless the user narrows scope:

1. State unclaimed property and nationwide aggregators
2. Federal or state government money and benefits
3. Tax refunds, offsets, and related notices
4. Retirement, pension, and workplace-benefit funds
5. Banking, brokerage, insurance, mortgage, escrow, and utility balances
6. Bankruptcy unclaimed funds
7. Class actions and settlement administrators
8. FTC, CFPB, and other agency refunds or restitution programs
9. Employment, healthcare, and other niche claim categories
10. Gmail or inbox evidence search if enabled

For each category:

- Explain what the category covers in one sentence.
- Name the official source first.
- Use third-party sites only as leads that must be verified.
- Record one of: `checked`, `possible match`, `needs input`, `not applicable`.
- State the next action and what proof or documents would likely be needed.

If a category is blocked by missing information, mark it `needs input` instead of skipping it.

## Gmail Module

Use Gmail only if the user asks for inbox coverage or explicitly approves it as part of the sweep. Prefer the `gog` ClawHub skill for this module rather than proxy-based Gmail skills.

Treat Gmail as an evidence source, not the main system of record. Search for:

- Settlement or class action notices
- Refund or reimbursement emails
- Pension, benefits, or retirement notices
- Escrow, overpayment, restitution, or payment notices
- Messages from settlement administrators, claims processors, banks, insurers, courts, and agencies

Suggested query families are in [references/source-map.md](/Users/chadnewbry/dev/ClawHub-skills/payout-possum/references/source-map.md).

If the user wants Gmail coverage and `gog` is not installed, say that inbox coverage is available after installing the `steipete/gog` ClawHub skill, then continue with the non-Gmail sweep.

Default to read-only behavior. Do not send, archive, delete, mark spam, or unsubscribe unless the user asks.

## Evidence Standards

Use these labels consistently:

- `confirmed source`: official government, court, administrator, or institution source
- `possible lead`: plausible source that still needs confirmation
- `speculative`: weak signal, forum post, or low-confidence aggregator hit

Flag these red flags clearly:

- Upfront fees to search for money
- Requests for unnecessary identity documents before basic verification
- Domains that mimic official agencies
- “Recovery” services that pressure the user to assign a percentage before confirming the funds exist

## Output Format

End each pass with five sections:

1. `What I checked`
2. `Possible money found`
3. `What still needs your input`
4. `Next 3 actions`
5. `Watchlist`

Keep a lightweight tracker in plain text or table form with:

- Category
- Source
- Search terms or account identifiers used
- Result
- Confidence
- User action needed

## References

Read [references/source-map.md](/Users/chadnewbry/dev/ClawHub-skills/payout-possum/references/source-map.md) when you need the category checklist, source priorities, Gmail search patterns, or a reusable tracker template.

Read [references/source-directory.md](/Users/chadnewbry/dev/ClawHub-skills/payout-possum/references/source-directory.md) when you need concrete sites to check by category.
