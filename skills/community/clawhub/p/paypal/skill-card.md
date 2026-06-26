## Description: <br>
Integrate PayPal payments with proper webhook verification, OAuth handling, and security validation for checkout flows and subscriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to integrate PayPal REST API checkout, subscriptions, payouts, webhook verification, OAuth token handling, refunds, and dispute workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated PayPal capture, refund, subscription, webhook, or dispute-handling code can affect payments if connected directly to production credentials. <br>
Mitigation: Use sandbox first and manually review payment-impacting code before connecting production credentials. <br>
Risk: PayPal client secrets could be exposed if copied into code or logs. <br>
Mitigation: Keep PayPal client secrets out of source code and logs, and use environment-specific credential handling. <br>
Risk: Unverified or duplicate webhooks could lead to unauthorized or repeated order processing. <br>
Mitigation: Verify PayPal webhook signatures through PayPal's verification API and record processed event IDs for idempotency. <br>


## Reference(s): <br>
- [PayPal skill release](https://clawhub.ai/ivangdavila/paypal) <br>
- [Code Patterns - PayPal Integration](patterns.md) <br>
- [Webhook Events - PayPal Integration](webhooks.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JavaScript, HTML, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance for PayPal integration patterns; no tools or required binaries are declared.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
