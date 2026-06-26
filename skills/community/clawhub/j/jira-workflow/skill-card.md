## Description: <br>
Integrates Jira Cloud project management so agents can search, create, update, transition, comment on, and inspect Jira issues, projects, and boards through the MorphixAI proxy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paul-leo](https://clawhub.ai/user/paul-leo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and project teams use this skill to manage Jira Cloud work items from an agent session, including listing projects, searching scoped JQL, creating issues, updating fields, transitioning statuses, and adding comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a MorphixAI API key and a linked Jira account to access Jira Cloud through a proxy. <br>
Mitigation: Store MORPHIXAI_API_KEY securely, avoid exposing it in prompts or logs, and link only the Jira account needed for the intended workspace. <br>
Risk: Jira actions can create issues, update fields, add comments, and transition workflow status. <br>
Mitigation: Review target project keys, issue keys, JQL filters, field updates, comments, and status transitions before execution, especially in production Jira projects. <br>
Risk: The security scan reported no artifact-backed concern but advised normal caution for network access, credential handling, file writes, or background behavior. <br>
Mitigation: Review the SKILL.md before deployment and monitor actual tool behavior during first use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paul-leo/jira-workflow) <br>
- [MorphixAI API keys](https://morphix.app/api-keys) <br>
- [MorphixAI connections](https://morphix.app/connections) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown with inline tool-call examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MORPHIXAI_API_KEY and a linked Jira account.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
