## Description:

开悟吧 is a platform-style OpenClaw skill that checks purchased features, activates eligible features, and installs required ClawHub skills when the user invokes it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[markma84](https://clawhub.ai/user/markma84)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to activate purchased kaiwu8 features from a configured account and to install any ClawHub skills those features require.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically install other skills and surface server-provided agent-change instructions without enough scoping or user approval.

Mitigation: Use it only with a trusted kaiwu8 service endpoint and API key, and review required installs and activation changes before applying them.

Risk: The kaiwu8 service and local configuration have significant influence over the OpenClaw environment.

Mitigation: Keep the configured endpoint and credentials controlled, and prefer a version that previews required installs and activation changes before applying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/markma84/skills/kaiwu8)
- [Publisher profile](https://clawhub.ai/user/markma84)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Console text with configuration examples and activation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report activation status, required skill installs, and service-provided what/why/how guidance.]

## Skill Version(s):

1.8.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
