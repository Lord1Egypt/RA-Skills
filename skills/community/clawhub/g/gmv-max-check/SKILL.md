---
name: gmv-max-check
description: Check whether a GMV Max setup is usable, risky, or ineligible based on configuration choices, order volume, ROI handling, and conflicting modes. Use when the user wants to avoid setup mistakes, understand why performance is unstable, or verify whether compensation eligibility is likely preserved.
---

# GMV Max Check

Check the setup before the account burns money or loses eligibility.

## Skill Card

- **Category:** Ads Operations
- **Core problem:** Is this GMV Max setup safe and usable?
- **Best for:** New launches, troubleshooting, and compensation-risk checks
- **Expected input:** GMV Max settings + order volume + recent handling notes
- **Expected output:** Configuration verdict + risks + next-fix actions
- **Creatop handoff:** Pass output into ad setup and troubleshooting workflows

## Before you run

Ask the user to clarify:
- current GMV Max objective / target
- whether ROI target was manually changed
- whether max delivery, promo mode, or creative boost is enabled
- daily order volume
- whether this is a new or mature item
- whether recent instability is the main issue

If the user does not know the settings, ask for screenshots or exported setup fields first.

## Optional tools / APIs

Useful but not required:
- ad account export
- campaign settings screenshots
- daily orders sheet
- ROI / spend export

If no API is connected, use screenshot or manual-input mode.

## Workflow

1. Confirm the setup context.
2. Review the configuration against known risk checks.
3. Identify conflicting settings or compensation-risk conditions.
4. Decide whether the setup is:
   - usable
   - usable with risk
   - misconfigured
5. List the next fixes in priority order.

## Output format

Return in this order:
1. Setup verdict
2. Main risk flags
3. Compensation-risk note
4. Priority fixes
5. What to monitor next

## Fallback mode

If the user only provides screenshots or rough settings:
- infer configuration as carefully as possible
- list assumptions explicitly
- avoid false certainty on compensation eligibility

## Quality rules

- Do not invent platform guarantees.
- Separate performance problems from setup problems.
- Flag uncertainty when settings are incomplete.
- Prioritize configuration conflicts before creative advice.

## License

Copyright (c) 2026 **Razestar**.

This skill is provided under **CC BY-NC-SA 4.0** for non-commercial use.
You may reuse and adapt it with attribution to Razestar, and share derivatives
under the same license.

Commercial use requires a separate paid commercial license from **Razestar**.
No trademark rights are granted.
