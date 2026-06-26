## Description: <br>
Record and replay event streams for debugging, testing, and audit purposes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to capture event streams into NDJSON recordings, replay them against downstream consumers, debug event-driven workflows, and audit event history with timestamps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Captured event payloads may contain sensitive or operationally important data. <br>
Mitigation: Store recordings in protected locations, delete them when no longer needed, and review payload handling requirements before sharing or replaying recordings. <br>
Risk: Wildcard capture or replay into live destinations can affect systems beyond the intended test scope. <br>
Mitigation: Prefer narrow topics over wildcard capture and replay only into isolated test targets unless explicitly authorized for a live destination. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-event-replay) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command patterns for recording NDJSON event streams and replaying them with configurable host, topic, timeout, file, and delay values.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
