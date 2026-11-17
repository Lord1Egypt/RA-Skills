---
name: hello-clawhub-demo
description: A minimal but complete demo skill that greets the user and prints the current UTC timestamp. Useful for verifying the ClawHub publish/install pipeline end to end.
metadata: { "openclaw": { "emoji": "👋", "category": "demo" } }
---

# Hello ClawHub Demo

A tiny skill that prints a greeting and the current UTC timestamp. It exists to
demonstrate the full TaskFlow + ClawHub publish pipeline: validate the skill
folder, publish it to the ClawHub registry, and verify it can be installed
back from the registry.

## When to use

- Demonstrating the ClawHub publish flow from a local skill folder.
- Verifying a skill folder is valid and ingestible by the registry.
- Smoke-testing that `clawhub publish` and `clawhub install` round-trip works.

## Steps

```bash
echo "Hello from hello-clawhub-demo @ $(date -u +%FT%TZ)"
```

## Expected output

A single line containing the greeting and an ISO-8601 UTC timestamp, e.g.:

```
Hello from hello-clawhub-demo @ 2026-08-21T00:00:00Z
```

## Notes

- No external dependencies or API keys are required.
- The skill folder must contain at least this `SKILL.md` file.
