## Description:

Connect an agent to Waffo Pancake to query stores, products, orders, payments, refunds, and customers, and to manage checkout, products, refunds, and subscriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Waffo merchants use the skill to inspect commerce data and perform supported store, product, checkout, subscription, and refund tasks through their connected Waffo account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI can install persistent skills across other agents, and the skill does not explain that impact.

Mitigation: Preinstall a verified CLI and set OO_SKILLS_SYNC_DISABLED=1 before invoking it, following the security guidance.

Risk: Write and destructive actions can change Waffo data, including publishing products, changing subscriptions, and submitting refunds.

Mitigation: Review the exact payload and effect with the user before write actions, and get explicit approval for destructive actions.

## Reference(s):

- [Waffo Pancake](https://www.waffo.ai)
- [Waffo API authentication documentation](https://docs.waffo.ai/api-reference/authentication)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [JSON request payloads and API results, with shell command examples in Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only queries and searches, plus state-changing actions that require user confirmation]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
