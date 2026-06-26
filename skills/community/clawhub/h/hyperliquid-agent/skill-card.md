## Description: <br>
Execution and risk-management framework for agents trading on Hyperliquid through a host-provided authenticated client, covering trade validation, position sizing, funding checks, order confirmation, and safe-mode halts without collecting or managing secrets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jurgenw81](https://clawhub.ai/user/jurgenw81) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to validate strategy signals, size positions, construct normalized Hyperliquid order requests, and monitor execution through a host-provided authenticated client while keeping credential handling outside the skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can drive live leveraged trading, which can cause financial loss if orders or position changes are executed without strong user controls. <br>
Mitigation: Use paper trading or dry-run first, require explicit confirmation for every live order or position change, and set tight exchange-side limits before enabling live execution. <br>
Risk: A host-provided authenticated session can place real orders if it is over-permissive or cannot be revoked quickly. <br>
Mitigation: Keep wallet signing and secret handling outside the skill, provide only the minimum required authenticated session, and ensure the session can be revoked immediately. <br>
Risk: Stale market data, inconsistent account state, or unconfirmed order state can produce unsafe execution decisions. <br>
Mitigation: Halt new trades when state cannot be read or reconciled, require order-state confirmation after submission, and use safe-mode behavior for inconsistent execution results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jurgenw81/hyperliquid-agent) <br>
- [Hyperliquid onboarding link](https://app.hyperliquid.xyz/join/M8UHZWP) <br>


## Skill Output: <br>
**Output Type(s):** [Structured data, Code, Guidance] <br>
**Output Format:** [JSON-like execution objects with human-readable reasons and example Python code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes trade status, reason, normalized order request, execution result, position state, and risk summary; secrets are outside the skill output.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
