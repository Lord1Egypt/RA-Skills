## Description: <br>
View and operate Lista Lending vaults/markets. Use when user asks about LENDING-ONLY positions or wants to deposit/withdraw/borrow/repay. For report-style overview, use lista instead. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lawson-ccy](https://clawhub.ai/user/lawson-ccy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to inspect Lista lending-only vault and market positions, select lending targets, and perform deposit, withdraw, supply, borrow, repay, or market-withdraw operations with wallet consent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate real wallet-adjacent lending transactions. <br>
Mitigation: Verify the selected wallet, chain, vault or market, amount, and RPC endpoint before approving any write action. <br>
Risk: Wallet session details and lending context may be stored or reused locally. <br>
Mitigation: Treat files under ~/.agent-wallet as sensitive and clear lending context after use. <br>
Risk: Debug logs may expose transaction or wallet-adjacent operational details. <br>
Mitigation: Enable debug logging only when needed and handle generated logs as sensitive data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lawson-ccy/lista-lending) <br>
- [Publisher profile](https://clawhub.ai/user/lawson-ccy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Human-readable summaries and tables derived from CLI JSON, with agent-side shell command references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write operations require wallet context and explicit user consent before signing.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
