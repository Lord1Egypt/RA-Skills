# Changelog

## 4.1.0 (2026-11-05)

The version is above every earlier release (including the old 4.0.x) so that ClawHub treats this as the latest.

**What changed**
- Updated to the current model lineup. `GET /v1/models` is the live list, with `supports_tools` for each model. Retired IDs map to current models (`X-Model-Remapped`).
- Tool / function calling works on `/v1/messages` and `/v1/chat/completions`, with streaming.
- Billing: requests are quoted from the actual prompt size, spend tokens get back what usage didn't need, failed or empty calls are never charged, and top-ups last 30 days.

**Safety**
- New "What this skill sends and costs" section, a confirm-cost rule, no autonomous loops, and model output and tool results treated as data.

**Metadata**
- `LIGHTNINGPROX_SPEND_TOKEN` is now optional, because L402 works without it. It is declared under `metadata.openclaw.envVars`.

**Removed**
- The `lightningprox-openai` npm wrapper section: that wrapper drops `tools`. The skill now points to the official OpenAI SDK with `base_url`.
- Hardcoded model counts.
