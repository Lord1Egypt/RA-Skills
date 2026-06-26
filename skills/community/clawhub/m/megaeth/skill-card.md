## Description: <br>
End-to-end MegaETH development playbook covering wallet operations, token swaps, synchronous transaction receipts, RPC batching, real-time mini-block subscriptions, storage-aware contract patterns, the MegaEVM gas model, WebSocket keepalive, bridging, and debugging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xGuardbot](https://clawhub.ai/user/0xGuardbot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to build, test, debug, and operate MegaETH applications, including wallet flows, smart contracts, RPC integrations, real-time frontends, swaps, bridging, and gas/storage optimization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives live blockchain transaction guidance that can move real funds. <br>
Mitigation: Manually verify chain ID, RPC URL, wallet, recipient, contract, spender, amount, gas, nonce, and slippage before any transfer, swap, bridge, approval, raw transaction, or deployment. <br>
Risk: Transaction examples may encourage high-impact on-chain actions with too few safety gates. <br>
Mitigation: Prefer testnet, simulation, dry runs, hardware wallets for large amounts, exact-amount approvals, and explicit user confirmation before signing or broadcasting. <br>
Risk: MegaETH-specific gas and storage behavior can make ordinary EVM assumptions unsafe or expensive. <br>
Mitigation: Use remote gas estimation for non-trivial operations, review SSTORE patterns, reuse storage slots where appropriate, and profile or replay transactions with MegaETH-aware tooling. <br>
Risk: Incorrect contract, token, bridge, or RPC endpoints can lead to failed or harmful interactions. <br>
Mitigation: Use trusted RPC endpoints, verified token lists, explorers, and official documentation to confirm addresses and network configuration before execution. <br>


## Reference(s): <br>
- [MegaETH AI Developer on ClawHub](https://clawhub.ai/0xGuardbot/megaeth) <br>
- [MegaETH Official Documentation](https://docs.megaeth.com) <br>
- [MegaETH Real-time API](https://docs.megaeth.com/realtime-api) <br>
- [MegaETH Testnet Guide](https://docs.megaeth.com/testnet) <br>
- [MegaETH Frontier Mainnet](https://docs.megaeth.com/frontier) <br>
- [MegaEVM](https://github.com/megaeth-labs/mega-evm) <br>
- [MegaEVM MiniRex Specification](https://github.com/megaeth-labs/mega-evm/blob/main/specs/MiniRex.md) <br>
- [MegaETH Token List](https://github.com/megaeth-labs/mega-tokenlist) <br>
- [EIP-7966 eth_sendRawTransactionSync](https://ethereum-magicians.org/t/eip-7966-eth-sendrawtransactionsync-method/24640) <br>
- [KyberSwap Aggregator Documentation](https://docs.kyberswap.com/kyberswap-solutions/kyberswap-aggregator) <br>
- [Solady](https://github.com/Vectorized/solady) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with code blocks, command examples, configuration snippets, checklists, and implementation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include transaction, wallet, contract, RPC, gas, storage, and deployment recommendations that require human review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
