## Description:

Manage crypto wallets and make x402 micropayments with USDC stablecoins on Polygon.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akshatgada](https://clawhub.ai/user/akshatgada)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent users use this skill to create or import wallets, check balances, set spending limits, and make x402 USDC micropayments to paid APIs on Polygon. It is intended for workflows where an agent must request approval, execute a payment, and report transaction status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles crypto wallet payments through an unpinned external llm-wallet-mcp package.

Mitigation: Pin and verify the llm-wallet-mcp package before use, avoid global or elevated installs, and review the package before connecting funds.

Risk: Payments may spend real funds when configured for Polygon mainnet.

Mitigation: Use a dedicated testnet wallet or low-balance wallet, keep conservative per-transaction and daily limits, and require approval after checking destination URL, amount, network, and recipient.

Risk: Wallet private keys and WALLET_ENCRYPTION_KEY are sensitive secrets.

Mitigation: Keep keys out of chats and repositories, store them in an environment variable or secret store, and back up wallet material securely.

## Reference(s):

- [LLM Wallet Skill Page](https://clawhub.ai/akshatgada/skills/llm-wallet)
- [x402 Protocol Overview](references/x402-protocol.md)
- [LLM Wallet Setup Guide](references/wallet-setup.md)
- [LLM Wallet Usage Examples](references/examples.md)
- [x402 Protocol Website](https://www.x402.org/)
- [Coinbase x402 Documentation](https://docs.cdp.coinbase.com/x402/welcome)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance, API Calls]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes wallet and payment workflow steps, approval prompts, spending-limit guidance, and transaction confirmation details.]

## Skill Version(s):

1.0.0 (source: server release metadata and README Version section)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
