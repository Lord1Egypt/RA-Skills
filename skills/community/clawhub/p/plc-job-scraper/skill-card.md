## Description:

Automaticky vyhledává PLC, automation a SCADA pracovní nabídky z LinkedIn, Indeed a dalších job boardů.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjmore66](https://clawhub.ai/user/cjmore66)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, automation engineers, PLC programmers, and technical job seekers use this skill to configure and run searches for PLC, automation, and SCADA job listings, then export results for review or follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a changeable third-party Apify actor for scraping.

Mitigation: Review the referenced actor before running it and prefer a pinned or trusted actor version.

Risk: Optional Google Sheets, Telegram, or scheduled automation can send job-search data externally or consume account resources repeatedly.

Mitigation: Use a dedicated least-privilege Apify token and enable external exports, notifications, or cron runs only after confirming the data-sharing and account-resource impact.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cjmore66/skills/plc-job-scraper)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, CSV, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON/CSV job-result outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May export job results to CSV or Google Sheets and optionally support recurring runs or notifications.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
