## Description:

Use the paid LDM Inbox Check MCP server to run real inbox-placement tests before OpenClaw agents send cold email or bulk outbound.

This skill is ready for commercial/non-commercial use.

## Publisher:

[live-direct-marketing](https://clawhub.ai/user/live-direct-marketing)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and outbound automation teams use this skill to run paid inbox-placement checks before sending cold email or bulk outbound campaigns. It helps agents inspect provider-level placement, authentication results, screenshots, quota status, and pass/fail guidance before deciding whether to send, revise, or pause.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes an unpinned npm MCP package with access to an Inbox Check API key, so executable behavior could change after review.

Mitigation: Pin and review the MCP package version in a lockfile-controlled deployment, use a narrowly scoped revocable API key, limit environment exposure, and require explicit approval for paid test creation or deletion.

Risk: Inbox checks consume paid or quota-backed usage.

Mitigation: Inspect quota before creating tests, reuse recent matching tests when appropriate, choose the smallest useful provider set, and ask the user before casual or repeated paid checks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/live-direct-marketing/skills/ldm-openclaw-inbox-mcp-skill)
- [Publisher Profile](https://clawhub.ai/user/live-direct-marketing)
- [Skill Homepage](https://github.com/live-direct-marketing/ldm-openclaw-inbox-mcp-skill)
- [MCP Package](https://www.npmjs.com/package/ldm-inbox-check-mcp)
- [MCP Repository](https://github.com/live-direct-marketing/ldm-inbox-check-mcp)
- [Inbox Check](https://check.live-direct-marketing.online)
- [Inbox Check MCP API Docs](https://check.live-direct-marketing.online/docs/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP tool-use guidance, pass/fail decisions, quota notes, authentication results, provider placement summaries, screenshots availability, and recommended fixes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
