## Description:

对中文小说、梗概或章节进行有文本依据的六维审稿，逐项说明证据、阅读影响、待确认问题和可执行修改。适用于编辑初筛、自检、横向比较和改稿复盘；评分是辅助意见，不代表签约、过审或市场结果。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution (MIT-0)

## Use Case:

面向中文小说作者和编辑，使用者可让 AI 按六个维度审阅提供的正文、章节或梗概，并获得带可定位原文证据、阅读影响和修改建议的编辑参考。需要保存结果时，可生成结构化 JSON 和排版后的 Markdown 报告。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 稿件可能包含未公开或敏感内容，保存的审稿报告也会引用原文。

Mitigation: 只提供愿意交由当前 AI 处理的稿件内容；将报告保存到合适的新目录，并妥善管理其访问权限。

Risk: 结构校验和 Markdown 排版不能证明引文或审稿判断准确。

Mitigation: 对照原稿核实每处引文、位置和判断，再使用审稿结论。

## Reference(s):

- [ClawHub release page](https://clawhub.ai/xxjrq/skills/novel-review-score)
- [六维评分量表](references/rubric.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Markdown]

**Output Format:** [中文审稿意见；可选 JSON 与 Markdown 报告]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [六维评价附原文证据、阅读影响和可执行建议；证据不足时标记待确认，不虚构分数。]

## Skill Version(s):

1.0.2 (source: server-resolved release, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
