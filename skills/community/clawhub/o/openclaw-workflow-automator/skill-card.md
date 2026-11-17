## Description:

Automate repeatable workflows with WhatsApp/Telegram notifications, Excel/CSV processing, browser automation, and flexible scheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qashsolutions](https://clawhub.ai/user/qashsolutions)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operations teams, and business users use this skill to turn plain-English workflow requests into approved, scheduled automations for file processing, browser data extraction, API calls, and messaging reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approved workflows can run shell commands and browser actions later without step-by-step supervision.

Mitigation: Use restricted_mode with explicit allowed_commands, review every command and destination URL before approval, and keep sensitive workflows in approval mode.

Risk: Browser automation may retain login sessions and create screenshots or logs containing private data.

Mitigation: Avoid autonomous runs for sensitive sites or private data, use per-workflow browser isolation, clear sessions when possible, and purge screenshots, run logs, audit logs, and browser sessions periodically.

Risk: Schedules may continue executing stale or changed workflow plans.

Mitigation: Use plan hash checks, approval expiry, run budgets, and audit-log review so autonomous runs require periodic reapproval.

Risk: Local workflow artifacts can accumulate across schedules, approvals, sessions, screenshots, and run logs.

Mitigation: Use the data inventory and purge commands to review stored data and delete unneeded workflow records.

## Reference(s):

- [Browser Automation Guide](references/browser-guide.md)
- [Scheduling Guide](references/scheduling-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown workflow plans with inline commands and JSON schedule, notification, and execution records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include approval prompts, browser action descriptions, execution summaries, and local audit or run-log paths.]

## Skill Version(s):

2.0.6 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
