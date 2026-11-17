## Description:

帮助小学家长根据孩子的作文文字或手写照片提出温和、具体的修改建议，并生成适合对孩子说的话术和轻量练习。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dm-kevin](https://clawhub.ai/user/dm-kevin)

### License/Terms of Use:

MIT-0

## Use Case:

小学家长用它检查孩子的作文、指导孩子自己修改，并获得家长版建议、孩子版反馈、亲子沟通话术和一项小练习。经家长明确开启后，也可维护单个孩子的写作成长档案。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 删除单次批改记录可能永久丢失已保存的孩子写作档案内容。

Mitigation: 删除前展示确切记录并征求家长确认，保留备份或要求明确的删除确认。

Risk: 未来启用的进阶服务可能上传孩子的作文内容。

Mitigation: 保持服务默认关闭；启用前核对服务地址、密钥配置和隐私说明，上传前取得家长明确同意。

## Reference(s):

- [ClawHub 技能页面](https://clawhub.ai/dm-kevin/skills/parent-composition-coach)
- [年级标准](artifact/references/grade-standards.md)
- [作文类型](artifact/references/composition-types.md)
- [基础版点评方法](artifact/references/basic-review-methods.md)
- [输出模板](artifact/references/output-templates.md)
- [成长档案协议](artifact/references/profile-schema.md)
- [进阶版点评服务设计](artifact/references/advanced-review.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [中文 Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [包括家长版建议、孩子版反馈、亲子话术和一项练习；不代写整篇作文。]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
