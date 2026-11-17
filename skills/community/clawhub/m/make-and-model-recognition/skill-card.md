## Description:

Detect the largest vehicle from an image using TrafficEye car-box detection, run make and model recognition for that vehicle, and return all license plates attached to the same road-user payload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eyedea-ai](https://clawhub.ai/user/eyedea-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to submit a local vehicle image to TrafficEye, select the largest detected road user, and present its make, model, box, and associated license plates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send sensitive vehicle images to an external TrafficEye endpoint.

Mitigation: Use it only with images that are appropriate to send to TrafficEye or another trusted deployment.

Risk: The API endpoint is configurable and the security evidence notes no host or HTTPS safeguards.

Mitigation: Keep TRAFFICEYE_API_URL set to the documented HTTPS TrafficEye endpoint unless the alternate endpoint is trusted.

Risk: API keys can be sent in query-string mode, where URLs are commonly logged.

Mitigation: Prefer the default header authentication mode and avoid TRAFFICEYE_API_KEY_MODE=query.

## Reference(s):

- [TrafficEye homepage](https://trafficeye.ai)
- [TrafficEye API reference](https://www.trafficeye.ai/api)
- [ClawHub skill page](https://clawhub.ai/eyedea-ai/skills/make-and-model-recognition)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON recognition output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the selected road-user payload with repeated box, plates, area, and source fields.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
