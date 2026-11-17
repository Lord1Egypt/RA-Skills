## Description:

国家统计局数据采集技能帮助代理规划、采集、处理和核验国家统计局宏观经济数据，包括GDP、CPI、PPI、产出缺口和Excel交付物。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yingjie-zhang-dev](https://clawhub.ai/user/yingjie-zhang-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, and developers use this skill to assemble Chinese macroeconomic datasets from NBS sources, document source links, calculate derived indicators such as output gap and GDP deflator estimates, and prepare Excel-based deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The crawler may overstate collection capability because the included script currently creates placeholder records with empty data values instead of fetching real NBS records.

Mitigation: Treat generated datasets as drafts until values are verified against official NBS publications or another trusted source.

Risk: The link verification script can make network requests to hyperlinks found in user-supplied Excel workbooks.

Mitigation: Run link verification only on trusted workbooks or after restricting URLs to official NBS domains.

Risk: Scripts that add charts or fix hyperlinks can save Excel files in place.

Mitigation: Keep a backup copy of workbooks before running scripts that modify files.

## Reference(s):

- [Workflow](references/workflow.md)
- [Indicator Notes](references/indicators.md)
- [Data Source URLs](references/sources.md)
- [National Bureau of Statistics of China](https://www.stats.gov.cn)
- [NBS Data Platform](https://data.stats.gov.cn)
- [NBS Data Releases](https://www.stats.gov.cn/sj/zxfb/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, Markdown]

**Output Format:** [Markdown guidance with shell commands and Python script references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify Excel workbooks, CSV checkpoints, and raw JSON data files when the bundled scripts are run.]

## Skill Version(s):

1.0.0 (source: server release evidence and README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
