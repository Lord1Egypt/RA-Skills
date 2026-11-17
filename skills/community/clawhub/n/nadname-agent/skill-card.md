## Description:

Nadname Agent registers .nad names on the Monad blockchain through Nad Name Service, including availability checks, pricing lookup, gas estimation, and registration commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daaab](https://clawhub.ai/user/daaab)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and web3 users use this skill to check .nad name availability, estimate costs, register names, and list names through Node.js scripts for Monad and Nad Name Service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles wallet private keys and irreversible blockchain transactions.

Mitigation: Review before installing, use only a low-value wallet, run dry-run first, and manually verify transaction details before sending.

Risk: Availability, ownership, and pricing lookups depend on external NAD and Monad services and should not be treated as authoritative without verification.

Mitigation: Cross-check name status, price, contract address, and transaction data in trusted NNS and Monad tools before committing funds.

Risk: Managed keystore behavior includes key-handling concerns called out by the security guidance.

Mitigation: Prefer a low-value wallet through the PRIVATE_KEY environment variable and avoid managed keystore mode until the plaintext fallback, custom encryption, transaction validation, and explicit confirmation issues are fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/daaab/skills/nadname-agent)
- [Nad Name Service Documentation](https://docs.nad.domains)
- [Nad Name Service App](https://app.nad.domains)
- [NAD Registration API Endpoint](https://api.nad.domains/api/register-request)
- [Monad Explorer](https://explorer.monad.xyz)
- [Monad Bridge](https://bridge.monad.xyz)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a low-value wallet private key or managed keystore, network access to NAD API and Monad RPC, and user review before transactions.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact package.json and _meta.json report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
