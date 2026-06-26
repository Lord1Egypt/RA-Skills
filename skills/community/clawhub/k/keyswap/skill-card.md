## Description: <br>
Rotate Claude Max API tokens for OpenClaw Anthropic profiles when a user provides a replacement `sk-ant-` token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jawaddxb](https://clawhub.ai/user/jawaddxb) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to rotate Claude Max API tokens for configured OpenClaw Anthropic profiles and check whether the gateway is healthy afterward. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can overwrite stored API tokens for configured OpenClaw Anthropic profiles. <br>
Mitigation: Back up auth-profiles.json, verify the profile names match the intended setup, and require explicit user confirmation before updating credentials. <br>
Risk: The skill can restart the OpenClaw gateway as part of token rotation. <br>
Mitigation: Run it only during an approved maintenance window or when a gateway restart is acceptable, and check gateway health after execution. <br>


## Reference(s): <br>
- [Key Swap on ClawHub](https://clawhub.ai/jawaddxb/keyswap) <br>
- [jawaddxb publisher profile](https://clawhub.ai/user/jawaddxb) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell command execution and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a replacement token beginning with `sk-ant-`, access to the OpenClaw auth profiles file, jq, and the OpenClaw gateway environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
