## Description:

个人记账 helps an agent record personal income and expenses from Chinese text or receipt images, store daily bill files, and summarize daily or monthly spending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jzw6](https://clawhub.ai/user/jzw6)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill for deliberate personal bookkeeping in Chinese, including recording income and expenses from text or receipt images and reviewing daily or monthly totals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically persist sensitive personal finance records from broad triggers, including image-only messages.

Mitigation: Use it only for deliberate personal bookkeeping, confirm ambiguous image-derived amounts before recording, and treat the bills directory as sensitive personal financial data.

Risk: Unsafe command-invocation guidance could expose the record script to incorrectly constructed shell commands.

Mitigation: Call record_bill.py with structured arguments instead of constructing a shell command string from user content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jzw6/skills/personal-accounting)
- [消费分类参考](references/categories.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with JSON command results and local Markdown bill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates bills/YYYY-MM-DD.md files and can return daily or monthly summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
