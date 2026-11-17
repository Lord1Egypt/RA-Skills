## Description:

Xata (xata.io). Use this skill for ANY Xata request — searching and reading data. Whenever a task involves Xata, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External developers use this skill to inspect Xata organizations, projects, branches, and available regions through their connected OOMOL account. It provides read-oriented CLI commands and returns the requested Xata data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup relies on a remote installer and hosted connector behavior that were not verified.

Mitigation: Review setup before installing, use a verified oo CLI version installed under your control, and confirm you accept OOMOL brokering the connection.

Risk: Broader agent changes and automatic skill synchronization are not fully disclosed.

Mitigation: Review the setup and CLI reference before use; set OO_SKILLS_SYNC_DISABLED=1 if you want to prevent automatic skill synchronization, and use a Xata key limited to the reads you need.

## Reference(s):

- [Xata API documentation](https://xata.io/docs/api-reference)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [Xata skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-xata)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON results and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-oriented Xata organization, project, branch, and region data.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
