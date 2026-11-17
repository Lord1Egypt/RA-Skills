## Description:

Kiwi helps agents handle general purchasing, supplier discovery, quote requests, price comparison, negotiation, delivery/MOQ questions, non-binding agreements, and handoff by using the kiwi_buyer_* tools from the ClawHub kiwi plugin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and procurement users use this skill to discover merchants or suppliers, request and compare quotes, negotiate terms, accept non-binding agreements after user confirmation, and generate checkout or purchase-order handoff links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help negotiate and approve procurement agreements through the external Kiwi plugin.

Mitigation: Confirm trust in the clawhub:kiwi plugin publisher before installation and keep explicit user confirmation before any approval action.

Risk: Automatic approval flows could bypass the intended procurement review step.

Mitigation: Do not enable automatic approvals; present the agreement summary to the user before calling kiwi_buyer_approve.

Risk: The skill produces non-binding agreements and handoff links rather than payment, order creation, or inventory reservation.

Mitigation: Review final terms before handoff and treat checkout or purchase-order completion as a separate downstream step.

## Reference(s):

- [kiwi-buyer on ClawHub](https://clawhub.ai/harrylabsj/skills/kiwi-buyer)
- [Publisher profile: harrylabsj](https://clawhub.ai/user/harrylabsj)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline tool names and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the ClawHub kiwi plugin and keeps approval actions gated on explicit user confirmation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
