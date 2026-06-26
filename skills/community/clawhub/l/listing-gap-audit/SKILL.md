---
name: listing-gap-audit
description: Audit listing competitiveness by comparing your PDP/listing against top competitors and surfacing the highest-impact copy/proof gaps. Use when the user asks why conversion is lagging, wants PDP rewrite priorities, or needs a competitor benchmark before launch.
---

# Listing Gap Audit

## Skill Card

- **Category:** PDP Optimization
- **Core problem:** How does our listing underperform compared with competitors?
- **Best for:** Listing rewrite prioritization
- **Expected input:** Your listing text + competitor listings + product constraints
- **Expected output:** Gap report across title, bullets, proof, offer framing, and action priorities
- **Creatop handoff:** Send priority rewrites into script/copy generation workflows

## Browser-first guidance

When live listing URLs are available, prefer **OpenClaw managed browser** to inspect your PDP and competitor PDPs before generating the audit.

Recommended order:
1. If the user already has copied listing text, use that first.
2. If URLs are available, inspect live pages with **OpenClaw managed browser**.
3. Use Browser Relay only when the user explicitly wants to inspect their current Chrome tab.

The default browser guidance should be OpenClaw managed browser, not a generic Playwright assumption.

## Workflow

1. Clarify the comparison goal.
   - Which listing is yours?
   - Which competitor pages matter most?
   - Is the user optimizing for CTR, conversion, trust, or claim safety?
2. Parse listing components: headline, bullets, proof, offer, objections.
3. Benchmark against competitor structure and claim density.
4. Score gaps by conversion impact and implementation effort.
5. Generate rewrite priorities with before/after guidance.

## Output format

Return in this order:
1. Executive summary (max 5 lines)
2. Priority actions (P0/P1/P2)
3. Evidence table (signal, confidence, risk)
4. 7-day execution plan

## Quality and safety rules

- Do not copy competitor claims verbatim.
- Flag compliance-sensitive claims explicitly.
- Keep recommendations feasible for current product constraints.
- If browser evidence is partial, label it clearly.

## License

Copyright (c) 2026 **Razestar**.

This skill is provided under **CC BY-NC-SA 4.0** for non-commercial use.
You may reuse and adapt it with attribution to Razestar, and share derivatives
under the same license.

Commercial use requires a separate paid commercial license from **Razestar**.
No trademark rights are granted.
