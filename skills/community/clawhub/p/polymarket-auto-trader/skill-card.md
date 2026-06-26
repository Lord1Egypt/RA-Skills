## Description: <br>
Polymarket Auto-Trader is an autonomous prediction-market trading skill that scans Polymarket, evaluates probabilities with an LLM, sizes positions with Kelly criterion, executes CLOB trades, and supports P&L monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[srikanthbellary](https://clawhub.ai/user/srikanthbellary) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and prediction-market traders use this skill to configure and run an autonomous Polymarket bot that evaluates markets with an LLM, sizes positions, places CLOB orders, and monitors P&L. <br>

### Deployment Geography for Use: <br>
Outside the United States, subject to local law and platform availability. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent persistent private-key-backed authority to approve contracts and place real trades. <br>
Mitigation: Use a dedicated low-balance wallet, keep approvals tightly bounded or revoke them when not needed, and set explicit spend limits before enabling automation. <br>
Risk: Private keys and API keys are required for trading and billing access. <br>
Mitigation: Do not paste secrets into prompts or logs; store them only in a locked-down environment file on a hardened VPS with restricted access. <br>
Risk: Autonomous trading and Polymarket access can create financial, legal, and jurisdictional risk. <br>
Mitigation: Verify Polymarket use is legal and permitted in the deployment jurisdiction, test with tiny amounts, monitor logs and P&L, and keep a clear way to stop the cron job. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/srikanthbellary/polymarket-auto-trader) <br>
- [Publisher Profile](https://clawhub.ai/user/srikanthbellary) <br>
- [Publisher Homepage](https://github.com/srikanthbellary) <br>
- [Polymarket API Reference](references/polymarket-api.md) <br>
- [Polymarket Contract Addresses](references/contract-addresses.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python script usage, and configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PRIVATE_KEY and LLM_API_KEY environment variables; outputs setup, approval, cron automation, trading, and monitoring guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
