## Description: <br>
Orchestrates collaborative agent sessions with persistent CRDT storage, signed update synchronization, and crash recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[404-UNKNOW](https://clawhub.ai/user/404-UNKNOW) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to create, synchronize, and reload persistent collaborative sessions for multi-agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent shared session data may contain sensitive or unintended state. <br>
Mitigation: Use only non-sensitive collaborative session data in an isolated workspace and define clear retention or purge controls before broader use. <br>
Risk: Session updates mutate shared state and are too loosely scoped without stronger controls. <br>
Mitigation: Require strict sessionId validation, participant allowlists, and auditable signature verification before using the skill with trusted workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/404-UNKNOW/operator-skill) <br>
- [Publisher profile](https://clawhub.ai/user/404-UNKNOW) <br>


## Skill Output: <br>
**Output Type(s):** [Structured data, Files, Configuration] <br>
**Output Format:** [JSON-style action responses with persisted CRDT snapshot and update-log files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns session identifiers, synchronization status, and base64-encoded merged session snapshots.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
