# OpenClaw Platform Notes

## Skill location

- User-wide: `~/.openclaw/skills/openclaw-deep-research/`
- Workspace-local: `skills/openclaw-deep-research/`

## Recommended usage

- Treat the skill as an AgentSkills-compatible workflow package.
- Write the research artifacts into the active workspace, not into the skill folder.
- Keep one canonical project directory even if OpenClaw loads the skill from a different location.

## Delegation guidance

- Use subagents only if the current OpenClaw installation exposes them.
- If OpenClaw is running in a simpler single-agent setup, keep the PM workflow local and use ledgers plus handoffs as the resume mechanism.

## Practical adjustment from the base skill

- The wording explicitly avoids assuming Codex-style orchestration.
- The file-backed workflow and evidence discipline remain unchanged.
