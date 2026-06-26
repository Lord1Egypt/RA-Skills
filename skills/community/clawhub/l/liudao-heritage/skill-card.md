## Description: <br>
Search, enrich, and manage family heritage and historical relationship data from the Liudao SQLite database for historical figure lookup, relationship-path questions, and privacy-aware personal records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sirius-777-llm](https://clawhub.ai/user/sirius-777-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to answer questions about historical figures, inspect family relationships, and help maintain Liudao heritage records while respecting private-entry access controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access private family records if viewer or creator identifiers are misapplied. <br>
Mitigation: Use only the intended heritage database, pass the correct viewer identifier for private lookups, and confirm authorization before exposing private entries. <br>
Risk: Record insertion or milestone updates may make persistent changes to personal data. <br>
Mitigation: Preview proposed changes before execution and use the skill only where login, permissions, backups, and an undo path are available. <br>


## Reference(s): <br>
- [Liudao Heritage ClawHub page](https://clawhub.ai/sirius-777-llm/liudao-heritage) <br>
- [Liudao database schema](artifact/references/db_schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON-backed text with shell command examples and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read from or propose updates to a SQLite heritage database; record changes should be previewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
