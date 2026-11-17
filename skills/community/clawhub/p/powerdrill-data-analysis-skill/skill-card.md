## Description:

This skill helps an agent analyze, explore, visualize, and query data using Powerdrill, including dataset management, local file upload, analysis sessions, natural-language analysis jobs, and retrieval of charts, tables, and insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[javainthinking](https://clawhub.ai/user/javainthinking)

### License/Terms of Use:

MIT

## Use Case:

Developers and analysts use this skill to connect an agent to Powerdrill for dataset upload, session management, and natural-language data analysis that can return narrative insights, tables, charts, citations, and follow-up questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local files can be uploaded to Powerdrill for analysis.

Mitigation: Use the skill only with data the user is allowed to send to Powerdrill, and require explicit user confirmation before each file upload.

Risk: Remote Powerdrill datasets and sessions can be deleted through cleanup or delete commands.

Mitigation: Require explicit user confirmation before dataset deletion, session deletion, or cleanup that includes a dataset ID.

Risk: Powerdrill credentials grant access to project resources.

Mitigation: Keep credentials scoped to a limited project and provide them through environment variables only when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/javainthinking/skills/powerdrill-data-analysis-skill)
- [Powerdrill API documentation](https://docs.powerdrill.ai/api-reference/v2)
- [Powerdrill quick start guide](https://docs.powerdrill.ai/developer-guides/quick-start-v2)
- [Powerdrill streaming response handling](https://docs.powerdrill.ai/api-reference/v2/streaming#streaming-response)
- [Powerdrill data source status documentation](https://docs.powerdrill.ai/api-reference/v2/how-to-check-data-sources)
- [Powerdrill MCP Server](https://github.com/powerdrillai/powerdrill-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell and Python examples, and JSON-like Powerdrill API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Powerdrill job responses may include analytical messages, code, table URLs, image URLs, source citations, suggested follow-up questions, and chart metadata; table and image URLs can expire.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
