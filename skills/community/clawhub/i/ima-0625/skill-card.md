## Description: <br>
Analyze stocks and cryptocurrencies using Yahoo Finance data, with portfolio tracking, watchlists, dividend analysis, stock scoring, trend scanning, and rumor or early-signal detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run command-line stock and cryptocurrency analysis, compare assets, track portfolios, manage watchlists, and scan market trend or rumor signals. Outputs are informational and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional X/Twitter social scanning uses sensitive AUTH_TOKEN and CT0 session credentials. <br>
Mitigation: Use the social scanners only when needed, keep credentials out of version control, store only required values, and rotate or revoke them if exposed. <br>
Risk: Ticker interests and portfolio context may be sent to third-party market-data, news, social, or SEC-related sources. <br>
Mitigation: Avoid running scans with sensitive holdings or watchlists unless the user accepts those third-party data disclosures. <br>
Risk: Portfolio and watchlist data persist locally. <br>
Mitigation: Review local storage before sharing machines, backups, logs, or skill directories. <br>
Risk: Trading signals can be incomplete, delayed, or misleading. <br>
Mitigation: Treat outputs as informational analysis, read caveats, and consult qualified financial advice before making investment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/ima-0625) <br>
- [Publisher profile](https://clawhub.ai/user/yinwuzhe) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>
- [CoinGecko](https://coingecko.com) <br>
- [CNN Fear & Greed Index](https://money.cnn.com/data/fear-and-greed/) <br>
- [SEC EDGAR](https://www.sec.gov/edgar) <br>
- [Google News](https://news.google.com) <br>
- [X](https://x.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Console text, JSON, and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local portfolio and watchlist files; optional social scanners require X/Twitter session credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter version 6.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
