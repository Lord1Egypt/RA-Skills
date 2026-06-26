## Description: <br>
Translates natural-language analytics requests into MySQL queries, inspects live database schemas, runs read-only SQL, and validates results before summarizing them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nocb](https://clawhub.ai/user/nocb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data analysts, and database operators use this skill to convert natural-language questions into validated MySQL queries against a live database. It supports schema discovery, cautious read-only execution, query debugging, and preview-only handling for requested write operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can query a live MySQL database, so broad credentials or production access could expose sensitive data. <br>
Mitigation: Use a dedicated read-only database account scoped to the needed schema and avoid production or admin credentials. <br>
Risk: Generated SQL may be incorrect or may not match the user's intended business meaning. <br>
Mitigation: Review important generated SQL and rely on the skill's structural and result validation before acting on outputs. <br>
Risk: Installing database drivers from untrusted sources could introduce supply-chain risk. <br>
Mitigation: Install Python database drivers only from trusted package sources. <br>


## Reference(s): <br>
- [Connection and safety](references/connection-and-safety.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown containing SQL code blocks, validation notes, sample rows, result summaries, assumptions, and caveats.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Result samples are kept small by default; write requests are presented as preview SELECT statements plus unexecuted SQL.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
