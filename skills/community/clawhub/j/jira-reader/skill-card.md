## Description:

Read-only Jira lookup commands, including JSON task-directory output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amaury95](https://clawhub.ai/user/amaury95)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to let an agent perform read-only Jira Cloud lookups, inspect issues and projects, run JQL searches, and produce JSON directories of current-user open tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read Jira data available to the supplied API token, which may include sensitive issue content.

Mitigation: Use a narrowly scoped read-only Atlassian token and install the skill only where Jira read access is intended.

Risk: Incorrect or untrusted Jira configuration can point the skill at the wrong tenant or expose credentials through local environment files.

Mitigation: Set JIRA_BASE_URL to the intended Jira Cloud tenant, prefer JIRA_CLOUD_ID to avoid discovery, and do not use an untrusted .env or JIRA_ENV_FILE.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amaury95/skills/jira-reader)
- [Publisher profile](https://clawhub.ai/user/amaury95)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Jira data is scoped by the configured Atlassian account, token permissions, project filter, and --max limit.]

## Skill Version(s):

0.4.0 (source: server release evidence, SKILL.md metadata, scripts/jira-reader.mjs VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
