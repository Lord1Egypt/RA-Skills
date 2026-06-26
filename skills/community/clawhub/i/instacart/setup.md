# Setup - Instacart

Use this when `~/instacart/` does not exist or is empty. Start naturally and keep the conversation focused on the user's Instacart workflow instead of file mechanics.

## Your Attitude

Be precise, implementation-minded, and careful with production boundaries. The user should feel this will save them from bad auth choices, weak product matches, and launch rejections.

## Priority Order

### 1. First: Integration

Within the first few exchanges, learn when this should activate again.

Good early questions:
- Should this jump in whenever Instacart, recipe pages, shopping lists, or retailer lookups come up?
- Should it activate only for real API work, or also for planning and launch-review questions?
- Should write-capable guidance be offered proactively, or only when explicitly requested?

Record the activation rule in `~/instacart/memory.md` so future sessions can reuse it.

### 2. Then: Choose the Operating Surface

Clarify which Instacart surface the user is actually trying to use:
- Developer Platform MCP
- Developer Platform REST
- Connect or fulfillment APIs

This matters more than language choice or SDK choice. If the wrong surface is selected, fix that first.

### 3. Then: Lock Environment and Safety

Learn the minimum needed operating context:
- development or production
- whether an API key already exists
- typical geography and retailer market
- whether the user wants read-only investigation, dry-run planning, or real page creation

If production is involved, ask enough to avoid assuming approval has already happened.

### 4. Finally: Adapt Depth

Some users want quick curl examples. Others want a full integration plan, launch checklist, or agent workflow. Match that depth without turning the conversation into a form.

## What You're Saving Internally

Capture:
- activation boundaries and preferred phrasing
- chosen Instacart surface
- default environment and geo assumptions
- approval boundary for write traffic
- preferred retailer or market constraints
- whether MCP, REST, or Connect is the default answer

Do not store raw API keys, secrets, or copied credentials.
