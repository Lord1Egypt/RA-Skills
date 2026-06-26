---
name: model-registry-manager
description: "Detect provider models, deduplicate them, remove unusable ones, register missing models into OpenClaw, and safely keep provider-native model ids/names during model catalog sync."
version: 1.3.0
---

# Model Registry Manager

Use this skill when managing OpenClaw model catalogs and provider model sync for any provider.

## What this skill covers
- Fetch provider model lists from the upstream `/models` endpoint
- Deduplicate returned models by provider-native model id
- Probe models and remove unusable ones from the registered catalog
- Register newly discovered usable models into OpenClaw config
- Keep provider-native ids and names instead of inventing renamed keys
- Validate the registry before enabling scheduled sync jobs

## Required workflow

### 1. Inspect config/schema first
Before changing config, inspect relevant config paths and read current config.

Usually inspect:
- `agents.defaults.model`
- `agents.defaults.models`
- `models.providers`

### 2. Detect before writing
Always fetch remote models first and compare with current config.
Do not write first when the state is unknown.

### 3. Keep provider-native ids/names
- Use the provider-returned model `id` as the canonical registry id suffix
- Use the provider-returned model `name` when available
- Do not normalize ids into a different slug format unless OpenClaw requires it

### 4. Validate before keeping
A model is only eligible for registration if it passes a lightweight probe.
If probing fails, treat it as unusable and exclude it from the registered catalog.

### 5. Do not auto-select primary/fallbacks
This skill should not automatically choose or rebuild primary/fallback chains.
During sync:
- keep provider model discovery, deduplication, probing, and registration focused on the catalog itself
- do not introduce heuristic primary selection here
- do not introduce heuristic fallback selection here
- if model routing policy is needed, manage it outside this skill

### 6. Do not bundle generic failover policy here
This skill should not define generic failover classes, retry ladders, downgrade policy, or circuit-breaker defaults.
Keep this skill focused on model registry sync and validation.

### 7. Schedule only after one clean run
First complete:
- one successful sync run
- one successful validation run
- one confirmation that primary/fallback settings are correct

Then you may add scheduled refresh jobs.

### 8. Default closing step: maintain the learnings archive
After finishing real work, check whether the run produced reusable operational knowledge.
Default behavior:
- if the user corrected you, add the correction to `.learnings/`
- if you debugged a failure, add the cause/fix to `.learnings/`
- if you found a better generic strategy, add it to `.learnings/`
- if you needed multiple attempts and eventually found a reliable path, add that successful path to `.learnings/`
- do not wait for the user to remind you

This is part of the skill’s normal operating procedure, not an optional extra.

## Validation checklist
- fetched remote model list successfully
- deduplicated duplicate remote ids
- excluded unusable models
- registered usable models
- gateway/service still healthy after config update

## How to make this skill truly general-purpose
To keep this skill generic instead of overfitting to one provider/model family:

### Keep generic
- provider-native ids and names
- provider model discovery and probe validation
- per-provider sync + global catalog merge

### Avoid hardcoding
- exact vendor model ids as permanent rules
- one provider’s naming quirks as universal truth
- one-off emergency fixes in the main sync algorithm
- model routing policy into registry sync

### Prefer this structure
- `SKILL.md`: only workflow + decision rules
- `scripts/`: deterministic sync/validate logic

## Scheduling policy for this workspace
After installation is validated, schedule these triggers:
- startup/heartbeat safety net
- recurring sync every 6 hours

Keep scheduled runs idempotent and safe to repeat.

## Setup
In an OpenClaw agent session, prefer the built-in `cron` tool instead of shelling out to `openclaw cron ...`.

After one clean validation run, ensure these recurring jobs exist (create missing ones, update same-name jobs if they already exist):
- `model-registry-manager validation safety-net`
- `model-registry-manager recurring sync`

Recommended default schedules (Asia/Shanghai):
- validation safety-net: `10 4 * * *`
- recurring sync: `40 */6 * * *`

Recommended job shape:
- `sessionTarget: "isolated"`
- `payload.kind: "agentTurn"`
- `payload.toolsAllow: ["exec", "read"]`
- `delivery.mode: "none"`
- failure alert enabled after 1 failure

Recommended task behavior:
- validation job runs `node skills/model-registry-manager/scripts/validate-model-sync.js`
- recurring sync runs `node skills/model-registry-manager/scripts/sync-models.js all 0 --restart`
- each job should read the latest report under `reports/model-registry/` and produce a concise summary

Do not enable recurring sync before a clean validation run.
