## Description:

Enables agents to analyze, explore, visualize, and query datasets through Powerdrill by managing datasets, uploading data sources, creating sessions, and running natural-language analysis jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[javainthinking](https://clawhub.ai/user/javainthinking)

### License/Terms of Use:

MIT

## Use Case:

Developers and data analysts use this skill to upload or select datasets, run natural-language analysis through Powerdrill, and retrieve analytical text, tables, charts, generated code, citations, and suggested follow-up questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload arbitrary local files and analysis questions to the third-party Powerdrill service.

Mitigation: Confirm selected file paths and data sensitivity before upload; avoid regulated or confidential data unless the user is authorized to send it to Powerdrill.

Risk: Powerdrill API credentials are required for all API operations.

Mitigation: Store `POWERDRILL_USER_ID` and `POWERDRILL_PROJECT_API_KEY` securely and avoid exposing them in logs, prompts, code snippets, or shared shell history.

Risk: Cleanup and delete commands can remove remote datasets or analysis sessions.

Mitigation: Confirm target dataset and session identifiers before deletion, especially when operating on existing datasets that should be retained.

## Reference(s):

- [Powerdrill API Documentation](https://docs.powerdrill.ai/api-reference/v2)
- [Powerdrill Quick Start Guide](https://docs.powerdrill.ai/developer-guides/quick-start-v2)
- [Powerdrill Streaming Response Handling](https://docs.powerdrill.ai/api-reference/v2/streaming#streaming-response)
- [Checking Data Source Status](https://docs.powerdrill.ai/api-reference/v2/how-to-check-data-sources)
- [Powerdrill MCP Server](https://github.com/powerdrillai/powerdrill-mcp)
- [ClawHub Skill Listing](https://clawhub.ai/javainthinking/skills/powerdrill-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with Python code examples, shell commands, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return Powerdrill response blocks including messages, code, table URLs, image URLs, source citations, follow-up questions, and chart metadata.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
