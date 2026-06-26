---
name: model-brain
description: Route each incoming message to the right Bankr/OpenClaw model or to a zero-LLM path based on task type, risk, and cost. Use when you need per-message model selection, cost-aware routing, deterministic skill bypasses, or a model recommendation for aaigotchi workflows.
---

# Model Brain

Use this skill when the goal is to choose the right model for a single message or action.

## Core policy

- Prefer `zero-llm` when a deterministic skill or script can do the job.
- Use the cheapest adequate model for low-risk work.
- Use `bankr/claude-sonnet-4.5` for routine wallet and treasury operations that are important but still normal.
- Escalate to `bankr/claude-opus-4.6` only for explicitly high-stakes, security-sensitive, or ambiguous wallet flows.
- Use `bankr/gpt-5.2-codex` for coding-heavy implementation work.
- Keep routing deterministic and rule-based before adding any LLM-on-LLM behavior.
- Treat the output as a routing recommendation, not as transaction authority.

## Default routes

- `zero-llm`
  - deterministic skills like `pet-me-master`
  - shellable tasks with no reasoning need
- `bankr/minimax-m2.5`
  - casual chat, lightweight rewriting, simple summaries, low-risk classification
- `bankr/claude-sonnet-4.5`
  - general reasoning, planning, product thinking, routine wallet ops
- `bankr/gpt-5.2-codex`
  - coding-heavy patching, repo surgery, implementation details
- `bankr/gemini-3-pro`
  - long-context synthesis and broad document digestion
- `bankr/gemini-3-flash`
  - lightweight vision and quick multimodal triage
- `bankr/claude-opus-4.6`
  - explicitly high-stakes wallet actions, security reviews, tricky architecture, final escalation

## Routing workflow

1. Check whether the request can be handled by a deterministic skill or script.
2. Classify the task: `chat`, `code`, `wallet`, `vision`, `long-context`, or `deterministic`.
3. Mark whether the request is high-stakes.
4. Route to the cheapest safe model.
5. Return the primary route, fallback route, and a short reason.

## Quick start

```bash
python3 {baseDir}/scripts/route_message.py --text "pet all my 53 gotchis" --json
python3 {baseDir}/scripts/route_message.py --text "rewrite this x thread shorter" --json
python3 {baseDir}/scripts/route_message.py --text "swap ETH to USDC and send to treasury" --json
bash {baseDir}/scripts/select_model.sh --text "build this feature in the repo" --mode summary
```

## Wrapper entrypoint

Use `scripts/select_model.sh` when you want a simple aaigotchi-friendly wrapper before model selection. It can emit just the route, full JSON, or shell-style env lines.

## References

- Read `references/routing-table.md` for the routing rules and escalation thresholds.
- Read `references/bankr-models.md` for the current Bankr model inventory and aaigotchi default.
