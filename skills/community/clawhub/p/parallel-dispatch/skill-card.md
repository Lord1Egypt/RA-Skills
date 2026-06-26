## Description: <br>
Parallel Dispatch helps agents plan parallel execution for independent, batched, and dependency-aware tasks with result aggregation and error handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daxiangnaoyang](https://clawhub.ai/user/daxiangnaoyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to decide when work can run concurrently, select a dispatch pattern, and aggregate results safely across independent, batched, or dependency-aware tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Parallel task execution can perform side-effecting work faster than a reviewer can inspect each action. <br>
Mitigation: Require explicit user confirmation before writes, document creation, API calls, or other side-effecting tasks; cap concurrency and check rate limits before dispatch. <br>
Risk: Simple parallel examples may hide failed or timed-out subtasks if reused without completion checks. <br>
Mitigation: Verify every submitted task completed and inspect per-task success, error, and timeout fields before relying on aggregated results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daxiangnaoyang/parallel-dispatch) <br>
- [Publisher profile](https://clawhub.ai/user/daxiangnaoyang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python, PowerShell, JSON, and YAML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes concurrency limits, timeout controls, scheduling patterns, result aggregation, and error-handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
