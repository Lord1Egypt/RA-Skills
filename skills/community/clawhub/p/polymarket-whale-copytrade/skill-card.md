## Description: <br>
Mirror high-performing whale wallets on Polymarket by monitoring configured wallet addresses for recent trades above a size threshold and copying them with Simmer safeguards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chokle](https://clawhub.ai/user/chokle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to automate Polymarket copytrading from selected whale wallets through Simmer, with configurable position sizing, wallet lists, dry-run mode, and live execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The packaged managed automation can place live financial trades every 15 minutes. <br>
Mitigation: Install only when unattended live copytrading is intended, remove or change the managed --live automaton for dry runs, and confirm live execution before deployment. <br>
Risk: Copied trades can create financial exposure based on configured whale wallets and imported markets. <br>
Mitigation: Review tracked wallets and market-import behavior, set strict Simmer spending limits, and use a restricted API key or account where possible. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chokle/polymarket-whale-copytrade) <br>
- [Simmer Docs](https://docs.simmer.markets) <br>
- [Simmer Skill Building Guide](https://docs.simmer.markets/skills/building) <br>
- [Polymarket](https://polymarket.com) <br>
- [Polymarket CLOB API](https://docs.polymarket.com) <br>
- [Polymarket Leaderboard](https://polymarket.com/leaderboard) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls] <br>
**Output Format:** [Command-line text output and JSON automaton reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; managed automation is configured to run live every 15 minutes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
