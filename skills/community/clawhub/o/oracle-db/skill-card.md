## Description:

Write Oracle SQL and PL/SQL with proper syntax, hints, and performance patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and database engineers use this skill for Oracle SQL and PL/SQL syntax help, performance patterns, transaction behavior, bind variables, hints, and common Oracle-specific traps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may help draft SQL or PL/SQL that changes database state or production data.

Mitigation: Review generated statements before execution, especially DDL, COMMIT, and statements run against production databases.

Risk: Dynamic SQL can introduce injection vulnerabilities when untrusted input is concatenated into statements.

Mitigation: Prefer bind variables and avoid concatenating untrusted input into dynamic SQL.

## Reference(s):

- [Oracle DB on ClawHub](https://clawhub.ai/ivangdavila/skills/oracle-db)
- [Publisher profile: ivangdavila](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with inline SQL, PL/SQL, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May draft database-changing SQL; review statements before running them against production data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
