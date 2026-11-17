## Description:

Jira automation for JiraATX (project DS). Create, update, comment, transition issues, list To Do tasks, sync repo, execute tasks end-to-end. Triggers: DS-XXX, Jira task, work on issue, list my tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clairproqc-star](https://clawhub.ai/user/clairproqc-star)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage JiraATX project DS issues, prepare mapped repositories for issue work, and run configured tests as part of an agent-assisted task workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package ships a plaintext Jira API token.

Mitigation: Do not install the package as-is; revoke the exposed token, remove it from all files and prior package versions, and require secure user-provided credentials.

Risk: The skill can create, update, comment on, and transition Jira issues.

Mitigation: Validate the Jira tenant URL, narrow triggers, and require explicit approval checkpoints before Jira mutations.

Risk: The skill can sync local repositories, create branches, edit files through the agent workflow, and run configured tests.

Mitigation: Require explicit approval before repo sync, file edits, or test execution, and review the mapped repository configuration before use.

## Reference(s):

- [Jira Task Manager on ClawHub](https://clawhub.ai/clairproqc-star/skills/jira-task-manager)
- [clairproqc-star publisher profile](https://clawhub.ai/user/clairproqc-star)
- [Jira Resources Reference](references/jira.md)
- [Repository Mapping Configuration](references/repos.json)
- [Jira tenant](https://attrix-team.atlassian.net/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command invocations and JSON-like script results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Jira APIs, run git commands, and execute configured tests when used in an agent workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
