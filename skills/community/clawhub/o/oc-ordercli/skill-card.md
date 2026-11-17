## Description:

Foodora-only CLI for checking past orders and active order status (Deliveroo WIP).

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators can use the CLI to inspect Foodora order history and track active deliveries. It also documents an optional reorder flow that adds items to a cart.

### Deployment Geography for Use:

Global, where Foodora is available

## Known Risks and Mitigations:

Risk: The documented reorder action can add items to a Foodora cart, beyond checking order status and history.

Mitigation: Review the reorder preview and verify the intended order and address before using --confirm.

## Reference(s):

- [Ordercli homepage](https://ordercli.sh)
- [Foodora](https://www.foodora.at/)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
