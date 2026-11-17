## Description:

视频号全流程运营工具，从选题策划到内容发布的数据驱动视频号运营体系

This skill is ready for commercial/non-commercial use.

## Publisher:

[golngod](https://clawhub.ai/user/golngod)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, OPC mentors, and channel operators use this skill to plan and run a WeChat Video Channel connected to public-account content. It supports topic selection, shooting preparation, content calendars, script drafting, publishing cadence, linkage strategy, and analytics review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local script helper builds an output path from caller-supplied filename text when saving generated scripts.

Mitigation: Use the helper only with trusted filenames, or update save_script to restrict input to a safe basename before writing files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/golngod/skills/opc-wechat-channel-ops)
- [Content strategy](references/content-strategy.md)
- [Shooting guide](references/shooting-guide.md)
- [Script template library](references/script-template.md)
- [Public-account linkage strategy](references/linkage-strategy.md)
- [Operation calendar](references/operation-calendar.md)
- [Coze platform](https://coze.cn)
- [OPC platform](https://opc.cn)

## Skill Output:

**Output Type(s):** [guidance, markdown, text, code, configuration]

**Output Format:** [Markdown guidance and Chinese short-video script text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes planning matrices, checklists, calendars, reusable oral-script templates, and an optional local helper that can save generated scripts as text files.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
