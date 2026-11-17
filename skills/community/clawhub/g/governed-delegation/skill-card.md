## Description:

Governed Delegation helps agents decide the allowed execution envelope for subagent work, including model tier, fail-closed behavior, and auditable spawn requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joaodriessen](https://clawhub.ai/user/joaodriessen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and orchestrator maintainers use this skill when delegation is under consideration and they need policy-guided model-tier, runner, and fail-closed decisions before spawning subagents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Critical delegation decisions could be unreliable if the referenced canonical routing policy or policy modules are absent or untrusted.

Mitigation: Confirm the canonical routing policy and intent-router policy modules are present and trusted before relying on the skill for critical delegation decisions.

Risk: Incorrect task classification could produce an unsuitable delegation envelope for high-risk work.

Mitigation: Classify taskClass, deterministic, criticalWrite, and requiresDeepReasoning before delegation, and fail closed for Class C/D or critical-write work.

## Reference(s):

- [Governed Delegation Skill Page](https://clawhub.ai/joaodriessen/skills/governed-delegation)
- [Canonical Model Routing Policy](docs/MODEL_ROUTING_POLICY.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON decision output and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper returns a single delegation decision object with an optional auditable spawn request envelope.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
