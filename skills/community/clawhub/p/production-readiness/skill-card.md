## Description:

Meta-skill that orchestrates logging, monitoring, error handling, performance, security, deployment, and testing skills to ensure a service is fully production-ready before launch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill before first deploys, major releases, quarterly reviews, post-incident hardening, dependency upgrades, and team handoffs to produce a unified production readiness assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable remote installer sources can change after review.

Mitigation: Pin installer sources to a fixed ClawHub version and an immutable release tag or commit before running installation commands.

Risk: The skill delegates parts of the review to other named skills or agents.

Mitigation: Review and trust the delegated skills before relying on the synthesized production readiness result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/production-readiness)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown readiness assessment with checklists, maturity guidance, and go/no-go recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Synthesizes delegated operational reviews across logging, error handling, performance, security, deployment, testing, and documentation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
