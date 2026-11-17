## Description:

Automatically queries and reports domestic and international gold prices every hour.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongjiahao371-pixel](https://clawhub.ai/user/hongjiahao371-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Users who monitor gold prices can run this skill manually or schedule it hourly to report Gold 9999, major brand gold, and bank gold bar prices from huangjinjiage.cn. Its output is informational and should be independently verified before financial decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reported prices come from a single website over HTTP and may be incorrect, stale, or modified in transit.

Mitigation: Verify prices against independent trusted sources before using them for financial decisions, and prefer an HTTPS or authenticated data source when adapting the skill.

Risk: Scheduled execution depends on a sibling Playwright scraper and an unchecked directory change, which can cause silent failures or unexpected script execution if the path is wrong.

Mitigation: Review the sibling scraper before installation, add an explicit directory-change failure check, and run scheduled jobs with least-privilege permissions.

Risk: The parser extracts matching price text from page output, so website layout changes can produce incomplete or misleading reports.

Mitigation: Monitor scheduled output, alert on empty or malformed reports, and validate extracted prices before sharing them downstream.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/hongjiahao371-pixel/skills/gold-price-auto)
- [Publisher profile](https://clawhub.ai/user/hongjiahao371-pixel)
- [Gold price data source](http://www.huangjinjiage.cn/jinrijinjia.html)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text report with optional shell and cron commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports extracted price strings in yuan per gram; no structured output contract is documented.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
