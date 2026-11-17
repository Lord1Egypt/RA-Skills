## Description:

Verifiable proofs for any computation. Ed25519 over SHA-256. TEE-backed signing, offline verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikeargento](https://clawhub.ai/user/mikeargento)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and engineers use this skill to commit explicit input bytes to a notary for signed proof generation and to verify returned proofs offline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commit operations send user-provided bytes to the configured notary endpoint over HTTPS.

Mitigation: Only commit data that is acceptable to send to the notary endpoint, and do not send credentials, private keys, or sensitive personal data.

Risk: Installing or running the Prethereum packages can introduce package supply-chain exposure.

Mitigation: Pin the package version where possible and inspect the package contents before installing.

## Reference(s):

- [Prethereum Skill Page](https://clawhub.ai/mikeargento/skills/prethereum)
- [Prethereum Wire Format](references/protocol.md)
- [Prethereum Repository](https://github.com/mikeargento/prethereum)
- [Prethereum MCP Source](https://github.com/mikeargento/prethereum/tree/main/packages/occ-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for proof generation and offline verification; commit operations send only user-provided bytes to the configured notary endpoint.]

## Skill Version(s):

0.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
