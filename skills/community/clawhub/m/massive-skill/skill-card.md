## Description: <br>
Access Massive(Polygon) stock, crypto, forex, options, indices, futures, market data, and news APIs via CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bruce-shi](https://clawhub.ai/user/bruce-shi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to retrieve Massive(Polygon) market data and news through documented CLI commands. It supports workflows that need JSON market, reference, options, forex, crypto, indices, futures, and news data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs the npm massive CLI through npx, which introduces package supply-chain exposure. <br>
Mitigation: Review or pin the npm package version before running commands. <br>
Risk: The skill requires a MASSIVE_API_KEY credential for API access. <br>
Mitigation: Provide only the required environment variable and avoid granting unnecessary filesystem or credential access. <br>


## Reference(s): <br>
- [Massive(Polygon) Skill Page](https://clawhub.ai/bruce-shi/massive-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/bruce-shi) <br>
- [Massive API](https://massive.com) <br>
- [Stocks Commands Reference](references/stocks_commands.md) <br>
- [Crypto Commands Reference](references/crypto_commands.md) <br>
- [Forex Commands Reference](references/forex_commands.md) <br>
- [Options Commands Reference](references/options_commands.md) <br>
- [Indices Commands Reference](references/indices_commands.md) <br>
- [Reference Data Commands Reference](references/reference_commands.md) <br>
- [Market Data Commands Reference](references/market_commands.md) <br>
- [News Commands Reference](references/news_commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI command results are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npx and MASSIVE_API_KEY; commands run the npm massive CLI.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
