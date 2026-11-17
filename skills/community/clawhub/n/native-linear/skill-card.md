## Description:

Query and manage Linear issues, projects, cycles, and teams via the Linear GraphQL API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codeninja23](https://clawhub.ai/user/codeninja23)

### License/Terms of Use:


## Use Case:

Developers and teams use this skill to inspect and manage Linear workspace issues, projects, cycles, teams, and workflow states from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a Linear API key to read and change Linear workspace items.

Mitigation: Use a least-privileged Linear key where possible and install the skill only for agent sessions that should access that workspace.

Risk: Create and update commands can modify important Linear issues.

Mitigation: Review command arguments and confirm intended workspace changes before running create or update operations.

Risk: The Linear API key could be exposed through logs or shared shells.

Mitigation: Avoid printing or sharing the key and keep it out of shared terminal history or captured logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/codeninja23/skills/native-linear)
- [Publisher profile](https://clawhub.ai/user/codeninja23)
- [Linear GraphQL API endpoint](https://api.linear.app/graphql)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and plain-text CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LINEAR_API_KEY and python3; commands call Linear directly through api.linear.app/graphql.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
