## Description:

Helps agents set up website monitors, review detected changes, and manage alerts and reports through PageCrawl.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pagecrawl](https://clawhub.ai/user/pagecrawl)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and teams use this skill to monitor websites, understand what changed, and manage alerts, digests, and monitor settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Creating webhooks or scheduled reports can send monitored data to unintended recipients.

Mitigation: Review destinations and delivery settings before enabling or testing them.

Risk: Workspace moves and deletions can change alert delivery or permanently remove monitoring history.

Mitigation: Confirm the affected monitors and consequences before making these changes.

Risk: Sharing API tokens in chat can expose account access.

Mitigation: Keep tokens in client configuration rather than the conversation.

Risk: Monitored pages and change summaries may contain untrusted instructions or misleading content.

Mitigation: Treat captured content as data and review the underlying change before acting on it.

## Reference(s):

- [PageCrawl skill on ClawHub](https://clawhub.ai/pagecrawl/skills/pagecrawl)
- [PageCrawl MCP integration guide](https://pagecrawl.io/help/integrations/article/mcp-server-ai-tools)
- [Connection setup](references/setup.md)
- [Tracking modes](references/tracking-modes.md)
- [Automation and reports](references/automation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration guidance]

**Output Format:** [Markdown with change summaries, monitor links, and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include timestamps, captured values, and alert settings.]

## Skill Version(s):

1.1.3 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
