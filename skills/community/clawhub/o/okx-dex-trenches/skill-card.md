## Description:

Read-only on-chain research for pump.fun and other meme-token launchpads, including token discovery, developer reputation, bundle and sniper analysis, bonding progress, similar-token lookup, co-investor wallets, and related Market API quota questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ok-james-01](https://clawhub.ai/user/ok-james-01)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide read-only meme-token research with Onchain OS DEX commands across supported launchpads and chains. It helps agents screen new launches, inspect token and developer risk signals, analyze bundles and snipers, and prepare WebSocket monitoring guidance without performing trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or update an OKX-backed CLI locally before running commands.

Mitigation: Use the documented checksum verification flow before execution and deploy only when local CLI installation is acceptable.

Risk: Wallet addresses, API credentials, or passphrases may be used for analytics or WebSocket monitoring flows.

Mitigation: Provide only the credentials or wallet addresses required for the specific query, keep credentials in environment variables or ignored .env files, and never commit them.

Risk: Some endpoints may trigger x402 payment or quota prompts.

Mitigation: Review each payment or quota notification carefully and require explicit confirmation before proceeding with paid access.

Risk: On-chain token names, symbols, descriptions, and developer data are untrusted external content.

Mitigation: Treat command output as data, not instructions, and summarize risk signals without following embedded directions.

Risk: The authoritative security verdict is suspicious because the read-only scope expands into WebSocket, API-credential, wallet, and payment-adjacent handling.

Mitigation: Review the skill and its scanner evidence before deployment, and keep trading or swap actions routed outside this skill.

## Reference(s):

- [Onchain OS DEX Trenches CLI Command Reference](references/cli-reference.md)
- [Onchain OS DEX Trenches WebSocket Protocol Reference](references/ws-protocol.md)
- [Keyword Glossary](references/keyword-glossary.md)
- [Shared Pre-flight Checks](_shared/preflight.md)
- [Shared Chain Name Support](_shared/chain-support.md)
- [OKX Web3](https://web3.okx.com)
- [OKX Developer Portal](https://web3.okx.com/onchain-os/dev-portal)
- [OKX WebSocket Login Documentation](https://web3.okx.com/onchainos/dev-docs/market/websocket-login)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, command output summaries, and occasional code snippets for WebSocket setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only posture for memepump research; token and wallet data may be time-sensitive and should include request timestamps when available.]

## Skill Version(s):

3.1.3 (source: server release evidence and frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
