## Description:

A Chinese-language OpenClaw expense-tracking skill that records expenses from natural-language input, categorizes spending, summarizes day/week/month totals, and stores entries in a local JSON file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glorysunshine](https://clawhub.ai/user/glorysunshine)

### License/Terms of Use:

MIT

## Use Case:

Individuals and developers use this skill to record personal spending in Chinese, query recent expense history, and review category-based spending summaries without relying on a remote service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Expense history is stored in a plaintext local data.json file.

Mitigation: Use the skill only in protected local directories, remove bundled sample data before real use, and avoid shared machines unless filesystem permissions protect the skill directory.

Risk: The release includes packaging cleanup issues and a malformed skill.json file.

Mitigation: Validate package metadata and repair or remove malformed files before production distribution.

Risk: The @openclaw/sdk dependency is declared with a floating compatible-version range.

Mitigation: Pin or remove the dependency before production use when reproducible installs are required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/glorysunshine/skills/openclaw-expense-tracker)
- [Publisher Profile](https://clawhub.ai/user/glorysunshine)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown responses with natural-language examples, command snippets, and JavaScript implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runtime skill returns Chinese text responses for expense entries, recent records, and spending summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
