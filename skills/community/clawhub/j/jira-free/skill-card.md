## Description: <br>
Jira集成引擎(免费版) helps agents guide Jira REST API workflows for issue management, sprint and board operations, JQL queries, and workflow transitions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project teams use this skill to plan and draft Jira REST API requests for issues, sprints, boards, JQL searches, workflow transitions, comments, and reporting. It is suited to Jira Cloud and Jira API workflows, not Jira plugin development or Jira Server/Data Center installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide create, update, sprint, transition, and comment operations against live Jira projects. <br>
Mitigation: Use least-privilege Jira API tokens and require explicit confirmation before running any write operation. <br>
Risk: Jira API tokens or account credentials can be exposed through prompts, shell history, logs, or shared command snippets. <br>
Mitigation: Keep tokens out of version control and shared transcripts, prefer environment variables or a secret manager, and rotate any token that may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/jira-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Atlassian API tokens](https://id.atlassian.com/manage-profile/security/api-tokens) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl examples and JSON response shapes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Jira REST API requests that read from or modify live Jira data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
