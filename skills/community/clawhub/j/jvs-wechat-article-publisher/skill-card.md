## Description:

A WeChat Official Account publishing skill that helps agents prepare formatted articles, upload images, create drafts, and support manual publishing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenyd002025](https://clawhub.ai/user/chenyd002025)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketing teams, and agencies use this skill to assemble WeChat Official Account articles, prepare image assets, create drafts in WeChat, and review them before manual publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles WeChat Official Account API credentials and unpublished article content.

Mitigation: Use a private, access-restricted config.json stored outside shared or synced repositories, and rotate the AppSecret if it may have been exposed.

Risk: The bundled Python scripts use unsafe TLS settings according to the security evidence.

Mitigation: Avoid the bundled Python scripts until TLS verification is fixed; prefer reviewed curl commands or patched scripts that verify TLS certificates.

Risk: Pasting real AppSecrets into shell commands can expose credentials through logs or shell history.

Mitigation: Pass secrets through protected configuration or environment handling and avoid committing, logging, or sharing real AppSecrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenyd002025/skills/jvs-wechat-article-publisher)
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com)
- [WeChat Official Account API documentation](https://developers.weixin.qq.com/doc/offiaccount/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and article template content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate WeChat draft metadata and image URL JSON files when bundled scripts are used.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
