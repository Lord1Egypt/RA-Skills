## Description: <br>
Life Capture parses daily-life notes into structured records, writes daily markdown notes, and syncs expenses, tasks, schedules, and ideas into a local SQLite database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[epitomizelu](https://clawhub.ai/user/epitomizelu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to capture personal life-log entries from natural language, classify them as expenses, tasks, schedules, or ideas, and persist them for later review and reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Personal journal entries may include sensitive details and are stored durably in local markdown and SQLite files. <br>
Mitigation: Keep the life folder private and avoid saving secrets or highly sensitive details. <br>
Risk: Natural-language parsing can be ambiguous before records are written. <br>
Mitigation: Use the parse-only workflow to review structured output before saving ambiguous entries. <br>


## Reference(s): <br>
- [Life Capture on ClawHub](https://clawhub.ai/epitomizelu/life-capture) <br>
- [Parser configuration](references/configuration.md) <br>
- [Example payloads and commands](references/examples.md) <br>
- [Schema](references/schema.md) <br>
- [Parser config JSON](references/parser_config.json) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Files] <br>
**Output Format:** [Markdown response with JSON record blocks, plus local daily markdown files and SQLite rows.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local paths under life/ and life/db/life.db; preserves raw user text and leaves unknown fields null.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
