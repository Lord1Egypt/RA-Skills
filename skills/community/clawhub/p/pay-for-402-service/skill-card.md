## Description: <br>
Guides an agent through an Alipay A402 buyer payment workflow after receiving an HTTP 402 response, including wallet checks, payment submission, payment-status queries, resource retry, and fulfillment acknowledgment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kangleyi](https://clawhub.ai/user/kangleyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to complete user-confirmed Alipay payments for services that return an HTTP 402 Payment Needed response. It is intended for payment flows where the agent must preserve the 402 payload, call the Alipay CLI, wait for user payment confirmation, then query status and return the purchased resource. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can initiate real payments through the Alipay CLI. <br>
Mitigation: Require explicit user confirmation in Alipay and verify the merchant, amount, domain, and displayed command before approving payment. <br>
Risk: Payment links, MEDIA paths, trade numbers, or resource URLs could be mishandled or altered during the flow. <br>
Mitigation: Preserve CLI output exactly when required, validate file names and command parameters, and stop on unexpected domains, unsafe paths, or unclear payment status. <br>
Risk: The skill requires a payment CLI and channel environment configuration. <br>
Mitigation: Install only if the Alipay payment CLI is trusted and configure AIPAY_OUTPUT_CHANNEL before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kangleyi/pay-for-402-service) <br>
- [Alipay payment skills homepage](https://github.com/alipay/payment-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with CLI commands and possible JSON or MEDIA-line CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce payment links, QR-code media references, trade numbers, payment-status results, and purchased resource content from the Alipay CLI.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
