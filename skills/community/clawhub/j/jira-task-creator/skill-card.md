## Description:

Create and manage Jira tasks using natural language input, smart user search, batch CSV import, and task analytics with flexible field support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ulanzicom](https://clawhub.ai/user/ulanzicom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to create Jira issues, search assignable users, import batches of tasks, and summarize task status from agent-driven workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send a Jira bearer token and issue or user data to a configured Jira URL, including plaintext HTTP.

Mitigation: Use only an HTTPS Jira URL you control, use a least-privilege Jira token, and rotate any token that was used over HTTP.

Risk: The skill can perform real Jira write operations through natural-language or batch task creation.

Mitigation: Add a preview and confirmation step before bulk or natural-language issue creation, and treat every successful call as a real Jira write.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ulanzicom/skills/jira-task-creator)
- [Artifact skill documentation](artifact/SKILL.md)
- [Artifact package metadata](artifact/package.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples, shell commands, configuration snippets, and Jira API result data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform real Jira create and lookup actions when configured with Jira credentials.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
