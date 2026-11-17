## Description:

Post-quantum signed SpendEnvelopes for AI agent payments using ML-DSA-65 signatures over Airwallex, Wise, Stripe, USDC-Base, and x402 rails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rayc0](https://clawhub.ai/user/rayc0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to create, verify, and revoke post-quantum signed payment spend envelopes for autonomous AI agents across supported payment rails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment envelope data may be exposed through under-scoped network behavior.

Mitigation: Use only in a sandbox or after source review; restrict and authenticate revocation network destinations and minimize remotely transmitted data before production use.

Risk: Revocation and nonce behavior may not match the safety claims made in the skill documentation.

Mitigation: Require the publisher to make verify_envelope accurately enforce or clearly exclude revocation and nonce checks before relying on the skill for payment authorization.

Risk: Secret-key handling and vulnerable development dependencies require review before production use.

Mitigation: Clarify how secret keys are supplied and protected, and update vulnerable development dependencies before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rayc0/skills/pqsafe-pay-v1)
- [PQSafe OpenClaw Skill Homepage](https://pqsafe.xyz/openclaw-skill)
- [PQSafe AgentPay OpenClaw API Docs](https://docs.pqsafe.xyz/agent-pay/openclaw)
- [AP2-PQ Profile RFC](https://pqsafe.xyz/ap2-pq-rfc)
- [NIST FIPS 204](https://csrc.nist.gov/pubs/fips/204/final)
- [npm Package @pqsafe/openclaw](https://www.npmjs.com/package/@pqsafe/openclaw)

## Skill Output:

**Output Type(s):** [JSON, API calls, Configuration]

**Output Format:** [JSON objects for signed envelopes, verification results, and revocation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and PQSAFE_API_KEY for normal use; PQSAFE_TEST_MODE supports local mock execution.]

## Skill Version(s):

0.1.0 (source: server release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
