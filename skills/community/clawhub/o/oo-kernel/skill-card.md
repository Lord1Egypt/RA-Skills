## Description:

Kernel (kernel.sh). Use this skill for ANY Kernel request — reading, creating, updating, and deleting data. Whenever a task involves Kernel, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to manage Kernel browser sessions through an OOMOL-connected account. It guides schema-first commands for listing, retrieving, creating, updating, and deleting sessions, with approval safeguards for changes and deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup runs downloaded CLI installer code, and may include installing additional agent skills; the downloaded installers were unavailable for inspection.

Mitigation: Review and approve the CLI installation separately before fallback setup, including any installation of additional agent skills.

## Reference(s):

- [Kernel homepage](https://kernel.sh)
- [Kernel API documentation](https://www.kernel.sh/docs/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses each action's live schema to shape JSON payloads; write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
