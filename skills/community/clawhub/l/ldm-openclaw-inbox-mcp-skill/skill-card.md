## Description: <br>
Use the paid LDM Inbox Check MCP server to run real inbox-placement tests before OpenClaw agents send cold email or bulk outbound. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[live-direct-marketing](https://clawhub.ai/user/live-direct-marketing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and outbound-automation operators use this skill to run paid inbox-placement checks through MCP before sending cold email or bulk outbound campaigns. It helps agents inspect quota, create seed-address tests, read placement and authentication results, and decide whether to send, revise, or pause. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive INBOX_CHECK_API_KEY for a third-party paid service. <br>
Mitigation: Store the API key securely, avoid printing or committing it, and install the MCP package only when the LDM Inbox Check service and npm package are trusted. <br>
Risk: Creating inbox-placement tests can consume paid quota. <br>
Mitigation: Check quota before creating tests, reuse recent relevant results when appropriate, and reserve paid tests for final or user-approved preflight workflows. <br>
Risk: Campaign drafts, headers, authentication results, and screenshots may be sent to an external provider. <br>
Mitigation: Avoid submitting regulated or confidential campaign content unless vendor and privacy requirements permit that data transfer. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/live-direct-marketing/ldm-openclaw-inbox-mcp-skill) <br>
- [Skill homepage](https://github.com/live-direct-marketing/ldm-openclaw-inbox-mcp-skill) <br>
- [MCP package](https://www.npmjs.com/package/ldm-inbox-check-mcp) <br>
- [Inbox Check service](https://check.live-direct-marketing.online) <br>
- [Inbox Check MCP API docs](https://check.live-direct-marketing.online/docs/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text with JSON configuration examples and MCP tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an INBOX_CHECK_API_KEY and may consume paid quota when creating inbox-placement tests.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
