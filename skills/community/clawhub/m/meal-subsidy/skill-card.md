## Description:

Automates 2hao HR meal-subsidy requests by reading attendance, checking late-departure eligibility, and filling and submitting eligible claims for a date, week, or month.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamy-lei](https://clawhub.ai/user/jamy-lei)

### License/Terms of Use:

MIT-0

## Use Case:

Employees using 2hao HR use this skill to check whether attendance records meet meal-subsidy rules and submit eligible claims for a specific date, the current week, or a month.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit HR meal-subsidy claims through a remotely debuggable browser.

Mitigation: Run it only in an isolated, trusted user account or disposable browser profile and require confirmation before each HR submission.

Risk: Chrome remote debugging can expose an authenticated browser session if it is left open.

Mitigation: Open the debugging port only while running the skill, close it afterward, and avoid shared machines or untrusted networks.

Risk: Generated screenshots, CSVs, logs, and browser profile data can contain sensitive work records.

Mitigation: Store generated files in a restricted location, clean them after review, and avoid sharing the artifacts.

Risk: The script may launch Chrome with `--no-sandbox` during automatic startup.

Mitigation: Remove `--no-sandbox` where possible and run the browser with least-privilege account permissions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jamy-lei/skills/meal-subsidy)
- [2hao HR Desk](https://i-wework.2haohr.com/desk/home)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Markdown guidance with CLI commands plus generated PNG screenshots, CSV records, and log text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Playwright with an authenticated Chrome session; generated files may include attendance screenshots, form screenshots, late-record CSVs, and logs.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
