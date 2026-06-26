## Description: <br>
Japan Operations OS for AI agents operating in the Japanese market, covering regulations, protocols, calendar, regional context, foreign entry, travel, entertainment, and persistent memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hiroshic9-png](https://clawhub.ai/user/hiroshic9-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents, developers, and business operators use this skill for Japan market-entry, compliance, etiquette, travel, regional, calendar, and entertainment lookups, plus optional persistent memory for notes and context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote persistent memory may store personal or business notes without clear privacy, deletion, retention, isolation, or access-control boundaries. <br>
Mitigation: Avoid submitting confidential business plans, client notes, employee information, passport or visa details, itineraries, and contact preferences unless the publisher documents acceptable controls. <br>
Risk: The skill references a remote service and an npm MCP package that should be trusted separately before use. <br>
Mitigation: Review the remote API behavior and verify the npm MCP package before running it in an agent environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hiroshic9-png/japan-business-operations) <br>
- [EDITION API documentation](https://api.edition.sh/docs) <br>
- [EDITION landing page](https://edition.sh) <br>
- [edition-mcp-server npm package](https://www.npmjs.com/package/edition-mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call a remote API and MCP server; persistent memory features can store user-provided notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
