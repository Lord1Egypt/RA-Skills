## Description:

Provides current weather conditions and forecasts for a specified location using public weather services such as wttr.in.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohdalhashemi98-hue](https://clawhub.ai/user/mohdalhashemi98-hue)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to fetch current conditions, rain checks, temperatures, and short forecasts for a requested city, region, or airport code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather queries are sent to a third-party weather endpoint and include the location being queried.

Mitigation: Avoid submitting sensitive locations and disclose that weather lookups leave the local agent environment.

Risk: Public weather responses may be unsuitable for severe alerts or safety-critical decisions.

Mitigation: Use official weather services for severe weather alerts, aviation, marine, or other safety-critical decisions.

Risk: The public weather endpoint is rate limited and may fail or degrade if overused.

Mitigation: Throttle repeated requests and retry later rather than issuing rapid repeated calls.

## Reference(s):

- [wttr.in help](https://wttr.in/:help)
- [ClawHub skill page](https://clawhub.ai/mohdalhashemi98-hue/skills/mh-weather)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and weather endpoint responses that may be text, JSON, or PNG.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl. No API key is needed. Weather queries send the requested location to a third-party weather endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
