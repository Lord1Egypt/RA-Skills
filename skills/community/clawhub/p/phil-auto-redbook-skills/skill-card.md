## Description:

小红书笔记素材创作技能。当用户需要创建小红书笔记素材时使用这个技能。技能包含：根据用户的需求和提供的资料，撰写小红书笔记内容（标题+正文），生成图片卡片（封面+正文卡片），以及发布小红书笔记。

This skill is ready for commercial/non-commercial use.

## Publisher:

[phil-guo](https://clawhub.ai/user/phil-guo)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to draft Xiaohongshu note content, render themed cover and body image cards from Markdown, and optionally publish the note to Xiaohongshu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing mode handles a live Xiaohongshu login cookie and can publish under that account.

Mitigation: Use publishing only with an account intended for this workflow, keep the cookie out of prompts and shared files, and rotate or revoke it if exposed.

Risk: API mode can send the login cookie to a configurable service.

Mitigation: Avoid API mode unless the service is local and trusted.

Risk: Rendering untrusted Markdown may expose the local rendering environment to unsafe content.

Mitigation: Render only trusted Markdown or run rendering in an isolated environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/phil-guo/skills/phil-auto-redbook-skills)
- [README](artifact/README.md)
- [Style Preview](artifact/STYLES.md)
- [Example Markdown](artifact/assets/example.md)
- [Xiaohongshu](https://www.xiaohongshu.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can render cover.png and card_*.png assets and can optionally publish through a Xiaohongshu account cookie.]

## Skill Version(s):

2.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
