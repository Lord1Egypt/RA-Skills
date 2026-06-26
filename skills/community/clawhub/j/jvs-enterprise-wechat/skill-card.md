## Description: <br>
This skill helps configure OpenClaw to connect with an Enterprise WeChat AI Bot over a WebSocket-based AI Bot setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenyd002025](https://clawhub.ai/user/chenyd002025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace administrators use this skill to configure an OpenClaw gateway for Enterprise WeChat AI Bot messaging. It covers credential entry, local channel configuration, restart commands, and basic connection troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Bot Secret is stored in the local OpenClaw configuration as part of the expected setup flow. <br>
Mitigation: Protect ~/.openclaw configuration files, avoid sharing or committing the secret, and rotate the secret if exposure is suspected. <br>
Risk: The default direct-message policy is open, which may allow broad access in production or sensitive workspaces. <br>
Mitigation: Use pairing or allowlist mode for production or sensitive deployments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenyd002025/jvs-enterprise-wechat) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a Python setup helper that writes Enterprise WeChat channel settings to the local OpenClaw configuration.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
