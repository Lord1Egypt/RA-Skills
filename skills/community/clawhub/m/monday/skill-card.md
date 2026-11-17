## Description:

Helps agents query and manage Monday.com boards, items, columns, groups, and workspaces through an authorized Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill to read Monday.com account and board data, manage work items, and set up approved automations through Maton.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Maton access to Monday.com may expose sensitive business data.

Mitigation: Use only if the user trusts Maton; prefer OAuth and grant the narrowest available scopes.

Risk: Writes, deletions, and hosted automations can change or remove business data.

Mitigation: Review the specific action, target, and effect with the user and obtain explicit approval before proceeding.

Risk: Trigger destinations may continuously forward event data to a third-party URL.

Mitigation: Require separate approval of the exact destination, data sent, and ongoing delivery before enabling forwarding.

## Reference(s):

- [Monday.com skill release](https://clawhub.ai/byungkyu/skills/monday)
- [Maton homepage](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Monday.com API basics](https://developer.monday.com/api-reference/docs/basics)
- [Monday.com GraphQL overview](https://developer.monday.com/api-reference/docs/introduction-to-graphql)
- [Monday.com boards reference](https://developer.monday.com/api-reference/reference/boards)
- [Maton scheduled trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with command and GraphQL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access, a Maton account, and an authorized Monday.com connection.]

## Skill Version(s):

1.2.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
