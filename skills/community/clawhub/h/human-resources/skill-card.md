## Description:

People-operations assistant covering the full employee lifecycle, including recruiting, onboarding, performance reviews, compensation analysis, org planning, policy lookup, and people reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobiaswestholm](https://clawhub.ai/user/tobiaswestholm)

### License/Terms of Use:

MIT-0

## Use Case:

HR teams, people-operations staff, managers, and recruiting teams use this skill to draft HR materials, analyze people-operations questions, prepare review and hiring workflows, look up policy context, and produce structured HR reports from user-provided or connected data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow installs core sub-skill instructions from an unpinned remote repository before the skill handles sensitive HR workflows.

Mitigation: Prefer a release that vendors the sub-skills or pins and verifies the upstream commit and hashes before installation.

Risk: Connected HRIS, ATS, email, chat, calendar, knowledge-base, and compensation-data systems can expose sensitive employee and candidate information.

Mitigation: Grant only the minimum connector access needed for the specific task and review outputs before acting on HR, compensation, recruiting, or policy guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobiaswestholm/skills/human-resources)
- [Remote sub-skill source used by setup.sh](https://github.com/anthropics/knowledge-work-plugins.git)
- [Slack MCP endpoint](https://mcp.slack.com/mcp)
- [Notion MCP endpoint](https://mcp.notion.com/mcp)
- [Atlassian MCP endpoint](https://mcp.atlassian.com/v1/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with structured templates, tables, checklists, and inline shell commands when setup is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use connected HRIS, ATS, knowledge-base, calendar, chat, email, or compensation-data context when the user grants access; otherwise operates from user-provided context.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
