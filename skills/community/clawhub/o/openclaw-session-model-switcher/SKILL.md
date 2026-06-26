---
name: model-switcher
description: Instantly switch the current OpenClaw session model; supports gpt, claude, qianwen, minimax, current model status, configured model listing, and restoring the default session model.
---

# Model Switcher Skill

## Core Rule
When the user asks to switch the current session model, resolve the target dynamically from the active OpenClaw configuration first, then switch the current session directly. Do not hardcode `provider/model` values inside the skill.

## Required Behavior

### Switch current session immediately
When the user says things like:
- `switch to gpt`
- `switch to claude`
- `use qianwen`
- `change to minimax`
- `switch to qwen3.5-flash`

The agent should:
- read `models.providers` from the current OpenClaw configuration
- use `skills/openclaw-session-model-switcher/model-aliases.json` for provider-level alias resolution
- dynamically match against configured models when the user provides a concrete model name or fragment
- directly execute `/model <provider/model>` in the current session after resolving a unique target

Recommended execution path:
- prefer `scripts/switch-model.sh <selection>` to resolve the target model
- once the script returns a unique model, execute the returned command in the current session
- if the environment supports a direct session-level model override tool, prefer that
- do not merely print `/model ...` as plain advice when direct execution is possible

### Restore default
When the user says things like:
- `restore default model`
- `reset model switch`
- `use the default model again`

The agent should directly execute:
- `/model default`

### Show current session model
When the user says things like:
- `what model am I using now`
- `show current model`
- `model status`

The agent should directly query the current session model state instead of only explaining how to check it.

### List configured models
When the user says things like:
- `what models are available`
- `list current models`
- `show configured models`
- `what qwen models do I have`

The agent should read `models.providers` from the current OpenClaw configuration and list switchable models. If the user specifies a provider, only list models for that provider.

## Resolution Rules
- trust only the current OpenClaw configuration in `models.providers`
- keep `model-aliases.json` limited to provider aliases and default semantics
- if a provider has only one configured model, use it directly
- if a provider has multiple models, prefer model-name matching from the user input
- if multiple candidates still remain, list the candidates and ask the user to choose
- if nothing matches, clearly say that no configured model matches the request

## Multi-Agent Rule
- this skill affects only the current persona in the current session
- do not modify global configuration
- do not affect other personas or sessions
- do not restart the Gateway

## Do
- switch the current session directly
- tell the user the current session model was switched
- mention that the change affects only the current session when helpful
- return candidate lists for ambiguous matches
- list current available models when the user is unsure
- consume script output at the upper layer instead of exposing raw stderr or internal errors

## Do Not
- do not edit `openclaw.json`
- do not restart the Gateway
- do not hardcode model IDs inside the skill
- do not maintain a static model list separate from the active configuration
- do not accidentally implement this as a global default model switch
- do not guess in multi-candidate cases
- do not dump raw JSON, stderr, or internal tool errors to normal users

## Suggested Script Interface
- `scripts/switch-model.sh <selection>`: resolve user input and return JSON
- `scripts/list-models.sh [provider]`: list all configured models or only one provider
- `scripts/model-status.sh`: output `/model status`

## Upper-Layer Interaction Flow

### For switch requests
When the user asks to switch models, the upper layer should:
1. call `scripts/switch-model.sh <selection>`
2. parse the JSON output
3. branch on `status`

- `status: ok`
  - execute the returned `command`
  - confirm which model was selected
  - mention that it only affects the current session when useful

- `status: ambiguous`
  - do not surface raw script output
  - convert `options` into a readable candidate list
  - ask the user to reply with a model name or number
  - do not guess

- `status: error`
  - explain naturally that no configured model matched
  - suggest listing available models when appropriate

### For list requests
When the user asks for available models or models from a specific provider:
1. call `scripts/list-models.sh [provider]`
2. present the result as a readable provider-grouped list
3. do not mix in models that are not present in the active configuration

### For status requests
When the user asks which model is currently active:
1. call `scripts/model-status.sh`
2. execute the session-level status query
3. present the result in natural language instead of only teaching the command

## Standard Reply Templates

### Switch success
- `Switched the current session to <provider/model>.`
- `Switched the current session to <provider/model>; this affects only the current session.`

### Ambiguous match
- `You can switch to these models:`
- `1. <provider/model-a>`
- `2. <provider/model-b>`
- `Reply with the model name or a number.`

If the user specified a provider:
- `You can switch to these <provider> models:`

### No match
- `No configured model matches "<selection>".`
- `I can list the models currently available in your configuration.`

### List models
- `These models are currently available in the active configuration:`
- list them grouped by provider

## Fallback Rule
Only if the current environment truly cannot execute native session commands should the agent fall back to replying with:
- the exact command to run
- why it cannot execute it directly in the current environment

That fallback is a degraded path, not the default path.
