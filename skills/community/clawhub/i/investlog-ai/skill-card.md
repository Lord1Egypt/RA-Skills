## Description: <br>
InvestLog AI lets agents query the InvestLog API for real-time U.S. stock quotes, valuation, financials, analyst views, ownership data, market news, technical indicators, and related stock research in English or Chinese. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nblicb](https://clawhub.ai/user/nblicb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer natural-language questions about U.S. stocks, including price action, valuation, financial statements, analyst ratings, ownership, trades, dividends, technical indicators, and market news. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Passing an API key in a URL query string can expose the credential through logs, browser history, or shared request traces. <br>
Mitigation: Use the free trial without a key when possible; if a key was placed in a URL, rotate it and avoid high-privilege or billing-sensitive keys until a header-based key pattern is available. <br>


## Reference(s): <br>
- [InvestLog API homepage](https://api.investlog.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Natural-language answer with optional Markdown tables, based on JSON responses from the InvestLog API.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include stock tickers, tabular metrics, trends, and remaining query count from the API response.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
