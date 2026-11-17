## Description:

收入追踪器 - 多平台收入记录、统计分析、趋势图表。适用于自由职业者、创作者、副业者。

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

Freelancers, creators, side-business operators, and small teams use this skill to record multi-source income, review income statistics, analyze source mix, generate trend views, and export local income records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive income records in a local JSON file and can export those records.

Mitigation: Use a private DATA_PATH, restrict file permissions, and avoid storing real income data in shared or synced locations unless encryption and access controls are in place.

Risk: CSV exports may include user-provided notes or sources that are unsafe to open directly in spreadsheet software.

Mitigation: Review and sanitize exported CSV content before opening it in spreadsheet tools or sharing it with others.

Risk: The lockfile contains insecure dependency download URLs.

Mitigation: Regenerate the lockfile with HTTPS registry URLs and remove unnecessary dependencies before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onlyloveher/skills/income-tracker-zhouli)
- [Clawdis homepage](https://clawhub.com/skills/income-tracker)

## Skill Output:

**Output Type(s):** [Text, JSON, CSV, Analysis]

**Output Format:** [JSON results with human-facing status text, ASCII charts, and CSV/JSON export payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local JSON data file controlled by DATA_PATH and defaults to CNY as the base currency.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
