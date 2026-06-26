## Description: <br>
Autonomous trading for AI agents on Solana and BNB Chain. Use when: (1) executing token swaps on DEXs (Raydium, PancakeSwap), (2) checking token prices and balances, (3) monitoring liquidity pools, (4) implementing trading strategies, (5) managing portfolio positions. Supports headless execution without browser interaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bnbcompanions](https://clawhub.ai/user/bnbcompanions) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use this skill to guide headless crypto trading workflows on Solana and BNB Chain, including token swaps, price checks, balance checks, pool monitoring, and strategy execution. It is intended for agents that can run Python scripts and manage wallet/RPC configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use wallet private keys to make real on-chain trades without strong confirmation or spending-limit safeguards. <br>
Mitigation: Use only a dedicated low-balance trading wallet, require explicit approval before live trades, and enforce token allowlists, maximum trade sizes, loss limits, and a stop mechanism. <br>
Risk: Live trading through RPC, DEX, and aggregator services can fail, return stale data, or execute under unfavorable market conditions. <br>
Mitigation: Run simulations or testnet flows first, use reliable RPC endpoints, keep conservative slippage limits, and monitor transaction failures before increasing trade size. <br>
Risk: Dependencies and trading scripts can affect private keys and submitted transactions. <br>
Mitigation: Pin and audit dependencies before installation and review script behavior before supplying wallet credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bnbcompanions/headless-crypto) <br>
- [Raydium reference](references/raydium.md) <br>
- [PancakeSwap reference](references/pancakeswap.md) <br>
- [Trading strategies reference](references/strategies.md) <br>
- [RPC endpoints reference](references/rpc_endpoints.md) <br>
- [Raydium docs](https://docs.raydium.io) <br>
- [Jupiter docs](https://docs.jup.ag) <br>
- [Solana Cookbook](https://solanacookbook.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code snippets, shell commands, configuration notes, and script outputs such as balances, prices, transaction hashes, and JSON-like result dictionaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Headless Python workflows may call external RPC, DEX, and aggregator APIs and may require wallet private keys or environment variables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
