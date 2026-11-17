## Description:

Jira API工具 helps agents automate Jira API workflows, including managed OAuth, JQL issue search, issue creation or updates, and board management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, enterprise teams, and automation workflow owners use this skill to search Jira issues with JQL, create or update issues, and manage Jira board workflows through API-backed agent interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify or delete Jira data without clearly scoped safeguards.

Mitigation: Use least-privilege Jira and Maton credentials, avoid delete or broad project-admin scopes unless required, and require explicit confirmation before writes, closes, deletes, or bulk changes.

Risk: The skill requests command execution and file-writing powers beyond normal Jira API use.

Mitigation: Treat local command execution and file-writing requests as separate privileged actions and review them before running.

Risk: The skill requires API credentials.

Mitigation: Store MATON_API_KEY outside source control, rotate credentials when needed, and use a dedicated account with only required Jira permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/jira-api-toolkit)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands, JavaScript examples, and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Jira API calls or configuration steps that require MATON_API_KEY and Jira/Maton connection state.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 1.0.10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
