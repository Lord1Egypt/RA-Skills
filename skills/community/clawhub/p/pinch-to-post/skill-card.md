## Description:

Manage WordPress sites through WP Pinch MCP tools as part of WP Pinch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickhamze](https://clawhub.ai/user/nickhamze)

### License/Terms of Use:


## Use Case:

External WordPress site owners and operators use this skill to manage posts, media, users, comments, settings, plugins, themes, governance checks, and WooCommerce workflows through WP Pinch MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate writes, publishing, plugin or theme changes, user changes, WooCommerce updates, cron changes, and bulk operations on a connected WordPress site.

Mitigation: Install it only for sites the agent is intended to manage, use draft-first workflows, and require explicit confirmation before publish, plugin/theme, user, WooCommerce, cron, and bulk actions.

Risk: Over-scoped WordPress credentials could allow broader site changes than the operator intended.

Mitigation: Use a least-privilege WordPress Application Password, prefer the OpenClaw Agent role or read-only mode when possible, and rotate credentials periodically.

Risk: Generic trigger words such as post or blog may route ordinary requests into this WordPress management skill.

Mitigation: Confirm the target site and intended WordPress action before taking operational steps, especially for write or bulk workflows.

Risk: Webhook and export workflows may expose site activity or content context if configured too broadly.

Mitigation: Configure webhook destinations deliberately, keep capture tokens private, and rely on the documented PII redaction behavior for user exports and activity feeds.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nickhamze/skills/pinch-to-post)
- [WP Pinch Homepage](https://wp-pinch.com)
- [WP Pinch Project](https://github.com/RegionallyFamous/wp-pinch)
- [WP Pinch Configuration Guide](https://github.com/RegionallyFamous/wp-pinch/wiki/Configuration)
- [WP Pinch Error Codes](https://github.com/RegionallyFamous/wp-pinch/wiki/Error-Codes)
- [WP Pinch Security Model](https://github.com/RegionallyFamous/wp-pinch/wiki/Security)

## Skill Output:

**Output Type(s):** [guidance, configuration]

**Output Format:** [Markdown instructions with MCP tool names and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WP_SITE_URL; WordPress authentication credentials are configured in the MCP server, not in the skill.]

## Skill Version(s):

5.5.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
