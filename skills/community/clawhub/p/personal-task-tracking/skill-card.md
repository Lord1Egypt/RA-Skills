## Description: <br>
Query and manage ClickUp via REST API and the local `scripts/query.sh` helper. Use when listing open or completed tasks, counting due work, looking up spaces or lists, checking assignee workload, fetching task details, creating tasks, or closing tasks in ClickUp. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mmaggiezhou](https://clawhub.ai/user/mmaggiezhou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and personal productivity users use this skill to query ClickUp task status, report due or completed work, inspect spaces and lists, and create or close ClickUp tasks through a configured API token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or close live ClickUp tasks in the connected workspace. <br>
Mitigation: Require the agent to show the exact list ID, task ID, title, and due date before creating or closing a task. <br>
Risk: The ClickUp API token could be mishandled or exposed during setup or execution. <br>
Mitigation: Use the least-privileged ClickUp token available and avoid printing the API key with echo or logs. <br>
Risk: The security scan verdict is suspicious because the skill can modify workspace state and lacks enough guardrails. <br>
Mitigation: Review the skill before installation and scan it before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mmaggiezhou/personal-task-tracking) <br>
- [ClickUp REST API task endpoint used by the skill](https://api.clickup.com/api/v2/team/{team_id}/task?include_closed=false&subtasks=true) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, curl, jq, CLICKUP_API_KEY, CLICKUP_TEAM_ID, and CLICKUP_ASSIGNEE_ID; helper commands can create or close live ClickUp tasks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
