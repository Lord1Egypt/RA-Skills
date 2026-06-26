## Description: <br>
Integrate payments with provider selection, checkout flows, subscription billing, and security best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and product teams use this skill to choose payment providers, design checkout and webhook flows, manage subscriptions, and apply payment security practices before launch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment flows can create real charges, refunds, subscription changes, or access changes if guidance is applied directly to production systems. <br>
Mitigation: Test in sandbox mode first and require explicit approval before live charges, refunds, subscription changes, or access changes. <br>
Risk: Handling or logging sensitive payment data can increase PCI and privacy exposure. <br>
Mitigation: Use hosted checkout or tokenization, never store card data, and redact sensitive fields from webhook logs with limited retention. <br>


## Reference(s): <br>
- [Payments ClawHub release](https://clawhub.ai/ivangdavila/payments) <br>
- [Provider comparison](artifact/providers.md) <br>
- [Payment integration patterns](artifact/integration.md) <br>
- [Subscription billing](artifact/subscriptions.md) <br>
- [Payment security](artifact/security.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with checklists, comparison tables, and implementation patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no code, install hooks, credentials, or autonomous payment actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
