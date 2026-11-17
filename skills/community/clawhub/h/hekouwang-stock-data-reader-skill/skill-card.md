## Description:

Reads public A-share stock data through akshare and produces neutral historical recap reports and charts with built-in financial compliance guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huiyonghkw](https://clawhub.ai/user/huiyonghkw)

### License/Terms of Use:

MIT

## Use Case:

External-facing content creators use it to compile public A-share market and company data into neutral post-event recaps, charts, and publication drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was benign but had medium confidence and partial inspection, including of the screenshot script; host permission enforcement was not verified.

Mitigation: Review the skill scripts and confirm that their network and file access fit the intended environment before installation.

Risk: Market data can be incomplete or vary across public data sources, and the report may be mistaken for investment advice.

Mitigation: Check figures against cited source data and company filings, include the data cutoff and fixed risk notice, and keep conclusions descriptive without recommendations or forecasts.

Risk: Fetching data connects to third-party market-data services and writes generated files to the selected output directory.

Mitigation: Confirm the stock code and use the skill's out/ directory or a dedicated output directory before running the fetch step.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huiyonghkw/skills/hekouwang-stock-data-reader-skill)
- [Project homepage (as listed in ClawHub metadata)](https://github.com/huiyonghkw/hekouwang-stock-data-reader-skill)
- [akshare project](https://github.com/akfamily/akshare)
- [Compliance guidance](artifact/references/compliance.md)
- [Report structure](artifact/references/report-structure.md)
- [LHB seat symmetry guidance](artifact/references/lhb-symmetry.md)

## Skill Output:

**Output Type(s):** [CSV data, JSON analysis, Markdown reports, HTML report pages, PNG charts]

**Output Format:** [CSV, JSON, Markdown, HTML, and PNG files]

**Output Parameters:** [1D (one A-share stock code per report run)]

**Other Properties Related to Output:** [Historical public-data recap with source and cutoff notes, a fixed risk notice, and no buy/sell recommendations or price forecasts.]

## Skill Version(s):

1.2.7 (source: release metadata and SKILL.md frontmatter; CHANGELOG top entry is 1.2.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
