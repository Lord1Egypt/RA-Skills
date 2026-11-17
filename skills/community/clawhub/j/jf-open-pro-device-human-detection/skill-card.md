## Description:

Enables agents to query and update JFTech device human detection and PTZ human tracking settings through the JFTech OpenAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jftech](https://clawhub.ai/user/jftech)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and device operators use this skill to inspect and change human detection alerts, detection sensitivity, PTZ human tracking, tracking sensitivity, and return-time behavior on compatible JFTech devices.

### Deployment Geography for Use:

China Mainland, Asia, Europe, and North America, matching the regional JFTech API endpoints listed in the skill metadata.

## Known Risks and Mitigations:

Risk: Signed requests containing sensitive device credentials can be sent to an endpoint selected through JF_ENDPOINT.

Mitigation: Keep JF_ENDPOINT unset or set it only to an official JFTech regional host, and run the skill only in a controlled runtime.

Risk: Set actions can change detection alerts, sensitivity, tracking, and return-time behavior on a security device.

Mitigation: Review the target device, channel, action, and requested values before execution, and restrict use to operators authorized to change device security settings.

Risk: The skill requires JF_APP_SECRET and JF_DEVICE_TOKEN to perform signed device API calls.

Mitigation: Provide credentials through protected environment variables, avoid logging or sharing them, and rotate them if exposure is suspected.

## Reference(s):

- [JFTech Open Platform documentation](https://docs.jftech.com)
- [ClawHub skill page](https://clawhub.ai/jftech/skills/jf-open-pro-device-human-detection)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and text CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JFTech OpenAPI credentials and a device token; set actions can change device detection and tracking settings.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
