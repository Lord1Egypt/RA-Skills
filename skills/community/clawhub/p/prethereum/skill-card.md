## Description: <br>
Prethereum creates verifiable proofs for user-provided computation artifacts using Ed25519 signatures over SHA-256 digests, with TEE-backed signing and offline verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikeargento](https://clawhub.ai/user/mikeargento) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and engineers use Prethereum to commit explicit byte payloads to a notary, receive self-contained proof JSON, and verify proofs offline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commit data is sent to the configured external notary endpoint. <br>
Mitigation: Only commit data that is acceptable to transmit; do not send credentials, private keys, or sensitive personal information. <br>
Risk: The workflow relies on npm packages for installation. <br>
Mitigation: Confirm packages come from the expected source before installing and consider pinning package versions. <br>


## Reference(s): <br>
- [Prethereum Wire Format](references/protocol.md) <br>
- [ClawHub Prethereum listing](https://clawhub.ai/mikeargento/prethereum) <br>
- [Declared Prethereum repository](https://github.com/mikeargento/prethereum) <br>
- [Declared MCP package source](https://github.com/mikeargento/prethereum/tree/main/packages/occ-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript and bash code blocks; proof outputs are self-contained JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commit operations send only user-provided bytes to the configured notary endpoint; verification is offline.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
