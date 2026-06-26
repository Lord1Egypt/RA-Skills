## Description: <br>
Use the openclaw_paid_action tool to list actions, generate USDC invoices, and execute only after manual payment confirmation on Solana. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[icetroll](https://clawhub.ai/user/icetroll) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to gate configured OpenClaw actions behind USDC payment, generate invoices, confirm Solana payments, and run the action only after payment is recorded. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a separate plugin implementation and configured local action scripts. <br>
Mitigation: Install only trusted plugin implementations, review every configured action script, and keep reviewed-script enforcement enabled. <br>
Risk: Misconfigured payment settings or exposed invoice data can route funds incorrectly or weaken payment tracking. <br>
Mitigation: Protect the invoice secret and invoice store, and verify the USDC recipient address before enabling paid actions. <br>
Risk: Configured actions can post publicly or modify important accounts after payment confirmation. <br>
Mitigation: Require human approval for sensitive actions and confirm payment manually before execution. <br>


## Reference(s): <br>
- [OpenClaw Paid Actions on ClawHub](https://clawhub.ai/icetroll/openclaw-paid-actions) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, API Calls, Shell commands] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and tool-call parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces payment instructions, signed invoice tokens, status checks, confirmation steps, and post-payment action execution guidance.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
