# Recovery Playbook

## Scope
Use this playbook when OpenClaw image understanding fails with symptoms like:
- `Unknown model`
- configured vision model exists in JSON but runtime does not recognize it
- image/OCR suddenly stops working across one or more agents

## Confirm the symptom first
Do runtime verification first:
1. Run `openclaw status`
2. Run an actual `image` tool call against a real local or inbound image
3. Treat runtime output as ground truth

Do not call it fixed if you only checked config files.

## Files to inspect
- `~/.openclaw/openclaw.json`
- `~/.openclaw/agents/<agent>/agent/models.json`

## Highest-probability root cause
A single invalid provider block inside agent-level `models.json` can cause the custom model registry to fail loading.

In the 2026-04-14 incident, the invalid block was a custom `codex` provider definition. Removing it restored image runtime registration.

## Minimal repair sequence
1. Back up the affected `models.json`
2. Remove only the invalid provider block
3. Restart gateway
4. Run a real image regression test
5. Notify affected agents

## Success criteria
All of these must be true:
- no `Unknown model`
- image tool returns a valid description or OCR result
- gateway healthy
- at least one real image regression passed

## Non-success criteria
These do not count as fixed:
- model exists in config
- service is running
- no real image tested
