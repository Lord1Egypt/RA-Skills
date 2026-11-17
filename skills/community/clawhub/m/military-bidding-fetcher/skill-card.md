## Description:

Fetches Chinese military procurement notices from three named procurement sites, filters them by bidding keywords and exclusions, and generates an Excel opportunity report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangpengle](https://clawhub.ai/user/zhangpengle)

### License/Terms of Use:

MIT-0

## Use Case:

Business development, capture, and procurement-monitoring users use this skill to collect recent military procurement notices, filter them by keywords, exclusions, and region, and produce a ranked Excel report for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated spreadsheets include untrusted text from remote procurement websites and the security evidence notes that this text is not formula-sanitized.

Mitigation: Treat generated workbooks as untrusted input, review them before sharing, and open them with spreadsheet protections appropriate for external data.

Risk: Local .env settings can change proxy behavior and output paths.

Mitigation: Run the skill from a controlled directory and review local configuration before execution, especially FETCHER_USE_PROXY, FETCHER_PROXY, and output settings.

Risk: The skill contacts named procurement websites and writes an Excel report locally.

Mitigation: Use it only where network access to those sites and local report generation are permitted by the user's organization.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangpengle/skills/military-bidding-fetcher)
- [Publisher profile](https://clawhub.ai/user/zhangpengle)
- [All-army weapon equipment procurement information network](https://www.weain.mil.cn/)
- [Military procurement network](https://www.plap.mil.cn/)
- [National University of Defense Technology procurement information](https://www.nudt.edu.cn/cgxx/index.htm)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Console text plus an Excel workbook (.xlsx)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workbook contains separate sheets for the configured procurement sources and includes keyword-based recommendation fields.]

## Skill Version(s):

0.2.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
