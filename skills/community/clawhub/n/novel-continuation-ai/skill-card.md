## Description:

当用户提供小说原文时，该技能提取语言风格、叙事节奏、角色语气和世界观设定，并以相同文风续写后续内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fenfenling](https://clawhub.ai/user/fenfenling)

### License/Terms of Use:

MIT-0

## Use Case:

External users and writers use this skill to continue Chinese novel chapters while preserving the source work's style, character voices, relationship dynamics, worldbuilding, and plot continuity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Style and plot notes can preserve manuscript details between sessions.

Mitigation: Review, redact, or clear references/style.md and references/plot_state.md before using sensitive, proprietary, or non-persistent manuscript material.

Risk: Continuation quality depends on complete source context and current plot notes.

Mitigation: Provide all relevant chapters and verify the reference notes before accepting generated continuation text.

## Reference(s):

- [情节状态](references/plot_state.md)
- [小说风格分析](references/style.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown with a ## 续写内容 section and optional updates to reference Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected continuation length is 2000-4000 Chinese characters when aligned with the source text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
