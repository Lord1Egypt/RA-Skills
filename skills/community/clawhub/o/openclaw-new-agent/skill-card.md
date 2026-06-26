## Description: <br>
Guides an OpenClaw user through creating an independent Feishu bot agent, including collecting configuration, backing up existing settings, creating a workspace, patching configuration, and validating the new bot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itzhouq](https://clawhub.ai/user/itzhouq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to add a separate Feishu bot agent to an existing OpenClaw installation without manually editing the full nested configuration. It helps collect bot credentials, create a parallel workspace, patch allowlist settings, and verify that routing works. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow asks users to provide a Feishu App Secret and modifies the local OpenClaw configuration. <br>
Mitigation: Use a dedicated low-privilege Feishu app, avoid sharing secrets in public or shared chats, review the config patch before restart, keep a backup, and rotate any secret that may have been exposed. <br>


## Reference(s): <br>
- [OpenClaw New Agent on ClawHub](https://clawhub.ai/itzhouq/openclaw-new-agent) <br>
- [ClawHub](https://clawhub.com) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>
- [Feishu OpenClaw multi-agent template](https://open.feishu.cn/page/openclaw?form=multiAgent) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces step-by-step operational guidance for an agent to create workspace files, patch OpenClaw configuration, and validate Feishu bot routing.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
