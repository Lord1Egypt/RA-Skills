## Description:

Configure Feishu as an OpenClaw messaging channel in about 15 minutes, including app creation, permissions, event subscription, and secure API integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to configure a Feishu bot as an OpenClaw message channel for single-chat and group-chat workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A public Feishu callback endpoint can receive unwanted traffic or be misused if callback verification and message encryption are not configured.

Mitigation: Configure callback verification, enable Feishu message encryption where supported, and avoid unrestricted public tunnels for production use.

Risk: Leaking the Feishu App Secret can allow unauthorized access to the app integration.

Mitigation: Keep the app secret out of shared files, restrict configuration file permissions, and rotate credentials regularly.

Risk: Overbroad Feishu app permissions or availability can expose more workspace data or users than intended.

Mitigation: Limit Feishu app permissions and app availability to the minimum scope needed for the OpenClaw integration.

## Reference(s):

- [Openclaw Feishu Setup on ClawHub](https://clawhub.ai/yang1002378395-cmyk/skills/openclaw-feishu-setup)
- [Feishu Open Platform App Console](https://open.feishu.cn/app)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with YAML configuration snippets and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language setup guidance with placeholder credential values]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact/package.json, and artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
