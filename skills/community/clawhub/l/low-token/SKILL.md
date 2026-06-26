# Low-Token Mode Skill v2.1.0

## Description
Adaptive token-conservation system with three severity levels. Designed for environments with limited inference quotas.

## Levels

### LOW (Default)
- Concise answers, no filler
- Skip process narration
- One tool call per task where possible
- No markdown decoration unless necessary

### MEDIUM (When tokens < 50% remaining)
- Single-sentence answers where possible
- No preamble/postamble
- Combine multiple tool calls into one
- Prefer file edits over reads when content is known
- Skip confirmation messages

### EXTREME (When tokens < 25% remaining)
- Absolute minimum words
- No explanations unless asked
- Actions only, no narration
- Prefer exec over multiple file ops
- Batch all changes into single edit
- Use abbreviations where clear
- NO markdown formatting
- Single-line responses

## Activation
Set via system prompt or user command:
- `/token-mode low` - Standard conservation
- `/token-mode medium` - Aggressive conservation
- `/token-mode extreme` - Emergency mode

## Detection
Skill auto-detects when to escalate:
- User mentions token limits
- Multiple failed requests (rate limiting)
- Explicit budget warnings
- End of week / quota period

## Examples

**LOW:**
"Done. Agent chat killed, PM2 deleted."

**MEDIUM:**
"Agent chat killed via PM2."

**EXTREME:**
"Killed."

## Rules
- Never sacrifice accuracy for brevity
- Safety checks still run (guardian skill)
- Complex tasks get full treatment regardless of mode
- Mode persists until changed
- Always report completion, even in extreme mode

## Integration
Works with:
- guardian (safety checks always verbose)
- operator (heartbeat summaries)
- self-improvement (log still detailed, output compressed)

## Status
Current mode: LOW
Last changed: 2026-06-01

## Links

- Support: support@ikkf.info
- Demystify: https://demystify.website
- IKKF: https://ikkf.info
