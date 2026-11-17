## Description:

Autonomous overnight work agent that decomposes research, writing, data, and code-review tasks, works through them with progress logging, and returns structured morning deliverables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fullstackcrew-alpha](https://clawhub.ai/user/fullstackcrew-alpha)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to queue longer-running research, drafting, data cleanup, or code-review work and receive a morning summary plus task-specific deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Overnight autonomous execution can produce incorrect research, writing, data, or code-review conclusions without real-time supervision.

Mitigation: Review the morning summary and final deliverables before relying on them for decisions or publishing them.

Risk: Telegram and webhook notifications can expose task names, paths, or summaries to third-party services.

Mitigation: Keep notifications local unless the Telegram bot and webhook endpoint are trusted, and avoid sensitive task details in notification text.

Risk: The security scan reports privacy and local-execution concerns around notification handling and fallback behavior.

Mitigation: Review and harden webhook validation, Telegram token handling, osascript notification construction, and fallback paths before unattended overnight use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fullstackcrew-alpha/skills/overnight-worker)
- [Task templates](artifact/references/task-templates.md)
- [Output format specifications](artifact/references/output-formats.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, CSV, JSON, progress logs, and notification messages depending on the requested task.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a timestamped work directory with PLAN.md, progress.log, morning-summary.md, and final task deliverables.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
