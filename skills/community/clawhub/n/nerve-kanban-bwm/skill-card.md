## Description: <br>
Interact with the Nerve Kanban board API to create, update, delete, reorder, execute, approve, reject, abort, propose, and configure Kanban tasks under /api/kanban. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blueworldmarketing](https://clawhub.ai/user/blueworldmarketing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate a Nerve Kanban board through its REST API, including task CRUD, workflow transitions, proposal review, and board configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The API includes sensitive board-changing actions such as delete, execute, approve, reject, complete, and configuration updates. <br>
Mitigation: Install only for trusted Nerve boards and confirm that the Nerve server enforces authentication, authorization, and audit logging before agents use shared or production boards. <br>
Risk: Concurrent task updates can conflict if an agent acts on stale task versions. <br>
Mitigation: Use the documented CAS version field, re-read on 409 version_conflict, and retry only with the server's latest task state. <br>


## Reference(s): <br>
- [Nerve Kanban API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with REST endpoint descriptions, JSON request and response shapes, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes task and proposal operations, board configuration, workflow transition rules, and CAS version guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
