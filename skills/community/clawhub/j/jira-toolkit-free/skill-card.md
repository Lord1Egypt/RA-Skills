## Description: <br>
Jira 事务工具包基础版 helps agents use natural language to view, create, update, transition, assign, and comment on Jira issues through CLI or tool-service workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project contributors use this skill to inspect Jira issues, run JQL searches, create single issues, update issue state or ownership, and add comments from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run commands and modify Jira data. <br>
Mitigation: Use a least-privilege Jira account and require explicit confirmation before create, update, transition, assignment, or comment actions. <br>
Risk: The artifact's local-only privacy statement may understate Jira backend data exposure. <br>
Mitigation: Treat Jira issue data and credentials as used with Atlassian or Jira backends and follow organizational data-handling rules. <br>
Risk: Broad trigger guidance may cause use outside the intended Jira issue-management scope. <br>
Mitigation: Invoke the skill only for Jira issue workflows and review generated commands or tool actions before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/jira-toolkit-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured JSON, text, or CSV result expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute Jira CLI or tool-service operations; require explicit confirmation before any create, update, transition, assignment, or comment action.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
