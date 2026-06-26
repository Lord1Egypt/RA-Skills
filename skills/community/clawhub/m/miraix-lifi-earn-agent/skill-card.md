## Description: <br>
Use this skill when the user wants to discover the best USDC vaults with LI.FI Earn, ask an agent to choose a safe vault on Base/Arbitrum/Ethereum, prepare a Composer-compatible deposit, execute the deposit with an Agentic Wallet, and explain which receipt token was received after deposit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richard7463](https://clawhub.ai/user/richard7463) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to discover USDC vaults on Base, Arbitrum, or Ethereum with LI.FI Earn, prepare Composer deposit quotes, execute deposits with an Agentic Wallet, and explain receipt tokens after deposit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide real wallet approvals and deposits without requiring a mandatory final transaction-specific confirmation step. <br>
Mitigation: Require explicit confirmation before every approval and deposit, showing the exact amount, chain, vault, token, spender address, and expected receipt token before signing. <br>
Risk: Vault discovery or quote guidance could lead to incorrect or misleading deposit decisions if the user assumes all results are live and safe. <br>
Mitigation: Base recommendations on returned API data, disclose seeded or fallback vault data when present, and ask the user to review the selected vault before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/richard7463/miraix-lifi-earn-agent) <br>
- [Publisher Profile](https://clawhub.ai/user/richard7463) <br>
- [Miraix Earn Discovery API](https://app.miraix.fun/api/earn/chat) <br>
- [Miraix Composer Quote API](https://app.miraix.fun/api/earn/quote) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Action-oriented vault recommendations, Composer quote preparation, execution guidance, and receipt-token explanations.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
