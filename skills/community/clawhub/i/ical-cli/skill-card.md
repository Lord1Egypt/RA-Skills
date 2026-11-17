## Description:

ical helps agents manage macOS Calendar events and calendars from the terminal using the ical CLI, including CRUD operations, natural-language dates, recurrence, alerts, import/export, and multiple output formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bro3886](https://clawhub.ai/user/bro3886)

### License/Terms of Use:


## Use Case:

Developers, external users, and agent workflows on macOS use this skill to inspect, create, update, delete, import, and export Apple Calendar data through terminal commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to read and modify local Apple Calendar data.

Mitigation: Grant Calendar permissions only after reviewing the release and confirming that calendar access is intended.

Risk: Delete, update, and import workflows can make calendar changes, and --force skips confirmation prompts.

Mitigation: Require explicit approval of exact event IDs, calendars, date ranges, and files before allowing destructive or bulk commands.

Risk: The ical skills install command writes skill files into supported agent skill directories.

Mitigation: Treat skill installation as a local agent behavior change and review the installed files before use.

Risk: Installing with @latest may pull an unpinned release.

Mitigation: Use a pinned, trusted release version where possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bro3886/skills/ical-cli)
- [Complete Command Reference](references/commands.md)
- [Natural Language Date Reference](references/dates.md)
- [go-eventkit Docs](https://github.com/BRO3886/go-eventkit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, command arguments, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON, CSV, or ICS command examples when guiding export/import workflows.]

## Skill Version(s):

0.6.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
