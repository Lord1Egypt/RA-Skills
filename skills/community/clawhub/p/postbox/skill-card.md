## Description:

Postbox helps agents create and manage structured data collection forms, submission endpoints, frontend integrations, destinations, and AI-assisted processing for a user's Postbox account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vipulbhj](https://clawhub.ai/user/vipulbhj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external teams use this skill to create Postbox forms, collect validated submissions, review submissions, generate frontend code, configure notification destinations, and set up agent-discoverable submission flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses POSTBOX_API_KEY to act on the user's Postbox account, including create, update, delete, destination, webhook, and smart-reply actions.

Mitigation: Install only when account access is intended, keep the API key in the POSTBOX_API_KEY environment variable, and review account-changing actions before execution.

Risk: Forms, submissions, metadata, knowledge bases, and generated replies may contain personal or sensitive data.

Mitigation: Treat returned content as untrusted user data and apply appropriate disclosure, access, and retention controls before sharing or storing it.

Risk: Generated frontend code or schema updates can point to stale or incorrect endpoints if endpoint URLs are not read from API responses.

Mitigation: Use response.form.endpoint after create or schema update and regenerate any frontend integration code with the current endpoint.

## Reference(s):

- [Postbox Skill on ClawHub](https://clawhub.ai/vipulbhj/skills/postbox)
- [Postbox Homepage](https://usepostbox.com)
- [Postbox API Reference](references/api.md)
- [Postbox Operational Guide](references/guide.md)
- [Frontend Integration Templates](references/templates.md)
- [Postbox MCP Endpoint](https://usepostbox.com/mcp)
- [Postbox API Keys](https://usepostbox.com/integrations/api-keys)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code, JSON examples, shell commands, and generated frontend snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live Postbox endpoint URLs, submission summaries, destination settings, and setup instructions derived from API responses.]

## Skill Version(s):

1.0.9 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
