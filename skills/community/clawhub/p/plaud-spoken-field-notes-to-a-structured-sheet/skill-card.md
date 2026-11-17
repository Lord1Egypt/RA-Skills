## Description:

Turns spoken site-visit notes from Plaud recordings into structured Google Sheets rows for measurements, specs, inspection findings, punch lists, service call notes, and similar field details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and field teams use this skill to process spoken Plaud site-visit dictations into spreadsheet rows without retyping measurements or job details. The workflow is designed for repeated runs that fetch new recordings, extract only spoken values, append rows to Google Sheets, and log processed recordings to avoid duplicates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup includes unpinned remote installers for supporting tools that can access recordings and spreadsheets.

Mitigation: Use pinned or ClawHub-reviewed install paths where available, and verify AgentPMT, Plaud, and Google Sheets permissions before enabling the workflow.

Risk: The workflow processes Plaud recordings and writes extracted content into Google Sheets.

Mitigation: Run it only on recordings and spreadsheets the user is authorized to process, and scope connected tool permissions to the needed accounts and sheets.

Risk: Incorrect field extraction could affect quotes, inspections, or service records.

Mitigation: Review the run summary and flagged blanks before acting on appended sheet rows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/plaud-spoken-field-notes-to-a-structured-sheet)
- [AgentPMT Workflow Page](https://www.agentpmt.com/agent-workflow-skills/plaud-spoken-field-notes-to-a-structured-sheet)
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [Get Users Current Time / Date Tool](https://clawhub.ai/agentpmt/get-users-current-time-date)
- [Plaud Tool](https://clawhub.ai/agentpmt/plaud)
- [Google Sheets Tool](https://clawhub.ai/agentpmt/google-sheets)

## Skill Output:

**Output Type(s):** [guidance, markdown, API calls, configuration, shell commands]

**Output Format:** [Markdown instructions with JSON tool-call examples and shell install commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workflow guidance for agent actions, including local-time handling, Plaud transcript retrieval, spoken-field extraction, Google Sheets appends, duplicate prevention, skipped-recording summaries, and run summaries.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
