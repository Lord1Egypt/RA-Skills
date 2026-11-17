## Description:

Query Naver Cloud Maps APIs for route navigation. Smart routing: Directions5 by default, auto-switches to Directions15 for 5+ waypoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beomsu317](https://clawhub.ai/user/beomsu317)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to calculate vehicle routes from Naver Cloud Maps using longitude,latitude coordinates, optional waypoints, route preferences, vehicle settings, and fuel settings. It returns distance, duration, toll fare, taxi fare, fuel cost, and route timing for driving trips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Route coordinates, waypoints, and authenticated routing requests are sent to Naver Cloud Maps.

Mitigation: Use the skill only for routes appropriate to share with Naver Cloud Maps, avoid sensitive personal routes when unnecessary, and scope the API key to Maps/Directions.

Risk: Production use depends on installed npm packages and API credentials.

Mitigation: Audit and update npm dependencies before production use, store credentials in environment variables, and rotate keys if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beomsu317/skills/ncloud-maps)
- [Naver Cloud Console](https://console.ncloud.com)
- [Naver Cloud Maps API Specification](references/api-spec.md)
- [NPM package](https://www.npmjs.com/package/ncloud-maps-skill)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON route results and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Route results include success status, start and goal coordinates, distance, duration, toll fare, taxi fare, fuel cost, departure time, and error text when a request fails.]

## Skill Version(s):

1.0.8 (source: package.json and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
