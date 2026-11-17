## Description:

Use a connected OOMOL Xero account to read, create, and update Xero data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People managing a connected Xero account can retrieve accounting information, create contacts or draft invoices, and update invoice status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup downloads and runs an installer whose complete local effects were not inspected.

Mitigation: Review and install a fixed CLI release yourself before using the skill.

Risk: Automatic synchronization could introduce broader changes to installed agent skills.

Mitigation: Consider disabling automatic skill synchronization.

Risk: Write actions can change accounting data in the connected Xero account.

Mitigation: Connect only the intended Xero account and retain confirmation for every accounting change.

## Reference(s):

- [Xero Accounting API documentation](https://developer.xero.com/documentation/api/accounting/overview)
- [Xero](https://www.xero.com)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, API responses, Accounting data]

**Output Format:** [Shell commands with JSON responses and accounting data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write actions require user confirmation before execution.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
