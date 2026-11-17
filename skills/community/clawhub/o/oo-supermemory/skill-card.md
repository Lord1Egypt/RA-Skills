## Description:

Connects an agent to Supermemory through OOMOL for reading, adding, updating, and deleting memory data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to search and read Supermemory context, add documents or memories, and update or remove stored data through their OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback runs downloaded installation code, and the installers' local changes were unavailable for inspection.

Mitigation: Review the CLI and installer behavior, including whether it installs other agent skills, and require approval before installation.

Risk: Actions can add or modify memories and documents, or permanently delete a document.

Mitigation: Keep user confirmation for write and destructive actions, including the exact target and payload.

Risk: Supermemory requests pass through OOMOL.

Mitigation: Use the connected account with awareness that requests are routed through OOMOL.

## Reference(s):

- [Supermemory API documentation](https://supermemory.ai/docs/api-reference/overview)
- [Supermemory](https://supermemory.ai)
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action payloads follow the live connector schema.]

## Skill Version(s):

1.0.5 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
