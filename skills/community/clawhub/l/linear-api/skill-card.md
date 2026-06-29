## Description: <br>
Linear API integration with managed OAuth for querying and managing issues, projects, teams, cycles, labels, and comments using GraphQL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query Linear work and prepare or execute approved issue, project, team, cycle, label, and comment operations through Maton's Linear GraphQL integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Maton as a proxy for the connected Linear account and requires a MATON_API_KEY. <br>
Mitigation: Install only when comfortable granting Maton-mediated access, keep MATON_API_KEY out of shared logs and terminal output, and rotate the key if exposure is suspected. <br>
Risk: Create, update, delete, and comment operations can change Linear data. <br>
Mitigation: Confirm the target resource and intended effect before running any write operation. <br>
Risk: Multiple Linear OAuth connections can send requests to the wrong account if no connection is specified. <br>
Mitigation: Specify the intended connection when more than one Linear connection is active. <br>


## Reference(s): <br>
- [ClawHub Linear Skill](https://clawhub.ai/byungkyu/skills/linear-api) <br>
- [byungkyu ClawHub Profile](https://clawhub.ai/user/byungkyu) <br>
- [Linear API Overview](https://linear.app/developers) <br>
- [Linear GraphQL Getting Started](https://linear.app/developers/graphql) <br>
- [Linear GraphQL Schema](https://studio.apollographql.com/public/Linear-API/schema/reference?variant=current) <br>
- [Linear API and Webhooks](https://linear.app/docs/api-and-webhooks) <br>
- [Maton CLI Manual](https://cli.maton.ai/manual) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with CLI examples, GraphQL snippets, and Python or JavaScript code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a valid Maton Linear OAuth connection.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
