## Description:

Operate Invoice Ninja to read and manage clients, invoices, and payments through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to look up Invoice Ninja clients, invoices, and payments and to create or update those records in an account connected through OOMOL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI setup may run unverified downloaded code, and cross-agent skill synchronization may make persistent changes to other agents’ skills.

Mitigation: Review and install a specific CLI version before use, disable cross-agent skill synchronization with the vendor-documented OO_SKILLS_SYNC_DISABLED setting, and confirm each financial change.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Invoice Ninja API documentation](https://invoiceninja.github.io/docs/api-reference/invoice-ninja-api-reference)
- [Invoice Ninja](https://invoiceninja.com)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can return Invoice Ninja data as JSON.]

## Skill Version(s):

1.0.5 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
