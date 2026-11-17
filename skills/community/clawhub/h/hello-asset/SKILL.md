---
name: hello-asset
description: A practical demonstration skill showing how to greet users with a customizable message. Useful for testing the skill publishing pipeline and as a template for new skill authors.
metadata: { "clawdbot": { "emoji": "👋" } }
---

# Hello Asset

Hello Asset is a minimal but functional skill that returns a friendly greeting. It serves two purposes:

1. **Pipeline demo** — proves the end-to-end flow from workspace authoring to ClawHub publishing.
2. **Template** — a clean starting point for new skill authors who want a working reference.

## When to Use

- You want to verify your ClawHub publishing pipeline works end-to-end.
- You need a lightweight template for a new skill.
- You're testing that skill installation and invocation function correctly.

## Usage

1. Load the skill: `hello-asset`
2. Invoke it — it returns a greeting message.
3. Optionally pass a name for a personalized greeting.

## Steps

1. **Load** — the agent reads SKILL.md and understands the skill's purpose.
2. **Invoke** — call the skill with an optional name parameter.
3. **Respond** — the skill returns a greeting string.

## Example

```
User: hello-asset Alice
Agent: Hello, Alice! 👋 Thanks for checking out Hello Asset — a demo skill showcasing the full author-to-publish pipeline on ClawHub.
```

## Metadata Notes

- **Version**: 1.0.0
- **Author**: terrycarter1985
- **License**: MIT
