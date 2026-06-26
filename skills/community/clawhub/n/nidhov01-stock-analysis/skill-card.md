## Description: <br>
Analyze stocks and cryptocurrencies using Yahoo Finance data, with portfolio management, watchlists and alerts, dividend analysis, multi-factor scoring, trend scanning, and rumor or early-signal detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nidhov01](https://clawhub.ai/user/nidhov01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and retail-investor workflows use this skill to run command-line stock and crypto analysis, compare tickers, track portfolios and watchlists, review dividends, and scan market, news, and social signals. Outputs are informational and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store local portfolio and watchlist data. <br>
Mitigation: Use it only on trusted machines, review the local state files before sharing the environment, and remove stored portfolio or watchlist data when it is no longer needed. <br>
Risk: Twitter/X social scanning can require sensitive AUTH_TOKEN and CT0 session credentials. <br>
Mitigation: Prefer running social scanning disabled; only provide those credentials if you understand their sensitivity and can store and revoke them appropriately. <br>
Risk: Personal notification and daily-review scripts include under-scoped Feishu reporting behavior. <br>
Mitigation: Review or remove the Feishu scripts and any hardcoded recipient or workspace paths before use. <br>
Risk: Financial analysis, rumor detection, and external market or news data may be stale, incomplete, or misleading. <br>
Mitigation: Treat outputs as informational, verify important signals with authoritative sources, and consult a licensed financial advisor before making investment decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nidhov01/nidhov01-stock-analysis) <br>
- [Publisher Profile](https://clawhub.ai/user/nidhov01) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Usage Guide](artifact/docs/USAGE.md) <br>
- [Technical Architecture](artifact/docs/ARCHITECTURE.md) <br>
- [Hot Scanner](artifact/docs/HOT_SCANNER.md) <br>
- [bird CLI](https://github.com/steipete/bird) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text reports, optional JSON, and Markdown command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local portfolio and watchlist files; output quality depends on external market, news, and social data availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 6.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
