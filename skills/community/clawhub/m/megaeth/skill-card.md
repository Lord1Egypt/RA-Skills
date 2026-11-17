## Description:

End-to-end MegaETH development playbook (Feb 2026). Covers wallet operations, token swaps (Kyber Network), eth_sendRawTransactionSync (EIP-7966) for instant receipts, JSON-RPC batching, real-time mini-block subscriptions, storage-aware contract patterns (Solady RedBlackTreeLib), MegaEVM gas model, WebSocket keepalive, bridging from Ethereum, and debugging with mega-evme.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xguardbot](https://clawhub.ai/user/0xguardbot)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to build MegaETH applications, configure wallet and RPC flows, write MegaEVM-aware contracts, optimize storage and gas behavior, and debug transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes examples for sending funds, token approvals, swaps, bridging, and deployment on mainnet.

Mitigation: Require explicit human confirmation before every funds-moving or contract-broadcast step, and verify chain ID, recipient, contract address, calldata, value, gas, and slippage before signing.

Risk: Mainnet examples could cause irreversible loss if followed automatically or with untrusted addresses.

Mitigation: Use testnet or small amounts first, pin installation sources, avoid unlimited token approvals, and prefer hardware wallets for large-value operations.

Risk: MegaEVM gas and storage behavior differs from standard EVM assumptions.

Mitigation: Use remote MegaETH gas estimation for non-trivial operations and review storage patterns, volatile data access, and large event emissions before deployment.

## Reference(s):

- [MegaETH Official Documentation](https://docs.megaeth.com)
- [MegaETH Real-time API](https://docs.megaeth.com/realtime-api)
- [MegaEVM Specification](https://github.com/megaeth-labs/mega-evm/blob/main/specs/MiniRex.md)
- [MegaETH Token List](https://github.com/megaeth-labs/mega-tokenlist)
- [EIP-7966 eth_sendRawTransactionSync](https://ethereum-magicians.org/t/eip-7966-eth-sendrawtransactionsync-method/24640)
- [KyberSwap Aggregator Documentation](https://docs.kyberswap.com/kyberswap-solutions/kyberswap-aggregator)
- [Solady](https://github.com/Vectorized/solady)
- [ClawHub Skill Page](https://clawhub.ai/0xguardbot/skills/megaeth)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MegaETH chain IDs, RPC endpoints, gas notes, contract patterns, and transaction review guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
