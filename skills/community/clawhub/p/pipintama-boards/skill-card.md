## Description:

Create, fetch, share, or change visibility for hosted Pipintama Boards through the MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidk2yoyo](https://clawhub.ai/user/davidk2yoyo)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and teams use this skill to create, retrieve, share, update, and export hosted visual boards for planning, brainstorming, process design, and system design.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Board source content is sent to the external Pipintama service.

Mitigation: Do not use the skill for secrets, credentials, regulated data, customer data, proprietary plans, or private architecture unless the service's data handling expectations have been reviewed.

Risk: New boards are shareable by default, which can expose sensitive content through hosted links.

Mitigation: Use private visibility for sensitive work and confirm visibility before creating or updating boards that contain confidential information.

Risk: The hosted MCP requires a Pipintama API key.

Mitigation: Provide credentials only through supported client authentication mechanisms and avoid placing keys or other secrets in board titles, source text, or notes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/davidk2yoyo/skills/pipintama-boards)
- [Pipintama MCP Endpoint](https://api.pipintama.com/mcp)
- [Pipintama MCP Health Check](https://api.pipintama.com/mcp-health)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or plain text containing hosted board URLs, optional PNG export URLs, and a short explanation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a valid Pipintama API key and defaults newly created boards to shared visibility unless the user requests public or private visibility.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
