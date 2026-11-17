## Description:

Log Analyzer monitors cron, system, and application logs to detect errors, analyze patterns, generate reports, and send Discord notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnyhot](https://clawhub.ai/user/sunnyhot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor OpenClaw cron logs and other configured log sources, identify failures or performance warnings, and produce operational summaries. It can also prepare notifications for configured Discord delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Operational log content may be sent to a fixed Discord destination.

Mitigation: Remove the hard-coded Discord target, make external notifications opt-in, and require the operator to configure an approved destination.

Risk: Log data can contain credentials, personal data, or other sensitive operational details.

Mitigation: Add secret redaction before reports are printed, stored, or sent externally, and limit log sources to explicitly approved paths.

Risk: Shell-string command execution can allow command injection through report content.

Mitigation: Replace shell-string execSync notification calls with an argument-based command invocation or a safer API call.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunnyhot/skills/openclaw-log-analyzer)
- [Publisher profile](https://clawhub.ai/user/sunnyhot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with summary text, JSON status data, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can include log excerpts, detected error counts, warning summaries, performance metrics, and notification text.]

## Skill Version(s):

1.0.0 (source: evidence release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
