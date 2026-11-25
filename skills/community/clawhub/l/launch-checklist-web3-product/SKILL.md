---
name: launch-checklist-web3-product
version: 1.0.0
description: A launch-day checklist for a Web3 product or token-adjacent release: contracts, keys, comms, monitoring, and the rollback plan. Use in the week before any mainnet launch.
---

# Launch Checklist Web3 Product

## Overview

Launches fail on logistics more than code: wrong address in the announcement, unmonitored contracts, no plan when the first bug report lands. This checklist sequences the final week so launch day is execution, not improvisation.

## When to use

The week before a mainnet launch, a token release, or opening a product to public funds.

## Workflow

1. **Freeze the facts** — final contract addresses, chain IDs, official links; one canonical source document, everything else copies from it
2. **Key custody check** — who holds which keys, on what hardware, with what backup; no launch-critical key in a hot wallet by accident
3. **Monitoring live before launch** — alerts on contract events, balance thresholds, and error rates, tested with a real ping
4. **Comms staged** — announcement copy with addresses pasted from the canonical doc (never retyped), support answers for the five likeliest questions, and a pinned 'official links only' post
5. **Rollback and pause plan** — what can be paused, by whom, in how many minutes; what cannot be rolled back and therefore gets extra review
6. **Dry-run the first hour** — a named human watches dashboards for the first hours; handoffs scheduled, not assumed

## Guardrails

- Never retype an address into launch copy — copy-paste from the canonical source and verify the checksum
- Impersonation accounts appear within minutes of a real launch — pre-register handles and warn users in advance
- If the pause plan is untested, the launch is not ready

## Output format

A launch checklist with owners and times: facts frozen, custody verified, monitoring tested, comms staged, rollback rehearsed.

---

Part of the Manteclaw free skill series. These workflow skills are free forever; Manteclaw's paid automation tools (runnable code, not just prompts) live at payhip.com/Manteclaw.
