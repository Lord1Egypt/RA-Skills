## Description:

掘金自动发布 - 一键发布文章到掘金，支持定时发布、标签优化、封面设置。适合：内容创作者、技术博主。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and technical bloggers use this skill to prepare, schedule, and publish Markdown articles to Juejin with tag, summary, cover, and queue guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A full Juejin account cookie can authorize publishing as the user until it is revoked or expires.

Mitigation: Use a low-risk Juejin account where possible, keep cookies out of shared or synced workspace files, and rotate or revoke the cookie after exposure.

Risk: The skill directs users to run local Python scripts that are not included in the artifact.

Mitigation: Inspect the referenced scripts before execution and run them only in a trusted workspace.

Risk: Automated or high-volume posting can publish unintended content or trigger Juejin platform limits.

Mitigation: Review each article and schedule before publishing, keep posting rates conservative, and confirm platform policy compliance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/skills/juejin-auto-publisher)
- [Juejin article draft API endpoint](https://api.juejin.cn/content_api/v1/article_draft/create)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, YAML configuration examples, and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a user-provided Juejin cookie.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
