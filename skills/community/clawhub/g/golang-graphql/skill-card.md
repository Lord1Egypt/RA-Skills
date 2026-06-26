## Description: <br>
Implements GraphQL APIs in Go using gqlgen or graph-gophers/graphql-go for schema design, resolver work, subscriptions, and integration with existing Go HTTP services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build or review Go GraphQL servers, including schema design, resolver implementation, DataLoader batching, subscriptions, testing, and production safety controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Proposed file edits, generated code, dependency changes, or Go commands such as go get and go generate could alter application behavior or supply chain state. <br>
Mitigation: Review diffs, dependency changes, generated files, and commands before applying them, especially in sensitive repositories. <br>
Risk: GraphQL implementation guidance affects production controls such as query limits, introspection exposure, authorization checks, error handling, subscription cancellation, and DataLoader scoping. <br>
Mitigation: Verify complexity or depth limits, production introspection gating, per-request DataLoaders, safe error formatting, authorization policy, and subscription cancellation against project requirements. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/samber/golang-graphql) <br>
- [Source Homepage](https://github.com/samber/cc-skills-golang) <br>
- [gqlgen Reference](references/gqlgen.md) <br>
- [graph-gophers/graphql-go Reference](references/graphql-go.md) <br>
- [Testing GraphQL in Go](references/testing.md) <br>
- [gqlgen](https://github.com/99designs/gqlgen) <br>
- [graph-gophers/graphql-go](https://github.com/graph-gophers/graphql-go) <br>
- [Relay Cursor Connections Specification](https://relay.dev/graphql/connections.htm) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with Go, GraphQL SDL, YAML configuration, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose file edits, dependency updates, gqlgen code generation, tests, and Go tooling commands for review before execution.] <br>

## Skill Version(s): <br>
0.0.3 (source: artifact SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
