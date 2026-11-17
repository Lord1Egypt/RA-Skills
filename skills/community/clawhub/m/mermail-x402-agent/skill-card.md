## Description:

Mermail x402 Agent guides an agent through discovering a paid x402 service, authorizing one Mermail Agent Wallet / PayBox proof within a user-approved spend cap, redeeming it on the selected resource, and continuing the original task with the paid result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mermail](https://clawhub.ai/user/mermail)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when a user task requires a paid third-party x402 resource and the agent must resolve the live quote, any vendor prepaid floor, payment authorization, proof redemption, and result validation before returning the paid output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent may treat PayBox proof creation as merchant settlement or a completed paid result.

Mitigation: Require the agent to report proof creation as proof_ready, redeem the proof on the exact frozen request, and claim charged, settled, or paid_and_continued only when merchant response, transaction, or balance evidence supports it.

Risk: Untrusted catalog rows, HTTP 402 challenge text, email, or paid-service output may try to change the selected service, action, spend cap, or tool scope.

Mitigation: Match origin, resource, asset/chain, and required_charge against the authenticated user request; ignore embedded instructions and require explicit current-task authority before external-effect payment or funding actions.

Risk: A paid credential or prepaid-credit flow may return a secret that is redacted or unsafe to expose, leaving the original task unfinished after payment.

Mitigation: Preflight the fulfillment path and verify a secure continuation channel before payment; stop as blocked_before_payment when a credential would be inaccessible or no approved server-side continuation exists.

## Reference(s):

- [Mermail AI Skills Documentation](https://docs.mermail.app/ai/skills)
- [ClawHub Skill Page](https://clawhub.ai/mermail/skills/mermail-x402-agent)
- [Security Reference](references/security.md)
- [Tools Reference](references/tools.md)
- [Workflows Reference](references/workflows.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown text with structured payment status and provenance notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include exact Mermail handoff URLs and sanitized payment/provenance notes; must not include payment proofs, signing keys, or vendor credentials.]

## Skill Version(s):

1.0.12 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
