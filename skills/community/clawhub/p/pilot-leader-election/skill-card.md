## Description:

Elect a coordinator with automatic failover using heartbeat-based leader election.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to coordinate multi-agent swarms that need a single leader, heartbeat checks, and automatic failover.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example leader-election flows may be under-protected for high-impact autonomous coordination.

Mitigation: Harden examples before use by restricting election group names, validating payload schemas, and requiring authenticated registry participants.

Risk: Shell and jq examples interpolate runtime values that could be unsafe if copied without input controls.

Mitigation: Quote and validate inputs, pass jq values with --arg, and avoid using untrusted values directly in command strings.

Risk: Heartbeat timeout and election decision logic may not be reliable enough without environment-specific review.

Mitigation: Review timeout thresholds, term handling, and failover behavior before relying on the skill for coordination.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-leader-election)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, jq, cksum, the pilot-protocol skill, and a running Pilot daemon.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
