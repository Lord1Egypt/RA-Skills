## Description: <br>
Operates Linear workspace issues, projects, and teams through the Linear GraphQL API using UXC, including read-first querying and guarded write operations with API key or OAuth authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to query Linear issues, teams, projects, and workflow state through GraphQL, then create, update, archive, or comment on issues when the user has configured credentials and confirmed the intended write. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can intentionally create, update, archive, or comment on Linear workspace data when credentials allow write access. <br>
Mitigation: Use the narrowest suitable Linear credential or OAuth scope, prefer read operations first, and require explicit confirmation before executing write operations. <br>
Risk: Misconfigured API keys, OAuth scopes, or endpoint bindings can expose access to the wrong Linear workspace or fail authentication. <br>
Mitigation: Verify the configured credential, binding, workspace, team, and issue identifiers before acting, and store secrets through environment variables or a secret manager rather than literal command history. <br>


## Reference(s): <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [Linear API Documentation](https://developers.linear.app) <br>
- [Linear GraphQL Schema](https://studio.apollographql.com/public/Linear-API) <br>
- [ClawHub Skill Page](https://clawhub.ai/jolestar/linear-graphql-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Linear GraphQL operation names, credential setup steps, API call examples, and guarded write-action recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
