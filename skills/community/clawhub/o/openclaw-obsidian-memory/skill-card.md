## Description:

OpenClaw Obsidian Memory helps an agent set up an Obsidian Vault-backed persistent memory system with Vault-first search, local memory fallback, note templates, backlink checks, and optional scheduled archive workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[masterxiaogu](https://clawhub.ai/user/masterxiaogu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure an Obsidian-backed local knowledge base for persistent memory retrieval, structured note creation, and archive maintenance. It is intended for users who deliberately want agent-level memory behavior rather than simple note search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can introduce an agent-level persistent memory system that consolidates sensitive local context and conversation summaries.

Mitigation: Install it only when persistent memory is desired, avoid storing secrets or private conversations in the Vault, and review proposed memory content before writing.

Risk: The skill proposes changes to AGENTS.md and MEMORY.md that may alter future agent behavior.

Mitigation: Review and approve any proposed AGENTS.md or MEMORY.md changes before applying them.

Risk: Optional daily and weekly cron jobs can archive information repeatedly with limited user oversight.

Mitigation: Skip scheduled jobs unless retention, review, and removal procedures are defined, and require confirmation before recurring writes or archives.

## Reference(s):

- [Note Templates](references/templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and generated note templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes proposed Vault directory layout, AGENTS.md and MEMORY.md memory-rule content, Node.js utility scripts, and optional cron command guidance.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
