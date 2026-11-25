## Description:

Triage OpenViking memory pipeline failures (empty memory, no extraction, recall misses): write a probe to expose the quota layer, check server-side events, then diagnose across network, auth, quota, threshold, and extraction layers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoyunlai](https://clawhub.ai/user/zuoyunlai)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to diagnose empty or stale OpenViking memories, verify whether writes reached server-side storage, and identify the likely failing pipeline layer and next troubleshooting step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A memory_store probe creates a write, and a delayed or missing tool response does not establish whether it succeeded; retrying blindly can create duplicate records.

Mitigation: Issue the probe once, then check the documented server-side event location before deciding whether another write is needed.

Risk: Some troubleshooting guidance is based on environment-specific observations and points to local procedures that are not included with this release.

Mitigation: Confirm conclusions against current probe results, timestamped server-side events and logs, and verify any referenced local procedure before following it.

Risk: The supplied security assessment reports medium confidence and a partial scan due to missing local references.

Mitigation: Review the unresolved references and the skill's guidance before relying on it for diagnosis.

## Reference(s):

- [ClawHub release: openviking-memory-triage](https://clawhub.ai/zuoyunlai/skills/openviking-memory-triage)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands]

**Output Format:** [Markdown with diagnostic evidence and recommended next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A five-layer triage conclusion with supporting probe, log, or server-side storage evidence.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
