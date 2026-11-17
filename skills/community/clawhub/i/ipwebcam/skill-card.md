## Description:

Transform an Android phone with IP Webcam into an intelligent Edge AI security system with OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alihmaou](https://clawhub.ai/user/alihmaou)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to configure an Android phone running IP Webcam as a local motion-monitoring camera with alert-driven AI review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill interacts with camera, audio, telemetry, and device-control endpoints.

Mitigation: Keep the IP Webcam endpoint on a trusted local network, enable authentication where available, and avoid public port forwarding.

Risk: Alert-triggered frames may be sent to an AI service.

Mitigation: Confirm that alert images are appropriate to share with the selected AI service before deployment.

Risk: Background monitoring loops can continue collecting camera data if lifecycle controls are unclear.

Mitigation: Review or add explicit start and stop controls before using continuous monitoring.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alihmaou/skills/ipwebcam)
- [Publisher profile](https://clawhub.ai/user/alihmaou)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local network camera endpoints, threshold guidance, dependency requirements, and operational security guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
