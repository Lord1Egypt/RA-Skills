## Description:

Create, fetch, share, or update hosted Pipintama Charts through the MCP server when a user needs a line, bar, pie, or radar chart from text or structured values, and the right output is a hosted chart link or PNG instead of only prose.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidk2yoyo](https://clawhub.ai/user/davidk2yoyo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create, retrieve, update, share, and export hosted Pipintama line, bar, pie, or radar charts from user-provided text or structured values.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chart contents are uploaded to Pipintama's hosted service.

Mitigation: Avoid confidential, regulated, or personal data unless the user explicitly accepts that data will be sent to the hosted service.

Risk: Charts are shared by default and may expose content through hosted links.

Mitigation: Confirm appropriate visibility for sensitive chart contents and use private visibility when the user asks for restricted access.

Risk: The skill requires a Pipintama API key for all hosted MCP actions.

Mitigation: Check for valid user-provided credentials before calling the MCP endpoint and never attempt authenticated requests without them.

## Reference(s):

- [Pipintama MCP endpoint](https://api.pipintama.com/mcp)
- [Pipintama MCP health check](https://api.pipintama.com/mcp-health)
- [ClawHub skill page](https://clawhub.ai/davidk2yoyo/skills/pipintama-charts)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown text with a hosted chart viewer URL, optional PNG export URL, and a short explanation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include tokenized share links for hosted charts and optional PNG export links.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
