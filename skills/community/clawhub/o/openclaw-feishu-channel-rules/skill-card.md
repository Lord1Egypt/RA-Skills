## Description:

This skill applies Lark/Feishu channel output rules and is always active in Lark conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenfa188](https://clawhub.ai/user/chenfa188)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to keep assistant responses in Lark/Feishu conversations concise, low ceremony, and compatible with Feishu Markdown constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Always-on formatting guidance can shape responses in Lark/Feishu conversations even when a user does not explicitly ask for formatting.

Mitigation: Install it only for Feishu/Lark conversation contexts where concise style and channel-specific Markdown are desired.

Risk: Feishu Markdown differs from standard Markdown, so unsupported syntax may render poorly in message cards.

Mitigation: Use the bundled Feishu Markdown syntax reference when formatting channel output.

## Reference(s):

- [Feishu Markdown Syntax Reference](references/markdown-syntax.md)
- [ClawHub Skill Page](https://clawhub.ai/chenfa188/skills/openclaw-feishu-channel-rules)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise prose and Lark/Feishu-compatible Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Always active in Lark conversations; does not add code execution, credential access, persistence, or hidden behavior.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
