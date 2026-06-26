# Setup — LM Studio

Read this when `~/lm-studio/` does not exist or is empty. Help quickly and stay local-first unless the user clearly wants a remote path.

## Operating Attitude

Be practical and skeptical. Get one known-good server plus model plus smoke test working before expanding into MCP, embeddings, or agent workflows.

## Priority Order

### 1. First: Integration

Clarify when this skill should activate in future conversations.

- Should it activate for LM Studio, local models, localhost OpenAI-compatible endpoints, embeddings, or MCP work?
- Should it jump in proactively when a local model is slow, failing, or producing bad structured output?
- Which topics should stay explicit-only, such as paid providers or remote inference?

### 2. Then: Establish the Current Runtime

Collect only details that change the plan.

- Operating system and rough hardware limits.
- Whether LM Studio app, `llmster`, or `lms` is already available.
- Whether the main priority is privacy, speed, cost avoidance, or app integration.

### 3. Finally: Capture Stable Defaults

Store only reusable operating defaults.

- Preferred local port if not the default.
- Known-good model identifiers for chat, coding, JSON, or embeddings.
- Whether MCP is in scope now or should stay off by default.

## Boundaries

- Answer the immediate LM Studio problem first, then refine reusable defaults.
- Avoid long onboarding or tutorials the user did not ask for.
- Never mention internal setup files or memory mechanics in user-facing replies.

## What to Capture Internally

Keep compact notes in `~/lm-studio/memory.md`.

- Activation boundaries and proactive behavior preferences.
- Verified port, server mode, and smoke-test method.
- Known-good models by workload.
- Recurring failure patterns such as OOM, context overflow, bad JSON, or MCP overload.
- Remote-access and MCP trust boundaries.
