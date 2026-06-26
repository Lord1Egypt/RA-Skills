## Description: <br>
Manage WordPress sites through WP Pinch MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickhamze](https://clawhub.ai/user/nickhamze) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External WordPress site owners and content teams use this skill to let an agent draft, update, repurpose, and govern site content through WP Pinch MCP tools. It supports content, media, taxonomy, comment, settings, plugin, theme, analytics, governance, WooCommerce, Ghost Writer, and Molt workflows when those tools are enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make changes to WordPress sites when the MCP server is configured with write-capable credentials. <br>
Mitigation: Install it only for sites intended for agent management, use least-privileged WordPress credentials or the OpenClaw Agent role, and keep read-only mode or write budgets enabled where possible. <br>
Risk: Broad triggers such as post, blog, and publish may make the skill available in more conversations than strictly necessary. <br>
Mitigation: Review when the skill is enabled, confirm scope before write or bulk operations, and check WP Pinch audit logs after sensitive actions. <br>
Risk: Publishing, role, plugin, theme, and bulk-edit actions can affect live site behavior or public content. <br>
Mitigation: Create drafts before publishing, orient with site-health or site-digest before significant changes, and require explicit user confirmation for destructive, bulk, or public-facing changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nickhamze/pinch-to-post) <br>
- [WP Pinch homepage](https://wp-pinch.com) <br>
- [WP Pinch configuration guide](https://github.com/RegionallyFamous/wp-pinch/wiki/Configuration) <br>
- [WP Pinch security model](https://github.com/RegionallyFamous/wp-pinch/wiki/Security) <br>
- [WP Pinch error codes](https://github.com/RegionallyFamous/wp-pinch/wiki/Error-Codes) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration instructions, API Calls, Markdown, Text] <br>
**Output Format:** [Markdown guidance and MCP tool requests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses WP_SITE_URL to target the WordPress site; credentials are configured in the MCP server rather than the skill.] <br>

## Skill Version(s): <br>
5.5.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
