## Description: <br>
Linear API integration with managed OAuth for querying and managing issues, projects, teams, cycles, labels, and comments using GraphQL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect and manage Linear workspace data through Maton-managed OAuth, including issues, comments, projects, teams, cycles, labels, workflow states, and users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change Linear workspace data through a Maton-managed OAuth connection. <br>
Mitigation: Install only when Maton is trusted with the connected Linear workspace, and keep the Maton API key scoped and stored as a sensitive credential. <br>
Risk: Requests may target the wrong Linear account when multiple OAuth connections are available. <br>
Mitigation: Confirm and specify the intended Linear connection before account-specific operations. <br>
Risk: Create, update, or delete operations can affect Linear issues, comments, projects, or OAuth connections. <br>
Mitigation: Require explicit user approval after reviewing the exact target resource and intended effect. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/linear-api) <br>
- [Linear API Overview](https://linear.app/developers) <br>
- [Linear GraphQL Getting Started](https://linear.app/developers/graphql) <br>
- [Linear GraphQL Schema](https://studio.apollographql.com/public/Linear-API/schema/reference?variant=current) <br>
- [Linear API and Webhooks](https://linear.app/docs/api-and-webhooks) <br>
- [Maton CLI Manual](https://cli.maton.ai/manual) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell, GraphQL, Python, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a selected Linear OAuth connection for account-specific operations.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
