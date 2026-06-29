## Description: <br>
Google Tasks API integration with managed OAuth for managing task lists and tasks with full CRUD operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to manage Google Tasks task lists and tasks through Maton, including reading, creating, updating, moving, deleting, and clearing tasks after confirming intended write actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, delete, move, and clear Google Tasks data through a Maton-managed connection. <br>
Mitigation: Confirm the exact task list, task, connection, and intended effect before any write, delete, move, or clear action. <br>
Risk: The skill depends on MATON_API_KEY and routes Google Tasks requests through Maton as a third-party proxy. <br>
Mitigation: Install only when Maton is acceptable for the use case, use the narrowest appropriate Google Tasks connection, and avoid printing or sharing MATON_API_KEY. <br>


## Reference(s): <br>
- [Google Tasks API Overview](https://developers.google.com/workspace/tasks) <br>
- [Tasks Reference](https://developers.google.com/workspace/tasks/reference/rest/v1/tasks) <br>
- [TaskLists Reference](https://developers.google.com/workspace/tasks/reference/rest/v1/tasklists) <br>
- [Maton CLI Manual](https://cli.maton.ai/manual) <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/skills/google-tasks-api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline shell, Python, JavaScript, HTTP, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, a valid MATON_API_KEY, and an active Google Tasks OAuth connection through Maton.] <br>

## Skill Version(s): <br>
1.0.6 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
