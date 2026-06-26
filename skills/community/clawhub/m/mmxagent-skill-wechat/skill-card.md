## Description: <br>
Connects a personal WeChat account to OpenClaw through a QR-code login flow, explicitly excluding enterprise WeChat and WeCom. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oreoandyuumi](https://clawhub.ai/user/oreoandyuumi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to bind a personal WeChat account, install or update the required WeChat plugin, generate a login QR code, confirm credentials before storage, and restart the gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The flow connects a personal WeChat account and writes a reusable bot token under ~/.openclaw. <br>
Mitigation: Run it only on a trusted, non-shared machine and require the user to review masked credential details before writing them to disk. <br>
Risk: The optional CDN upload can expose a one-time authorization QR code outside the local workspace. <br>
Mitigation: Prefer the local QR image file and use CDN upload only when the user cannot access the local file. <br>
Risk: The setup installs npm packages and uses a registry mirror during execution. <br>
Mitigation: Proceed only when the user trusts the package sources and the registry mirror used by the setup. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/oreoandyuumi/mmxagent-skill-wechat) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline bash commands and credential-review prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local QR PNG and writes account credential configuration only after user confirmation.] <br>

## Skill Version(s): <br>
1.0.3 (source: server evidence release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
