## Description:

AIEO monitoring helps agents track brand visibility, answer quality, competitor mentions, and business impact across AI search and chat platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenerlee](https://clawhub.ai/user/kenerlee)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, growth, and analytics teams use this skill to run recurring AIEO checks, compare brand visibility across AI platforms, calculate monitoring metrics, and prepare Markdown reports for follow-up optimization work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser-based monitoring can capture screenshots and AI responses that include unrelated account, chat, customer, analytics, or business data.

Mitigation: Confirm the exact brand, platforms, and test questions before automation; use clean sessions where possible and redact or exclude unrelated sensitive data from screenshots and reports.

Risk: Generated monitoring outputs may contain business conversion data, analytics screenshots, and competitive findings.

Mitigation: Store the monitoring/ directory in a restricted location, share reports only with the intended team, and delete stale screenshots or reports when they are no longer needed.

Risk: Broad auto-trigger phrases could start monitoring work before the user has confirmed scope.

Mitigation: Ask for confirmation of brand, monitoring cadence, target platforms, and question set before collecting data or writing monitoring artifacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kenerlee/skills/moments-aieo-monitoring)
- [Monitoring metrics reference](artifact/references/monitoring_metrics.md)
- [Tools guide](artifact/references/tools_guide.md)
- [Monitoring report template](artifact/assets/monitoring_report_template.md)
- [Tracking spreadsheet template](artifact/assets/tracking_spreadsheet.md)
- [Quick check template](artifact/assets/quick_check_template.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, Markdown tracking tables, metric calculations, browser automation steps, and screenshot file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates monitoring reports and evidence under a monitoring/ directory when used by an agent with file and browser automation access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
