## Description: <br>
Provides real-time market price data for 25,000+ assets across crypto, equities, forex, ETFs, commodities, and global indices via Juglans Finance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juglans-ai](https://clawhub.ai/user/juglans-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to answer stock, crypto, forex, commodity, ETF, index, and exchange-rate questions with live market data instead of fabricated prices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional unpinned GitHub-based installation steps may run or download changing remote content. <br>
Mitigation: Prefer installing through ClawHub, or review downloaded files before running the shell installer. <br>
Risk: Asset symbols requested through the skill are sent to Juglans Finance. <br>
Mitigation: Avoid sending sensitive or private watchlists unless sharing those symbols with Juglans Finance is acceptable. <br>
Risk: Market data may be unavailable, stale outside market hours, or missing for unsupported identifiers. <br>
Mitigation: Report missing data honestly, include source context, and avoid fabricating prices when the API does not return a quote. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/juglans-ai/market-price) <br>
- [Juglans Finance API](https://finance.juglans.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown text with shell commands and formatted quote summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Price requests may send asset symbols to Juglans Finance; outside market hours responses may reflect the latest available close.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
