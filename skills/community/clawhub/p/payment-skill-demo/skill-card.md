## Description: <br>
Provides payment tools for creating payment requests, checking payment status, and initiating refunds through a configured payment API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neverSatRabbit](https://clawhub.ai/user/neverSatRabbit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external commerce workflows can invoke the CLI-backed tools to create customer payment authorization requests, check transaction status, and initiate refunds against a configured payment provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create payment requests and initiate refunds with live credentials without a clearly enforced confirmation boundary. <br>
Mitigation: Use test or least-privilege credentials first, and require an external approval and audit process before allowing create_payment or refund_payment against production accounts. <br>
Risk: Payment operations depend on the configured payment endpoint and publisher-controlled integration. <br>
Mitigation: Install only if the publisher and configured endpoint are trusted, verify the payment API URL and TLS settings, and scope credentials to the intended environment. <br>
Risk: Diagnostics, logs, or terminal output may expose operational details when shared. <br>
Mitigation: Avoid running diagnostics in shared terminals or logs, and review generated log output before sharing it outside the operating team. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/neverSatRabbit/payment-skill-demo) <br>
- [Publisher profile](https://clawhub.ai/user/neverSatRabbit) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Shell commands, Configuration] <br>
**Output Format:** [JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires payment API credentials in environment variables and returns success, status, transaction, payment, refund, verification URL, or error fields depending on the command.] <br>

## Skill Version(s): <br>
v1.0.3 (source: server release metadata; artifact frontmatter states 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
