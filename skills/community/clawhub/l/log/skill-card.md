## Description: <br>
A privacy-first, local-first provenance protocol for agent workflows that emits structured audit records for important decisions, tool calls, state changes, and errors so the host environment can store, verify, and review them safely. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AGIstack](https://clawhub.ai/user/AGIstack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to emit concise, redacted provenance records for important workflow events, including decisions, tool executions, state changes, failures, and approval signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Log records may still reveal sensitive workflow context if stored without appropriate controls. <br>
Mitigation: Use host-side retention, access control, and redaction policies that match the sensitivity of the workflows being logged. <br>
Risk: The skill emits approval signals but does not enforce blocking, persistence, encryption, or immutability. <br>
Mitigation: Rely on the host environment to implement approval gates and storage guarantees before using the records for audit or compliance workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AGIstack/log) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown with a fenced JSON log record prefixed by [LOG_ENTRY]] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Records are expected to be minimal, factual, privacy-safe, and redacted before host storage.] <br>

## Skill Version(s): <br>
1.1.1 (source: release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
