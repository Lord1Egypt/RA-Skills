## Description:

Connects to HighGo DB using a bundled HighGo-modified psycopg2 driver with Python 2.7 and SM4 support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ygp987](https://clawhub.ai/user/ygp987)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to connect to HighGo DB and run SQL queries or database validation commands through the bundled driver.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute write-capable SQL against a real HighGo database.

Mitigation: Use a least-privileged, preferably non-production database account and review SQL before execution.

Risk: Database credentials may be exposed when placed directly in command-line DSNs.

Mitigation: Avoid putting passwords in shell history or shared command logs; use protected credential handling where possible.

Risk: The optional --driver path can load arbitrary local driver code.

Mitigation: Use only trusted, integrity-verified driver directories and prefer the bundled driver when appropriate.

## Reference(s):

- [HighGo DB driver details](references/driver_info.md)
- [ClawHub skill page](https://clawhub.ai/ygp987/skills/highgo-db)
- [Publisher profile](https://clawhub.ai/user/ygp987)
- [psycopg project](https://psycopg.org/)
- [PostgreSQL documentation](https://www.postgresql.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce database query results or error messages from the execution script.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
