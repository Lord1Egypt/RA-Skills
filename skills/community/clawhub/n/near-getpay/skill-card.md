## Description: <br>
Accept crypto payments (NEAR, USDC, USDT) via a beautiful payment page with PingPay or HOT PAY integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cuongdcdev](https://clawhub.ai/user/cuongdcdev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, merchants, creators, and developers use this skill to configure and launch a hosted crypto payment page for NEAR, USDC, or USDT payments through PingPay or HOT PAY. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill starts a local payment server that can become publicly reachable through a tunnel. <br>
Mitigation: Run it only in an environment intended to receive public traffic, review exposed routes before use, and stop the tunnel when payment collection is complete. <br>
Risk: Payment provider credentials and payment recipient settings can affect real funds. <br>
Mitigation: Store API keys in a local .env or secret store, do not paste secrets into chat, and verify the actual recipient in the PingPay or HOT PAY dashboard before sharing links. <br>
Risk: The artifact includes invoice-paying NEAR Intents code paths that are not central to the advertised hosted payment page flow. <br>
Mitigation: Remove or separately review those code paths before use, especially where they could execute token swaps, bridging, or invoice payment actions. <br>
Risk: The advertised HOT PAY webhook signature protection is not authoritative according to the security evidence. <br>
Mitigation: Do not rely on webhook confirmations for fulfillment until actual signature verification is implemented and tested. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cuongdcdev/near-getpay) <br>
- [Publisher profile](https://clawhub.ai/user/cuongdcdev) <br>
- [PingPay](https://pingpay.io) <br>
- [PingPay documentation](https://pingpay.io/docs) <br>
- [HOT PAY admin](https://pay.hot-labs.org/admin/overview) <br>
- [localhost.run](https://localhost.run) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands, environment configuration, and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup steps, local server commands, payment page links, checkout links, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
