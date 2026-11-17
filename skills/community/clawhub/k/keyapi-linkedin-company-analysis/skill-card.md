## Description:

Explore and analyze LinkedIn companies by retrieving company profiles, employee directories, published posts, job listings with filters, job counts, and individual job details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lycici](https://clawhub.ai/user/lycici)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to collect LinkedIn company intelligence, including company profiles, people, content activity, hiring signals, and job details through KeyAPI's LinkedIn MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled runner can connect to a configurable MCP server and has broader MCP access than the LinkedIn analysis workflow alone requires.

Mitigation: Keep KEYAPI_SERVER_URL unset unless the destination is trusted, and verify commands use the expected LinkedIn platform and tool names before execution.

Risk: KEYAPI_TOKEN and cached API responses may be stored in plaintext workspace files.

Mitigation: Provide KEYAPI_TOKEN through a safer secret mechanism where possible, avoid entering tokens interactively, and use the skill only where plaintext .env and .keyapi-cache files are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lycici/skills/keyapi-linkedin-company-analysis)
- [KeyAPI](https://keyapi.ai/)
- [KeyAPI LinkedIn MCP server](https://mcp.keyapi.ai/linkedin/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured company intelligence reports from cached KeyAPI MCP responses.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
