## Description:

PaySpawn adds spending controls to AI agents that make API payments, including x402 auto-pay, daily limits, per-transaction limits, address allowlists, and fleet provisioning on Base with USDC.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adambrainai](https://clawhub.ai/user/adambrainai)

### License/Terms of Use:


## Use Case:

Developers and teams use this skill to add bounded payment capability to agents that call paid APIs or send USDC autonomously. It guides credential setup, SDK installation, per-agent limits, allowlists, revocation, and fleet provisioning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables financially sensitive agent payment behavior using a spending credential.

Mitigation: Use the lowest daily and per-transaction limits, set recipient allowlists and short expirations, and keep on-chain revocation available.

Risk: The install guidance uses an unpinned npm install command for a financial SDK.

Mitigation: Prefer an exact reviewed SDK version or lockfile before deploying the skill.

Risk: Exposure of the PaySpawn credential could authorize payments within the configured limits.

Mitigation: Store PAYSPAWN_CREDENTIAL as a secret and scope it with minimum privilege, expiry, and destination restrictions.

## Reference(s):

- [PaySpawn](https://payspawn.ai)
- [PaySpawn Dashboard](https://payspawn.ai/dashboard)
- [npm: @payspawn/sdk](https://www.npmjs.com/package/@payspawn/sdk)
- [PaySpawn SDK audit source](https://github.com/adambrainai/payspawn)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with bash and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes payment credential setup, SDK installation, spending-limit configuration, fleet provisioning, and operational controls.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
