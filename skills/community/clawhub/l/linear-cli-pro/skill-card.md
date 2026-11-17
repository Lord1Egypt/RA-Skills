## Description:

Linear CLI专家 guides developers using the Linear CLI from coding agents through stable JSON workflows, dry-run write operations, safer Markdown handling, bulk issue operations, and authentication recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to have an agent operate Linear through the local linear CLI for issue creation, updates, comments, labels, triage, bulk changes, and GraphQL fallback workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to read or change Linear issues, labels, comments, workflow states, and related workspace data using existing Linear credentials.

Mitigation: Install and invoke it only for workflows where agent-operated Linear access is intended, and require dry-run or preview confirmation before write or bulk operations.

Risk: Token retrieval examples and credential handling can expose Linear credentials if run in logged shells or shared transcripts.

Mitigation: Avoid token-retrieval examples in logged shells and prefer configured authentication mechanisms such as interactive login or controlled environment variables.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/thcjp/skills/linear-cli-pro)
- [Linear GraphQL API endpoint](https://api.linear.app/graphql)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline bash, JSON, and GraphQL code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Emphasizes dry-run previews, JSON responses, file/stdin Markdown input, and post-operation validation.]

## Skill Version(s):

1.0.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
