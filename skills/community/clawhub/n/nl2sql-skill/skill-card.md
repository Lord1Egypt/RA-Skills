## Description:

Converts natural-language data questions into read-only SQL queries and Markdown analysis reports using a staged multi-agent workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shlysz](https://clawhub.ai/user/shlysz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data analysts use this skill to turn natural-language business questions into SQL, interpret query results, and produce structured Markdown data analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-driven database reads may expose sensitive tables or data outside the intended analysis scope.

Mitigation: Connect the agent through database-side read-only roles scoped to expected schemas and avoid highly sensitive tables unless users explicitly expect analysis of that data.

Risk: Generated SQL or analysis reports may be incomplete or misleading if schema linking, query repair, or supplemental queries choose the wrong fields.

Mitigation: Review generated SQL, query results, and report conclusions before using them for business decisions.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown reports with SQL code blocks and concise natural-language answers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces read-only SELECT/WITH SQL and reports failures after bounded self-repair attempts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
