## Description: <br>
Guides an agent through creating, querying, updating, and deleting Feishu tasks and task lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenfa188](https://clawhub.ai/user/chenfa188) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users use this skill when they want an assistant to manage Feishu tasks and task lists, including creating tasks, listing unfinished work, updating due dates, completing or reopening tasks, and managing task-list membership. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad or ambiguous task-management requests can modify or delete the wrong Feishu task, assignee, or list membership. <br>
Mitigation: Use specific task or list names and GUIDs, and confirm before deletes, assignee changes, or membership changes. <br>
Risk: Created tasks may be hard to edit later if the requester is not included as a task member. <br>
Mitigation: Provide current_user_id from message context when creating tasks so the requester is added as a follower when needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration] <br>
**Output Format:** [Markdown with JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes required Feishu task and task-list parameters, role guidance, time-format guidance, and troubleshooting notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
