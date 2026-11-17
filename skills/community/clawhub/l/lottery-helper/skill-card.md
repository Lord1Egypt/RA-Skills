## Description:

彩票助手 queries draw results for 双色球, 大乐透, 排列三, 排列五, 福彩3D, 北京快乐8, 七乐彩, and 七星彩; exports results to txt, markdown, XLSX, or SQLite; and can generate entertainment-only number recommendations with stated rationale.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuce1ge](https://clawhub.ai/user/zhuce1ge)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to retrieve Chinese lottery draw data, export it in common file formats, and request clearly disclaimed entertainment-only number recommendations based on historical data analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated XLSX files can contain unvalidated external lottery data.

Mitigation: Review exported data before opening or sharing spreadsheets, use spreadsheet protections, and prefer txt, markdown, or SQLite export when Excel output is not needed.

Risk: The skill contacts data.17500.cn and depends on that third-party data source.

Mitigation: Use the skill only when contacting that host is acceptable, and review the destination and returned data before relying on results.

Risk: Lottery recommendations could be misunderstood as predictive or financial advice.

Mitigation: Keep the skill's disclaimer with recommendation output and treat recommendations as entertainment only, not as a promise of improved odds.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuce1ge/skills/lottery-helper)
- [Lottery data API reference](references/apis.md)
- [Lottery odds reference](references/odds.md)
- [17500 lottery data endpoint pattern](https://data.17500.cn/{code}_{asc|desc}.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown or plain text responses with optional txt, md, xlsx, and sqlite export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call data.17500.cn and write local export files when the user requests export.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
