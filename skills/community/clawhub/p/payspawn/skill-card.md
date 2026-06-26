## Description: <br>
PaySpawn adds smart-contract-enforced spending controls to AI agents that make API payments, including x402 auto-pay, daily and per-transaction limits, address allowlists, and fleet provisioning on Base with USDC. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adambrainai](https://clawhub.ai/user/adambrainai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators of autonomous agents use this skill to configure PaySpawn credentials and SDK calls so agents can pay x402 APIs or send USDC on Base within human-defined spending limits. It also supports fleet provisioning where multiple agents receive separate credentials from a shared budget pool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can authorize real USDC spending within configured limits. <br>
Mitigation: Set minimal daily and per-transaction limits, use recipient allowlists where possible, choose a short expiry, and pause or revoke credentials when they are no longer needed. <br>
Risk: PAYSPAWN_CREDENTIAL is a secret spend permission even though it is not a wallet private key. <br>
Mitigation: Store the credential only in secret environment storage and avoid exposing it in prompts, logs, screenshots, or shared configuration. <br>
Risk: The payment behavior depends on the installed @payspawn/sdk package. <br>
Mitigation: Pin and verify the SDK version before deployment and review package updates before widening spending limits. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/adambrainai/payspawn) <br>
- [PaySpawn website](https://payspawn.ai) <br>
- [PaySpawn dashboard](https://payspawn.ai/dashboard) <br>
- [npm: @payspawn/sdk](https://www.npmjs.com/package/@payspawn/sdk) <br>
- [SDK audit repository](https://github.com/adambrainai/payspawn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires @payspawn/sdk and an optional secret PAYSPAWN_CREDENTIAL; payment authority is limited by credential caps, allowlists, and expiry.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
