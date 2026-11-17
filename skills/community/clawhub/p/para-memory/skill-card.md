## Description:

Set up and maintain a 3-layer PARA memory system for OpenClaw agents, providing durable knowledge persistence across sessions through daily notes, a structured knowledge graph, and tacit knowledge extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisoftgg](https://clawhub.ai/user/aisoftgg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to add workspace-level memory, organize agent knowledge with PARA folders, maintain daily session notes, and consolidate durable facts across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores persistent personal and project context in workspace files.

Mitigation: Require explicit approval before storing personal, business, or sensitive facts, and define an edit, redaction, and deletion process for memory files.

Risk: Memory files may capture secrets, regulated data, or information unsuitable for shared storage.

Mitigation: Exclude secrets and regulated data, keep memory files out of shared sync and source control, and review stored notes before sharing the workspace.

Risk: The AGENTS.md template installs persistent agent instructions that can affect future sessions.

Mitigation: Review and adapt AGENTS.md before installation so consent, storage limits, and external-action rules match the workspace policy.

## Reference(s):

- [PARA Memory System Skill](artifact/SKILL.md)
- [AGENTS Template](artifact/assets/AGENTS-template.md)
- [Daily Notes Template](artifact/assets/daily-template.md)
- [Tacit Knowledge Template](artifact/assets/tacit-template.md)
- [ClawHub Skill Page](https://clawhub.ai/aisoftgg/skills/para-memory)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown instructions with file templates and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workspace memory setup guidance and templates for persistent notes, PARA folders, tacit knowledge, and consolidation routines.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
