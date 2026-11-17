## Description:

Provides persistent, searchable, context-aware memory storage for AI agents to retain user preferences, corrections, procedures, and project context across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vedantsingh60](https://clawhub.ai/user/vedantsingh60)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to store, search, update, import, export, and inject local memory context into AI prompts so recurring preferences, corrections, and project procedures can persist across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memories may contain sensitive information that is persisted, exported, or re-injected into prompts.

Mitigation: Use the skill only for non-secret memories, keep .persistentmind and export files out of source control and shared folders, and review generated context before prompt use.

Risk: Imported memory files can introduce untrusted or misleading context.

Mitigation: Import memory files only from trusted sources and inspect their contents before allowing them to influence agent behavior.

Risk: Memory from different projects may be mixed when the same storage path is reused.

Mitigation: Use separate storage paths for projects or workspaces where confidentiality boundaries matter.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vedantsingh60/skills/persisent-mind)
- [Publisher Profile](https://clawhub.ai/user/vedantsingh60)
- [README](artifact/README.md)
- [Skill Documentation](artifact/SKILL.md)
- [MIT License](artifact/LICENSE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown context blocks, Python code snippets, and JSON memory or export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores memory locally by default in .persistentmind/ and does not require external API credentials.]

## Skill Version(s):

1.0.0 (source: release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
