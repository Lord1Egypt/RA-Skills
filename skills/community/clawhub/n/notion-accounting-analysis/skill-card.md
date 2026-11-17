## Description:

Analyzes Notion accounting data by reading expense and income data sources, resolving relation-based categories, summarizing finances by time period, category, tag, and large expenses, and generating a Markdown financial report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimislg](https://clawhub.ai/user/jimislg)

### License/Terms of Use:

MIT-0

## Use Case:

External Notion accounting users and agents use this skill to fetch personal or household finance records from Notion, resolve category relations, and produce a readable Markdown financial analysis report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a Notion bearer token for access to financial data.

Mitigation: Use a dedicated least-privilege Notion integration shared only with the required accounting databases, and avoid placing the token directly in shell history or shared logs.

Risk: The generated /workspace finance report may contain sensitive personal or household financial records.

Mitigation: Treat the report as sensitive local data and delete, redact, or restrict access to it when it is no longer needed.

Risk: Financial summaries can be incomplete or misleading if Notion relation pages are inaccessible or database fields do not match the expected schema.

Mitigation: Review unresolved relation IDs and grant the Notion integration access only to the needed pages before relying on the report.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/jimislg/skills/notion-accounting-analysis)
- [ClawHub publisher profile](https://clawhub.ai/user/jimislg)
- [Notion integrations setup](https://www.notion.so/my-integrations)
- [Notion search API endpoint referenced by artifact](https://api.notion.com/v1/search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with console summaries and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a yearly finance report to /workspace when the bundled Node.js script is run.]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact frontmatter says 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
