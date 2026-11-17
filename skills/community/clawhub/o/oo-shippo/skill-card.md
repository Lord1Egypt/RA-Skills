## Description:

Operate Shippo to retrieve tracking information, manage addresses and parcels, and validate address records through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Shippo account users and agents use this skill to retrieve tracking status, manage address and parcel records, and validate addresses through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The first-time setup fallback downloads and runs installer code that has not been independently verified, and the setup instructions do not require explicit approval before execution.

Mitigation: Review the installer and first-run skill changes before setup; use a pinned, independently verified installation where possible.

Risk: Using the connected Shippo account sends account data through OOMOL, and account-changing actions can alter Shippo records.

Mitigation: Keep confirmation enabled for account changes and confirm the exact payload and effect before running write actions.

## Reference(s):

- [Shippo API reference](https://docs.goshippo.com/api-reference/overview)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Shippo](https://goshippo.com)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions may run directly; address and parcel creation require user confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
