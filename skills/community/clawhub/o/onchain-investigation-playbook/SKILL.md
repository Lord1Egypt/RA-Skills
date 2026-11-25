---
name: onchain-investigation-playbook
version: 1.0.0
description: Investigate an on-chain question step by step: identify the wallets, follow the flows, and separate confirmed links from guesses. Use for tracing funds, checking exposure, or verifying a claim.
---

# Onchain Investigation Playbook

## Overview

On-chain investigation is evidence work: every hop needs a transaction, and every conclusion needs a confidence level. This playbook keeps the chain of evidence clean so the conclusion can be trusted — and challenged.

## When to use

When tracing stolen funds, checking whether a protocol touches a flagged contract, or verifying a claim about wallet behavior.

## Workflow

1. **Fix the question** — one sentence; investigations sprawl without it
2. **Anchor the starting points** — the exact addresses/transactions in question, from a primary source
3. **Follow flows hop by hop** — each hop recorded with its tx hash; never skip a hop because the pattern 'looks obvious'
4. **Label the actors carefully** — an address is an address; an identity is a claim that needs its own evidence
5. **Grade every finding** — confirmed (on-chain), probable (pattern), unknown (gap); never blur the grades in the write-up
6. **State the limits** — what the data cannot show (off-chain agreements, exchange-internal moves)

## Guardrails

- Never name a person or project as a wrongdoer on pattern evidence alone
- Screenshots are not evidence — tx hashes are
- Stop and report when the trail goes cold instead of inventing the next hop

## Output format

An investigation report: question, anchors, hop-by-hop trail with hashes, findings graded by confidence, limits.

---

Part of the Manteclaw free skill series. These workflow skills are free forever; Manteclaw's paid automation tools (runnable code, not just prompts) live at payhip.com/Manteclaw.
