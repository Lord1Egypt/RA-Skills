## Description:

Coordinates Lingqu discovery-page Banner promotion workflows, including reservation intake, asset collection, schedule comparison, exception handling, tracking-table updates, and delegated promotion operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cloudmusiccio](https://clawhub.ai/user/cloudmusiccio)

### License/Terms of Use:

MIT-0

## Use Case:

Operations and product marketing employees use this skill to coordinate Lingqu discovery-page Banner reservations, material intake, schedule reconciliation, cancellations, replacements, and promotion handoffs while maintaining a shared tracking table.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad chat-triggered authority can change persistent campaign workflow state or trigger delegated production promotion actions.

Mitigation: Deploy only in controlled Lingqu Banner channels, restrict eligible groups and senders, and require explicit confirmation or authorization before accepting schedule changes, cancellations, replacements, or delegated promotion mutation handoffs.

Risk: Submitted images, URLs, and campaign metadata may be passed into the delegated promotion workflow.

Mitigation: Document how promotion-apply-skills handles submitted materials and review images, links, and campaign metadata under the operator's normal approval process before production use.

## Reference(s):

- [Lingqu Banner Config on ClawHub](https://clawhub.ai/cloudmusiccio/skills/lingqu-banner-config)
- [Configuration Matrix](references/config-matrix.md)
- [Hard Rules](references/hard-rules.md)
- [Phase One Reserve](references/phase-one-reserve.md)
- [Phase Two Material](references/phase-two-material.md)
- [Phase Three Config](references/phase-three-config.md)
- [Phase Three Exceptions](references/phase-three-exceptions.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with structured handoff details and occasional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include tracking-table updates, operator-facing confirmations or questions, and handoff instructions for delegated promotion operations.]

## Skill Version(s):

1.0.12 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
