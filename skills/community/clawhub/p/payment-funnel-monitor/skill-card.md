## Description: <br>
Monitor the payment last mile from initiation through authorization outcomes and local payment-method gaps to recover conversion lost to failed checkouts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RIJOYAI](https://clawhub.ai/user/RIJOYAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Commerce operators, growth teams, support teams, and developers use this skill to diagnose payment-step failures, interpret gateway decline families, and prioritize local payment methods for underperforming markets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment reports and decline-code samples may contain sensitive customer or transaction details. <br>
Mitigation: Share only the minimum needed metrics and prefer anonymized decline-code samples over raw customer exports. <br>
Risk: Gateway, fraud-rule, 3DS, or payment-method recommendations can affect checkout behavior and revenue. <br>
Mitigation: Manually verify recommended gateway or payment-method changes before applying them. <br>


## Reference(s): <br>
- [Payment codes and local methods](references/payment_codes_and_methods.md) <br>
- [Payment Funnel Monitor on ClawHub](https://clawhub.ai/RIJOYAI/payment-funnel-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown tables and checklist-style recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses merchant-provided payment metrics, country performance, gateway codes, ticket themes, and enabled payment methods when available.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
