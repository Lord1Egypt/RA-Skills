## Description:

个人财务管理助手 validates personal finance CSV exports, categorizes transactions, summarizes income and expenses, and generates local finance reports and savings guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzhaofeng-max](https://clawhub.ai/user/wangzhaofeng-max)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to analyze bank or credit-card CSV exports locally, validate required fields, categorize spending, and produce summaries or reports without cloud upload. It is most useful for personal finance review workflows that need account masking and configurable category rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact documents recurring Feishu report delivery, which conflicts with offline/no-network privacy claims for financial data.

Mitigation: Do not enable or copy Feishu cron report configuration unless the schedule, recipient, redaction, and removal process are explicitly controlled.

Risk: Categorized CSV exports may overwrite files or expose sensitive transaction details if paths and spreadsheet handling are careless.

Mitigation: Use cautious output paths, avoid overwriting existing files, and open exported CSVs with spreadsheet formula execution disabled when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangzhaofeng-max/skills/personal-finance-pro)
- [Publisher profile](https://clawhub.ai/user/wangzhaofeng-max)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [category-rules.json](artifact/config/category-rules.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, CSV files, Guidance]

**Output Format:** [Markdown guidance with bash commands, terminal reports, and optional categorized CSV output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes local CSV inputs; masks account numbers in displayed and exported categorized output.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
