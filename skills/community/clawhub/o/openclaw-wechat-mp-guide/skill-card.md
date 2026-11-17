## Description:

Openclaw Wechat Mp Guide explains how to connect an OpenClaw AI assistant to a WeChat Official Account for automated message replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, media operators, and developers use this guide to configure WeChat Official Account credentials, callback settings, and OpenClaw commands so an AI assistant can respond to user messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide includes an unsafe fixed callback token example for WeChat server verification.

Mitigation: Generate a unique high-entropy callback token for each deployment and do not reuse the documented example value.

Risk: Automated message and image processing can create privacy and retention obligations for account operators.

Mitigation: Publish clear user-facing notice, limit retention and logging, and protect AppSecret, token, and EncodingAESKey as secrets.

## Reference(s):

- [WeChat Official Accounts Platform](https://mp.weixin.qq.com)
- [ClawHub Skill Page](https://clawhub.ai/yang1002378395-cmyk/skills/openclaw-wechat-mp-guide)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guide with shell and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup steps, credential placeholders, troubleshooting checks, and pricing/contact notes.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and skill.json remain 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
