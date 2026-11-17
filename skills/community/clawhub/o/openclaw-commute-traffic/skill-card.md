## Description:

Check real-time traffic conditions for a route between two locations using TomTom.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xavjer](https://clawhub.ai/user/xavjer)

### License/Terms of Use:


## Use Case:

External users and agent operators use this skill to check live driving conditions, commute time, route alternatives, and whether to leave now for an origin-destination pair.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Route origins and destinations are sent to TomTom for geocoding and traffic lookup.

Mitigation: Install only when sharing route locations with TomTom is acceptable, and avoid submitting sensitive personal locations unless necessary.

Risk: The skill prose describes any route, but the script geocoding request is hardcoded with countrySet=CH.

Mitigation: Treat results as Switzerland-biased and ask for more specific locations or coordinates when routes outside Switzerland are needed.

Risk: The helper script requires a TomTom API key.

Mitigation: Provide TOMTOM_API_KEY through the configured environment or secret mechanism and rotate the key if it is exposed.

## Reference(s):

- [TomTom API Response Reference](references/tomtom-api-response.md)
- [TomTom Developer Portal](https://developer.tomtom.com)
- [Commute Traffic on ClawHub](https://clawhub.ai/xavjer/skills/openclaw-commute-traffic)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON from the traffic-check script plus concise user-facing traffic guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and TOMTOM_API_KEY; geocoding is biased to Switzerland by countrySet=CH.]

## Skill Version(s):

2.0.0 (source: frontmatter); release metadata version 0.1.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
