## Description:

Detect and read the largest license plate from an image using the TrafficEye REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[radekzc](https://clawhub.ai/user/radekzc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to submit a local vehicle image to the TrafficEye API, parse the recognition response, and report the largest detected license plate with its OCR text and plate metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Vehicle images and plate data are uploaded to TrafficEye or another configured endpoint.

Mitigation: Use the skill only when the user is comfortable sending the selected image and plate data to that service, and configure TRAFFICEYE_API_URL to a trusted HTTPS host.

Risk: API credentials may be exposed if query-string transport is used or if keys are over-privileged.

Mitigation: Prefer header or bearer authentication, avoid query-string API key transport unless required, and use a scoped TrafficEye API key.

## Reference(s):

- [TrafficEye](https://trafficeye.ai)
- [TrafficEye API](https://www.trafficeye.ai/api)
- [ClawHub skill page](https://clawhub.ai/radekzc/skills/license-plate-reader)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON recognition output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper returns the selected plate payload, recognized text, polygon area, and source path within the API response.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
