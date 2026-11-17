---
name: pick-a-model
description: Choose a model on Kyma API for a specific job by comparing real per-token price, measured 30-day uptime, and fit for the task. Use when the user asks which model to use, what the cheapest model for something is, whether a model is up or reliable, how two models compare on price, or wants a model configured for Cline, Cursor, Claude Code, Roo Code or another coding agent.
---

# Pick a model on Kyma API

Answer with measured numbers from the Kyma MCP tools. Never guess a price or an uptime figure.

## When to use

- "Which model should I use for X?"
- "What is the cheapest model that can do X?"
- "Is <model> up right now?" / "Is <model> reliable?"
- "Set up Cline / Cursor / Claude Code with a good model."

## Steps

1. If the user named an agent (Cline, Cursor, Claude Code, Roo Code, Aider, OpenCode, Kilo Code), call `recommend_model` with that agent first. It returns a model plus a ready-to-paste config example. Start from that answer instead of building one yourself.
2. Otherwise call `list_models` to see what is actually served today. Filter to the ones that fit the job: context window, tool calling, vision, reasoning.
3. Call `list_pricing` for the shortlist and compare input and output price per million tokens. Output price dominates for chat and agent loops; input price dominates for long-context or document work, where prompt caching cuts input cost further.
4. Call `get_model_uptime` for each candidate. Uptime is measured over the last 30 days from real observations, not self-reported. Do not recommend a model whose uptime is visibly worse than a same-tier alternative at a similar price.
5. Call `get_model` on the winner to confirm context window, tool support and modality before you hand it over.

## Reporting

- Give one recommendation, then one cheaper alternative and one stronger alternative, each with its price and 30-day uptime.
- Quote the exact model id the user has to paste, not a friendly name.
- Say when a number came from a tool call so the user knows it is live, not remembered.
- If a candidate is missing an uptime figure, say so rather than treating it as healthy.

## Do not

- Do not name or speculate about which inference backend serves a model. Model creators (Google, Meta, DeepSeek, Alibaba, Anthropic, OpenAI) are part of a model's identity and are fine to mention; the machine it runs on is not.
- Do not invent prices, context windows or uptime percentages. If a tool did not return it, say it is unknown.
- Do not send a completion to "test" a model here. That is billed — see the send-a-test-completion skill.
