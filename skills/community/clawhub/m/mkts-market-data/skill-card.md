## Description: <br>
Real-time market data, portfolio tracking, trade journaling, screening, and news for stocks, crypto, ETFs, commodities, and forex - no API key required to start. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdliriano](https://clawhub.ai/user/sdliriano) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve market data, screen assets, compare tickers, summarize financial news, and manage portfolio, journal, and watchlist records through mkts.io API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market queries and portfolio, journal, or watchlist content may be sent to mkts.io. <br>
Mitigation: Send only the data needed for the user request, avoid unnecessary private details, and confirm before transmitting sensitive portfolio or journal content. <br>
Risk: Portfolio, journal, and watchlist endpoints can create, update, delete, or clear user records. <br>
Mitigation: Treat POST, PATCH, and DELETE commands as state-changing operations; confirm the action, target IDs, and affected counts with the user before execution. <br>
Risk: The optional MKTS_API_KEY grants higher limits and access to authenticated endpoints. <br>
Mitigation: Keep MKTS_API_KEY private, pass it through the environment or request header only, and avoid printing or storing it in generated output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdliriano/mkts-market-data) <br>
- [mkts API base URL](https://mkts.io/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with curl commands and JSON response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl; MKTS_API_KEY is optional for basic market data and required for portfolio, journal, watchlist, portfolio card, and ask endpoints.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
