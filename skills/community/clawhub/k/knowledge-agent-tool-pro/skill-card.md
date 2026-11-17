## Description:

Provides enterprise knowledge management workflows for shared team knowledge bases, semantic search, automatic summaries, knowledge graph creation, permissions, audit logs, and monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, knowledge workers, and team administrators use this skill to manage team knowledge bases, search and summarize stored material, build knowledge graphs, and manage permissions and audit workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose command execution and file operations against private or shared knowledge-base storage.

Mitigation: Review sync, permission, invite, export, and filesystem commands before allowing execution, especially in environments with private documents or shared team data.

Risk: Callbacks, cloud embedding services, or API-backed semantic workflows can expose private documents or metadata if misconfigured.

Mitigation: Use callback_url only with trusted endpoints and keep embedding or API credentials in environment variables or a secret store.

Risk: Broad knowledge-management workflows may alter permissions, shared storage, or exported knowledge assets.

Mitigation: Install only for intended knowledge-base workflows and confirm the know CLI, shared paths, and permission model before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/knowledge-agent-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose file reads, file writes, CLI execution, exports, and team sync workflows; review commands before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
