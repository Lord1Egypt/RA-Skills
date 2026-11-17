## Description:

Megaeth Developer is an end-to-end MegaETH development playbook for wallet operations, token swaps, real-time RPC flows, frontend patterns, smart contracts, gas modeling, storage optimization, testing, and debugging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xbreadguy](https://clawhub.ai/user/0xbreadguy)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to build, test, debug, and operate MegaETH applications, including wallets, transaction flows, token swaps, WebSocket subscriptions, and MegaEVM smart contracts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact wallet, swap, approval, bridge, transfer, signed transaction, and deployment guidance can cause fund loss if copied directly.

Mitigation: Require explicit human confirmation for each value-moving action and verify chain ID, RPC endpoint, contract addresses, token addresses, spender or router addresses, amounts, slippage, calldata, and simulation results from authoritative sources.

Risk: Mainnet examples and gas assumptions may be unsafe or inconsistent for a specific project or current network state.

Mitigation: Prefer testnet first, use remote MegaETH estimation for non-trivial operations, and independently confirm current gas limits, fees, router addresses, and bridge details before signing or deploying.

Risk: External repositories, libraries, and tooling referenced by the artifact can change after release.

Mitigation: Pin external repositories and dependencies before building or installing them, and review source, permissions, and release integrity before use.

## Reference(s):

- [MegaETH Docs](https://docs.megaeth.com)
- [MegaETH Real-time API](https://docs.megaeth.com/realtime-api)
- [MegaETH Frontier](https://docs.megaeth.com/frontier)
- [MegaETH Testnet Guide](https://docs.megaeth.com/testnet)
- [MegaEVM Source](https://github.com/megaeth-labs/mega-evm)
- [MegaEVM MiniRex Spec](https://github.com/megaeth-labs/mega-evm/blob/main/specs/MiniRex.md)
- [MegaETH Token List](https://github.com/megaeth-labs/mega-tokenlist)
- [Solady RedBlackTreeLib](https://github.com/Vectorized/solady/blob/main/src/utils/RedBlackTreeLib.sol)
- [EIP-7966 eth_sendRawTransactionSync](https://ethereum-magicians.org/t/eip-7966-eth-sendrawtransactionsync-method/24640)
- [KyberSwap Aggregator Docs](https://docs.kyberswap.com/kyberswap-solutions/kyberswap-aggregator)
- [Envio HyperSync](https://docs.envio.dev/docs/HyperSync/overview)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include transaction, deployment, RPC, gas, and security review guidance that should be checked against authoritative network sources before use.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
