## Description:

使用中文生成、改写、检查和修正面向普通用户的 Markji 卡片语法（亦称“墨墨记忆卡”语法）内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[celend](https://clawhub.ai/user/celend)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content authors use this skill to create, rewrite, check, and correct Markji memory-card syntax in Chinese. It helps convert notes into paste-ready cards with cloze deletion, choices, text styling, formulas, media references, and related-card links when supported evidence is provided.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated media, audio, or related-card IDs may be incorrect if the user has not supplied real IDs.

Mitigation: Use only user-provided IDs; otherwise generate media-free card text or explicit placeholders only when the user asks for a template.

Risk: Complex Markji syntax can fail when tags, separators, escaping, block placement, or nesting rules are wrong.

Mitigation: Apply the bundled syntax guide and self-checklist, and fall back to plain text or a simpler supported form when a requested format cannot be represented reliably.

## Reference(s):

- [Markji card syntax guide](references/markji-card-syntax.md)
- [Markji](https://markji.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown containing a single text code block with paste-ready Markji card syntax unless explanation is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese prose with required Markji syntax tags preserved exactly]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
