## Description:

Use the OOMOL-connected Nyne.ai account to read, create, and update data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search and enrich people and companies, check usage, and retrieve results through a connected Nyne.ai account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI can automatically change skills across other agents, an effect this skill does not explain.

Mitigation: Review the CLI's cross-agent skill changes before setup; if unwanted, set OO_SKILLS_SYNC_DISABLED=1 before CLI execution and use a separately reviewed installation. Confirm submitted identifiers, searches, and billable effects.

Risk: The remote installer and hosted implementation remain unverified.

Mitigation: Review and verify the installation and hosted implementation before relying on them.

## Reference(s):

- [Nyne.ai](https://nyne.ai)
- [Nyne.ai API documentation](https://api.nyne.ai/documentation/authentication)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown instructions with shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes read operations and user-confirmed write actions.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
