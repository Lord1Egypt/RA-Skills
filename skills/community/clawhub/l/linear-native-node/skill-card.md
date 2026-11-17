## Description:

Linear Native Node helps agents use Linear's GraphQL API from native Node.js to read workspace data and perform explicitly approved issue, project, comment, status, and priority updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jwestburg](https://clawhub.ai/user/jwestburg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to query Linear workspace data, summarize assigned work, generate branch names, and perform approved issue or project mutations through the bundled Node script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Linear API key whose access follows the connected account's permissions.

Mitigation: Use the least-privileged Linear key available and store it only in the process environment for the current session.

Risk: Command output can include workspace-sensitive issue details, URLs, names, or emails.

Mitigation: Review and redact Linear output before sharing logs, examples, or summaries externally.

Risk: Approved write commands can mutate Linear issues, comments, priorities, statuses, or projects.

Mitigation: Run write commands only when the requested Linear action, target, and intended mutation are explicit, and require the --execute gate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jwestburg/skills/linear-native-node)
- [Linear GraphQL API endpoint](https://api.linear.app/graphql)
- [Linear API key settings](https://linear.app/settings/api)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands; runtime output is plain text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LINEAR_API_KEY. Write commands require --execute after explicit approval for the intended Linear mutation.]

## Skill Version(s):

1.0.22 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
