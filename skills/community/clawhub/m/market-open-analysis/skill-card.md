## Description: <br>
openpd automatically collects WTI crude oil and gold price data, analyzes overnight market news, and sends a weekday opening-market prediction report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linshengyyy](https://clawhub.ai/user/linshengyyy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use openpd to automate weekday morning WTI crude oil and gold opening-market reports. The skill combines commodity price data and overnight news into a Markdown report and sends it through OpenClaw messaging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install persistent weekday cron jobs that continue collecting data and sending market reports. <br>
Mitigation: Review the exact cron entries before installation and use the documented status or uninstall flow to disable scheduled jobs when they are no longer needed. <br>
Risk: Commodity and news API keys may be stored in plaintext Python source or configuration files. <br>
Mitigation: Keep the skill directory private and prefer environment variables or a locked-down secrets file instead of committing credentials into source files. <br>
Risk: Market-opening predictions can be wrong or misleading if price feeds, news search results, or simple sentiment rules are incomplete. <br>
Mitigation: Treat reports as informational automation only, review the underlying data before acting, and preserve the documented warning that predictions are not investment advice. <br>
Risk: Reports are pushed through OpenClaw messaging to configured users or channels. <br>
Mitigation: Confirm the target user and channel before enabling scheduled sends to avoid disclosing market analysis or operational details to the wrong recipient. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linshengyyy/market-open-analysis) <br>
- [README.md](artifact/README.md) <br>
- [API_KEY.example.md](artifact/API_KEY.example.md) <br>
- [INSTALL.md](artifact/INSTALL.md) <br>
- [CommodityPriceAPI](https://commoditypriceapi.com) <br>
- [CommodityPriceAPI rates endpoint](https://api.commoditypriceapi.com/v2) <br>
- [East Money Miaoxiang news search endpoint](https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown market report, JSON price data files, logs, and setup guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-supplied CommodityPriceAPI, East Money Miaoxiang news API, and OpenClaw messaging configuration; may install weekday cron jobs.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
