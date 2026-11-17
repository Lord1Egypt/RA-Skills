## Description:

Industrial-grade scheduling and resource optimization for AI agents that solves task scheduling with energy matching, budget allocation, and LP/MIP constraint problems in milliseconds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whatsonyourmind](https://clawhub.ai/user/whatsonyourmind)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to solve scheduling, budget allocation, staffing, routing, capacity planning, and other constrained optimization problems through OraClaw's solver API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optimization inputs and API credentials are sent to OraClaw's solver service.

Mitigation: Install only after confirming the publisher and service are trusted for the scheduling, budget, staffing, or planning data being submitted.

Risk: Solver calls may incur the disclosed USDC/x402 pricing after any free tier.

Mitigation: Review pricing and usage limits before deployment, and monitor ORACLAW_API_KEY usage in production workflows.

## Reference(s):

- [OraClaw Solver Homepage](https://oraclaw.dev/solver)
- [ClawHub Skill Page](https://clawhub.ai/whatsonyourmind/skills/oraclaw-solver)

## Skill Output:

**Output Type(s):** [Guidance, JSON, Configuration]

**Output Format:** [Markdown guidance with JSON request examples and solver status descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ORACLAW_API_KEY and may incur the disclosed USDC/x402 per-call pricing after any free tier.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
