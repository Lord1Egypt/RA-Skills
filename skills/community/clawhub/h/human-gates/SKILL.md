---
name: human-gates
description: >
  Part of the Overpowered skill suite.
  Design or review where human approval, judgment, or accountability must remain in an automated workflow. Use when automation crosses authority, legal, financial, safety, irreversible, or genuinely ambiguous decisions; do not preserve manual steps merely because they exist today.
metadata:
  suite: overpowered
  suite_url: https://github.com/raguets/overpowered
  level: "0-primitive"
  version: "0.1.0"
---

# Overpowered / Human Gates

## Core rule

**Keep humans for authority, accountability, material ambiguity, and unacceptable risk — not for work a deterministic or agentic system can reliably perform.**

## Procedure

For each candidate human step:

1. Identify why the human is currently involved.
2. Classify the reason:
   - **authority** — only an authorized person may decide;
   - **accountability** — an accountable owner must accept the outcome;
   - **material ambiguity** — available evidence cannot reliably determine the case;
   - **risk control** — error cost exceeds the accepted automation boundary;
   - **legacy/manual habit** — no durable reason remains.
3. Automate legacy/manual steps when controls are sufficient.
4. Define each retained gate with:
   - trigger condition;
   - decision owner or role;
   - evidence presented to the human;
   - allowed decisions;
   - timeout/delegation path;
   - downstream effect.

## Output contract

```text
Gate | Trigger | Why human | Required evidence | Owner | Outcomes
```

## Gotchas

- “Human in the loop” is not a design; define the exact gate.
- Do not make a human re-check deterministic calculations unless policy requires it.
- Historical manual ownership is not proof that human judgment is needed.
- Never infer delegated authority from precedent alone.

## Stop condition

Stop when every retained human step has a concrete reason and every removed human step has an adequate automated control.
