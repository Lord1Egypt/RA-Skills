## Description:

GraphQL schema static auditor that reads .graphql SDL files or introspection JSON to identify N+1 exposure hotspots, unbounded query depth, deprecated field drift, naming convention violations, circular references, missing pagination, broad scalar types, and related resolver or query-complexity fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review GraphQL schemas for security, reliability, performance, and API-design issues before deployment or schema changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deprecated-operation findings may be incomplete if operation parsing is not added.

Mitigation: Treat deprecated-operation results as triage and verify findings against the application's operation files before relying on them.

Risk: Repository-wide scans can read more local project files than intended.

Mitigation: Run the skill from the intended schema directory or provide explicit schema and operation paths.

Risk: The example npx command can fetch an unpinned package.

Mitigation: Use a trusted installed dependency or pin the package version before running schema extraction.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-graphql-schema-audit)
- [Publisher homepage](https://canlah.ai)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report with issue summaries, fix guidance, code snippets, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local static-analysis guidance for GraphQL schema files and introspection JSON; no external API use is described.]

## Skill Version(s):

1.0.3 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
