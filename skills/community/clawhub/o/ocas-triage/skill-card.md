## Description: <br>
System scheduler and priority queue manager. Determines what gets attention next across all pending work. Use when prioritizing competing tasks, checking queue state, preempting active work, auditing execution order, or passing a complex long-running task to Mentor. Assigns heartbeat cadence based on task priority before handoff. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[indigokarasu](https://clawhub.ai/user/indigokarasu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to prioritize competing work, inspect queue state, preempt active tasks, and hand complex long-running tasks to Mentor with priority-linked heartbeat cadence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local queue, journal, and history files can retain sensitive task details. <br>
Mitigation: Avoid placing secrets or highly sensitive details in task text, and periodically review or clear .triage data when retained history is sensitive. <br>
Risk: A scheduler can accidentally reorder or interrupt active work if invoked for the wrong task. <br>
Mitigation: Use it for explicit prioritization, queue status, interrupts, or Mentor handoffs, and review active and pending tasks before acting on preemption. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/indigokarasu/ocas-triage) <br>
- [Triage boundary contracts](references/boundary_contracts.md) <br>
- [Triage journal specification](references/journal_spec.md) <br>
- [Triage schemas](references/schemas.md) <br>
- [Triage scoring model](references/scoring_model.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [JSONL task and signal records with concise status or routing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local .triage queue, signal, decision, history, journal, and report files; Mentor-routed task_ready signals include heartbeat interval fields.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
