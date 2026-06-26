## Description: <br>
People-operations assistant covering the full employee lifecycle: recruiting, onboarding, performance reviews, compensation analysis, org planning, policy lookup, and people reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobiaswestholm](https://clawhub.ai/user/tobiaswestholm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR teams, people managers, recruiters, and employees use this skill to draft HR materials, analyze people-operations questions, prepare recruiting and onboarding workflows, review compensation context, and summarize policy or workforce data supplied by the user or connected systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can activate around sensitive HR topics and may handle employee, candidate, compensation, chat, calendar, and email data. <br>
Mitigation: Limit connected-system scopes, require explicit user confirmation before retrieving or sharing person-specific records, and avoid broad automatic use in casual conversations. <br>
Risk: The setup script fetches remote sub-skills that are not pinned in this package. <br>
Mitigation: Review the fetched sub-skills before deployment and verify their contents before connecting production HR systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tobiaswestholm/human-resources) <br>
- [Publisher profile](https://clawhub.ai/user/tobiaswestholm) <br>
- [Slack MCP server](https://mcp.slack.com/mcp) <br>
- [Notion MCP server](https://mcp.notion.com/mcp) <br>
- [Atlassian MCP server](https://mcp.atlassian.com/v1/mcp) <br>
- [Bootstrap dependency repository](https://github.com/anthropics/knowledge-work-plugins.git) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with tables and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference connected HRIS, ATS, knowledge base, calendar, chat, email, and compensation systems when configured by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
