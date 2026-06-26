## Description: <br>
End-to-end MegaETH development playbook (Feb 2026). Covers wallet operations, token swaps (Kyber Network), eth_sendRawTransactionSync (EIP-7966) for instant receipts, JSON-RPC batching, real-time mini-block subscriptions, storage-aware contract patterns (Solady RedBlackTreeLib), MegaEVM gas model, WebSocket keepalive, bridging from Ethereum, and debugging with mega-evme. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xBreadguy](https://clawhub.ai/user/0xBreadguy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to build MegaETH applications, configure wallets and RPC flows, optimize transaction submission, and develop or debug MegaEVM smart contracts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes examples for real blockchain transactions, swaps, approvals, bridging, and deployments. <br>
Mitigation: Before executing commands or signing transactions, verify chain ID, recipient, token, amount, spender, slippage, bridge address, and gas settings; use testnet or small-value trials first. <br>
Risk: MegaETH storage costs can make contracts vulnerable to gas-draining storage allocation patterns. <br>
Mitigation: Review SSTORE patterns, limit arbitrary key writes, charge users for storage costs, and prefer slot-reuse designs where appropriate. <br>
Risk: Local EVM simulations may use incorrect gas assumptions for MegaEVM. <br>
Mitigation: Use MegaETH remote gas estimation, test on forked or live testnet conditions, and replay/profile transactions with mega-evme for higher-risk contract changes. <br>
Risk: Fast transaction and mini-block behavior can create timing, retry, and finality assumptions that differ from standard EVM workflows. <br>
Mitigation: Treat synchronous receipts as soft finality for high-value actions, wait for additional confirmations when needed, and design time-sensitive logic with MegaETH's timing constraints in mind. <br>


## Reference(s): <br>
- [MegaETH Docs](https://docs.megaeth.com) <br>
- [MegaETH Real-time API](https://docs.megaeth.com/realtime-api) <br>
- [MegaETH Testnet Guide](https://docs.megaeth.com/testnet) <br>
- [MegaETH Frontier](https://docs.megaeth.com/frontier) <br>
- [MegaEVM](https://github.com/megaeth-labs/mega-evm) <br>
- [MegaEVM Spec (MiniRex)](https://github.com/megaeth-labs/mega-evm/blob/main/specs/MiniRex.md) <br>
- [MegaETH Token List](https://github.com/megaeth-labs/mega-tokenlist) <br>
- [Solady](https://github.com/Vectorized/solady) <br>
- [KyberSwap Aggregator Docs](https://docs.kyberswap.com/kyberswap-solutions/kyberswap-aggregator) <br>
- [EIP-7966 Discussion](https://ethereum-magicians.org/t/eip-7966-eth-sendrawtransactionsync-method/24640) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MegaETH-specific transaction, RPC, wallet, gas, storage, testing, and deployment guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
