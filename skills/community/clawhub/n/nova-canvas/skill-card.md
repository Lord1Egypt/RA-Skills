## Description:

Generate images using Amazon Nova Canvas via AWS Bedrock with multiple AWS authentication methods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wujiaming88](https://clawhub.ai/user/wujiaming88)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate PNG image files from text prompts through Amazon Nova Canvas on AWS Bedrock when the requested task is image creation rather than editing, video, or HTML canvas rendering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling may leak AWS secrets or bearer tokens when secrets are passed on the command line or included in command transcripts.

Mitigation: Prefer AWS profiles, SSO, IAM roles, or environment-managed credentials, and avoid passing AWS secrets or bearer tokens as command-line arguments.

Risk: Untrusted region values can affect the Bedrock endpoint used for bearer-token requests.

Mitigation: Use trusted AWS regions and validate region input or rely on an AWS SDK endpoint resolver before using bearer-token authentication.

## Reference(s):

- [Nova Canvas ClawHub skill page](https://clawhub.ai/wujiaming88/skills/nova-canvas)
- [Publisher profile](https://clawhub.ai/user/wujiaming88)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [PNG image files with console status text and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates one to five images per invocation and requires AWS Bedrock access with Nova Canvas enabled.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
