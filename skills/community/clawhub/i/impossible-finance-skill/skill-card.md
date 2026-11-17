## Description:

BSC (Binance Smart Chain) trading on Impossible Finance DEX: wallet creation, token swaps, pair discovery, and balance management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kj-script](https://clawhub.ai/user/kj-script)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to configure a BSC wallet, discover Impossible Finance token pairs, check balances, and prepare or execute token swaps with user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a spend-capable BSC private key for irreversible financial transactions.

Mitigation: Use only a fresh, low-balance wallet and require explicit confirmation of token addresses, amounts, slippage, approvals, and transaction destination before any swap.

Risk: The default wallet flow stores private key material in a local wallet file.

Mitigation: Prefer the encrypted keystore option or an external signer, restrict file permissions, and never log or transmit the private key.

Risk: Dependency or configuration drift could change how transactions are prepared or signed.

Mitigation: Pin dependencies and review BSC RPC, router, factory, wrapped token, and ClawChain registration settings before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kj-script/skills/impossible-finance-skill)
- [Impossible Finance](https://impossible.finance)
- [Impossible Finance Swap](https://app.impossible.finance/swap)
- [Impossible Finance Docs](https://docs.impossible.finance)
- [Impossible Finance GitHub](https://github.com/ImpossibleFinance)
- [BSC explorer](https://bscscan.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JavaScript examples, configuration values, wallet file JSON examples, and transaction links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local wallet setup instructions, token and pair discovery steps, swap preparation guidance, and BSC transaction hashes.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
