## Description: <br>
Generates concise morning briefings for Argentina and LATAM with local date formatting, workweek context, Argentine holidays, optional agenda items, and fiscal due dates when a related calendar skill is installed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[centriqs](https://clawhub.ai/user/centriqs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and small-business users in Argentina and LATAM use this skill to start the day with a short briefing that combines calendar context, holidays, personal agenda entries, and optional fiscal reminders. <br>

### Deployment Geography for Use: <br>
Argentina and LATAM <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read local briefing configuration and agenda files, which can contain sensitive meeting or client details. <br>
Mitigation: Keep confidential details and full tax identifiers out of local briefing files, and use the briefing only in private one-to-one contexts. <br>
Risk: Casual aliases such as morning greetings may activate the skill and reveal local agenda details. <br>
Mitigation: Use explicit commands such as "briefing hoy" when accidental activation would be a concern. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/centriqs/latam-timezone-briefing) <br>
- [Publisher profile](https://clawhub.ai/user/centriqs) <br>
- [Centriqs homepage](https://centriqs.io) <br>
- [argentina-fiscal-calendar related skill](https://clawhub.ai/centriqs/argentina-fiscal-calendar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style briefing text with optional shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Offline output; may include local agenda details when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
