## Description:

NadFun helps agents work with the nad.fun Monad token launchpad for bonding-curve trading, token creation, quotes, token data, event indexing, and REST API access using viem.

This skill is ready for commercial/non-commercial use.

## Publisher:

[portdeveloper](https://clawhub.ai/user/portdeveloper)

### License/Terms of Use:


## Use Case:

Developers, trading bot builders, token creators, and analytics teams use this skill to integrate NadFun trading, token creation, quoting, wallet, and event-query workflows on Monad testnet or mainnet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet private keys, wallet signatures, session cookies, and API keys may be exposed if examples are copied directly into source code or logs.

Mitigation: Use testnet first, keep secrets in environment variables or a secret manager, never paste real private keys into examples, and never print private keys or API keys.

Risk: Trading and token examples can create token approvals, including unlimited approvals, or sign transactions on the wrong network or contract.

Mitigation: Prefer exact approvals, verify spender addresses, contract addresses, chain IDs, amounts, and slippage before signing, and reset or revoke allowances when no longer needed.

Risk: The artifact includes curl-based skill file downloads from mutable remote URLs.

Mitigation: Avoid remote update flows unless downloaded files and hashes can be verified against trusted release evidence.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/portdeveloper/skills/nadfun)
- [NadFun](https://nad.fun)
- [ABI Reference](https://nad.fun/abi.md)
- [Agent API Reference](https://nad.fun/agent-api.md)
- [Token Creation Guide](https://nad.fun/create.md)
- [Historical Event Querying Guide](https://nad.fun/indexer.md)
- [Quote Guide](https://nad.fun/quote.md)
- [Token Operations Guide](https://nad.fun/token.md)
- [Trading Guide](https://nad.fun/trading.md)
- [Wallet Guide](https://nad.fun/wallet.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes examples for Monad testnet and mainnet; users should verify network, contract addresses, secrets, and transaction details before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
