## Description:

Controls a paired Android Node device's USB camera for single-frame capture, streaming frame events, stopping streams, and closing camera callbacks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lxx328](https://clawhub.ai/user/lxx328)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to capture still images or receive camera frames from a paired Node device for remote monitoring, visual inspection, and downstream vision analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Camera frames may expose private spaces or sensitive visual information.

Mitigation: Use the skill only with trusted devices in appropriate locations, and avoid capturing or streaming images from private areas without approval.

Risk: Captured images are served over HTTP from the Node device and frame URLs may be pushed through cloud events.

Mitigation: Use trusted networks and paired devices only, and avoid exposing the device HTTP server or image URLs beyond the intended agent workflow.

Risk: Calling camera.close stops stream callbacks but may not guarantee hardware shutdown.

Mitigation: Confirm the Node device camera state after sensitive sessions and rely on the device UI or lifecycle controls when hardware shutdown is required.

Risk: The helper script can download from supplied URLs, decode base64 frame data, and write to supplied output paths.

Mitigation: Pass only trusted image URLs, frame data, and output paths to the helper script.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lxx328/skills/node-camera)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, JSON, code]

**Output Format:** [Markdown guidance with JSON command payloads and optional helper-script commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill returns image URLs for captured frames and may guide agents to download JPEG images from the Node device HTTP server.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
