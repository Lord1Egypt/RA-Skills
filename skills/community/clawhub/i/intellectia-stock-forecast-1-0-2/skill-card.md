## Description: <br>
US Stock AI Trading Assistant | Intellectia AI Stock Forecast - Smart analysis of stock entry/exit points, target price predictions, probability calculations, and technical ratings, with support for "Should I Buy" investment decision Q&A. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Renixaus](https://clawhub.ai/user/Renixaus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to request single-symbol stock, ETF, or crypto forecasts and structured "Should I Buy?" analysis through the Intellectia API. It is intended for informational financial analysis, not professional investment or trading advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticker queries are sent to the Intellectia API. <br>
Mitigation: Install and use only if sharing ticker queries with Intellectia is acceptable for the user's workflow. <br>
Risk: Forecasts and "Should I Buy" responses may be delayed or unsuitable for time-sensitive trading decisions. <br>
Mitigation: Treat outputs as informational analysis only and consult qualified financial professionals before making investment decisions. <br>
Risk: Python examples depend on the external requests package. <br>
Mitigation: Review and install the requests dependency from a trusted package source before running Python examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Renixaus/intellectia-stock-forecast-1-0-2) <br>
- [Intellectia](https://intellectia.ai/?channelId=601&activityId=1) <br>
- [Intellectia forecast API endpoint](https://api.intellectia.ai/gateway/v1/stock/screener-public) <br>
- [Intellectia Should I Buy API endpoint](https://api.intellectia.ai/gateway/v1/finance/should-i-buy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with optional curl commands, Python requests examples, and JSON-derived analysis summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and python3; Python examples use the requests package. Sends ticker queries to Intellectia and supports one-symbol forecast requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
