## Description:

HumanLike Memory / Human-Like Memory is a persistent AI agent memory system for long-term memory search, recall, and save. It helps agents store facts, preferences, and decisions and keep context across sessions for conversation continuity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[humanlike2026](https://clawhub.ai/user/humanlike2026)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and OpenClaw users use this skill to let an agent explicitly recall, search, and save long-term memory when prior context, durable preferences, or confirmed decisions are useful. It is intended for smart-triggered memory workflows rather than every-turn background recall or saving.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send memory queries and saved conversation context to a configured remote Human-Like Memory service.

Mitigation: Install and use it only when remote memory storage is acceptable, and send only content intended for storage.

Risk: Saved content may include broad conversation context or tool data when capture is enabled.

Mitigation: Disable tool-call capture unless it is explicitly needed, avoid saving secrets or raw tool output, and review stored memories periodically.

Risk: Recalled memories may contain stale or untrusted historical context.

Mitigation: Treat recalled memory as context for review rather than as authoritative instructions.

## Reference(s):

- [Human-Like Memory homepage](https://plugin.human-like.me)
- [Human-Like Memory privacy policy](https://plugin.human-like.me/privacy)
- [ClawHub skill page](https://clawhub.ai/humanlike2026/skills/humanlike-memory)
- [ClawHub source listing](https://clawhub.ai/humanlike2026/humanlike-memory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include recalled memory summaries, save confirmations, configuration status, and error guidance.]

## Skill Version(s):

1.0.12 (source: ClawHub release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
