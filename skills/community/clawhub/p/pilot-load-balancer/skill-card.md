## Description:

Distribute tasks across worker pools with health-aware load balancing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to distribute tasks across Pilot Protocol worker agents with round-robin, least-connections, or health-aware routing while tracking worker capacity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends task-assignment messages to worker pools.

Mitigation: Install only for Pilot Protocol worker pools where this message flow is expected and acceptable.

Risk: The shell examples use a /tmp state file and string-built JSON payloads.

Mitigation: Before production use, replace the /tmp state file with a private locked state location and build JSON payloads with a JSON-aware encoder.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-load-balancer)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl, jq, uuidgen, the pilot-protocol skill, and a running pilotctl daemon.]

## Skill Version(s):

1.0.0 (source: server release metadata, created 2026-04-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
