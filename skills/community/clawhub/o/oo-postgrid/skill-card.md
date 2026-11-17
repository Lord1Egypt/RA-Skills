## Description:

Use this skill to read, create, update, and delete PostGrid contacts and templates through the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use the skill to inspect PostGrid action schemas and manage contacts and templates through their connected PostGrid account. Writes require user confirmation, and deletions require explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses remote installer code, and the CLI can install or synchronize agent skills; remote installers and hosted credential handling have not been independently verified.

Mitigation: Review the installer and its effects before setup, use a reviewed version-pinned installation, and set OO_SKILLS_SYNC_DISABLED=1 to prevent startup skill synchronization.

Risk: PostGrid write and deletion actions can change or remove account data.

Mitigation: Confirm the exact payload and effect before writes, and get explicit approval for the target of every deletion.

## Reference(s):

- [PostGrid API documentation](https://postgrid.readme.io/)
- [PostGrid homepage](https://www.postgrid.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference (environment variables)](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions return PostGrid data through the oo CLI; write and destructive actions require user approval.]

## Skill Version(s):

1.0.5 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
