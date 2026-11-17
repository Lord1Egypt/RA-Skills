## Description:

Accept crypto payments (NEAR, USDC, USDT) via a beautiful payment page with PingPay or HOT PAY integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cuongdcdev](https://clawhub.ai/user/cuongdcdev)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to configure and launch hosted crypto payment pages for NEAR, USDC, and USDT payments through PingPay or HOT PAY. It helps an agent guide setup, run the local payment server, and share generated checkout links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment-link and checkout-session creation can be exposed through a public tunnel.

Mitigation: Keep the service private until privileged endpoints are authenticated, rate-limited, and deployed behind a trusted configured origin.

Risk: Provider credentials may be mishandled during setup.

Mitigation: Store API keys in a local secret file or secret manager, avoid pasting keys into chat, and prefer scoped test keys during setup.

Risk: Webhook payment status updates may be accepted without verified signatures.

Mitigation: Verify HOT PAY webhook signatures before trusting payment status updates or fulfillment signals.

Risk: Tunnel setup can weaken SSH trust if host-key verification is disabled.

Mitigation: Use a dedicated protected SSH key and enable host-key verification before exposing the payment service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cuongdcdev/skills/near-getpay)
- [PingPay documentation](https://pingpay.io/docs)
- [HOT PAY dashboard documentation](https://pay.hot-labs.org/admin)
- [localhost.run tunneling service](https://localhost.run)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration snippets, JSON examples, and generated payment URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include provider setup steps, environment variable names, local server commands, and public checkout links.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
