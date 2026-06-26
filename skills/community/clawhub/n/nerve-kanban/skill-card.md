## Description: <br>
Nerve Kanban lets agents interact with the Nerve Kanban board API to create, update, move, execute, approve, reject, abort, and configure tasks under /api/kanban. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanford](https://clawhub.ai/user/seanford) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to manage Nerve Kanban board tasks, proposals, workflow transitions, and board configuration through the documented REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documents state-changing actions including deletes, config changes, task execution, completion, approval, rejection, and abort operations. <br>
Mitigation: Require explicit operator approval for destructive or workflow-changing requests before sending them to the Nerve server. <br>
Risk: Kanban task completion and execution state depend on the Nerve server enforcing access control and run ownership. <br>
Mitigation: Use this skill only with a Nerve server that enforces authentication, authorization, and run ownership checks, especially for completion webhook calls. <br>
Risk: Concurrent task updates can conflict with the server's current task version. <br>
Mitigation: Include the current task version in update and reorder requests, then re-read and retry with the latest task when the API returns a version conflict. <br>


## Reference(s): <br>
- [Nerve Kanban API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces task, proposal, workflow, and board-configuration requests for the Nerve Kanban REST API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
