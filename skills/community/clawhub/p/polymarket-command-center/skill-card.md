## Description: <br>
Read-only Polymarket interface for browsing trending markets, viewing detailed odds, searching active markets, and tracking watchlists through public Gamma and CLOB APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingmadellc](https://clawhub.ai/user/kingmadellc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to fetch read-only Polymarket market data, compare odds, search active markets, and monitor configured watchlists without API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market queries and configured watchlist slugs may be sent to public Polymarket APIs. <br>
Mitigation: Avoid entering private text as market queries or watchlist slugs. <br>
Risk: The local watchlist file is user-controlled configuration. <br>
Mitigation: Review watchlist configuration before relying on results in sensitive workflows. <br>
Risk: Market data can be unavailable, delayed, or affected by local cache freshness. <br>
Mitigation: Verify important market decisions against Polymarket directly and account for the skill's short cache TTL. <br>


## Reference(s): <br>
- [Polymarket API Reference](references/api-reference.md) <br>
- [Gamma API](https://gamma-api.polymarket.com) <br>
- [CLOB API](https://clob.polymarket.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/kingmadellc/polymarket-command-center) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown-formatted text with command examples, market summaries, probability bars, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May contact public Polymarket APIs and may read a local watchlist configuration file.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
