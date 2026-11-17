## Description:

Searches and retrieves public health datasets and records from CDC Open Data through a Socrata-backed MCP server using dataset keywords or IDs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, public health analysts, and agents use this skill to find CDC public datasets by keyword and retrieve rows from known Socrata dataset IDs for analysis or reporting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CDC dataset searches and dataset IDs are sent through a third-party gateway.

Mitigation: Review the gateway operator and privacy terms before installing; do not send private prompts, credentials, or sensitive health information unless those terms are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/b-gutman/skills/pipeworx-cdc)
- [CDC Open Data](https://data.cdc.gov)
- [Pipeworx CDC MCP gateway](https://gateway.pipeworx.io/cdc/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, configuration]

**Output Format:** [Plain text or Markdown summaries of dataset search results and records, plus JSON MCP server configuration for setup.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns public CDC dataset names, descriptions, IDs, update details, and dataset rows when available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
