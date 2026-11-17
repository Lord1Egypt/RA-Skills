## Description:

Location Service helps agents convert between coordinates and addresses, calculate distances, parse Google Maps URLs, and prepare location inputs for weather queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jakah2551](https://clawhub.ai/user/jakah2551)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to normalize addresses, coordinates, and Google Maps links for geocoding, distance calculation, and weather-location workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic Google Maps short-link resolution can make unsafe outbound requests.

Mitigation: Review before installing where internal services or sensitive network metadata are reachable; prefer a version that validates exact URL hostnames and restricts redirects.

Risk: Location inputs may disclose home, workplace, or current-location details to external geocoding providers.

Mitigation: Only submit location data that is acceptable to share with external providers.

Risk: The dispatcher runs helper scripts from a fixed external path.

Mitigation: Prefer a version that runs bundled helper scripts by relative path and review script paths before installation.

## Reference(s):

- [Location Service examples](artifact/references/examples.md)
- [OpenStreetMap Nominatim API](artifact/references/nominatim_api.md)
- [ClawHub skill page](https://clawhub.ai/jakah2551/skills/location-service)
- [Publisher profile](https://clawhub.ai/user/jakah2551)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call external geocoding services; errors are returned as text diagnostics.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
