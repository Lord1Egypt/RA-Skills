## Description: <br>
Tracks recent IPOs and generates TradingView watchlists. Auto-triggers on phrases like "recent IPOs", "tradingview watchlist", "IPO calendar", "IPO tracker", "IPO report", "new stock listings", or "IPO data". <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sarkcesscrewpay](https://clawhub.ai/user/sarkcesscrewpay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to collect recent IPO data, enrich it with market details, and produce TradingView watchlists, reports, and CSV exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may run scripts, install dependencies, fetch live market data, and write export files. <br>
Mitigation: Ask before running commands or writing files, and review generated outputs before using them. <br>
Risk: IPO and market data can be incomplete, stale, or unsuitable as investment advice. <br>
Mitigation: Treat generated reports and watchlists as research aids and verify market information with authoritative sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sarkcesscrewpay/ipo-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown summary with generated text and CSV/watchlist files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write ipo_watchlist.txt, ipo_report.txt, and ipo_data.csv when the supporting script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
