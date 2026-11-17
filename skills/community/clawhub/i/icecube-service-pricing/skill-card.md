## Description:

Provides standardized pricing tables, quote templates, payment workflow language, and income tracking guidance for OpenClaw-related service offerings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ares521521-design](https://clawhub.ai/user/ares521521-design)

### License/Terms of Use:

MIT-0

## Use Case:

External service providers and OpenClaw consultants use this skill to prepare service quotes, payment schedules, collection messages, and monthly service income records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent service records may expose customer names, payment amounts, receivables, or payment status.

Mitigation: Use only approved private storage, avoid shared or synced memory for customer and receivable data, define retention and deletion rules, and never store payment credentials or full account details.

Risk: Generic pricing or payment conversations may be steered into this specific IceCube service workflow.

Mitigation: Enable the skill only for intended IceCube or OpenClaw service-pricing contexts and review generated quotes before sending them to customers.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown with pricing tables, quote templates, checklists, and message templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include RMB-denominated prices, payment milestones, payment-channel guidance, and customer status tracking templates.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
