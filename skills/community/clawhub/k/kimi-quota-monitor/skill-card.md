## Description:

Kimi Quota Monitor helps an agent configure and run Kimi membership quota checks, calculate monthly quota-cycle usage, and prepare daily WeChat reports through openclaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawntribbiani](https://clawhub.ai/user/shawntribbiani)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor Kimi Chat subscription quota, calculate quota-cycle usage against a monthly reset schedule, troubleshoot quota fetching, and configure daily WeChat quota reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable Kimi cookies and localStorage tokens may expose the user's account if committed, shared, or stored with broad local permissions.

Mitigation: Keep configured files and kimi_cookies.json out of source control, use a private trusted environment, and restrict permissions on configuration and log files.

Risk: A scheduled cron job repeatedly uses the user's Kimi session and sends messages through openclaw.

Mitigation: Confirm the openclaw-weixin target before scheduling, monitor logs, and disable or rotate credentials when access is no longer needed.

Risk: Debug page-body logging may reveal sensitive page content in local logs.

Mitigation: Remove or disable debug page-body logging before routine use.

## Reference(s):

- [Kimi Quota Monitor Skill](https://clawhub.ai/shawntribbiani/skills/kimi-quota-monitor)
- [Kimi subscription quota page](https://www.kimi.com/membership/subscription)
- [Quota rules](artifact/quota_rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated quota report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied Kimi cookies, localStorage tokens, and an openclaw-weixin target before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
