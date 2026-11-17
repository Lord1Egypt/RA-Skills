## Description:

Planit generates AI-optimized travel itineraries from natural language travel requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yoborlon-alpha](https://clawhub.ai/user/yoborlon-alpha)

### License/Terms of Use:

MIT

## Use Case:

External users use Planit to turn natural-language trip requests into suggested itineraries with transportation options, hotel recommendations, attraction schedules, and cost estimates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Travel requests, user identifiers, configuration, and optional bearer credentials may be sent to a remote backend over plaintext HTTP by default.

Mitigation: Configure the endpoint to a trusted HTTPS service before use and avoid sending sensitive travel details or credentials until transport security is confirmed.

Risk: Telemetry behavior may not match the privacy claims in the artifact documentation.

Mitigation: Review telemetry fields and backend handling before deployment, and clarify data collection practices for users.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Structured itinerary responses and user-facing text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include itinerary details, clarification prompts, actions, and telemetry events handled through the configured backend service.]

## Skill Version(s):

2.0.8 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
