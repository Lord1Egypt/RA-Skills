## Description:

Hourly Report helps agents set up scheduled Douyin livestream reports that collect live metrics each hour and post Markdown summaries to a DingTalk group.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangfan158](https://clawhub.ai/user/yangfan158)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to configure and run hourly Douyin livestream performance reports, including API-based reporting for regular use and crawl-based reporting for temporary tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crawl mode can produce incomplete or unstable report data and may simulate transaction metrics.

Mitigation: Use API mode for production reporting and label or exclude simulated financial metrics from real business reports.

Risk: The script accepts live URLs and webhook endpoints that can cause unintended browser or network activity if misconfigured.

Mitigation: Restrict liveUrl values to Douyin live pages and DingTalk webhook values to approved DingTalk robot endpoints.

Risk: Browser automation with reduced sandboxing and command-line secrets can increase operational exposure.

Mitigation: Keep Chromium sandboxing enabled where possible, store credentials outside command-line arguments, and pin dependencies with a lockfile.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangfan158/skills/hourly-report)
- [Douyin Open Platform](https://open.douyin.com/)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and Node.js configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces scheduled hourly and daily summary reports for DingTalk; crawl mode may use simulated transaction metrics.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
