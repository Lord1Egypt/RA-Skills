## Description:

Provides payment-related agent tools to create payment requests, query payment status, and initiate refunds through a CLI-backed payment API integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neversatrabbit](https://clawhub.ai/user/neversatrabbit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to initiate payment requests, check transaction status, and request refunds against a configured payment API. It is intended for workflows where payment credentials, API endpoints, and refund authority can be controlled by the deploying organization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports that refunds can be initiated without enforcing the approval promised by the skill metadata.

Mitigation: Require an external refund approval process and restrict refund-capable API credentials until the skill enforces approval in code.

Risk: Payment API credentials and endpoint configuration are security-sensitive.

Mitigation: Use least-privilege API keys, keep PAYMENT_API_URL fixed to a trusted HTTPS payment host, and rotate credentials that may have appeared in setup or diagnostic output.

Risk: Diagnostics or logs may expose sensitive payment configuration in shared environments.

Mitigation: Avoid running diagnostics where logs are shared and review log handling before deployment.

## Reference(s):

- [Payment Skill Demo on ClawHub](https://clawhub.ai/neversatrabbit/skills/payment-skill-demo)
- [neversatrabbit publisher profile](https://clawhub.ai/user/neversatrabbit)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON results from CLI tool execution with setup and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PAYMENT_API_KEY and PAYMENT_API_SECRET; may use optional encryption and logging environment variables.]

## Skill Version(s):

v1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
