# Publish Notes

## Suggested publish summary

Structured root-cause debugging for commands, tools, automations, and unclear failures.

## Suggested changelog

Initial OpenClaw-adapted release.

## Example publish command

```bash
clawhub publish ./skills/systematic-debugging \
  --slug systematic-debugging \
  --name "Systematic Debugging" \
  --version 0.1.0 \
  --changelog "Initial OpenClaw-adapted release."
```

## Final review checklist

- description is concise and triggerable
- body is practical, not theoretical only
- examples match real OpenClaw usage
- no unsupported platform-specific assumptions
