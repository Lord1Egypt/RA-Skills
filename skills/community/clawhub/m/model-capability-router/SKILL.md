---
name: model-capability-router
description: "Recommend an available OpenClaw model and thinking level for a task. Choose from the configured subscription models or ask for GPT only."
---

# Model Capability Router for OpenClaw

Ask "Which model should I use for this task?" to get a model, a thinking level, and a short reason. The router makes recommendations. You choose whether to switch.

## Use it in OpenClaw

1. Install it with `openclaw skills install @theangrypit/model-capability-router`.
2. In chat, ask "Use Model Capability Router to pick a model for this review." Add "GPT only" to restrict the choice to GPT.
3. Use `/model list` to see the model IDs available in that chat. To apply a recommendation to the current session, use `/model <provider/model>`. Use `/think` to see the thinking levels available for your model.

## Make a recommendation

- Default to the [OpenClaw subscription guide](references/openclaw-subscriptions.md) for GPT, Claude, Gemini, Grok, and Composer. Use the [GPT-only guide](references/gpt-only.md) when requested.
- Check the models and tools available to the current OpenClaw session. Use the exact provider and model ID when verified. Ask the user to check the model picker if the catalog is unavailable.
- Preserve the user's explicit model, thinking level, and provider account. Recommend a thinking level the selected model supports. A listed model or an API price does not establish subscription access.
- Keep the work in the current session when its model can do the job. If the user requests a subagent, use OpenClaw's native subagent controls and check the child session can use the requested model and tools.
- Give the recommended model, thinking level, and one task-specific reason. If the preferred model is unavailable, explain what is missing and suggest a verified option on an existing authorized provider.

For comparisons, see the [pricing and benchmark notes](references/gpt62-20261117.md). Published API prices do not measure your subscription allowance.
