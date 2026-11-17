## Description:

龙虾内容工厂批量生成小红书信息图和视频，并支持定时自动发布。

This skill is ready for commercial/non-commercial use.

## Publisher:

[houdaliang](https://clawhub.ai/user/houdaliang)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and operators use this skill to define Xiaohongshu posts, generate infographic cards and slideshow videos, and prepare manual or scheduled publishing through a logged-in browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent scheduled browser automation can continue operating after installation and affect a logged-in Xiaohongshu session.

Mitigation: Avoid cron setup unless lifecycle controls are added, and require user review before any final publishing action.

Risk: The content generator calls an external mutable make_card.py path outside the reviewed package.

Mitigation: Change generate-today.py to call the bundled make_card.py and pin required dependencies before deployment.

Risk: Browser publishing fills page content through innerHTML in a logged-in session.

Mitigation: Replace innerHTML body filling with plain-text insertion and review generated content before publishing.

## Reference(s):

- [小红书帖子模板](artifact/references/post-templates.md)
- [小红书发布规则](artifact/references/publish-rules.md)
- [ClawHub skill page](https://clawhub.ai/houdaliang/skills/guiji-xhs-factory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands and generated PNG, MP4, and JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates infographic images, slideshow videos, and a content queue manifest; browser publishing requires user review before the final publish action.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
