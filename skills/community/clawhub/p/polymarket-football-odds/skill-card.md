## Description: <br>
Analyze Polymarket football/soccer match URLs and estimate match win/draw probabilities using API-Football/API-SPORTS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[remixmm](https://clawhub.ai/user/remixmm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze a Polymarket soccer event or market URL, identify the likely fixture, retrieve API-Football predictions, and summarize home, draw, away, and target-team probabilities with caveats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the provided Polymarket slug to Polymarket's public Gamma API and sends fixture lookup requests plus the API-Football key to API-Football. <br>
Mitigation: Use a dedicated API-Football key with quota limits where possible and avoid placing credentials in files or messages. <br>
Risk: Fixture matching can be ambiguous when team names, dates, leagues, or time zones do not line up cleanly across sources. <br>
Mitigation: Check the extracted teams and fixture confidence, ask the user to confirm low-confidence matches, or rerun with a known fixture ID. <br>
Risk: API-Football predictions and Polymarket prices are third-party signals and should not be treated as betting advice or guaranteed probabilities. <br>
Mitigation: Present the output with caveats and distinguish model prediction percentages from market-implied prices. <br>


## Reference(s): <br>
- [API reference notes](references/api-football-polymarket.md) <br>
- [API-Football v3 documentation](https://www.api-football.com/documentation-v3) <br>
- [Polymarket market data docs](https://docs.polymarket.com/market-data/fetching-markets) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Human-readable summary or structured JSON from a command-line analysis script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include fixture candidates, match confidence, market prices, API-Football prediction percentages, and caveats about model predictions and market-implied prices.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
