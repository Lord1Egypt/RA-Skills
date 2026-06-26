## Description: <br>
Aggregate and classify financial news sentiment into Risk-On / Risk-Off signals for market and individual stocks using the Finskills API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[finskills](https://clawhub.ai/user/finskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Traders, analysts, and market-focused agent users use this skill to fetch financial news through Finskills, classify sentiment across markets, tickers, and sectors, and identify catalysts for informational market research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Finskills API key and sends requested symbols, sectors, or market topics to the Finskills API. <br>
Mitigation: Use a dedicated API key, avoid sending topics you are not comfortable sharing with Finskills, and rotate or revoke the key if it is exposed. <br>
Risk: Financial news sentiment can be stale, incomplete, or incorrectly classified and should not be treated as financial advice. <br>
Mitigation: Confirm high-impact news with primary sources such as company investor relations pages or official filings before relying on the report. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/finskills/news-sentiment-analyst) <br>
- [Project homepage](https://github.com/finskills/news-sentiment-analyst) <br>
- [Finskills API](https://finskills.net) <br>
- [Finskills registration](https://finskills.net/register) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown structured financial news and sentiment report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses FINSKILLS_API_KEY; general market news is described as free-tier, while broader latest-news and stock-specific news may require a Pro plan.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
