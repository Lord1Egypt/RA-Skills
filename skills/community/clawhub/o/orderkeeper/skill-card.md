## Description:

Post-purchase order and after-sales management skill for mainland China shopping and delivery scenarios that records order state, arrival, return or exchange windows, price-protection windows, warranty period, and issue evidence, then decides whether the user should request a refund, replacement, reshipment, compensation, warranty service, or wait; generates customer-service scripts; and outputs an after-sales card linking receipt, warranty, and outcome.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to organize post-purchase order problems, preserve evidence, identify urgent refund, exchange, reshipment, compensation, price-protection, or warranty actions, and generate concise Chinese customer-service scripts and after-sales cards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process private order, receipt, invoice, warranty, chat, or screenshot details.

Mitigation: Share only the order details needed for the after-sales decision and redact unnecessary personal data before use.

Risk: Generated customer-service wording may not match the user's preferred language, platform policy, or exact order facts.

Mitigation: Review and adjust each generated message before sending it to a seller, platform, carrier, or service provider.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/orderkeeper)
- [After-Sales Cards](references/after-sales-cards.md)
- [Deadline Triage](references/deadline-triage.md)
- [Support Script Frames](references/support-script-frames.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style Chinese after-sales verdicts, evidence checklists, customer-service scripts, and after-sales cards]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code or tool calls; outputs depend on user-provided order details, screenshots, deadlines, receipts, warranty information, and policy evidence.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
