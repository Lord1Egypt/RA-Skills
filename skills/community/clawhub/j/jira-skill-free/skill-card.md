## Description: <br>
Jira集成助手-免费版 helps agents read Jira Cloud issues by searching tickets, viewing issue details, generating browser links, listing available transitions, and showing the user's open assigned issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project teams use this skill to browse Jira Cloud work items from an agent session without performing Jira write actions. It is suited for searching issues, checking details and transitions, generating Jira browser links, and reviewing assigned open work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on the user's Jira API token and may read Jira ticket data available to that account. <br>
Mitigation: Use a least-privilege Jira token, avoid highly sensitive Jira projects unless approved by the organization, and review agent-mediated Jira access before installation. <br>
Risk: If JIRA_BOARD is unset, searches may span all Jira projects the token can access. <br>
Mitigation: Set JIRA_BOARD to constrain the project scope whenever possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/jira-skill-free) <br>
- [Atlassian API token management](https://id.atlassian.com/manage-profile/security/api-tokens) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Jira Cloud queries require JIRA_EMAIL, JIRA_API_TOKEN, JIRA_URL, and optional JIRA_BOARD; output may include Jira issue data.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; SKILL.md frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
