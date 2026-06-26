# OpenClaw Session Model Switcher

Instantly switch the current OpenClaw session model without editing global config or restarting the Gateway.

## Features

- Switch the current session to a target model
- Restore the default session model
- Check the current session model status
- List the models currently configured in OpenClaw
- Support provider aliases and model-name fragment matching

## Design Principles

- Affect only the current session
- Trust only `models.providers` from the active OpenClaw configuration
- Do not edit `openclaw.json`
- Do not restart the Gateway
- Return candidate choices instead of guessing when the match is ambiguous

## Usage

### Switch models

```text
switch to gpt
switch to claude
use qianwen
change to minimax
switch to qwen3.5-flash
```

### Restore default

```text
restore default model
reset model switch
use the default model again
```

### Query status

```text
what model am I using now
show current model
model status
```

### List models

```text
what models are available
list current models
show configured models
what qwen models do I have
```

## How It Works

1. Call `scripts/switch-model.sh <selection>` to resolve the target
2. Match dynamically against `models.providers` from the active configuration
3. Return one of three outcomes:
   - `ok`: an exact `/model ...` command
   - `ambiguous`: a candidate list
   - `error`: no configured model matched
4. Let the upper-layer agent execute the correct session-level action

## Scripts

- `scripts/switch-model.sh`: resolve user input and return JSON
- `scripts/list-models.sh [provider]`: list all models or one provider
- `scripts/model-status.sh`: output `/model status`
- `skills/openclaw-session-model-switcher/handler.sh`: convert script results into user-facing guidance

## Examples

### Successful switch

```text
Run this command to switch the current session model:
/model openai/gpt-5.4

Note: this switches only the current session.
```

### Ambiguous match

```text
You can switch to these qwen models:
1. qwen/qwen3.5-flash
2. qwen/qwen3-vl-flash
Reply with the model name or a number.
```

### No match

```text
No configured model matches "foo".
I can list the models currently available in your configuration.
```

## Pre-publish Checklist

- `SKILL.md`, `README.md`, and `handler.sh` describe the same behavior
- No wording suggests global config edits or Gateway restarts
- `ok`, `ambiguous`, and `error` results are all handled cleanly
- The model list shows only real models from the active configuration
