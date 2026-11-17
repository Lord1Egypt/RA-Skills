## Description:

Privacy-first, self-hosted chat memory for OpenClaw - save and recall conversation history across sessions without any cloud dependency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ukkit](https://clawhub.ai/user/ukkit)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use Memcord to add self-hosted persistent memory to conversations, including saving meaningful session context and recalling it later.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chat history may be persisted locally in plaintext and recalled automatically in later sessions.

Mitigation: Use the skill only with clear consent, avoid saving sensitive conversations, and confirm where memory files are stored and how they can be deleted.

Risk: The configured uvx command runs an unpinned external memcord package that was not included in the artifact for review.

Mitigation: Prefer an exact pinned package version and verify the package source before installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ukkit/skills/memcord)
- [Publisher Profile](https://clawhub.ai/user/ukkit)

## Skill Output:

**Output Type(s):** [markdown, configuration, guidance, shell commands]

**Output Format:** [Markdown with JSON5 configuration examples and tool-use guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides installation of the memcord MCP server through uvx and documents the memcord_auto_save and memcord_read tools.]

## Skill Version(s):

4.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
