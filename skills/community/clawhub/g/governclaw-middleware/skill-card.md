## Description:

GovernClaw Policy Enforcer helps OpenClaw agents route HTTP requests through a GovernClaw policy service before execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aakash2289](https://clawhub.ai/user/aakash2289)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw agent builders use this skill to mediate external HTTP API calls through a GovernClaw policy service and receive explicit block reasons when policy denies a request. The current artifact implements governed HTTP behavior, not shell, file, or browser governance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured GovernClaw policy service receives request URLs, headers, bodies, and session or agent context for governed HTTP calls.

Mitigation: Set GOVERNCLAW_URL only to a GovernClaw service that is trusted and authorized to receive those request details.

Risk: Allowed HTTP requests can be rewritten by the policy service before execution.

Mitigation: Review policy service behavior and audit logs, and avoid sending secrets through governedHttp unless disclosure and rewriting are acceptable.

Risk: The current artifact implements HTTP governance only, even though broader shell, file, and browser wrappers are described as future work.

Mitigation: Continue using separate controls for shell, file, and browser actions until governed wrappers for those actions are implemented and reviewed.

## Reference(s):


## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON-like tool responses containing allowed HTTP results, request errors, or policy block reasons.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Governed HTTP calls can include audit logs on blocked requests, and allowed calls may use an effective payload returned by the policy service.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
