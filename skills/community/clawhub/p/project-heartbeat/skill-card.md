## Description: <br>
Project Heartbeat helps agents design controlled continuation loops for long-running projects that need periodic wake-ups, explicit continue conditions, stop boundaries, pending-decision handling, progress logging, and resume rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daowuu](https://clawhub.ai/user/daowuu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project maintainers use this skill to decide whether a long-running project is a good fit for heartbeat-style continuation, then define cadence, continue conditions, stop boundaries, progress artifacts, pending-decision handling, and resume behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scan evidence says the target skill artifact was not available for direct confirmation in that review. <br>
Mitigation: Install with normal caution and review the packaged artifact files before use. <br>
Risk: Heartbeat-style continuation can create false progress if cycles continue without durable project artifact updates. <br>
Mitigation: Require each cycle to update a durable artifact such as STATE.md, TODO.md, PENDING-DECISIONS.md, HEARTBEAT-LOG.md, or a tracked decision or review document. <br>


## Reference(s): <br>
- [Project Heartbeat ClawHub page](https://clawhub.ai/daowuu/project-heartbeat) <br>
- [Boundaries](references/boundaries.md) <br>
- [Continuation Integrity](references/continuation-integrity.md) <br>
- [Examples](references/examples.md) <br>
- [Pending Decisions Template](references/pending-decisions-template.md) <br>
- [Heartbeat Log Template](references/heartbeat-log-template.md) <br>
- [Summary + Handoff](references/summary-handoff.md) <br>
- [Deferred Backlog](references/deferred-backlog.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with optional plain-text script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
0.4.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
