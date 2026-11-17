## Description:

使用 GPT Image 2 通过 AI Hive 生成或编辑包含指定中文、英文、数字或多语言文案的海报、包装、菜单、信息图和广告图片，并要求逐字校验输出文字。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, designers, marketers, and developers use this skill to generate or edit commercial images where approved copy must appear exactly, including posters, packaging, menus, infographics, ads, and localized visuals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles an AI Hive API key and can send credential-bearing requests to a configured base URL.

Mitigation: Keep the default AI Hive endpoint unless the replacement is fully trusted, avoid untrusted AI_HIVE_BASE_URL or --base-url values, and use a dedicated low-privilege API key when possible.

Risk: Reference media passed to the skill may be uploaded to AI Hive for generation or editing.

Mitigation: Only pass media files that are intended for upload and avoid using sensitive or unrelated assets as references.

Risk: Generated image text may contain altered characters, digits, punctuation, spacing, or layout.

Mitigation: Maintain a copy lock table, manually verify each generated character against it, and recreate high-risk legal, price, medical, financial, certification, or instruction text in professional layout tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/gpt-image-2-exact-text-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API access page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with bash commands; image tasks may download PNG files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AI Hive API credentials and may upload reference media; generated images require manual text QA.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
