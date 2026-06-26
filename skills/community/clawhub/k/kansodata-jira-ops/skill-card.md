## Description: <br>
A read-only operational skill for Jira Cloud analysis focused on issue context, blockers, backlog triage, and stakeholder status updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kansodata](https://clawhub.ai/user/kansodata) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product, engineering, and support teams use this skill to inspect Jira Cloud issues, summarize current status, identify blockers, triage backlogs, and draft stakeholder updates without modifying Jira. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated summaries may include sensitive Jira business data from issues, comments, and worklogs. <br>
Mitigation: Restrict the Jira plugin account to intended projects and read-only scopes, and share outputs only with authorized recipients. <br>
Risk: Incomplete Jira data or insufficient permissions can lead to overconfident blocker, priority, or status conclusions. <br>
Mitigation: Preserve the skill's required separation between observed facts, inferences, and missing data before acting on its guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kansodata/kansodata-jira-ops) <br>
- [Publisher profile](https://clawhub.ai/user/kansodata) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Usage rules](artifact/usage-rules.md) <br>
- [Examples](artifact/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Separates observed Jira facts, inferences, and missing data or insufficient permissions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
