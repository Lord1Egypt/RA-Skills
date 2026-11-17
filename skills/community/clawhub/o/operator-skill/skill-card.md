## Description:

Orchestrates collaborative agent sessions with CRDT-backed persistent storage, append-only update logs, and session recovery actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[404-unknow](https://clawhub.ai/user/404-unknow)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to create, synchronize, and reload collaborative agent sessions that persist CRDT state on disk. It is intended for multi-agent workflows that need durable session recovery across runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session IDs and caller-chosen keys may have too much authority over persisted collaboration data.

Mitigation: Validate session IDs, enforce session ownership or participant ACLs, and bind accepted signatures to authorized session keys and nonces before using shared or sensitive sessions.

Risk: Unbounded payload or storage growth could affect workspace stability.

Mitigation: Add payload size limits, storage quotas, and retention controls for session snapshots and update logs.

Risk: The implementation and package metadata reference different Loro package names.

Mitigation: Resolve the loro versus loro-crdt dependency mismatch and rebuild before release or installation.

Risk: Persisted collaboration data may contain sensitive information.

Mitigation: Use an isolated workspace and avoid storing secrets or sensitive collaboration data until the security guidance is addressed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/404-unknow/skills/operator-skill)
- [Publisher profile](https://clawhub.ai/user/404-unknow)

## Skill Output:

**Output Type(s):** [JSON, Files, Configuration, Guidance]

**Output Format:** [JSON action responses with persisted snapshot and update-log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and reads session data under data/sessions; team.load returns a base64 full-merged snapshot.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
