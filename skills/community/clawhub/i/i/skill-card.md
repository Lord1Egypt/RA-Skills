## Description:

Memo helps an agent record work notes, search saved history, manage todos, and generate work-summary reports from a local JSON record store.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qu8](https://clawhub.ai/user/qu8)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and individual users use Memo to capture conversational work notes, query prior records, track unfinished todos, and export structured Markdown summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores work notes locally and may display saved note contents in chat.

Mitigation: Use it only for notes appropriate for local storage and ask before revealing broad sets of saved records.

Risk: The skill can create, update, or pause WorkBuddy reminders and includes guidance for direct automation database access.

Mitigation: Review reminder changes before applying them and prefer constrained automation tooling over direct database edits.

Risk: Report exports may write Markdown files outside a dedicated notes folder when a custom path is supplied.

Mitigation: Confirm custom export paths and restrict routine exports to a known Memo or WorkBuddy directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qu8/skills/i)
- [WorkBuddy documentation](https://www.codebuddy.cn/docs/workbuddy/Overview)
- [Field recognition rules](artifact/references/field-rules.md)
- [Report format](artifact/references/report-format.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chat responses, JSON records, Markdown reports, Python API and CLI examples, and automation configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores records in a local records.json file and can export reports as Markdown files.]

## Skill Version(s):

2.0.1 (source: frontmatter, skill.yaml, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
