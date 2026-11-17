## Description:

Convert Markdown to Slack mrkdwn, Teams HTML, Jira ADF, or plain text via the markdown-convert MCP server. Use when the agent will post or paste into Slack, Microsoft Teams, Jira Cloud, or needs stripped text for another channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ysskrishna](https://clawhub.ai/user/ysskrishna)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use the conversion tools to adapt Markdown for Slack, Microsoft Teams, Jira Cloud, or plain text destinations. Choose the tool that matches the destination's expected format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using a formatter that does not match the destination can produce unusable content.

Mitigation: Use the tools-and-next-hops reference to match the destination with Slack mrkdwn, Teams HTML, Jira ADF, or plain text.

Risk: Input over 200,000 characters returns a tool error.

Mitigation: Keep each conversion input within the documented 200,000-character limit.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ysskrishna/skills/markdown-convert)
- [Tools and next hops](https://github.com/ysskrishna/markdown-convert-mcp#tools-and-next-hops)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, JSON]

**Output Format:** [Slack mrkdwn, Teams HTML, Jira ADF JSON string, or plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Conversion input is limited to 200,000 characters.]

## Skill Version(s):

1.2.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
