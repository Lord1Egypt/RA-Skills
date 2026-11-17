## Description:

Use the OOMOL-connected RevenueCat account to search and read customer, subscription, entitlement, offering, product, project, and revenue data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to inspect RevenueCat customer and subscription records, product configuration, entitlements, projects, and revenue metrics through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback CLI setup runs an unverified remote installer without a clear approval step.

Mitigation: Review and approve CLI setup separately, and verify the CLI release and downloaded runtime before installation.

Risk: The connected account can expose sensitive customer and revenue data.

Mitigation: Use a RevenueCat key limited to the projects and read permissions required for the task.

## Reference(s):

- [RevenueCat API v2 documentation](https://www.revenuecat.com/docs/api-v2)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [RevenueCat](https://www.revenuecat.com)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON]

**Output Format:** [Structured RevenueCat data returned as JSON and summarized in text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read results depend on the connected RevenueCat account and its permissions.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
