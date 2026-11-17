## Description:

Generates cross-platform content globalization daily reports by querying RedFoxHub data across WeChat Official Accounts, Douyin, WeChat Channels, Xiaohongshu, Kuaishou, and Bilibili, then clustering topics and summarizing creative trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Content globalization creators, operations teams, MCN agencies, planners, and data analysts use this skill to monitor cross-platform trending content, compare platform and topic performance, and produce daily HTML and Markdown trend reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML reports are built from remote API content and may automatically open in a browser; evidence.security flags unsafe escaping and recommends review before installation.

Mitigation: Review or patch report generation before use so API-sourced fields are escaped, URLs are limited to safe schemes, and browser opening requires explicit consent.

Risk: The skill sends query filters and a RedFoxHub API key to redfox.hk and writes reports or cache files locally.

Mitigation: Install only when comfortable with that data flow, scope and rotate the API key where possible, and treat local reports and cache files as potentially sensitive.

Risk: The subscription feature is identified as unreliable by evidence.security guidance.

Mitigation: Treat subscription output as untrusted until its documentation and behavior are checked in the installed environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/redfox-data/skills/multi-content-feed)
- [Publisher Profile](https://clawhub.ai/user/redfox-data)
- [RedFoxHub](https://redfox.hk)
- [Core Workflow](artifact/references/core_workflow.md)
- [Examples](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML files, Shell commands, Configuration]

**Output Format:** [Markdown summary with a generated HTML daily report and shell commands for the bundled Python workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a REDFOX_API_KEY; may send query filters to redfox.hk and write reports or cache files locally.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
