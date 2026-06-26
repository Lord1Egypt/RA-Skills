## Description: <br>
Install, configure, run, and troubleshoot a Windows WeChat desktop automation and BHMailer/OpenClaw mail bridge bundle, including File Transfer Assistant workflows, plugin config, sidecar setup, and operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YJLi-new](https://clawhub.ai/user/YJLi-new) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install, configure, run, and troubleshoot a Windows-local WeChat desktop automation bridge that connects OpenClaw with BHMailer mail lookup and watch workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bridge can route messages and mail data between WeChat groups, BHMailer, the plugin host, and the Windows sidecar. <br>
Mitigation: Install only where the operator controls the WeChat groups, BHMailer account, plugin host, sidecar host, and related network access. <br>
Risk: Development secrets, broad admin access, or exposed local services could allow unauthorized bridge commands or data access. <br>
Mitigation: Change all development secrets, restrict admin commands, and keep services bound to localhost or a trusted network. <br>
Risk: Visual fallback mode can send WeChat screenshots or extracted text to a configured VLM endpoint. <br>
Mitigation: Disable remote VLM unless users consent to screenshot upload and avoid use in chats or mailboxes containing highly sensitive content. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/YJLi-new/openclaw-wechat-mail-bridge-windows) <br>
- [Project homepage](https://github.com/YJLi-new/OPENCLAW-SKILLS/tree/main/wechat-mail-bridge-skill/clawhub-openclaw-wechat-mail-bridge-windows) <br>
- [Windows Quick Install](references/install-windows.md) <br>
- [Config Reference](references/config.md) <br>
- [Sidecar Config Reference](references/sidecar-config.md) <br>
- [Operations](references/operations.md) <br>
- [Release Notes](references/release-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local artifact files, Windows setup commands, OpenClaw plugin configuration, and sidecar configuration.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata and release notes) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
