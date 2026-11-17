## Description:

Implements GraphQL APIs in Go using gqlgen or graph-gophers/graphql-go, covering schema design, resolvers, subscriptions, testing, and production safety.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to build and review Go GraphQL APIs, choose gqlgen or graph-gophers/graphql-go, write schema and resolver code, prevent N+1 query patterns, test handlers and subscriptions, and apply production safety limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad outbound curl access beyond its documented workflows.

Mitigation: Review the curl permission before installation, especially in repositories with secrets or untrusted content.

Risk: Mutable latest-based tool commands can make generated GraphQL code or guidance less reproducible.

Mitigation: Prefer scoped documentation tools and pin gqlgen to a reviewed version before running generation commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samber/skills/golang-graphql)
- [ClawHub metadata homepage](https://github.com/samber/cc-skills-golang)
- [gqlgen reference](references/gqlgen.md)
- [graph-gophers/graphql-go reference](references/graphql-go.md)
- [Testing GraphQL in Go](references/testing.md)
- [gqlgen](https://github.com/99designs/gqlgen)
- [graph-gophers/graphql-go](https://github.com/graph-gophers/graphql-go)
- [Relay cursor connections spec](https://relay.dev/graphql/connections.htm)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Go, GraphQL SDL, YAML, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Applies to Go source files and may recommend Go tooling commands when relevant.]

## Skill Version(s):

0.2.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
