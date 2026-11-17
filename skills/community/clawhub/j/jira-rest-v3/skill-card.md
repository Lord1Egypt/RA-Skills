## Description:

Perform Jira Cloud daily tasks via REST API v3 and Jira Software Agile API, including issue search, creation, updates, comments, worklogs, boards, sprints, and transitions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thecybercore](https://clawhub.ai/user/thecybercore)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to have an agent perform Jira Cloud issue, comment, worklog, board, sprint, and transition tasks by building, executing, and summarizing real REST calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses live Jira credentials for real API calls.

Mitigation: Use a least-privilege Jira token, keep secrets out of logs and repositories, and install only when live Jira API access is intended.

Risk: A misconfigured base URL could send requests outside the approved Jira tenant.

Mitigation: Set ATREST_JIRA_BASE_URL only to the approved HTTPS Atlassian tenant before running requests.

Risk: Create, update, transition, and delete requests can change Jira data.

Mitigation: Review mutating requests before execution and require explicit user intent for destructive actions.

Risk: Temporary JSON payload files may persist or collide when reused.

Mitigation: Prefer unique temporary file names and clean up payload files after requests complete.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thecybercore/skills/jira-rest-v3)
- [CLI REST Quick Reference](refs/cli-rest-quickref.md)
- [Jira JSON Quick Reference](refs/jira-json-quickref.md)
- [JQL Cheat Sheet](refs/jql-cheatsheet.md)
- [App Embedding Quick Reference](refs/app-embedding-quickref.md)
- [OpenClaw Environment Example](refs/openclaw_env_example.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline Bash, PowerShell, curl, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces concrete Jira REST request guidance, command templates, environment variable requirements, JSON payload shapes, and response-summary conventions.]

## Skill Version(s):

1.1.0 (source: evidence.release.version and artifact manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
