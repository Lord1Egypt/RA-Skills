## Description:

Track oven usage and cooking schedules. Use when logging bake sessions, setting cook reminders, checking inventory, reviewing stats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use Oven to log bake sessions, inventory, schedules, reminders, maintenance, usage, costs, and tips, then review, search, or export local oven history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Logged oven entries and exports are saved locally in plaintext under ~/.local/share/oven.

Mitigation: Avoid entering sensitive personal or confidential details, and review or delete local logs and exports before sharing the machine or backups.

Risk: CSV exports may contain user-entered values that spreadsheet software can interpret as formulas.

Mitigation: Review or sanitize CSV exports before opening them in spreadsheet software or sharing them with others.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bytesagain3/skills/oven)
- [Publisher Profile](https://clawhub.ai/user/bytesagain3)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Files]

**Output Format:** [Command-line text output and local JSON, CSV, or TXT exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local plaintext logs and exports under ~/.local/share/oven.]

## Skill Version(s):

2.0.1 (source: server release evidence and target metadata; artifact frontmatter/script report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
