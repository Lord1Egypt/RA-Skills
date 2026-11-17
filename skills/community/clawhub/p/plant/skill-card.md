## Description:

Manage houseplant care with watering and fertilizer schedules. Use when adding plants, tracking watering, scheduling fertilizing, setting care reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

External users use Plant to manage local houseplant care notes, including watering, fertilizing, reminders, inventory, reports, and care activity history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local plant or household-care records may include sensitive personal or financial details.

Mitigation: Keep entries limited to plant-care information and review local records before sharing exported files.

Risk: CSV export values are not safely escaped before opening in spreadsheet software.

Mitigation: Inspect and sanitize exported CSV values before opening them in spreadsheets or sharing them with others.

## Reference(s):

- [Plant on ClawHub](https://clawhub.ai/xueyetianya/skills/plant)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON, CSV]

**Output Format:** [Terminal text with optional JSON, CSV, or plain text exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local records under ~/.local/share/plant and can export logged entries for backup.]

## Skill Version(s):

2.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
