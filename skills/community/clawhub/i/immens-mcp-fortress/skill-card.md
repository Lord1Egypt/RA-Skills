## Description: <br>
Connects OpenClaw to WordPress sites running Immens MCP Fortress so agents can manage content, media, comments, users, WooCommerce, SEO, translations, and other WordPress operations through MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[studioimmens](https://clawhub.ai/user/studioimmens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site operators use this skill to connect an AI agent to a trusted WordPress MCP access point and manage publishing, ecommerce, SEO, media, comments, users, and plugin integrations from OpenClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad live WordPress administrative power, including destructive or business-impacting operations. <br>
Mitigation: Use a staging site or least-privilege access point first, keep backups available, and require explicit human approval before deletes, user or account changes, code snippet changes, bulk edits, cache flushes, SEO changes, or WooCommerce and customer operations. <br>
Risk: The integration depends on sensitive bearer-token credentials for a WordPress access point. <br>
Mitigation: Connect only to access points the user intentionally trusts, keep API keys secret, restrict access by IP where possible, and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/studioimmens/immens-mcp-fortress) <br>
- [Immens MCP Fortress WordPress plugin](https://wordpress.org/plugins/immens-mcp-fortress/) <br>
- [Declared project repository](https://github.com/Studio-Immens/immens-mcp-fortress) <br>
- [Immens MCP Fortress Pro](https://studioimmens.com/immens-mcp-fortress-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted WordPress MCP access point and bearer-token credential.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
