## Description: <br>
Project 0 guides agents through permissionless DeFi yield, borrowing, and rate-arbitrage workflows on Solana using P0 data APIs and wallet-authorized transactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[borcherd](https://clawhub.ai/user/borcherd) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to evaluate P0 deposit yields, borrowing options, and advanced Solana DeFi strategies, then prepare or execute wallet-authorized deposits, borrows, repayments, withdrawals, and swaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through Solana transactions that require wallet signing and may move funds. <br>
Mitigation: Use only a dedicated, low-balance wallet and require explicit review of amounts, protocols, destination accounts, fees, and slippage before each signing step. <br>
Risk: Using a primary wallet or seed-derived key can expose high-value funds to agent mistakes or misuse. <br>
Mitigation: Do not use a primary wallet or seed-derived keypair; provide a limited-purpose keypair only for the intended P0 activity. <br>
Risk: The security summary says confirmation before moving funds is not consistently required. <br>
Mitigation: Require the agent to present the full plan and obtain user confirmation before every transaction that signs or broadcasts on-chain. <br>
Risk: Swap flows may share transaction details with a third-party routing service. <br>
Mitigation: Review any Jupiter swap request, including token route, slippage, fees, and third-party data sharing, before approving execution. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/borcherd/project-0) <br>
- [Project 0 Homepage](https://0.xyz) <br>
- [Project 0 Protocol Overview](https://docs.0.xyz/) <br>
- [Project 0 TypeScript SDK](https://docs.0.xyz/typescript-sdk/overview) <br>
- [P0 Banks API](https://ai.0.xyz/api/banks) <br>
- [P0 Strategies API](https://ai.0.xyz/api/strategies) <br>
- [P0 Wallet API](https://ai.0.xyz/api/wallet/{address}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only analysis can use public P0 APIs; on-chain actions require user-provided wallet and RPC configuration.] <br>

## Skill Version(s): <br>
2.2.6 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
