## Description: <br>
OpenClaw Helper provides a deployment and troubleshooting cheat sheet for OpenClaw, including nine-stage deployment guidance, common error fixes, and log keyword explanations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mwangxiang](https://clawhub.ai/user/mwangxiang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and server administrators use this skill to configure OpenClaw deployments, set AI model and Feishu channel settings, restart the gateway, inspect logs, and troubleshoot common setup errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Root SSH and remote service commands can change or restart an OpenClaw server. <br>
Mitigation: Use only on servers you administer, verify the target IP and environment, and review commands before execution. <br>
Risk: Model and Feishu channel setup can expose API keys, app IDs, and app secrets in terminals or logs. <br>
Mitigation: Avoid shared terminals and logs, treat substituted values as secrets, and quote values safely when filling command templates. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command templates and troubleshooting tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes remote SSH command templates and configuration snippets with placeholders for IP addresses and credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
