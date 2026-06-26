## Description: <br>
Google Tasks API integration with managed OAuth for reading, creating, updating, and deleting Google Tasks task lists and tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage Google Tasks task lists and tasks through Maton-managed OAuth, including listing, creating, updating, moving, clearing, and deleting task data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MATON_API_KEY and connection URLs grant access to the connected Google Tasks account. <br>
Mitigation: Keep credentials and connection URLs private, store the API key in the environment, and avoid sharing them in prompts, logs, or screenshots. <br>
Risk: Requests may target the wrong Google Tasks account when multiple Maton connections exist. <br>
Mitigation: Specify the intended connection before running account-specific operations. <br>
Risk: Write, delete, move, and clear operations can modify or remove task data. <br>
Mitigation: Confirm the exact task list, task, and intended effect with the user before executing changes. <br>


## Reference(s): <br>
- [Google Tasks ClawHub Release](https://clawhub.ai/byungkyu/google-tasks-api) <br>
- [Google Tasks API Overview](https://developers.google.com/workspace/tasks) <br>
- [Google Tasks Tasks Reference](https://developers.google.com/workspace/tasks/reference/rest/v1/tasks) <br>
- [Google Tasks TaskLists Reference](https://developers.google.com/workspace/tasks/reference/rest/v1/tasklists) <br>
- [Maton CLI Manual](https://cli.maton.ai/manual) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, HTTP endpoints, and Python or JavaScript examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY and a Maton OAuth connection; write, delete, and clear operations require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
