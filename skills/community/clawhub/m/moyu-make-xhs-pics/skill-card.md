## Description:

Converts a Markdown article into Xiaohongshu-style cover, illustration, and companion images using DashScope or MiniMax, with selectable styles and layouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulforcoding](https://clawhub.ai/user/paulforcoding)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to turn local Markdown articles into Xiaohongshu-style image sets for social content workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Article-derived prompts may be sent to MiniMax or DashScope.

Mitigation: Do not use confidential, personal, or proprietary Markdown unless the relevant provider terms have been reviewed.

Risk: Runtime behavior depends on external image-generation APIs and Python dependencies.

Mitigation: Run the skill with least privilege and pin dependencies before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paulforcoding/skills/moyu-make-xhs-pics)
- [Project homepage](https://github.com/paulforcoding/make-xhs-pics)
- [baoyu-skills prompt reference](https://github.com/JimLiu/baoyu-skills)
- [MiniMax image generation endpoint](https://api.minimaxi.com/v1/image_generation)
- [DashScope generation endpoint](https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python and shell examples; generated image file paths at runtime]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime output depends on selected provider, article content, style, layout, and requested image counts.]

## Skill Version(s):

v1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
