## Description: <br>
AI内容生成器 - 小红书文案、视频脚本、多平台内容一键生成。接入SkillPay收费，每次调用0.001 USDT。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ffffff9331](https://clawhub.ai/user/ffffff9331) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External creators and operators use this skill to generate paid draft content for Xiaohongshu posts, short-form video scripts, WeChat public-account articles, and multi-platform adaptation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically charge through an external billing service using an embedded fallback API key and an unclear default user account. <br>
Mitigation: Review before installing, require an explicit billing user ID, remove the hardcoded fallback key, and require clear approval before any charge is attempted. <br>
Risk: The security verdict is suspicious and the generated content is template-style rather than real AI-generated content. <br>
Mitigation: Treat outputs as drafts, review them before publication, and verify that the paid execution behavior matches user expectations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ffffff9331/paid-content-generator) <br>
- [Publisher profile](https://clawhub.ai/user/ffffff9331) <br>
- [SkillPay billing service](https://skillpay.me) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style text emitted by a Node.js command-line script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports xiaohongshu, video, and article content templates; billing may occur before output is produced.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
