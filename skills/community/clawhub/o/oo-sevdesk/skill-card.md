## Description:

Use this skill to read, create, update, or delete sevdesk data through the connected sevdesk account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People working with sevdesk use this skill to list and retrieve contacts, or create, update, and delete them through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses a remote CLI installer, and synchronization may affect broader agent skills.

Mitigation: Review and pin a verified CLI before installation; review the CLI command reference and decide whether to opt out of synchronization.

Risk: Creating, updating, or deleting contacts changes sevdesk data.

Mitigation: Connect only the intended sevdesk account, verify the target and exact change, and retain user approval before execution.

## Reference(s):

- [sevdesk](https://sevdesk.com)
- [sevdesk API documentation](https://api.sevdesk.de/)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured JSON results and concise natural-language responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Contact changes and deletions require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
