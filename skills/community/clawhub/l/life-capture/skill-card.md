## Description:

Capture daily-life notes into Markdown and SQLite by parsing natural-language entries for expenses, tasks, schedules, reminders, and ideas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[epitomizelu](https://clawhub.ai/user/epitomizelu)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to turn personal life-log notes into organized Markdown records and structured SQLite rows for later review and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted structured input may write Markdown outside the intended daily-notes folder.

Mitigation: Review before installing, avoid saving JSON records from untrusted sources, preview parsed records before writing, and run the skill in a restricted or test directory until path containment is added.

Risk: The skill stores personal life-log data locally in Markdown files and a SQLite database.

Mitigation: Use it only with data you are comfortable storing locally under the configured life directory and database path.

## Reference(s):

- [Parser configuration](references/configuration.md)
- [Example payloads and commands](references/examples.md)
- [Parser config JSON](references/parser_config.json)
- [SQLite schema](references/schema.md)
- [Life Capture ClawHub page](https://clawhub.ai/epitomizelu/skills/life-capture)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Shell commands, Configuration]

**Output Format:** [Markdown summary with parsed JSON records, plus Markdown daily-note files and SQLite database rows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local life-log data under the configured root directory and SQLite database.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
