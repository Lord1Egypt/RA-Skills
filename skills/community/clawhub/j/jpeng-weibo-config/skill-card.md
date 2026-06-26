## Description: <br>
Connects a Weibo channel to OpenClaw by collecting a Weibo AppId and AppSecret and configuring them with the OpenClaw CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure Weibo channel credentials for an OpenClaw deployment. It asks for the required AppId and AppSecret, applies them through OpenClaw configuration commands, and verifies the channel configuration when possible. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Weibo AppSecret is stored persistently in OpenClaw configuration. <br>
Mitigation: Use least-privileged or test credentials where possible, avoid exposing the AppSecret in logs or transcripts, and rotate it if disclosure is suspected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jpengcheng523-netizen/jpeng-weibo-config) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Handles user-provided Weibo AppId and AppSecret values for OpenClaw configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
