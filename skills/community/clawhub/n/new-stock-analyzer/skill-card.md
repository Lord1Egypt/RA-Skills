## Description:

New Stock Analyzer helps OpenClaw users query and analyze A-share IPO subscriptions using public market data sources, with risk scoring, subscription suggestions, and scheduled session notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[future2017](https://clawhub.ai/user/future2017)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to monitor upcoming A-share IPO subscriptions, compare public data sources, review generated risk assessments, and receive daily or weekly IPO reports. Developers may also use it as a Python-based market-data automation workflow with local caching and cron scheduling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can add a persistent daily cron job.

Mitigation: Install and test in an unprivileged account, review the generated crontab entry before enabling it, and document a clear uninstall path for the scheduled job.

Risk: Some financial-data requests use insecure HTTP endpoints.

Mitigation: Switch supported data sources to verified HTTPS endpoints before relying on reports for operational use.

Risk: Generated notices include a hardcoded private-network service URL.

Mitigation: Remove or replace the private-network URL before deployment so notifications do not expose environment-specific internal addresses.

Risk: The skill produces IPO subscription suggestions and position guidance.

Mitigation: Treat outputs as informational market summaries only and preserve clear user-facing language that the reports are not investment advice.

Risk: Python package requirements are version ranges rather than pinned dependencies.

Mitigation: Use a dedicated virtual environment and pin dependency versions for reviewed deployments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/future2017/skills/new-stock-analyzer)
- [Publisher profile](https://clawhub.ai/user/future2017)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)
- [CFI new stock data source](https://newstock.cfi.cn/)
- [Eastmoney IPO data endpoint](http://datacenter-web.eastmoney.com/api/data/v1/get)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and terminal text with optional shell commands and YAML configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include IPO summaries, per-stock risk assessments, subscription suggestions, OpenClaw notification text, and scheduled-job setup guidance.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
