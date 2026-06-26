## Description: <br>
Analyzes a specific Polymarket wallet with Nansen CLI commands to show trader bets, trade history, PnL breakdown, and market context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External analysts, developers, and agents use this skill to inspect a Polymarket trader address, retrieve recent trades, compare resolved and unresolved PnL, and identify market context for the wallet's positions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs Nansen CLI research commands that require a Nansen API key and may consume API quota. <br>
Mitigation: Confirm the NANSEN_API_KEY is appropriate for the environment, trust the installed nansen-cli package, and monitor API usage. <br>
Risk: Wallet trade and PnL analysis depends on Nansen and Polymarket data returned for the supplied address. <br>
Mitigation: Validate the wallet address, prefer addresses sourced from trades-by-market as documented, and review resolved versus unresolved market results before relying on conclusions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nansen-devops/nansen-polymarket-trader-profile) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/nansen-devops) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the NANSEN_API_KEY environment variable and the nansen CLI.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
