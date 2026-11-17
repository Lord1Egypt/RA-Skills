## Description:

为 AI 情景动画生成结构化的中英双语分镜稿，包含场景、角色、视觉基调和时长建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitruck](https://clawhub.ai/user/gitruck)

### License/Terms of Use:

MIT-0

## Use Case:

External creators use the skill to turn assigned narration beats into portable bilingual storyboards for AI video tools. The storyboard format preserves source lines, character descriptions, a visual tone, and approximate shot durations for review and downstream production.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected project material may be sent to an external generation service.

Mitigation: Choose and review which material to submit to the selected service.

Risk: Importing generated clips can make project-scoped timeline changes, and replacement may discard manual edits.

Mitigation: Review imported clips and project changes before continuing; approve replacement only when you intend to discard manual edits.

## Reference(s):

- [Sparse key scenes and character references](artifact/references/sparse-key-scenes.md)
- [Gitruck CLI](https://github.com/Gitruck/cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured bilingual Markdown storyboard]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese and English sections; the Chinese source script is retained untranslated; headings follow the AI Drama Desk storyboard parser contract.]

## Skill Version(s):

1.3.9 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
