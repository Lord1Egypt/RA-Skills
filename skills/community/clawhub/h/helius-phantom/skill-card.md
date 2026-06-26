## Description: <br>
Build frontend Solana applications with Phantom Connect SDK and Helius infrastructure, including React, React Native, browser SDK integration, transaction signing, API key proxying, token gating, NFT minting, crypto payments, real-time updates, and secure frontend architecture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xIchigo](https://clawhub.ai/user/0xIchigo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers building Solana web or mobile applications use this skill to connect Phantom wallets, integrate Helius infrastructure, submit and verify transactions, query portfolio and asset data, and apply frontend security patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill covers real Solana transaction signing and submission workflows. <br>
Mitigation: Require explicit user confirmation before any transfer, mint, message signature, signup, upgrade, renewal, or paid operation. <br>
Risk: API keys, local credentials, and keypairs may be used during Helius setup and integration. <br>
Mitigation: Keep secrets in restricted local or server-side storage, avoid client-exposed environment variables, and inspect generated code for leaked credentials. <br>
Risk: API-provided transactions can request high-impact wallet actions. <br>
Mitigation: Inspect transaction contents before signing and prefer devnet or test flows while developing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/0xIchigo/helius-phantom) <br>
- [React SDK Reference](references/react-sdk.md) <br>
- [React Native SDK Reference](references/react-native-sdk.md) <br>
- [Browser SDK Reference](references/browser-sdk.md) <br>
- [Frontend Security - API Keys, CORS and Proxying](references/frontend-security.md) <br>
- [Integration Patterns - Phantom and Helius](references/integration-patterns.md) <br>
- [Transaction Patterns Reference](references/transactions.md) <br>
- [Helius Sender - Transaction Submission](references/helius-sender.md) <br>
- [Helius Docs](https://www.helius.dev/docs) <br>
- [Phantom Developer Docs](https://docs.phantom.com) <br>
- [Phantom Portal](https://phantom.com/portal) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with code snippets, command examples, configuration notes, and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose wallet, transaction, API proxy, and key-management flows that require user review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
