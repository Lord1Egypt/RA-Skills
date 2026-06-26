## Description: <br>
Helps agents turn natural-language data questions into SQL-oriented workflows with query classification, schema context generation, confidence scoring, clarification, fallback review, and audit logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abhinas90](https://clawhub.ai/user/abhinas90) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data teams use this skill to add natural-language database querying workflows to OpenClaw agents, including schema inspection, confidence-based routing, user clarification, human review fallback, and local audit trails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Database connection details or credentials may be exposed through database URLs or generated schema context. <br>
Mitigation: Use read-only database credentials, avoid embedding passwords in database URLs, and manage secrets outside skill inputs and generated files. <br>
Risk: Audit databases and exported JSON files may contain sensitive user queries, generated SQL, user IDs, session IDs, or business data. <br>
Mitigation: Restrict permissions on audit.db and exported JSON files, and add redaction, retention, and authorization controls before production use. <br>
Risk: Automatically executing generated SQL can expose incorrect or overbroad data when confidence routing is misconfigured. <br>
Mitigation: Keep database credentials read-only and require clarification or human review for lower-confidence, ambiguous, or safety-sensitive queries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abhinas90/nl-to-sql-query-builder) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with Python components, shell commands, and JSON outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local SQLite audit databases and exported JSON files containing query, user, schema, or generated SQL data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
