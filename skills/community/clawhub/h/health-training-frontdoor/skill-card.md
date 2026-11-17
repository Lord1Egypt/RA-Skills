## Description:

Narrow first-class front door for live Fitbit/training retrieval via stable JSON actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joaodriessen](https://clawhub.ai/user/joaodriessen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw agents use this skill to retrieve live Fitbit, health, and training data through a narrow read-only JSON action contract instead of assembling low-level commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can bring sensitive personal health and training memory into agent context when used for coaching.

Mitigation: Install only if that local memory exposure is acceptable, or separate coaching references into a differently scoped skill.

Risk: The retrieval wrapper depends on authenticated Fitbit connector tooling and live local data.

Mitigation: Use it only where read-only Fitbit and training retrieval is expected, and do not use it for authentication bypass or write-capable operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joaodriessen/skills/health-training-frontdoor)
- [Practical Programming for Strength Training reference](reference/practical-programming/INDEX.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Compact JSON with action results and Markdown usage guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only retrieval surface with bounded supported actions and positive integer day windows.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
