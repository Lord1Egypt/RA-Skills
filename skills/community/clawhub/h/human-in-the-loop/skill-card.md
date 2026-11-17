## Description:

Gates each agent write behind approval of an exact action, with expiring single-use decisions, crash reconciliation, and a drafts-only filter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexbloch-ia](https://clawhub.ai/user/alexbloch-ia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to require human approval before an agent creates or changes records, sends content, or makes payments. It also supports draft-only workflows and recovery when a write's outcome is uncertain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approval secrets or local approval state could be exposed through poorly chosen storage paths or permissions.

Mitigation: Choose state and lock paths deliberately, restrict access to them, and protect the approval secret.

Risk: Pruning applied entries before reconciliation lookups can no longer reach them may allow duplicate writes.

Mitigation: Retain applied entries until reconciliation lookups no longer need them; prune only after that window closes.

## Reference(s):

- [Human in the Loop release on ClawHub](https://clawhub.ai/alexbloch-ia/skills/human-in-the-loop)
- [OpenClaw homepage](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Guidance, Text, Shell commands]

**Output Format:** [Markdown guidance and plain-text approval requests, status, and run summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Approval is limited to one exact action; unresolved writes require reconciliation before retry.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
