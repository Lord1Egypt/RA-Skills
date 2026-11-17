## Description:

Creates structured meeting preparation briefs with background research, agenda context, action checklists, communication strategy, HTML output, and optional Tencent Docs synchronization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[monica8825](https://clawhub.ai/user/monica8825)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external meeting participants use this skill to turn meeting context, attachments, and public research into concise pre-meeting briefs for business discussions, project reviews, and collaboration planning. The skill is intended for internal preparation and review before sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive meeting materials, attachments, and internal planning context.

Mitigation: Use only appropriate source material, avoid adding unnecessary sensitive data, and review generated briefs before sharing.

Risk: Optional Tencent Docs synchronization may store generated meeting content in an external document service.

Mitigation: Enable sync only for material approved for Tencent Docs storage and verify document access permissions.

Risk: Generated meeting summaries, public research, or strategy suggestions may be incomplete, outdated, or incorrect.

Mitigation: Review facts, preserve uncertainty labels, and confirm key items before using the brief in a meeting.

## Reference(s):

- [会前材料 HTML 模板设计规范](references/html-template-guide.md)
- [Meeting Prep HTML Template](assets/meeting-prep-template.html)
- [ClawHub Skill Page](https://clawhub.ai/monica8825/skills/meeting-prep-brief)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Structured HTML brief with optional Markdown/Tencent Docs version, checklists, tables, and source notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May process user-supplied meeting materials and optionally sync generated content to Tencent Docs when configured.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
