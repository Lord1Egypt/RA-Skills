## Description:

生成、改写、检查和修正 Markji 墨墨记忆卡内容。适用于把笔记转换成可粘贴的卡片，添加挖空、选择题、文字样式、公式、代码块、媒体或卡片关联，以及排查标签、转义、换行和嵌套错误。

This skill is ready for commercial/non-commercial use.

## Publisher:

[celend](https://clawhub.ai/user/celend)

### License/Terms of Use:

MIT-0

## Use Case:

使用 Markji 的学习者可将学习笔记转换为可直接粘贴的 GV3 记忆卡，也可检查和修正现有卡片的语法。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Explanations and generated content default to Chinese, which may not suit every user or audience.

Mitigation: Specify the desired language when it differs from Chinese, and review the output for the intended audience.

Risk: Some GV3 features may not work in clients without support for styled cloze, formula cloze, choice formulas, or code blocks.

Mitigation: Use the documented plain text cloze, ordinary formula, or plain text alternatives when a feature is unsupported.

## Reference(s):

- [Markji Card Syntax Reference](references/markji-card-syntax.md)
- [Markji](https://markji.com)
- [ClawHub Skill Page](https://clawhub.ai/celend/skills/markji-card-syntax)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markji GV3 card content in text code blocks, with concise Chinese explanations or corrections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses GV3 syntax. Styled cloze, formula cloze, choice formulas, and code blocks require client support; plain text alternatives are documented.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
