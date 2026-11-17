## Description:

Manage and automate multiple WordPress sites through Massblogger's hosted MCP server, including AI content generation, editing, publishing, media, SEO, and bulk operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[klitmose](https://clawhub.ai/user/klitmose)

### License/Terms of Use:

MIT-0

## Use Case:

External WordPress site owners and content operators use this skill to let an agent manage posts, pages, media, SEO metadata, scheduling, comments, and cross-site content workflows through Massblogger. It is suited to content portfolio management where hosted MCP access and WordPress Application Passwords are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The hosted service receives broad ongoing authority to manage WordPress content and administrative operations.

Mitigation: Use a dedicated least-privilege WordPress account, avoid Administrator credentials unless required, and review production workflows before installing.

Risk: Content workflows can publish or bulk-change multiple posts or sites.

Mitigation: Enable publish guard for content workflows and use dry-run options before cross-site search/replace or spam deletion.

Risk: MCP tokens or WordPress Application Passwords could expose site access if mishandled.

Mitigation: Store secrets in the OpenClaw runtime environment, do not paste them into prompts, and revoke or rotate both the Massblogger MCP token and WordPress Application Password if access is no longer needed or may be exposed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/klitmose/skills/massblogger)
- [Publisher Profile](https://clawhub.ai/user/klitmose)
- [Massblogger](https://massblogger.com)
- [MCP Setup Docs](https://massblogger.com/docs/openclaw)
- [WordPress Application Passwords Guide](https://massblogger.com/docs/wordpress/application-passwords)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, bash, and text examples for MCP configuration and WordPress content operations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger remote MCP actions that read, create, update, publish, delete, or bulk-modify WordPress and Massblogger-managed content.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
