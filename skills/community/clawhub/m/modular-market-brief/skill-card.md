## Description: <br>
Generate modular, data-backed market reports (AM/PM) across global assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boilerrat](https://clawhub.ai/user/boilerrat) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, employees, and analysts use this skill to generate concise AM/PM market briefs, cross-asset dashboards, top-mover summaries, trend tables, and a single best-idea wrap-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Helper scripts can query third-party financial data services with ticker symbols supplied by the user. <br>
Mitigation: Run the scripts only with ticker symbols that are acceptable to disclose to those services, and disclose network use before execution. <br>
Risk: Public market-data endpoints may be rate-limited, unavailable, changed, or incomplete. <br>
Mitigation: Treat generated prices, movers, and trend labels as best-effort inputs and verify important figures against authoritative market data before use. <br>
Risk: Market briefs and trend labels can be mistaken for trade recommendations. <br>
Mitigation: Present outputs as patterns, biases, and scenarios with invalidation points; do not place trades or state certainty. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/boilerrat/modular-market-brief) <br>
- [Yahoo Finance Screener Endpoint](https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved) <br>
- [TMX Money Canadian Markets](https://money.tmx.com/en/canadian-markets) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown market brief with optional JSON or markdown tables from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May query public third-party financial data services for user-provided ticker symbols.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
