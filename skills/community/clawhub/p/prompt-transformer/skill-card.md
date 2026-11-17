## Description:

Transform messages that begin with `@prt` or `@prompt` into structured, copy-ready prompts for coding, prototyping, planning, and other build-oriented tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keyzzzoe](https://clawhub.ai/user/keyzzzoe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert natural-language requests into clearer prompts for coding, prototyping, product planning, research-style gathering, and multi-step task breakdown. It can also ask restrained clarification questions or answer normally when a prefixed message is casual chat or simple Q&A.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some response labels and examples default to Chinese, which may reduce clarity for non-Chinese users.

Mitigation: Review language fit for the target audience and localize the output contract before deployment when needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/keyzzzoe/skills/prompt-transformer)
- [English Guide](artifact/references/guide-en.md)
- [Chinese Guide](artifact/references/guide-zh.md)
- [Decision Guide](artifact/references/decision-guide.md)
- [Prompt Patterns](artifact/references/prompt-patterns.md)
- [Prompt Transformer Examples](artifact/references/examples.md)
- [Debug / Iteration History](artifact/references/debug-history.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown prompt text with a short handling summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one-turn prompt transformations, minimal clarification questions, or normal chat replies for bypassed inputs.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
