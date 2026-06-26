## Description: <br>
Exploit NOAA/Open-Meteo forecast vs Polymarket temperature market mispricing. Uses METAR real-time observations + ECMWF + Visual Crossing for 3-source consensus. Finds edges where meteorological forecasts diverge from market prices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[themsquared](https://clawhub.ai/user/themsquared) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and market-analysis agents use this skill to scan Polymarket weather markets, compare prices with meteorological forecasts, and optionally prepare or execute trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is a real-money Polymarket trading skill with under-documented wallet use and delegated trade execution. <br>
Mitigation: Review or supply the referenced trader.py component, confirm which wallet and private key are exposed, and set strict external spending limits before enabling buy mode. <br>
Risk: Buy mode can execute trades based on forecast-derived market signals. <br>
Mitigation: Use --dry-run first, inspect proposed trades and sizing, and require explicit operator approval before live execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/themsquared/polymarket-weather-scanner-pro) <br>
- [Publisher profile](https://clawhub.ai/user/themsquared) <br>
- [Polymarket Gamma API endpoint](https://gamma-api.polymarket.com) <br>
- [Open-Meteo forecast API endpoint](https://api.open-meteo.com/v1/forecast) <br>
- [Visual Crossing timeline API endpoint](https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe scanner output, dry-run results, configuration prerequisites, and trade execution commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
