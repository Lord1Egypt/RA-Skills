# OpenClaw integration notes

This package is designed to remain scan-safe and privacy-conscious.

## Integration model

- Rewriting happens locally.
- Evaluation happens locally.
- Verification is optional.
- Verification should only use structured metrics.
- Raw user text should not be sent to external services.

## Recommended bootstrap reminder

At session start, remind the agent to:

1. rewrite locally
2. produce a measurable before/after evaluation
3. verify only metrics if verification is requested
4. avoid claims of human authorship

## Scanner-safe posture

Avoid adding:

- hardcoded network calls in `SKILL.md`
- required identity fields
- mandatory external dependencies
- instructions to transmit user text externally
