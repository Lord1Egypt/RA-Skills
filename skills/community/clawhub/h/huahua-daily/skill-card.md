## Description:

Helps agents review HuahuaDaily fund holdings, market data, transactions, quantitative analysis, and community information, and prepare trade or import requests for confirmation in the app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baiye1997](https://clawhub.ai/user/baiye1997)

### License/Terms of Use:

MIT-0

## Use Case:

HuahuaDaily users and their agents can inspect fund portfolios and market activity, analyze investment data, and submit trade or bulk-import requests for confirmation in the HuahuaDaily app. The companion CLI handles local images and large exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portfolio data and Agent Tokens can expose sensitive financial information.

Mitigation: Use a narrowly scoped Agent Token and avoid displaying or sharing the token and unnecessary account details.

Risk: Submitting a local report file may disclose unreviewed contents to a remote service.

Mitigation: Review both the file contents and destination before allowing the report-submit CLI to use a user-provided path.

Risk: Unpinned remote installation commands may retrieve changed code.

Mitigation: Install from a pinned, reviewed release or commit; prefer the official remote MCP or core profile when suitable.

## Reference(s):

- [ClawHub release](https://clawhub.ai/baiye1997/skills/huahua-daily)
- [Portfolio and sync guidance](references/portfolio.md)
- [Fund and market guidance](references/fund-market.md)
- [Trade and import guidance](references/trade-import.md)
- [Local files and exports](references/cli-artifacts.md)
- [Date and safety guidance](references/date-safety.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Natural-language responses with structured results and optional CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Trade and import requests require confirmation in the app; large exports are saved to local files.]

## Skill Version(s):

4.1.14 (source: skill frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
