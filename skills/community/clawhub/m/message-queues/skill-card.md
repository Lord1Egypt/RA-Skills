## Description:

Message Queues provides a deep workflow for queue versus topic selection, ordering and partitions, retries and DLQ, idempotency, backpressure, observability, and failure design when integrating workers, event buses, or debugging poison messages and lag.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawkk](https://clawhub.ai/user/clawkk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design or troubleshoot message-queue and event-driven workflows, including delivery semantics, ordering, partitioning, retries, DLQs, replay, lag, and operational readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider-specific queue behavior may differ from the architectural guidance and could affect production correctness.

Mitigation: Verify details such as SQS visibility timeouts and Kafka ordering guarantees against current vendor documentation before making production changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawkk/skills/message-queues)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown guidance with staged workflow prompts, checklists, and concise architectural recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no sensitive access, execution, or persistence requested.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
