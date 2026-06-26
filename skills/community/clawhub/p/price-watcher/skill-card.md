## Description: <br>
Monitor product URLs to track and alert on significant price changes using a local watchlist without requiring API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to maintain a local watchlist of product URLs, check current prices, compare changes against a threshold, and produce markdown alerts for drops, increases, or fetch errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches user-supplied product URLs and stores product names, URLs, prices, and price history in a local watchlist. <br>
Mitigation: Use only public product URLs, avoid internal or sensitive URLs, and review local watchlist contents before sharing logs or reports. <br>
Risk: Scheduled checks or webhook notifications can repeatedly fetch sites or send price data to an external service. <br>
Mitigation: Review cron entries and webhook destinations before enabling automation, and keep webhook URLs out of shared files and command history. <br>
Risk: Retailer anti-bot controls or layout changes may cause fetch errors or missing prices. <br>
Mitigation: Treat fetch_error and no_price results as signals to review manually, and provide explicit price entries when automatic extraction is unreliable. <br>


## Reference(s): <br>
- [Price Watcher Setup Guide](references/setup-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/newageinvestments25-byte/price-watcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON examples; scripts produce JSON results and markdown alert reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Price history is stored locally in watchlist.json; compare.py supports a configurable percentage threshold.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
