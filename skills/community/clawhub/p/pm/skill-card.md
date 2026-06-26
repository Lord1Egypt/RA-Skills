## Description: <br>
PM guides an agent through project planning, API contract design, task breakdown, iterative implementation, testing, and status updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zengn1](https://clawhub.ai/user/zengn1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to have an agent establish architecture and API contracts, split work into small tasks, implement changes iteratively, run local verification, and keep planning and error logs current. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to manage planning documents, edit code, and run local tests in a project. <br>
Mitigation: Install it only in projects where that workflow is intended, and review generated planning files, code changes, and test results before approving continued work. <br>
Risk: Status and error logs may shape later development decisions if they are inaccurate or outdated. <br>
Mitigation: Review ARCHITECTURE.md, TASK_TRACKER.md, and ERROR_LOG.md after each completed task and correct stale or misleading entries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zengn1/pm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with project documents, code changes, test commands, and status updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update ARCHITECTURE.md, TASK_TRACKER.md, and ERROR_LOG.md in the active project.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
