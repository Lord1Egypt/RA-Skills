## Description:

Complete MILKEE accounting integration for Swiss businesses, covering projects, customers, time tracking, tasks, products, daily summaries, and fuzzy project matching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xenofex7](https://clawhub.ai/user/xenofex7)

### License/Terms of Use:


## Use Case:

Swiss business operators, consultants, and agents use this skill to read and modify MILKEE accounting records, including customers, projects, products, tasks, and billable time entries.

### Deployment Geography for Use:

Switzerland

## Known Risks and Mitigations:

Risk: The skill can read and modify MILKEE business records such as customers, projects, products, tasks, and time entries.

Mitigation: Install only with a MILKEE account whose API token has the intended authority, and review proposed record-changing actions before execution.

Risk: The documentation includes realistic credential examples that could be copied into logs, chat, shell history, or committed configuration.

Mitigation: Use only your own MILKEE token, treat it as a secret, and rotate any token that may have been exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xenofex7/skills/milkee)
- [MILKEE API Documentation](https://apidocs.milkee.ch/api)
- [MILKEE Authentication Documentation](https://apidocs.milkee.ch/api/authentifizierung.html)
- [API Endpoints Reference](references/api-endpoints.md)
- [Configuration Guide](references/configuration.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Command-line text output with Markdown setup documentation and inline shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses MILKEE_API_TOKEN and MILKEE_COMPANY_ID environment variables; stores local timer state in ~/.milkee_timer.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
