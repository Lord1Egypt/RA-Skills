## Description: <br>
Manage Paystack customers, transactions, payment pages, transfers, and payment operations via the Paystack API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage Paystack payment workflows from an OpenClaw agent, including transaction lookup, payment verification, customer management, payment page creation, and transfer-related operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paystack write, transfer, payment-page, delete, and cancellation operations can affect real payment resources or real money. <br>
Mitigation: Preview and confirm the exact target resource, amount, recipient, and intended effect before executing any write or payment operation. <br>
Risk: The skill requires Paystack access through ClawLink and therefore depends on sensitive account credentials managed outside the chat. <br>
Mitigation: Install only when the user trusts ClawLink with Paystack API access, avoid asking for API keys in chat, and revoke the Paystack or ClawLink connection when it is no longer needed. <br>
Risk: Available Paystack tools may vary by the live ClawLink catalog or connection state. <br>
Mitigation: List integrations and describe or search Paystack tools before execution instead of guessing unavailable capabilities. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/paystack-payments) <br>
- [Paystack API Documentation](https://paystack.com/docs/api/) <br>
- [Paystack Transaction API](https://paystack.com/docs/api/transaction/) <br>
- [Paystack Customer API](https://paystack.com/docs/api/customer/) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool-call parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the live Paystack tool catalog through ClawLink; write, destructive, transfer, and payment operations require user confirmation.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
