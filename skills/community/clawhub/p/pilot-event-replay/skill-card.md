## Description:

Record and replay event streams for debugging, testing, and audit purposes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Pilot Event Replay to capture Pilot Protocol event streams into NDJSON recordings, replay them into test targets, debug event-driven workflows, and audit event history with timestamps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad event captures can record sensitive event data.

Mitigation: Capture only authorized streams, avoid broad wildcard captures unless necessary, use a private directory with restrictive permissions, and redact sensitive data before sharing recordings.

Risk: Replaying events can trigger duplicate downstream side effects.

Mitigation: Replay only into isolated test targets unless downstream systems are known to handle duplicate events safely.

## Reference(s):

- [Pilot Event Replay on ClawHub](https://clawhub.ai/teoslayer/skills/pilot-event-replay)
- [Pilot Protocol](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce NDJSON recording and replay commands that require pilotctl, jq, and a running Pilot Protocol daemon.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
