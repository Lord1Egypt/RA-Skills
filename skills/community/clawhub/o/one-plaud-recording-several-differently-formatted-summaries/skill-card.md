## Description:

This skill guides an agent to read a Plaud transcript once, generate every user-defined summary format from the same source text, write the results to Google Docs, and log processed recordings in Google Sheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use this skill to turn new Plaud recordings into several audience-specific summaries in one run, such as recaps, decisions-only notes, and action lists. It is useful when summary formats are configured in Google Sheets and final outputs should be collected in Google Docs with a processed-recording log.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles sensitive Plaud transcripts and writes derived notes to Google Docs and Google Sheets.

Mitigation: Grant Plaud, Google Sheets, and Google Docs only the minimum permissions needed, and confirm document and sheet sharing settings before use.

Risk: Mutable install or update instructions and referenced AgentPMT skills can change behavior after review.

Mitigation: Review and pin the installer path and referenced AgentPMT skills before use.

Risk: Recording timestamps can be misfiled if Plaud local names and UTC fields are compared without timezone conversion.

Mitigation: Resolve the user's timezone first, treat start_at as UTC, convert it to local time, and filter recordings only after conversion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/one-plaud-recording-several-differently-formatted-summaries)
- [AgentPMT workflow page](https://www.agentpmt.com/agent-workflow-skills/one-plaud-recording-several-differently-formatted-summaries)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [Get Users Current Time / Date skill](https://clawhub.ai/agentpmt/get-users-current-time-date)
- [Google Sheets skill](https://clawhub.ai/agentpmt/google-sheets)
- [Plaud skill](https://clawhub.ai/agentpmt/plaud)
- [Google Docs Connector skill](https://clawhub.ai/agentpmt/google-docs-connector)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Markdown, Text, Configuration]

**Output Format:** [Markdown workflow instructions with JSON and shell-command examples; agent outputs are Google Docs sections and Google Sheets log rows.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a user-selected recording window, Plaud transcript data, and Google Sheets format definitions to produce one document per recording.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
