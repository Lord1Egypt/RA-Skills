## Description: <br>
Postal mail API for AI agents: send physical mail, use inbound context, and join the launching-soon mailbox address beta (street + mailbox number). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arbengine](https://clawhub.ai/user/arbengine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use mailbox.bot to connect agents to outbound physical mail, forwarded inbound document context, and linked postal thread workflows. Approved beta users can evaluate mailing mailbox address workflows with street address, scan/photo intake, and agent notifications. <br>

### Deployment Geography for Use: <br>
Global for software integration; the real mailing mailbox address beta is described as starting in Southern California, then Utah and Nevada. <br>

## Known Risks and Mitigations: <br>
Risk: Agents can initiate real-world mail authority, including destructive mailbox actions and outbound production mail. <br>
Mitigation: Use sandbox or dry-run keys first, enable force_approval and spend limits, and require explicit human approval for destructive actions or production sends. <br>
Risk: The skill requires sensitive credentials that can authorize postal workflows and charges. <br>
Mitigation: Prefer agent-scoped keys, keep credentials out of prompts and logs, and rotate keys if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/arbengine/mailbox-bot) <br>
- [mailbox.bot Website](https://mailbox.bot) <br>
- [MCP Install Guide](https://mailbox.bot/mcp-install) <br>
- [API Docs](https://mailbox.bot/api-docs) <br>
- [OpenAPI Specification](https://mailbox.bot/openapi.json) <br>
- [Public MCP Tool Catalog](https://mailbox.bot/api/mcp/tools-public) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON, shell command, and REST/MCP request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include authenticated API requests; sandbox and dry-run modes are documented for testing before live mail.] <br>

## Skill Version(s): <br>
5.1.5 (source: server release metadata, frontmatter, server.json, smithery.yaml, changelog released 2026-06-05) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
