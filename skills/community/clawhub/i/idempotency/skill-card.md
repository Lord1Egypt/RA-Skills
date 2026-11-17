## Description:

Guides agents through designing idempotent APIs, workers, and payment flows by identifying retry surfaces, choosing idempotency keys, defining storage and TTL, avoiding exactly-once assumptions, and testing duplicate delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codenova58](https://clawhub.ai/user/codenova58)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when designing safe mutating APIs, queue consumers, background jobs, and payment or inventory workflows that must tolerate retries and duplicate delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applying idempotency guidance incorrectly to payment or business-critical systems can affect production data behavior.

Mitigation: Review retention windows, tenant scoping, audit requirements, and conflict rules before deploying changes.

Risk: The skill provides design guidance that may be incomplete for a specific architecture or delivery system.

Mitigation: Validate the chosen API and worker patterns with duplicate-delivery tests before relying on them in production.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/codenova58/skills/idempotency)
- [Publisher Profile](https://clawhub.ai/user/codenova58)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance and review checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable output; the skill provides structured workflow guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
