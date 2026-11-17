## Description:

杰峰设备画面翻转技能（开发版）。支持画面左右翻转（镜像）、上下翻转设置，适用于摄像头画面方向调整。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and camera operators use this skill to query or change JFTech camera image orientation settings, including horizontal mirroring and vertical flipping, for installed devices.

### Deployment Geography for Use:

China mainland, Asia, Europe, and North America

## Known Risks and Mitigations:

Risk: Camera credentials can be sent to a host selected through JF_ENDPOINT.

Mitigation: Use the skill only in controlled environments and keep JF_ENDPOINT fixed to a trusted JFTech regional host.

Risk: Write actions can persistently change camera image orientation.

Mitigation: Run write actions only after confirming the target device, channel, and desired flip or mirror state.

Risk: Broader Camera.Param settings may be overwritten if writes proceed from incomplete camera configuration data.

Mitigation: Review current camera parameters before write actions and avoid writes when Camera.Param is missing until the publisher implements fail-closed behavior.

Risk: App secrets and device tokens are required for operation.

Mitigation: Protect JF_APP_SECRET and JF_DEVICE_TOKEN, rotate expired tokens, and avoid exposing command environments or logs that contain credentials.

## Reference(s):

- [JFTech Open Platform documentation](https://docs.jftech.com)
- [ClawHub skill page](https://clawhub.ai/jftech/skills/jf-open-pro-device-image-flip)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can perform authenticated JFTech OpenAPI calls to query or persistently update camera flip settings when required credentials are supplied.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
