## Description: <br>
Manages macOS Calendar events and calendars from the terminal with the ical CLI, including CRUD operations, natural language dates, recurrence rules, alerts, interactive mode, import/export, and multiple output formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BRO3886](https://clawhub.ai/user/BRO3886) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and end users use this skill to manage Apple Calendar from an agent or terminal workflow, automate calendar tasks, and generate scripts around the macOS ical CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The ical CLI can read, create, update, import, export, and delete macOS Calendar data after Calendar access is granted. <br>
Mitigation: Install only if the upstream CLI is trusted, scope agent actions to specific calendars and date ranges, and treat exported calendar files as sensitive data. <br>
Risk: Deletes, imports, calendar deletion, --force, and skill install or uninstall commands can make broad or irreversible changes. <br>
Mitigation: Require explicit user approval before these actions and use exact event IDs where possible. <br>


## Reference(s): <br>
- [Command Reference](references/commands.md) <br>
- [Natural Language Date Reference](references/dates.md) <br>
- [go-eventkit API](https://github.com/BRO3886/go-eventkit) <br>
- [ClawHub Skill Page](https://clawhub.ai/BRO3886/ical-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include calendar command suggestions, import/export guidance, and user-approval checkpoints for destructive calendar actions.] <br>

## Skill Version(s): <br>
0.6.0 (source: server release metadata; artifact frontmatter lists 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
