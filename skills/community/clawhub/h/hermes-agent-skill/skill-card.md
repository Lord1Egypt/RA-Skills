## Description:

Hermes Agent Skill helps OpenClaw agents coordinate work through topic-based routing, session integration, opt-in memory search, and GEPA-style workflow summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[briefness](https://clawhub.ai/user/briefness)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to coordinate multiple OpenClaw subagents, distribute task events, track progress, search optional local memory, and summarize repeated successful workflows into reusable skill cards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared agent routing and session integration can expose sensitive task payloads, tags, metadata, or step results across agents.

Mitigation: Review before installing in mixed-trust environments, avoid secrets in task data, and use the skill only with agents and sessions that are intended to share this information.

Risk: When persistence is enabled, local ~/.hermes databases can retain sensitive memory and execution data.

Mitigation: Keep persistence disabled unless needed, leave sensitive filtering enabled, and treat the local databases as sensitive files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/briefness/skills/hermes-agent-skill)
- [Publisher Profile](https://clawhub.ai/user/briefness)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples and environment-variable configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local SQLite databases under ~/.hermes only when persistence is explicitly enabled.]

## Skill Version(s):

1.0.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
