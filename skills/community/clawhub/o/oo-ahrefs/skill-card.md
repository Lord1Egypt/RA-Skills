## Description:

Use Ahrefs through an OOMOL-connected account to retrieve keyword, site, country, and subscription usage data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to retrieve Ahrefs keyword overviews, site metrics, country-level metrics, and subscription usage through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute downloaded code that was unavailable for inspection.

Mitigation: Review setup instructions, install a verified oo CLI release yourself, and require approval for later installations.

Risk: Automatic skill synchronization can change other agent skills; using the connector also shares Ahrefs account access and queries with OOMOL.

Mitigation: Disable automatic skill synchronization if you do not want other skills changed, and use the connector only if you trust OOMOL with the connected account and queries.

## Reference(s):

- [Ahrefs](https://ahrefs.com/)
- [Ahrefs API documentation](https://docs.ahrefs.com/en/api/docs/introduction)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-ahrefs)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON connector results with concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only keyword, site, country, and subscription usage results.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
