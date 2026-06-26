## Description: <br>
Guide for building with the Ika TypeScript SDK (@ika.xyz/sdk) on Mysten Sui v2 for dWallet creation, cross-chain transaction signing, encryption-key management, and TypeScript/JavaScript Ika network integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omersadika](https://clawhub.ai/user/omersadika) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to build TypeScript applications with the Ika SDK, including dWallet lifecycle flows, Sui integration, signing workflows, and curve/signature/hash validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet seeds, private keys, decryption keys, or secret shares could be exposed if copied into prompts, logs, examples, or repositories. <br>
Mitigation: Use test keys in examples, keep real secrets out of agent context and source control, and review generated code for accidental secret handling. <br>
Risk: Signing examples can create real financial or network effects when run against the wrong network or with production credentials. <br>
Mitigation: Run examples on testnet first, verify the configured network, and inspect every transaction before signing or executing it. <br>
Risk: Shared or autonomous dWallet signing can grant authority beyond the user's intended control model. <br>
Mitigation: Use shared or autonomous signing only when that authority model is deliberate and documented for the application. <br>


## Reference(s): <br>
- [Ika](https://ika.xyz) <br>
- [API Reference](references/api-reference.md) <br>
- [End-to-End Flows](references/flows.md) <br>
- [Types and Validation](references/types-and-validation.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with TypeScript and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include wallet-signing and transaction examples that require user review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
