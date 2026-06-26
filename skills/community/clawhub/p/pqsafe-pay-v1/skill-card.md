## Description: <br>
Post-quantum signed SpendEnvelopes for AI agent payments using ML-DSA-65 signatures over Airwallex, Wise, Stripe, USDC-Base, and x402 rails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rayc0](https://clawhub.ai/user/rayc0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let OpenClaw-compatible agents create, verify, and revoke spend envelopes for bounded autonomous payments. It is intended for payment flows that need post-quantum signatures, recipient allowlists, expiry, and revocation controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create payment authorization envelopes, so a mistaken or compromised invocation may authorize spend within the configured limits. <br>
Mitigation: Use test mode first, set small spend caps and short TTLs, restrict recipients, and require human approval before create or revoke operations. <br>
Risk: The release requires sensitive credentials and has inconsistent documentation about key handling. <br>
Mitigation: Confirm the intended key model before installing, keep production private keys and API keys out of prompts and logs, and provide secrets through the runtime environment or a secret manager. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/rayc0/pqsafe-pay-v1) <br>
- [PQSafe OpenClaw skill homepage](https://pqsafe.xyz/openclaw-skill) <br>
- [PQSafe AgentPay OpenClaw API docs](https://docs.pqsafe.xyz/agent-pay/openclaw) <br>
- [AP2-PQ Profile RFC](https://pqsafe.xyz/ap2-pq-rfc) <br>
- [NIST FIPS 204](https://csrc.nist.gov/pubs/fips/204/final) <br>
- [npm package @pqsafe/openclaw](https://www.npmjs.com/package/@pqsafe/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Configuration] <br>
**Output Format:** [JSON operation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces signed SpendEnvelope payloads, verification results, and revocation receipts; production use requires payment credentials or signing keys.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata, frontmatter, package.json, skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
