## Description:

Use the OOMOL-connected GraphHopper service to calculate routes, isochrones, travel matrices, geocode locations, and list routing profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to query GraphHopper routing and location services through an existing OOMOL connection. It returns route, isochrone, matrix, geocoding, or profile data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI setup may download and execute code that was not verified in the supplied package.

Mitigation: Before first-time setup, review and explicitly approve a verified CLI installation, and check its first-run skill installation behavior.

Risk: Addresses and coordinates pass through OOMOL to GraphHopper, and requests may consume credit.

Mitigation: Send only location data approved for this service, and check expected credit use before making requests.

## Reference(s):

- [GraphHopper API documentation](https://docs.graphhopper.com/)
- [GraphHopper homepage](https://www.graphhopper.com)
- [GraphHopper skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-graphhopper)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON service results with command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected action and supplied locations or routing parameters.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
