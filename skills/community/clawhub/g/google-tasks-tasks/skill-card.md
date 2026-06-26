## Description: <br>
Google Tasks API integration with managed OAuth for managing task lists, tasks, due dates, notes, and completion state in Google Tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an OpenClaw chat workflow to Google Tasks through ClawLink, then list, create, update, complete, move, and delete tasks or task lists in the connected Google account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a connected Google account through managed OAuth, so tool calls can access task lists and task data for that account. <br>
Mitigation: Use the documented connection checks before task operations, keep account access scoped to the intended Google account, and review requested permissions before use. <br>
Risk: Write and destructive operations can create, update, move, delete, or clear Google Tasks resources. <br>
Mitigation: Preview and confirm the target resource and intended effect before any write or destructive call, and prefer list or get operations before changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/google-tasks-tasks) <br>
- [Google Tasks API Overview](https://developers.google.com/tasks/reference/rest) <br>
- [Google Tasks Tasklists Reference](https://developers.google.com/tasks/reference/rest/v1/tasklists) <br>
- [Google Tasks Tasks Reference](https://developers.google.com/tasks/reference/rest/v1/tasks) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline shell commands and JSON parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Google Tasks data returned by ClawLink tools and setup guidance for the ClawLink plugin.] <br>

## Skill Version(s): <br>
1.0.6 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
