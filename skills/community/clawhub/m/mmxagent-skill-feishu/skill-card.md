## Description: <br>
Helps an agent connect a Feishu bot through a direct API registration flow, return the required OpenClaw link, poll for client credentials after user confirmation, and continue with later OpenClaw setup steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oreoandyuumi](https://clawhub.ai/user/oreoandyuumi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when connecting, binding, or creating a Feishu bot for OpenClaw. It guides the agent through the direct registration link flow, waits for user confirmation, polls for credentials, and resumes the remaining OpenClaw setup and pairing steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Feishu client credentials, including a client secret, during the integration flow. <br>
Mitigation: Provide secrets only through environment variables or an approved secret manager, avoid pasting them into chat, and rotate the secret if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oreoandyuumi/mmxagent-skill-feishu) <br>
- [Feishu app registration API endpoint](https://accounts.feishu.cn/oauth/v1/app/registration) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and user-facing setup instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a clickable Feishu setup link, status guidance for pending authorization, and follow-up OpenClaw pairing instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
