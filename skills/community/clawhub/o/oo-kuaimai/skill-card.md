## Description:

Kuaimai ERP (kuaimai.com). Use this skill for ANY Kuaimai ERP request — reading, creating, and updating data. Whenever a task involves Kuaimai ERP, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to read Kuaimai ERP product, inventory, order, sales stockout, shop, and warehouse data through a connected account. It can also refresh the ERP session, which changes account state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute downloaded installer code that has not been verified.

Mitigation: Install and verify a fixed CLI release yourself, and require approval for setup changes.

Risk: Automatic agent-skill synchronization may change the instructions the agent follows.

Mitigation: Review or disable automatic synchronization.

Risk: ERP actions can access account data, and session refresh changes account state.

Mitigation: Connect only the intended ERP account and retain user confirmation for write actions.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Kuaimai ERP](https://www.kuaimai.com/)
- [Kuaimai API documentation](https://open.kuaimai.com/docs/api/API%E5对接说明/%E6%8E%A5%E5%85%A5%E6%8C%87%E5%8D%97/)
- [Kuaimai ERP on ClawHub](https://clawhub.ai/oomol/skills/oo-kuaimai)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Structured data]

**Output Format:** [CLI commands, JSON payloads, and structured ERP responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action schemas should be checked before requests; session refresh changes account state.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
