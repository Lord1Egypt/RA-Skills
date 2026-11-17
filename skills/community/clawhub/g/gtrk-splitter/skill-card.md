## Description:

将已剪好的口播工程拆分为 beat 级视觉派单，指定画面主层与辅助层，并生成供 gtrk 校验落地的机器可读清单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitruck](https://clawhub.ai/user/gitruck)

### License/Terms of Use:

MIT-0

## Use Case:

面向视频创作者与剪辑团队，把已完成剪辑的口播工程转成按 beat 划分的 A-roll、动态图、AI 情景再现和影视素材派单，并由 gtrk CLI 校验和落地。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow writes project annotations and may perform requested edits.

Mitigation: Keep a project backup and review proposed changes before applying them.

Risk: Cloud steps may involve usage costs or data handling considerations.

Mitigation: Review expected costs and data handling before requesting full production; cloud credentials are optional for cloud steps.

Risk: The external gtrk CLI was not audited as part of this skill review.

Mitigation: Review the CLI's behavior and permissions before relying on it in a production workflow.

## Reference(s):

- [gtrk CLI](https://github.com/Gitruck/cli)
- [视觉拆分字段契约](artifact/references/field-schema.md)
- [视觉拆分 JSON 示例](artifact/references/example-visual-split.json)
- [ClawHub skill release](https://clawhub.ai/gitruck/skills/gtrk-splitter)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Shell commands, Guidance]

**Output Format:** [JSON visual dispatch manifest and Markdown visual split brief, with gtrk CLI commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Beat-level assignments use utterance ID spans; timing is projected by gtrk.]

## Skill Version(s):

1.3.10 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
