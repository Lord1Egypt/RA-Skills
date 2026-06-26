## Description: <br>
Kim msg account setup helper for configuring the Kim Channel plugin so OpenClaw can exchange messages through Kim, the Kuaishou/Kwai IM channel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LeeGoDamn](https://clawhub.ai/user/LeeGoDamn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to install, configure, diagnose, and verify the Kim Channel integration for OpenClaw. It provides guided setup steps and shell commands for plugin installation, Kim application credentials, webhook configuration, gateway restart, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow asks for appKey, secretKey, and verificationToken values that could expose real messaging credentials if pasted into chat or stored insecurely. <br>
Mitigation: Use the skill only on a trusted workstation, avoid pasting credentials into chat, and prefer a secure secret store or local masked input. <br>
Risk: The setup scripts modify OpenClaw Kim channel configuration and can restart the gateway. <br>
Mitigation: Review the configuration changes before confirming setup and run the skill during an approved maintenance window when gateway restart is acceptable. <br>
Risk: The plugin installation step depends on the @ks-openclaw/kim package and an internal npm registry. <br>
Mitigation: Check the package source and version before installation and confirm the expected registry is configured. <br>


## Reference(s): <br>
- [Kim Msg Account Skill page](https://clawhub.ai/LeeGoDamn/kim-msg-account) <br>
- [Publisher profile](https://clawhub.ai/user/LeeGoDamn) <br>
- [Kim open platform](https://kim.kuaishou.com/) <br>
- [OpenApi service platform](https://open.kuaishou.com/) <br>
- [Full Kim Channel configuration guide](https://docs.corp.kuaishou.com/d/home/fcAA_W4zGstwslCQxlwehh1d2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include masked credential summaries and diagnostic status text.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
