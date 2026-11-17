---
name: nous-model-deal-router
description: Use when choosing best-value Nous Portal models.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [hermes, nous-portal, models, cost, routing, approvals]
    related_skills: [hermes-agent, hermes-token-efficiency]
---

# Nous Portal Model Deal Router

## Overview

Select the **cheapest Nous Portal model that reliably meets the requested workload**, including temporary sales. This is a recommendation-and-approval workflow: never change the provider, default model, or current-session model without explicit user approval.

## When to Use

- “Pick the best model for the money.”
- “Find a discounted / sale model on Nous Portal.”
- “Switch me to the cheapest model that is still good.”
- “What should I use for coding, research, or routine agent work?”
- “Review this model picker and recommend one.”

Do not use for a non-Nous provider unless the user expands scope. Never auto-switch simply because a model is cheaper.

## Evidence Rules

1. **Use current evidence.** Catalog, prices, promotions, and availability change. Prefer the current Portal model picker, `hermes model --refresh`, `hermes portal info`, or a user-provided current screenshot.
2. **Confirm Nous is usable.** Run `hermes portal info`; ensure the user is authenticated and record the configured provider/current default.
3. **A sale requires explicit UI evidence.** Treat an item as on sale only when the live picker shows a promotion/discount and/or a visible “was” price. A cache-read rate is not automatically a sale.
4. **State labels faithfully.** Do not invent pricing units or call a price column “cached input” unless the picker labels it that way.
5. **Do not use stale screenshot values as live facts.** Date them and refresh before making a recommendation whenever possible.

## Selection Procedure

### 1. Classify the work

Use the request; if it is absent, default to **balanced agentic work** (tool use, coding, research, file edits).

| Workload | Primary criterion |
|---|---|
| Routine / high-volume tools | lowest reliable total cost; solid tool calling |
| Coding / debugging | code quality and tool reliability; output price matters |
| Research / long-context synthesis | reasoning, context capacity, synthesis quality |
| Architecture / high-stakes work | strongest suitable model; cost secondary |
| Casual drafting / experiments | lowest cost with acceptable quality |

### 2. Establish a capability floor

Pick the least-expensive candidate that clears the relevant floor:

- **Budget:** dependable low-cost agentic/coding model.
- **Balanced (default):** strong general agentic model—not merely adequate.
- **Premium:** best suitable reasoning/coding model for difficult work.

Free models are experimental/low-stakes by default. Do not recommend one for important work purely because it costs zero.

### 3. Compare total cost, not just input tokens

Compare the displayed final input and output prices after discount. Weight output more heavily for code generation and research synthesis; weight input somewhat more for concise tool actions. Mention cache pricing separately only if repeated prompts make it material.

Do not manufacture precision. Use “materially cheaper” unless the displayed figures support an explicit ratio.

### 4. Filter and decide

Exclude unavailable entries, models missing a verified price, models not in the current Portal picker, and models which official Portal guidance says are unsuitable for Hermes Agent's tool-calling loop. A large discount alone cannot overcome a poor fit.

### 5. Present a concise recommendation

Lead with one winner and one lower-cost alternative:

```text
Best value for <workload>: `<provider/model>`
Why: <fit> at <shown input/output rate>; <visible sale detail if applicable>.
Cheaper alternative: `<provider/model>` at <rate>, trading off <specific capability/reliability>.
Current model: `<provider/model>` at <rate>, if known.

Switch the default Nous model to `<provider/model>`?
```

If the winner is already the current model, explicitly recommend keeping it and **do not ask to switch**. Ask for approval only when the proposed model differs from the current model.

## Approval Gate and Switching

A recommendation is **not** permission. Switch only after a clear instruction such as “yes, switch,” “approve that model,” or “use it as my default.” Clarify ambiguous replies.

### Persistent default

After approval, use the official CLI:

```bash
hermes config set model.provider nous
hermes config set model.default <approved-provider/model>
```

Then run `hermes config` and report the resulting `model.provider` and `model.default` exactly.

### One-off invocation

After approval, use an explicit override without changing the user's default:

```bash
hermes chat --provider nous --model <approved-provider/model> -q "<request>"
```

### Existing session

Explain that the user changes the active conversation with:

```text
/model <approved-provider/model>
```

A config default change takes effect for new sessions; do not claim it changed the running conversation.

## Example from a Dated Menu

A screenshot from 2026-08-02 displayed `openai/gpt-5.6-terra` at $1.00/$6.00 per million input/output tokens, marked 60% off, and `deepseek/deepseek-v4-pro` at $0.35/$0.70. For balanced agentic work, Terra may be the capability/value choice; for routine coding where spend dominates, DeepSeek may be the better budget choice. This is **not** a standing recommendation: refresh live prices and availability first.

## Common Pitfalls

1. **Cheapest equals best.** Apply the workload's capability floor first.
2. **Discount percentage over final price.** Compare the actual displayed final rates.
3. **Cache pricing mistaken for a promotion.** Keep those concepts separate.
4. **Silent model change.** Always get explicit approval first.
5. **Wall of rankings.** Give one recommendation and one cheaper alternative unless a full ranking is requested.
6. **Forgetting session semantics.** `/model` affects the active session; config defaults affect new sessions.

## Verification Checklist

- [ ] Portal login/provider and current price evidence verified.
- [ ] Workload and capability floor identified.
- [ ] Final displayed input/output costs compared.
- [ ] One recommended model plus one cheaper alternative presented.
- [ ] Explicit approval obtained before switching.
- [ ] Final provider/model verified after a persistent change.
