## Description:

Search German commercial-register organizations and retrieve company profiles through Handelsregister AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business users can search German commercial-register organizations and retrieve company profiles, with optional paid enrichment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may execute an unverified downloaded installer and add skills for other agents.

Mitigation: Review and pin the CLI installation, require approval before executing downloaded installers, and set OO_SKILLS_SYNC_DISABLED=1 for CLI invocations.

Risk: Enrichment requests may incur charges.

Mitigation: Check whether enrichment is needed and review applicable OOMOL and provider billing before requesting it.

## Reference(s):

- [Handelsregister AI](https://handelsregister.ai)
- [Handelsregister AI API documentation](https://handelsregister.ai/en/documentation)

## Skill Output:

**Output Type(s):** [Structured data, Company information]

**Output Format:** [JSON search results and company profile details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available results depend on the search criteria and source data; enrichment may incur charges.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
