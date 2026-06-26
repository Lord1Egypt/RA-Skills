## Description: <br>
Newspulse provides cryptocurrency news command-line outputs, including a mock latest-news view and RSS-backed keyword search. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[gztanht](https://clawhub.ai/user/gztanht) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use Newspulse to query and display cryptocurrency news summaries or keyword-filtered RSS results during market-monitoring workflows. Users should independently verify reported crypto news before acting on it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The main news command can display mock cryptocurrency headlines as if they are current news. <br>
Mitigation: Treat the latest-news output as sample data unless live fetching is clearly enabled, and verify crypto news against independent sources before using it for trading, monitoring, or alerts. <br>
Risk: Cryptocurrency news and sentiment outputs may be incomplete, stale, or dependent on third-party source availability. <br>
Mitigation: Use the skill as an informational aid only and cross-check important events with primary or reputable news sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gztanht/newspulse) <br>
- [CoinDesk RSS feed](https://www.coindesk.com/arc/outboundfeeds/rss/) <br>
- [Cointelegraph RSS feed](https://cointelegraph.com/rss) <br>
- [The Block RSS feed](https://www.theblock.co/rss.xml) <br>
- [Decrypt RSS feed](https://decrypt.co/feed) <br>
- [Bitcoin Magazine RSS feed](https://bitcoinmagazine.com/.rss/full.xml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Console text and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [News results may include mock latest-news entries; keyword search attempts live RSS retrieval from configured public feeds.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
