# Lean Claude Code Harness

Distills the highest-value harness patterns from Claude Code-style runtimes into a small, auditable skill.

ClawHub:

- https://clawhub.ai/aznikline/lean-claude-code-harness

## What It Teaches

- how to keep a CLI harness thin
- how to make config precedence explicit
- how to gate tools before execution
- how to keep the tool surface small
- how to persist transcripts and keep the query loop inspectable

## What It Rejects by Default

- telemetry
- remote-managed settings
- hidden kill-switches
- private feature flags
- product-only branching logic

## Best Fit

Use this skill when an agent runtime is getting harder to explain than to run.
