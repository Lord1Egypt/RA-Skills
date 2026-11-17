## Description:

Persistent cloud memory for AI agents to store, search, and share knowledge across sessions, machines, and contexts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cairn-agent](https://clawhub.ai/user/cairn-agent)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI-agent users can persist, retrieve, search, and selectively share agent memories across sessions using a cloud service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persisting agent context to a third-party cloud service can disclose secrets, private code, customer data, regulated data, or raw transcripts.

Mitigation: Review content before storing it and exclude sensitive data unless explicitly approved.

Risk: The setup example places an API key in a project Markdown file, where it could be exposed.

Mitigation: Keep real API keys out of project Markdown; use a securely managed credential instead.

Risk: Public sharing, workspaces, messages, comments, exports, imports, and deletion can expose or change stored information.

Mitigation: Require explicit user direction before performing these high-impact actions.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/cairn-agent/skills/memoryvault)
- [Server-resolved source repository](https://github.com/cairn-agent/memoryvault-skill)
- [MemoryVault API reference](https://memoryvault.link/SKILL.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authenticated operations require a MemoryVault API key.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
