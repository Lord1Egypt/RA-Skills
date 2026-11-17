## Description:

Maintenance helps users log home maintenance tasks, set reminders, track repair history, manage inventory, and export local records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to keep a local record of household maintenance, repair schedules, appliance upkeep, costs, checklists, and inventory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Maintenance notes, schedules, costs, and inventory are stored as plaintext under ~/.local/share/maintenance.

Mitigation: Avoid entering secrets or highly sensitive household details, and restrict access to the local account and data directory.

Risk: CSV and JSON exports are not safely encoded.

Mitigation: Treat exported files cautiously, sanitize them before sharing or opening in other tools, and avoid exporting sensitive entries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/maintenance)
- [Publisher homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands; CLI output and exports may be text, JSON, CSV, or plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local records under ~/.local/share/maintenance and can export JSON, CSV, or text files.]

## Skill Version(s):

2.0.1 (source: release evidence; artifact frontmatter and script report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
