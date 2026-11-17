## Description:

Organizes OpenClaw's persistent memory into a concise routing table, topic and contact files, and optional chronological summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richgoodson](https://clawhub.ai/user/richgoodson)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to keep long-running agent memory organized across projects and contacts, distill daily notes, and optionally create periodic summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory files may retain secrets or sensitive personal information.

Mitigation: Keep passwords, API keys, secrets, and sensitive personal data out of MEMORY.md and memory files.

Risk: The full preset can create recurring synthesis jobs and additional archive files.

Mitigation: Review the full preset before enabling it, and approve scheduled jobs and file changes only when needed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/richgoodson/skills/hierarchical-agent-memory)
- [Configuration reference](references/configuration.md)
- [Onboarding guide](references/onboarding-guide.md)
- [Migration guide](references/migration-v2-to-v3.md)

## Skill Output:

**Output Type(s):** [Markdown memory files, Configuration guidance, Status reports]

**Output Format:** [Markdown and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Memory changes require user approval; the optional full preset can produce scheduled archive summaries.]

## Skill Version(s):

3.2.0 (source: skill metadata and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
