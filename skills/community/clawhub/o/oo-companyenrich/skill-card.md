## Description:

Search CompanyEnrich and retrieve company data through a connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business users use the skill to search CompanyEnrich and retrieve company profiles by domain or company properties, find similar companies, and check account capabilities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unreviewed software, and the remote installers' exact local effects were unavailable for inspection.

Mitigation: Review and install a fixed CLI release yourself before use.

Risk: Automatic skill synchronization may introduce broader agent changes without clear user control.

Mitigation: Review the synchronization behavior and decide whether to allow it.

Risk: CompanyEnrich requests pass through OOMOL and may consume credits.

Mitigation: Check account and credit usage before running actions when cost matters.

## Reference(s):

- [CompanyEnrich API documentation](https://docs.companyenrich.com/docs/getting-started)
- [CompanyEnrich homepage](https://companyenrich.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Text summaries and structured JSON company data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected account and the selected CompanyEnrich action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
