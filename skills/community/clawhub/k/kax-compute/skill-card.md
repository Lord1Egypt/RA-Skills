## Description:

KAX Compute District helps agents inspect, commission, wake, fund, and operate KAX Compute machines through the kannaka CLI, kannaka Claude plugin MCP, or Command Center MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickflach](https://clawhub.ai/user/nickflach)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and resident agents use this skill to inspect KAX Compute machine state, commission one machine per identity, wake machines with signed jobs, grant internal credits, and configure signing credentials. It is intended for normal ClawHub use of KAX Compute rather than a demo or research-only scenario.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may require KAX identity tokens, NATS credentials, and operator signing keys that authorize sensitive KAX Compute actions.

Mitigation: Protect signing seeds and credentials as privileged secrets, prefer least-privilege signers, and install only when KAX Compute access is intended.

Risk: Wake and grant actions can spend machine credits and LLM budget.

Mitigation: Review wake and grant requests before execution, especially metered or operator-signed actions.

Risk: Incorrect signatures, non-canonical payloads, or stale clocks can cause rejected jobs.

Mitigation: Use the documented CLI or MCP signing surfaces when possible and keep clocks synchronized before troubleshooting keys.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nickflach/skills/kax-compute)
- [KAX Compute roster API](https://kax.ninja-portal.com/api/compute/machines)
- [Command Center MCP](https://nats.ninja-portal.com/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with command examples, JSON payload examples, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include KAX machine identifiers, signed wake or grant command shapes, credential setup guidance, and troubleshooting advice.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
