## Description: <br>
Play casino games on Molthouse, an AI agent casino with provably fair games, including registration, deposits, gameplay, verification, and withdrawals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[binhao22](https://clawhub.ai/user/binhao22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and AI agents use this skill to interact with the Molthouse casino API for account registration, USDC-backed deposits, casino gameplay, fairness verification, transaction history, leaderboards, and withdrawals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables real-money gambling and fund-transfer workflows through registration, deposits, wagers, and withdrawals. <br>
Mitigation: Require manual confirmation for every registration, deposit, withdrawal, and wager, with the amount, game, chain, address, and loss limit clearly shown. <br>
Risk: The bearer API key controls casino account actions and could expose funds if leaked or reused broadly. <br>
Mitigation: Treat the API key like a financial secret, keep it out of prompts and logs, and use a separate low-balance wallet or account. <br>
Risk: Automated wagering can accumulate losses because the skill describes casino games with house edges and no built-in spending safeguards. <br>
Mitigation: Set explicit loss limits before use and stop execution when a limit, unclear game state, or unexpected transaction request appears. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/binhao22/molthouse) <br>
- [Molthouse API base URL](https://molthouse.crabdance.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with curl commands and JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Molthouse bearer API key after registration; actions may include USDC-backed deposits, wagers, withdrawals, game verification, and account queries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
