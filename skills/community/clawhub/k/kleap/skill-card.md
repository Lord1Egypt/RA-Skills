## Description:

Ship and run a live website or web app end-to-end — hosting, database, auth, forms/leads, analytics, custom domains — driven from this agent via the kleap CLI (npx, no install).

This skill is ready for commercial/non-commercial use.

## Publisher:

[kleap](https://clawhub.ai/user/kleap)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to create and manage hosted Kleap websites and apps, including their files, databases, leads, analytics, and domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the latest remote CLI without a fixed version may introduce unreviewed changes.

Mitigation: Use the CLI only if you trust its supply chain; review changes before running it with access to live apps.

Risk: Broad, persistent credentials can grant the agent access to production apps and data.

Mitigation: Prefer scoped or temporary API keys where possible, revoke unused keys, and avoid production data unless needed.

Risk: Database changes, file removal, publishing, and reading or exporting leads can alter or expose sensitive information.

Mitigation: Require explicit user confirmation before deletes, updates, file removals, publishing, or reading and exporting leads.

## Reference(s):

- [Kleap MCP homepage](https://kleap.co/mcp)
- [Kleap on ClawHub](https://clawhub.ai/kleap/skills/kleap)
- [Kleap recipes](artifact/references/recipes.md)
- [Kleap troubleshooting](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with CLI commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report confirmed live site URLs, database results, or domain checkout links; supports structured CLI results with --json.]

## Skill Version(s):

1.1.0 (source: skill frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
