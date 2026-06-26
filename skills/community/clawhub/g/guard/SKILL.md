---
name: guard
description: Deep AI safety guardrails workflow—policy definition, input/output filtering, monitoring, escalation, and false-positive handling. Use when reducing harmful outputs, misuse, or policy violations in LLM products.
---

# AI Guardrails (Deep Workflow)

Guardrails turn **product and legal policy** into **enforced behavior**: blocking, rewriting, logging, and human review—with attention to **false positives** and **latency**.

## When to Offer This Workflow

**Trigger conditions:**

- Launching consumer-facing LLM features
- Jailbreak attempts, policy violations, or PII leakage risks
- Region-specific compliance (minors, regulated advice)

**Initial offer:**

Use **six stages**: (1) policy scope, (2) threat model, (3) controls stack, (4) implementation patterns, (5) monitoring & review, (6) iteration & appeals). Confirm latency budget and jurisdictions.

---

## Stage 1: Policy Scope

**Goal:** Define prohibited categories (hate, sexual content, violence, self-harm, malware instructions, etc.) and required disclaimers for sensitive domains (medical, legal).

**Exit condition:** Policy document owned by legal/product; escalation path for gray areas.

---

## Stage 2: Threat Model

**Goal:** Identify adversaries (prompt injection, data exfiltration, tool abuse) and assets (user data, system prompts, connectors).

---

## Stage 3: Controls Stack

**Goal:** Layer defenses: input screening, model safety APIs, output classifiers, tool sandboxing, allowlists for tools and URLs.

---

## Stage 4: Implementation Patterns

**Goal:** Structured refusal messages; telemetry on every block; distinguish block vs rewrite vs warn; avoid silent failures.

---

## Stage 5: Monitoring & Review

**Goal:** Sample borderline cases for human review; dashboards on block rates by category; abuse spike alerts.

---

## Stage 6: Iteration & Appeals

**Goal:** User appeals path where appropriate; version policy changes; measure false positives by locale and use case.

---

## Final Review Checklist

- [ ] Policy categories and owners defined
- [ ] Threat model aligned with product
- [ ] Layered controls with clear responsibilities
- [ ] Telemetry and review for edge cases
- [ ] Appeals and iteration process where applicable

## Tips for Effective Guidance

- Defense in depth—no single classifier is sufficient.
- Pair with **moderation** for UGC and **tool-calling** for agent safety.

## Handling Deviations

- Enterprise internal bots: emphasize data-leak prevention and connector scope over public “safety” categories alone.
