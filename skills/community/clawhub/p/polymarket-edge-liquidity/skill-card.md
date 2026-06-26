## Description: <br>
Trades active Polymarket-imported markets on Simmer when estimated edge and liquidity filters pass. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drserkandedeoglu](https://clawhub.ai/user/drserkandedeoglu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to scan active Polymarket-imported markets on Simmer and dry-run or place trades when configured edge and liquidity thresholds pass. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place trades through the configured Simmer account. <br>
Mitigation: Run the default dry-run first, verify TRADING_VENUE and TRADE_AMOUNT, keep limits conservative, and use --live only when trade execution is intended. <br>
Risk: The skill requires a Simmer API key. <br>
Mitigation: Install only when comfortable granting SIMMER_API_KEY access, and provide the key through the environment rather than hard-coding it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drserkandedeoglu/polymarket-edge-liquidity) <br>
- [Publisher profile](https://clawhub.ai/user/drserkandedeoglu) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Console text with markdown setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to dry-run and only places trades when --live is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
