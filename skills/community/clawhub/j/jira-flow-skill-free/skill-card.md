## Description: <br>
Jira Flow Skill Free helps agents assist developers with Jira Cloud task search, issue updates, worklog entry, and hours summaries through terminal-driven REST API workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and small teams use this skill to manage Jira Cloud work from an agent-assisted terminal workflow. It supports finding issues, viewing details, applying status transitions, assigning tasks, adding comments, creating issues, logging work, and summarizing hours. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can connect to a real company Jira instance and access project data using user-provided credentials. <br>
Mitigation: Review before installing, use a least-privilege Atlassian API token, and restrict JIRA_BOARD where possible. <br>
Risk: Agent-driven commands can change Jira state, including status transitions, assignments, comments, issue creation, and worklog entries. <br>
Mitigation: Require explicit user confirmation before any command that mutates Jira data. <br>
Risk: Jira API tokens may be exposed if placed in shared shell profiles, logs, command history, or committed files. <br>
Mitigation: Keep tokens in a protected local environment or secret manager, avoid logging them, and never commit credentials. <br>


## Reference(s): <br>
- [Jira Flow Skill Free on ClawHub](https://clawhub.ai/thcjp/skills/jira-flow-skill-free) <br>
- [thcjp publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Atlassian API token management](https://id.atlassian.com/manage-profile/security/api-tokens) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON or text command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided Jira Cloud URL, email, API token, optional board scope, and command-line tools curl, jq, bc, and python3.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
