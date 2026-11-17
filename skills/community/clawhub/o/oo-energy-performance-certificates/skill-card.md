## Description:

Searches and retrieves UK Energy Performance Certificate records through the connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users can search domestic, non-domestic, and public-building certificates, or retrieve a certificate by number, through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup executes downloaded code whose contents and exact installed-release behavior are unverified, without a clear approval step.

Mitigation: Review setup first; prefer an independently verified, version-pinned CLI installation and explicitly approve its system changes.

Risk: Certificate requests pass through OOMOL.

Mitigation: Consider whether the request details are appropriate to send through OOMOL before using the skill.

## Reference(s):

- [Energy Performance Certificates service](https://get-energy-performance-data.communities.gov.uk)
- [API technical documentation](https://get-energy-performance-data.communities.gov.uk/api-technical-documentation)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://raw.githubusercontent.com/oomol-lab/oo-cli/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [API data, JSON, Text]

**Output Format:** [JSON certificate records with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns certificate search results or details for the requested action.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
