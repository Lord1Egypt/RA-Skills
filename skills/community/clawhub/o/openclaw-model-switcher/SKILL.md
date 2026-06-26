---
name: model-switcher
description: "Switch the OpenClaw default model safely. Triggers: switch model, change model, 切换模型, 换模型, switch to XX model. Use when the user wants to change the default AI model. Reads openclaw.json, validates the target model exists in the configured provider list, backs up config, modifies only agents.defaults.model.primary, restarts gateway, and auto-rolls back on failure."
---

# Model Switcher

Switch the OpenClaw default model with backup, validation, and automatic rollback.

## Workflow

### Step 1: Validate Model Name

Read `~/.openclaw/openclaw.json`. Extract:
- Current model from `agents.defaults.model.primary`
- Available models from `models.providers` list

Match user request against available models (exact, alias, or partial match):
- Exact: `zai/glm-5` → direct hit
- Alias: "GLM 5" → `zai/glm-5`; "doubao" → `volcengine-plan/doubao-seed-2.0-pro`
- Partial: "deepseek" → `volcengine-plan/deepseek-v3.2`

### Step 2: Abort if Not Found

If no match, **stop and report**:
- List all available models
- Ask user to pick one

Never guess or execute blindly.

### Step 3: Execute Switch

```bash
python3 scripts/model_switch.py <full-model-name> --retry 3
```

The script handles: backup → modify config → restart gateway → health check → auto-rollback on failure.

### Step 4: Expect Session Interruption

Gateway restart kills the current session. This is normal. The session resumes automatically after Gateway recovers.

## Constraints

1. Only modify `agents.defaults.model.primary` — never touch the provider list
2. Always validate model exists before switching
3. Backups stored in `~/.openclaw/config_backups/`
4. Script has full backup + rollback — config will never be lost
