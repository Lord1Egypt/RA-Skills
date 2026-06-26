---
name: hudl-model-switch
description: Switch between LLM models on the Huddle01 GRU gateway. Use this skill whenever the user mentions switching models, changing models, upgrading, downgrading, "switch to opus", "use minimax", "use claude", "use the smart model", "use the cheap model", "change model", "swap model", or any variation of wanting a different LLM. Also trigger when the user asks "what model am I on", "which model", or "current model". This skill ONLY works with the hudl provider backed by gru.huddle01.io.
---

# hudl-model-switch

Switch the active LLM model for this OpenClaw agent via the Huddle01 GRU gateway.

## Non-negotiable rules

- This skill only applies to the `hudl` provider backed by `gru.huddle01.io`.
- The target model value in config must always be `hudl/<model-id>`.
- Never edit JSON manually for model switching. Always use `scripts/switch-model.sh`.
- Never modify provider wiring during a switch (`models.providers.hudl.baseUrl`, `apiKey`, and other unrelated keys stay unchanged).
- Treat any post-switch mismatch, missing model field, or non-`hudl/` result as a hard failure. Do not restart in that state.
- For status/reporting, the active agent model is the source of truth. `agents.defaults.model.primary` is only a default and may be stale.

## Prerequisites

This skill **only works** when the OpenClaw config has a `hudl` provider pointing at `gru.huddle01.io`. If the provider is missing or the baseUrl is different, **stop and tell the user** this skill requires the Huddle01 GRU gateway.

## Step-by-step

### On any switch/change request

**Step 1: Validate provider + config path (required)**

Run:

```bash
bash <skill_dir>/scripts/validate.sh
```

- Exit `0`: continue.
- Exit `1`: stop. Show the exact validation error and tell the user no config changes were made.
- Validation resolves config in this order: `OPENCLAW_CONFIG`, `~/.openclaw/config.json`, `~/.openclaw/openclaw.json`.
- The provider check is strict: the `hudl` provider must exist, `apiKey` must be present, and `baseUrl` must point at host `gru.huddle01.io`.

**Step 2: Resolve the exact target model ID (required)**

Use `<skill_dir>/references/models.md` to map user intent to a canonical model.

Normalization rules:
- If the resolved model does not start with `hudl/`, prepend `hudl/`.
- If the user already supplied `hudl/...`, keep it unchanged.
- Never write a non-`hudl/` model into config.
- Reject empty model IDs, `hudl/` by itself, or values with spaces.
- For unknown models, still normalize to `hudl/<user-value>` and warn clearly that the model must exist on GRU or requests will fail.

Ambiguity rules:
- If request is ambiguous (for example "claude" could be Opus/Sonnet/Haiku), choose the catalog default alias mapping (currently `hudl/claude-opus-4.6`) and state what was chosen.
- If the user asks for a specific variant, obey that exact variant.

**Step 3: Capture current state before mutation (required)**

Read and note current values so the response can show before/after:
- active agent model (`agents.list[*].model.primary`, preferring agent `id: "main"`)
- default model (`agents.defaults.model.primary`)
- If `.agents.list` has no entries, stop. This skill is for switching an active agent model, so a config with no agent entries is not a valid target.
- When active and default differ, describe that as a mismatch and treat the active agent model as the model currently in use.

**Step 4: Switch model via script (required)**

Run:

```bash
bash <skill_dir>/scripts/switch-model.sh <hudl-model-id>
```

`switch-model.sh` is the source of truth and must be used instead of manual edits.

Expected behavior from script:
- Updates `agents.defaults.model.primary`
- Updates active agent model (`agents.list[*].model.primary`, preferring `id: "main"`, otherwise first agent)
- Normalizes `models.providers.hudl.models[*].id` so every catalog ID is `hudl/...`
- Ensures the target model exists in `models.providers.hudl.models`
- Preserves unrelated configuration
- Fails if the resulting active/default model fields are empty, not `hudl/`-prefixed, or do not exactly match the requested target
- Fails if the provider model catalog still contains non-`hudl/` IDs or is missing the target model

Failure handling:
- If script fails, stop and show the script error.
- Do not "repair" the config manually inside the skill. If the script does not leave config in a valid final state, stop and surface the failure.

**Step 5: Verify post-switch values before restart (required)**

Confirm both fields now point to the normalized target model and both are `hudl/...`.

- If aligned: continue.
- If not aligned: report mismatch and stop. Do not restart.

**Step 6: Restart + report final state (required)**

Before restart, tell the user:
- restart is starting now
- service may take a couple of minutes to come back
- you will confirm applied model values after restart

Run:

```bash
openclaw restart
```

After restart, report:
- restart completion status
- previous active/default model values
- new active/default model values
- alignment status (aligned or mismatch)
- exact final model ID in use
- provider catalog normalization status

### On "what model am I on" / "current model"

1. Run validation (`scripts/validate.sh`).
2. Read the resolved config (`config.json` or `openclaw.json`).
3. Report:
   - current active agent model (`agents.list[*].model.primary`, prefer `id: "main"`)
   - current default model (`agents.defaults.model.primary`)
   - whether they are aligned
   - whether each value is correctly `hudl/`-prefixed
   - config path used for the check

Reporting rules:
- Do not say "current model is X" based only on `agents.defaults.model.primary`.
- If `agents.list[*].model.primary` and `agents.defaults.model.primary` differ, say the active agent model is currently in use and the default is stale/misaligned.
- When the user asks to "show on file" or "prove it from config", show both paths and values:
  - `agents.list[main-or-first].model.primary`
  - `agents.defaults.model.primary`

No restart is needed for read-only status checks.

## Example exchanges

**Switch to Opus:**
```
User: switch to opus
Agent: Checking GRU gateway config... verified.
Agent: Resolved target model: hudl/claude-opus-4.6.
Agent: Current models -> active: hudl/minimax-m2.5, default: hudl/minimax-m2.5.
Agent: Running switch script... success.
Agent: Provider model catalog normalized and includes hudl/claude-opus-4.6.
Agent: Restarting gateway now; it may take a couple minutes.
Agent: Restart complete. Active: hudl/claude-opus-4.6, default: hudl/claude-opus-4.6 (aligned).
```

**Mismatched config on status check:**
```
User: what model am I on?
Agent: Config path: /home/ubuntu/.openclaw/openclaw.json
Agent: Active model in use: hudl/minimax-m2.5 (from agents.list[id=main].model.primary)
Agent: Default model: gpt-4.1 (from agents.defaults.model.primary)
Agent: Status: mismatch. The gateway is currently using hudl/minimax-m2.5; the default value is stale and should not be reported as the live model.
```

**No hudl provider:**
```
User: switch to opus
Agent: (validate.sh failed)
Agent: This skill requires the Huddle01 GRU gateway (hudl provider with baseUrl gru.huddle01.io) in your OpenClaw config. No changes were made.
```

**Unknown model:**
```
User: switch to deepseek-r2
Agent: Heads up: deepseek-r2 is not in the known catalog. I will set hudl/deepseek-r2; requests will fail unless that model exists on your GRU gateway.
Agent: Switching to hudl/deepseek-r2...
```
