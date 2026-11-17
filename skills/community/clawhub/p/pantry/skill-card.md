## Description:

Organize pantry stock, expiry dates, and shopping lists. Use when adding items, checking inventory, scheduling restocks, setting expiry reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

External users and household operators use Pantry to record pantry inventory, expiry reminders, shopping lists, costs, maintenance notes, and recent activity through a local command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pantry and household notes are saved as plain local log files in ~/.local/share/pantry.

Mitigation: Avoid entering credentials, financial details, sensitive schedules, or private household information.

Risk: CSV exports can carry sensitive household data and may be risky when opened in spreadsheet software.

Mitigation: Review exported CSV files before sharing or opening them in spreadsheet tools.

## Reference(s):

- [Pantry on ClawHub](https://clawhub.ai/xueyetianya/skills/pantry)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands and CLI output; exports may be JSON, CSV, or plain text files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores pantry logs locally under ~/.local/share/pantry and can export logged entries.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter and script report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
