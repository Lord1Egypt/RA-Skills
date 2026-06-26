## Description: <br>
Track and interpret SEC Form 4 insider buying and selling activity across US-listed equities using the Finskills API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[finskills](https://clawhub.ai/user/finskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to fetch and summarize SEC Form 4 insider transaction data for US-listed equities. It helps screen for insider buying, selling, cluster activity, and related filing context as informational market analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Finskills API key and sends ticker, watchlist, and filing lookup queries to Finskills. <br>
Mitigation: Treat FINSKILLS_API_KEY as a secret, verify the provider before use, and avoid sending sensitive watchlists unless that data sharing is acceptable. <br>
Risk: The generated buy, sell, or caution signal could be mistaken for financial advice. <br>
Mitigation: Treat outputs as informational analysis and review them alongside fundamentals, valuation, and independent investment judgment. <br>
Risk: Form 4 data can be delayed and insider selling can be ambiguous. <br>
Mitigation: Check filing dates, note possible two-business-day reporting delays, and interpret selling signals with the caveats included in the skill output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/finskills/insider-trade-tracker) <br>
- [Project homepage](https://github.com/finskills/insider-trade-tracker) <br>
- [Finskills API registration](https://finskills.net/register) <br>
- [Finskills insider trades endpoint](https://finskills.net/v1/free/sec/insider-trades/{SYMBOL}) <br>
- [Finskills SEC filings endpoint](https://finskills.net/v1/free/sec/filings/{CIK}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Guidance] <br>
**Output Format:** [Markdown report with structured insider sentiment, recent transactions, signal analysis, caveats, and an overall verdict] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FINSKILLS_API_KEY and sends ticker, watchlist, and filing lookup queries to Finskills.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
