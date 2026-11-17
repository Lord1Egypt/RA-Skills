## Description:

Retrieves current air-quality and weather data and lists supported IQAir AirVisual locations through the OOMOL-connected service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected IQAir AirVisual account can retrieve current air-quality and weather data for a supported city or their nearest supported city. They can also list countries, states, and cities with active stations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may run a changing remote installer with unclear execution scope, and its contents remain unverified.

Mitigation: Review and approve CLI setup separately before installation; prefer a fixed, verified release and review bundled-skill synchronization settings.

## Reference(s):

- [IQAir AirVisual](https://www.iqair.com)
- [IQAir API documentation](https://api-docs.iqair.com/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill release](https://clawhub.ai/oomol/skills/oo-iqair-airvisual)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON service responses and concise natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Current air-quality and weather results depend on supported locations and active stations.]

## Skill Version(s):

1.0.5 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
