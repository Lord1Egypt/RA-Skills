## Description:

Use an OOMOL-connected account to search and read Anrok customer, product, filing, mapping, tax-category, and transaction data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and tax operations teams use this skill to retrieve customer, product, filing, product-mapping, tax-category, and transaction data from their connected Anrok account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions offer remote installer scripts whose contents and installation effects were unavailable for verification.

Mitigation: Review the CLI and installer separately, and require approval before running a fallback installer.

Risk: Connecting Anrok allows OOMOL to mediate access to sensitive business data.

Mitigation: Connect only the intended Anrok account and follow the organization’s controls for access to its business data.

## Reference(s):

- [Anrok API documentation](https://apidocs.anrok.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Text and structured JSON action results, with shell command examples in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only lookups; some list actions support cursor pagination.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
