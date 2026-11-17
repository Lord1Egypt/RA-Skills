## Description:

Search and read Printavo account, contact, customer, order, and task data through the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve Printavo account information and business records, including contacts, customers, quotes, invoices, and tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may execute unverified software or introduce broader changes to an agent's skills.

Mitigation: Install a verified version and consider disabling broader skill synchronization with OO_SKILLS_SYNC_DISABLED=1.

Risk: Printavo business data may be processed by OOMOL.

Mitigation: Confirm that OOMOL is an approved processor for the data before connecting Printavo.

## Reference(s):

- [Printavo API documentation](https://www.printavo.com/docs/api/v2)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands]

**Output Format:** [JSON connector responses, shell commands, and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Printavo account and business data]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
