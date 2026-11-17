## Description:

Persistent memory system for AI agents: daily logs, long-term memory, identity files, and heartbeat-driven recall.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdssen](https://clawhub.ai/user/clawdssen)

### License/Terms of Use:

CC-BY-NC-4.0

## Use Case:

Developers and operators use this skill to install and maintain a local persistent memory system for an AI agent, including identity, operator profile, long-term memory, daily notes, heartbeat state, and session startup files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory files may capture personal or sensitive context and later be loaded into future sessions.

Mitigation: Install only in a private workspace where persistent personal memory is appropriate, and avoid storing secrets, regulated data, or anything unsuitable for future sessions.

Risk: The installed instructions may cause future agents to read and update personal memory files automatically with incomplete privacy and control boundaries.

Mitigation: Before use, review AGENTS.md and HEARTBEAT.md, narrow automatic read or update rules, and require confirmation before writing long-term memory or changing USER.md or SOUL.md.

## Reference(s):

- [Memory OS Blueprint](references/blueprint.yaml)
- [Memory OS Guide](references/guide.md)
- [Memory OS on ClawHub](https://clawhub.ai/clawdssen/skills/memory-os)
- [The Agent Ledger](https://theagentledger.com)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Guidance, Files]

**Output Format:** [Markdown files, JSON state, and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local workspace memory files after user confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
