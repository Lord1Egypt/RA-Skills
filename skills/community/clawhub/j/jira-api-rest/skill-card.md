## Description:

Automate Jira Cloud operations for issues, worklogs, comments, transitions, boards, sprints, advanced JQL searches, and direct REST API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[temperatio](https://clawhub.ai/user/temperatio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate Jira Cloud from an agent workflow when they need REST coverage for issues, worklogs, JQL searches, and Agile board or sprint tasks that are not covered by jira-cli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generic request command can send Jira credentials to a non-Jira URL if misused or influenced by untrusted instructions.

Mitigation: Use narrowly scoped Jira tokens, avoid the generic request command except with Jira-relative paths, and add validation that rejects absolute URLs and verifies the final Jira origin.

Risk: The skill can edit or delete Jira data, including worklogs, issues, comments, transitions, assignments, links, and sprints.

Mitigation: Require explicit human confirmation before destructive or broad Jira changes and review command parameters before execution.

## Reference(s):

- [Jira REST notes](references/jira-rest-notes.md)
- [Endpoint map](references/endpoint-map.md)
- [Agile boards and sprints](references/agile-sprints.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; helper commands emit JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Jira configuration and a netrc API token; destructive Jira operations should be confirmed before execution.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
