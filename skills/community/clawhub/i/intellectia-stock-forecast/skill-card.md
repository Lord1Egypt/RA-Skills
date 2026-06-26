## Description: <br>
US Stock AI Trading Assistant | Intellectia AI Stock Forecast - Smart analysis of stock entry/exit points, target price predictions, probability calculations, and technical ratings. Supports "Should I Buy" investment decision Q&A. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xanxustan](https://clawhub.ai/user/xanxustan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to query Intellectia for a single stock, ETF, or crypto ticker forecast and to produce structured "Should I Buy?" analysis. It is intended for informational market analysis, not personalized financial advice or time-sensitive trading decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticker-based queries are sent to Intellectia. <br>
Mitigation: Avoid including private financial details in prompts and limit requests to the ticker and asset type needed for the analysis. <br>
Risk: Forecasts and "Should I Buy?" responses may be delayed or unsuitable for time-sensitive trading. <br>
Mitigation: Treat outputs as informational analysis, not personalized investment advice, and consult qualified professionals or real-time sources before making financial decisions. <br>
Risk: The optional Python workflow installs the requests package. <br>
Mitigation: Install optional dependencies in an isolated Python environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xanxustan/intellectia-stock-forecast) <br>
- [Publisher Profile](https://clawhub.ai/user/xanxustan) <br>
- [Intellectia](https://intellectia.ai/?channelId=601&activityId=1) <br>
- [Intellectia Forecast API](https://api.intellectia.ai/gateway/v1/stock/screener-public) <br>
- [Intellectia Should I Buy API](https://api.intellectia.ai/gateway/v1/finance/should-i-buy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline JSON, cURL, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs summarize API responses and should preserve the skill's informational-use and delayed-data cautions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
