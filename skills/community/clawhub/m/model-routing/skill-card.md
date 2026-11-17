## Description:

Automatically routes agent requests to an appropriate model based on task type, explicit model overrides, safety caps, retry behavior, and budget limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sam-k-migz](https://clawhub.ai/user/sam-k-migz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to choose cost- and capability-appropriate models for coding, reasoning, simple, and general tasks while respecting explicit model locks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model routing can affect answer quality, latency, and cost when a request is assigned to a different model tier.

Mitigation: Respect explicit user, organization, channel, and session model overrides before applying automatic routing.

Risk: Routing traces may expose task classification and selected model information to internal telemetry systems.

Mitigation: Record only lightweight routing data and confirm trace handling where users do not want routing traces retained.

Risk: Retries and fallbacks can increase cost or change behavior if they move requests to higher tiers.

Mitigation: Use the documented per-turn budget ceiling and only downgrade model tiers during retry fallback.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sam-k-migz/skills/model-routing)
- [Publisher profile](https://clawhub.ai/user/sam-k-migz)

## Skill Output:

**Output Type(s):** [guidance, configuration]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Model-selection guidance with retry, concurrency, token-cap, budget, fallback, and lightweight telemetry considerations.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
