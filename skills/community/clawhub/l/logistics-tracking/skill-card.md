## Description: <br>
Track international packages by tracking number across 3100+ carriers via 17track, with optional TRACK17_API_KEY support and a Playwright fallback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shopmeskills](https://clawhub.ai/user/shopmeskills) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and support teams use this skill to check package status, delivery estimates, customs events, carrier identity, and batch tracking results from tracking numbers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external npm MCP server package. <br>
Mitigation: Verify the @shopmeagent/logistics-tracking-mcp package source before installation and pin a trusted version where possible. <br>
Risk: Tracking numbers and package events may be shared with 17track or a hosted MCP endpoint. <br>
Mitigation: Use trusted endpoints, avoid submitting unnecessary personal data, and prefer the official 17track API-key mode for reliability. <br>
Risk: TRACK17_API_KEY can grant access to the configured tracking API account. <br>
Mitigation: Protect TRACK17_API_KEY as a secret and avoid exposing it in shared MCP client configuration. <br>
Risk: A hosted MCP endpoint can be abused if exposed without controls. <br>
Mitigation: Serve hosted endpoints over HTTPS with authentication, rate limits, and monitoring. <br>
Risk: The Playwright fallback requires a headless browser and may be less reliable than official API access. <br>
Mitigation: Install Playwright only when needed and use TRACK17_API_KEY for production or high-reliability use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shopmeskills/logistics-tracking) <br>
- [Publisher Profile](https://clawhub.ai/user/shopmeskills) <br>
- [17track API](https://api.17track.net) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with JSON MCP configuration examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return tracking status, current location, event timeline, carrier identification, batch tracking results, and status explanations.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
