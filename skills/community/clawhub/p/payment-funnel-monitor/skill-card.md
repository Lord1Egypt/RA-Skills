## Description:

Monitor the payment last mile from initiation through authorization outcome and local payment method gaps to recover conversion lost to failed checkouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rijoyai](https://clawhub.ai/user/rijoyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, ecommerce operators, and payment teams use this skill to investigate payment-step conversion loss, group gateway or decline failures, and prioritize local payment methods for underperforming markets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment analysis can expose sensitive customer payment details or credentials if raw operational exports are shared unnecessarily.

Mitigation: Use aggregated success rates, gateway error codes, ticket themes, and country-level summaries; avoid sharing raw customer payment details or credentials.

Risk: Gateway code meanings and local payment method availability can vary by provider and market.

Mitigation: Confirm recommendations against the merchant's live gateway, PSP settings, and current provider documentation before making production changes.

## Reference(s):

- [Payment codes and local methods](references/payment_codes_and_methods.md)
- [Payment Funnel Monitor on ClawHub](https://clawhub.ai/rijoyai/skills/payment-funnel-monitor)
- [RIJOY-AI publisher profile](https://clawhub.ai/user/rijoyai)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown with tables and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses merchant-provided payment metrics, gateway error codes, country-level summaries, and enabled payment methods when available.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
