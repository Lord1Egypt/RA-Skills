# Architecture Notes

## Why this package is script-assisted

OpenClaw skills are text-first and are loaded from bundled, managed, or workspace directories. They are centered on `SKILL.md`, but real-world model routing and sub-agent override behavior can vary by provider and release.

That means pure prompt-only logic is not enough for strong availability. This package therefore separates:

- **policy** in the skill text and YAML configs
- **state** in `.imperial_state.json`
- **routing logic** in Python scripts

## Availability model

### Role layer
- router-chief
- cabinet-planner
- specialist departments
- review
- emergency-scribe

### Health layer
- model health
- provider health
- auth-group health

### Degrade policy
When healthy auth groups collapse, switch to a local or most-stable model and reduce task ambition while preserving continuity.
