## Description: <br>
Advisory reference for Safaricom M-Pesa Daraja integration planning, reviews, sandbox testing, callbacks, reconciliation, and production-readiness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nevilpaulo](https://clawhub.ai/user/nevilpaulo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan, implement, review, test, and prepare Safaricom M-Pesa Daraja integrations without giving the agent authority to move money. It focuses on sandbox-first payment flows, callback idempotency, masked logging, reconciliation, and production-readiness checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment-sensitive generated code could expose credentials, personal data, transaction identifiers, or real payment behavior if used without review. <br>
Mitigation: Keep real Daraja credentials out of repositories, use sandbox endpoints by default, require explicit approval before live payment actions, and review callback storage and logs for personal or transaction data exposure. <br>
Risk: Callbacks and reconciliation can create duplicate fulfillment or ambiguous payment states if they are not idempotent. <br>
Mitigation: Validate callback shape, persist events safely, deduplicate by Daraja identifiers such as CheckoutRequestID, ConversationID, or TransactionID, and maintain a manual reconciliation path. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nevilpaulo/mpesa-daraja) <br>
- [Publisher profile](https://clawhub.ai/user/nevilpaulo) <br>
- [Daraja Endpoint Reference](references/api-endpoints.md) <br>
- [STK Push / Lipa na M-Pesa Online](references/stk-push.md) <br>
- [Production Readiness](references/production-readiness.md) <br>
- [M-Pesa Daraja Test Cases](references/test-cases.md) <br>
- [M-Pesa Daraja Examples](references/examples.md) <br>
- [Safaricom Daraja developer portal](https://developer.safaricom.co.ke/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration, Shell commands] <br>
**Output Format:** [Markdown with code snippets, configuration examples, review findings, test plans, and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory-only outputs; generated implementation should be reviewed before use with live payment systems.] <br>

## Skill Version(s): <br>
1.2.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
