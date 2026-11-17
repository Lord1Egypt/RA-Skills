## Description:

从 Amazon 评论中的安装、使用和维护疑问提炼说明内容改进重点，并整理相应证据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

商品运营人员可用此技能从 Amazon 评论中的安装、使用和维护问题提炼说明书改进建议，并查看支撑建议的评论证据。它用于生成分析与建议，不会自动发布或修改商品页面。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: This instruction-improvement skill includes broader account controls and can spend credits despite its promised confirmation limits.

Mitigation: Prefer a version restricted to instruction improvement with enforced spending approval. Set ARI to ask before every charge, choose manual collection for one-time work, review recurring schedules and competitor monitoring, and do not assume deepdive is a free preview.

## Reference(s):

- [ARI CLI and API reference](references/reference.md)
- [Instruction improvement workflow](references/operation-workflow.md)
- [ARI operations workspace](https://ari.funewa.com/zh/operations)
- [ClawHub release page](https://clawhub.ai/funewa/skills/instruction-improve)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown product operations analysis with evidence-backed documentation improvement suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Grounded in available product and review data; does not modify or publish Amazon listings.]

## Skill Version(s):

1.5.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
