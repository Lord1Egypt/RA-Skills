## Description: <br>
Automates Jira Cloud REST and Agile API operations, including worklogs, JQL search, issues, sprints, and direct authenticated REST requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[temperatio](https://clawhub.ai/user/temperatio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate Jira Cloud from a workspace when jira-cli does not cover the needed REST or Agile API operation. It supports inspecting and changing issues, worklogs, comments, transitions, assignments, links, boards, sprints, and one-off authenticated REST calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act through the user's Jira account, including edit, delete, bulk inspection, and raw authenticated REST operations. <br>
Mitigation: Use a least-privilege Jira API token and review every edit, delete, bulk, or generic request command before running it. <br>
Risk: Generic REST requests can reach Jira endpoints without skill-specific guardrails. <br>
Mitigation: Check the exact HTTP method, path, query parameters, and payload before using the generic request command. <br>


## Reference(s): <br>
- [Jira REST Notes](references/jira-rest-notes.md) <br>
- [Endpoint Map](references/endpoint-map.md) <br>
- [Agile Sprints](references/agile-sprints.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands; helper commands print JSON to stdout.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Jira Cloud configuration and a Jira API token in netrc; edit, delete, bulk, and raw request operations should be reviewed before execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
