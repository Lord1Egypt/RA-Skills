## Description: <br>
Task queue management for creating, listing, cancelling, retrying, and daemon-running background tasks with priority-based execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michealxie001](https://clawhub.ai/user/michealxie001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users can use this skill to manage background task queues, inspect task state, retry failed work, and run a local scheduler daemon for controlled automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Background task execution may run handlers or long-lived work with the authority of the agent process. <br>
Mitigation: Run the scheduler in a controlled environment with least privilege, review task handlers before enabling them, and limit access to trusted users. <br>
Risk: Documented WebSocket task updates could expose task status, parameters, or results if deployed without authentication or transport protection. <br>
Mitigation: Keep any WebSocket service bound to localhost unless authentication and TLS are added, and avoid broadcasting sensitive task results. <br>
Risk: The artifact documents cron, WebSocket, and persistence behavior that is incomplete or not implemented in the provided files. <br>
Mitigation: Validate the specific CLI and API paths before relying on scheduled, real-time, or persistent behavior in production workflows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/michealxie001/oc-task-scheduler) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; CLI output is plain text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit task identifiers, status summaries, and JSON-like task metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
