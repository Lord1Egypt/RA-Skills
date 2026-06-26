## Description: <br>
Guides developers integrating Ika dWallet 2PC-MPC protocol into Sui Move contracts for cross-chain signing, dWallet creation, presigning, future signing, and key import flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omersadika](https://clawhub.ai/user/omersadika) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when building Sui Move contracts and TypeScript integration flows that rely on Ika dWallets for cross-chain signing, presign management, future signing, key import, and shared-signing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples cover real wallet signing, raw private keys, secret shares, and irreversible conversion to shared signing mode. <br>
Mitigation: Use testnet first, pin dependencies, never log or hardcode private keys or secret shares, and require informed user or operator approval before converting a wallet to shared signing mode. <br>
Risk: Contract patterns that authorize cross-chain signatures can create security-sensitive signing paths if copied without review. <br>
Mitigation: Review access controls, message approval logic, presign lifecycle, fee handling, and every signing path before production deployment. <br>


## Reference(s): <br>
- [Ika](https://ika.xyz) <br>
- [Protocol Complete Reference](references/protocols-detailed.md) <br>
- [Integration Patterns Reference](references/patterns.md) <br>
- [TypeScript Integration Reference](references/typescript-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Move, TypeScript, TOML, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the Sui CLI for workflows that execute Sui commands; examples should be adapted and reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
