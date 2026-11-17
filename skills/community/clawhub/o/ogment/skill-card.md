## Description:

Invoke MCP tools via the Ogment CLI to access Linear, Notion, Gmail, PostHog, and other SaaS integrations through Ogment's governance layer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asoviche](https://clawhub.ai/user/asoviche)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Ogment to authenticate with the Ogment CLI, discover connected SaaS tools, inspect tool schemas, and invoke MCP tools through a governed approval flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can mediate broad access to connected SaaS services, including messaging, records, and database tools.

Mitigation: Review connected Ogment accounts and require explicit confirmation before sending messages, changing records, deleting data, or running database SQL.

## Reference(s):

- [Ogment homepage](https://ogment.ai)
- [ClawHub Ogment skill page](https://clawhub.ai/asoviche/skills/ogment)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides authentication, catalog discovery, schema inspection, and governed tool invocation with JSON inputs.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
