## Description:

妙想自选管理skill，基于东方财富通行证账户数据及行情底层数据构建，支持通过自然语言查询、添加、删除自选股。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jessecq1995](https://clawhub.ai/user/jessecq1995)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query, add, and delete Eastmoney account stock watchlist entries through command-line or natural-language commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Free-form input may add or delete authenticated watchlist entries without a separate confirmation step.

Mitigation: Use explicit query, add, or delete commands when possible and review natural-language commands before execution.

Risk: The skill uses an Eastmoney API key and writes account-related watchlist output files.

Mitigation: Keep MX_APIKEY out of shared project files and use a private output directory for generated CSV and raw JSON files.

Risk: The release evidence reports a suspicious security verdict due to authenticated account-data handling with limited safeguards.

Mitigation: Review the skill before installing and use it only in trusted runtime environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jessecq1995/skills/mx-selfselect)
- [Publisher profile](https://clawhub.ai/user/jessecq1995)
- [Eastmoney API host](https://mkapi2.dfcfs.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Console text with generated CSV and raw JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MX_APIKEY and can write output files under a configured output directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
