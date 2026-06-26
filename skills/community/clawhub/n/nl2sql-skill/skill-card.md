## Description: <br>
Converts natural-language data questions into read-only SQL queries, repairs query failures, and produces natural-language answers and Markdown analysis reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shlysz](https://clawhub.ai/user/shlysz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data analysts, and agent builders use this skill to turn business questions into database queries and structured analysis reports. It is intended for natural-language data lookup, SQL drafting, query-result explanation, and Markdown reporting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SQL could access sensitive or overly broad data if connected to unrestricted databases. <br>
Mitigation: Use a least-privilege read-only database account and restrict available schemas, tables, and rows before enabling the skill. <br>
Risk: Generated or repaired queries may be incorrect, misleading, or expensive to execute. <br>
Mitigation: Review queries before execution where appropriate, enforce query timeouts and result limits, and use logging and result redaction for sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/shlysz/nl2sql-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown report with SQL code blocks and natural-language analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces SELECT or WITH SQL guidance, natural-language answers, and optional follow-up query suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
