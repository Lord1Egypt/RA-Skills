## Description:

Provides a local weather lookup that returns current conditions for a requested location using an external weather service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zywss](https://clawhub.ai/user/zywss)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer simple local weather questions by supplying a location and receiving a concise current-conditions summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather queries send the requested location to wttr.in.

Mitigation: Avoid entering sensitive or unnecessary precise locations, and disclose the external weather-service request path before use.

Risk: The documentation describes forecasts, alerts, and historical data, while the current implementation returns only a basic current-weather response.

Mitigation: Set user expectations to current conditions unless the implementation is expanded and retested.

Risk: The lockfile resolves dependencies through a non-default registry mirror and the dependency declaration uses a range.

Mitigation: Prefer an approved registry lockfile and exact dependency pinning for reproducible deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zywss/skills/my-local-weather)
- [Publisher profile](https://clawhub.ai/user/zywss)
- [wttr.in weather service](https://wttr.in)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Plain text weather summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Currently implemented as a current-weather response with Chinese labels; it defaults to Beijing when no location is provided.]

## Skill Version(s):

1.0.0 (source: release evidence, package.json, _meta.json, package-lock.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
