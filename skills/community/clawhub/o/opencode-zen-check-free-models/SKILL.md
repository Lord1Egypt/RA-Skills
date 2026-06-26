---
name: opencode-zen-check-free-models
description: Monitors the OpenCode Zen pricing page for new free models and offers to update your default configuration.
version: 1.0.0
user-invocable: true
requires:
  bins:
    - curl
---

# OpenCode Zen - Check Free Models

When this skill is triggered, follow this logic to keep the user's environment updated with the best available free models:

## 1. Fetch Pricing Page
Fetch the HTML content of the OpenCode Zen pricing documentation:
```bash
curl -sL [https://opencode.ai/docs/zen/#pricing](https://opencode.ai/docs/zen/#pricing)
```

## 2. Extract Free Models
Parse the webpage content (specifically looking at the pricing tables or lists) to identify available models. Extract the names/IDs of any models where the input/output cost is listed as "Free", $0.00, or models with names containing "free" (as well as known free stealth models like `big-pickle`).

## 3. State Comparison
Check the extracted list of free models against the state file located at `./zen_seen_models.json` within the current workspace.
- **If no changes are detected:** Exit silently. Do not notify the user unless they manually invoked this skill.
- **If a new free model is detected:** 
    1. Alert the user: "🚀 **OpenCode Zen Update:** I found a new free model on the pricing page: `[Model ID]`. It is now available."
    2. Ask: "Would you like me to set `[Model ID]` as your new default model for OpenClaw (for all Agents, Compaction, and Heartbeat)?"

## 4. Execution
- **If the user confirms:** Update the local OpenClaw configuration file in the workspace (e.g., `config.yaml`) or set the relevant environment variables to the new model ID.
- **Finalize:** Save the newly updated list of free models as a JSON array to `./zen_seen_models.json` in the workspace to ensure the user is not prompted again for these specific models.
