## Description:

Search and read Klipfolio data and assets through the user's OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Klipfolio can ask an agent to find and retrieve clients, dashboards, data sources, and Klips available to their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may run remote CLI installers whose effects have not been verified.

Mitigation: Review and approve CLI setup separately, verify the installer, use a Klipfolio connection limited to needed reads, and consider disabling CLI skill synchronization.

## Reference(s):

- [Klipfolio API documentation](https://apidocs.klipfolio.com/reference)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Klipfolio](https://www.klipfolio.com)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [Klipfolio asset data as JSON, with concise text summaries when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are limited to assets visible to the connected account.]

## Skill Version(s):

1.0.4 (source: artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
