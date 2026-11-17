## Description:

Helps agents read, search, create, comment on, assign, and transition Jira issues across Jira Cloud, Server, and Data Center.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weiguang1017](https://clawhub.ai/user/weiguang1017)

### License/Terms of Use:

MIT

## Use Case:

Developers and teams use this skill to inspect Jira issues, search with JQL, and manage issue creation, comments, assignments, and workflow transitions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write actions can change live Jira issues without a built-in confirmation gate, including after automatic invocation.

Mitigation: Before creating, commenting, assigning, or transitioning, show the exact issue key, operation, and target value and obtain user confirmation.

Risk: Jira credentials can grant more access than the task requires or be exposed if stored insecurely.

Mitigation: Use an account with only the needed project permissions; keep tokens in environment variables or a protected config file outside version control.

## Reference(s):

- [Source repository (server-resolved provenance)](https://github.com/weiguang1017/jira-devops-skill)
- [ClawHub skill release](https://clawhub.ai/weiguang1017/skills/jira-devops-skill)
- [Jira Skills usage guide](references/USAGE.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown guidance and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command results vary by operation; errors return a nonzero exit status.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
