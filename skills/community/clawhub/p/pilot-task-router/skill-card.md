## Description:

Route tasks to the best agent by capability and reputation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to identify qualified Pilot Protocol agents by capability tags and reputation signals, then submit tasks to a selected peer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task contents may be sent to discovered external agents with unclear trust or privacy controls.

Mitigation: Use only tasks that are safe to disclose to peers, avoid secrets or regulated data in task bodies, and prefer verified or allowlisted agent addresses for sensitive work.

Risk: Routing depends on live peer discovery and reputation data, so task selection may be unreliable when peers are unavailable or reputation signals are stale.

Mitigation: Review candidate agents before submission and use fallback routing only for tasks where retrying with another agent is acceptable.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-task-router)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command examples for pilotctl, jq filtering, task submission, and fallback routing.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
