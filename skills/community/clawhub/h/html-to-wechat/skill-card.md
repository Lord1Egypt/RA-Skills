## Description:

Takes existing HTML content from a file, URL, or pasted source, checks and converts it for WeChat compatibility, prepares a cover image, and publishes the result to a WeChat Official Account draft box.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lutongsuo](https://clawhub.ai/user/lutongsuo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content teams, and WeChat Official Account operators use this skill to turn existing HTML into a WeChat-compatible article draft, including compatibility checks, inline-style conversion, cover compression, and draft upload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow requires access to WeChat Official Account credentials.

Mitigation: Use environment variables or interactive prompts, keep secrets out of chats and source files, and review the workflow before installation.

Risk: The workflow uploads article content and generated assets to WeChat.

Mitigation: Review the generated HTML, cover image, title, and digest before allowing the final draft upload.

Risk: The workflow relies on unpinned dependency and companion-skill installation.

Mitigation: Install dependencies and the companion skill deliberately, and prefer pinned versions where operational controls allow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lutongsuo/skills/html-to-wechat)
- [WeChat Official Account Platform](https://mp.weixin.qq.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration steps, validation results, and publication status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce intermediate HTML and compressed cover-image files before publishing a draft through the companion WeChat workflow.]

## Skill Version(s):

1.0.0 (source: artifact/SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
