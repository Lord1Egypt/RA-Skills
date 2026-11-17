## Description:

Institutional Tracker Ai helps agents scan A-share AI-chain stocks using Tushare data, multi-factor signal scoring, market-regime checks, sentiment inputs, and backtesting to identify possible institutional accumulation signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[casparzhong-cloud](https://clawhub.ai/user/casparzhong-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to run daily scans, generate HTML reports, and backtest possible institutional accumulation signals for A-share AI-chain equities. The outputs are research signals and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the configured Tushare token and market queries to the configured API endpoint.

Mitigation: Use a trusted HTTPS Tushare endpoint, avoid unofficial proxy tokens unless that exposure is acceptable, and rotate the token if it may have been exposed.

Risk: Optional NeoData and Xiaohongshu paths can execute local helper scripts outside the skill package.

Mitigation: Review those helper-script paths before use, disable them when they are not needed, and run the skill in an environment where only trusted local tools are available.

Risk: Generated HTML reports may contain data from a proxy or other external sources.

Mitigation: Treat reports as untrusted output, open them in a controlled browser context, and avoid distributing them as authoritative financial advice.

Risk: The skill produces trading-related research signals that can be incorrect or misleading.

Mitigation: Use the output for research review only and require independent validation before any financial decision.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/casparzhong-cloud/skills/institutional-tracker-ai)
- [Project Homepage](https://github.com/casparzhong-cloud/institutional-tracker-ai)
- [Algorithm Methodology](references/algorithm_methodology.md)
- [Backtest Framework](references/backtest_framework.md)
- [Paper and Open Source Citations](references/paper_citations.md)
- [Install Guide](references/install_guide.md)
- [build-web/ta](https://github.com/build-web/ta)
- [ChipDistribution](https://github.com/liumenglife/ChipDistribution)
- [smart-money-concepts](https://github.com/Siva7891/smart-money-concepts)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands, Python configuration edits, generated JSON score files, and HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, local configuration of a Tushare token and API endpoint, and optional local helper scripts for auxiliary data sources.]

## Skill Version(s):

0.1.0 (source: release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
