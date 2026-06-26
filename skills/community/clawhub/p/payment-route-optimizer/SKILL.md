---
name: payment-route-optimizer
description: Build payment-routing diagnostics, route matrices, retry and failover policies, rollout guardrails, and merchant-friendly planning briefs for payment, checkout, finance, and cross-border ecommerce teams. Use when comparing PSPs, acquirers, local methods, authorization rate, processing cost, or chargeback-sensitive routing decisions without touching live payment traffic.
---

# Payment Route Optimizer

## Overview

Use this skill to turn payment-operations context into an offline routing strategy brief. It is best for merchants and product teams that need clearer routing logic, safer failover planning, and a readable rollout package.

This MVP is planning-oriented. It does **not** switch live traffic, move money, inspect raw PAN data, or replace compliance review. It translates merchant goals into route candidates, retry guardrails, and implementation notes.

## Trigger

Use this skill when the user wants to:
- improve authorization rate or payment success rate
- reduce payment processing cost without blindly sacrificing approval
- compare PSPs, acquirers, local methods, or failover setups
- prepare a routing policy review, outage plan, or market-launch payment strategy
- generate a rollout checklist for engineering, finance, or payment ops

### Example prompts
- "Help me improve card authorization in Brazil"
- "Create a payment failover plan before peak season"
- "We need a routing matrix that balances approval and fee cost"
- "Turn these PSP notes into a rollout playbook"

## Workflow

1. Capture the objective, markets, payment methods, and major constraints.
2. Normalize the current routing question into approval, cost, risk, or balanced mode.
3. Generate segment-level route candidates and backup paths.
4. Add retry rules, failover guardrails, and rollout sequencing.
5. Return a markdown planning brief for review by product, finance, and engineering.

## Inputs

The user can provide any mix of:
- payment-log summaries or pasted findings
- PSP, acquirer, local method, or fee-sheet context
- market, currency, issuer, BIN, device, or amount-band concerns
- goals around authorization, cost, fraud, 3DS friction, or resilience
- rollout constraints, such as human approval, engineering bandwidth, or peak-season risk

## Outputs

Return a markdown brief with:
- routing objective and planning mode
- baseline diagnostic
- suggested route matrix
- retry and failover policy
- rollout plan
- monitoring guardrails
- compliance and limitation notes

## Safety

- Do not claim to execute live routing changes.
- Keep raw card data out of scope and assume only masked or tokenized inputs.
- Treat compliance, PCI, fraud, and chargeback review as external control layers.
- Require human approval before any production policy is adopted.

## Examples

### Example 1
Input: merchant wants better card approval in Brazil and Europe with two PSPs.

Output: recommend a segment-level routing matrix, one-retry rule for soft declines, and a staged rollout with market-specific monitoring.

### Example 2
Input: payment team wants an outage fallback plan before peak season.

Output: generate timeout, soft-decline, and provider-outage failover guidance with rollback triggers.

## Acceptance Criteria

- Return markdown text.
- Include diagnosis, route matrix, retry or failover guidance, and rollout sections.
- Keep the output readable for non-engineers.
- Make the offline and approval-required boundary explicit.
