## Description: <br>
Scan Polymarket prediction markets for book arbitrage opportunities in multi-outcome markets, generate a formatted report, and deliver it via Telegram and email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caoqi](https://clawhub.ai/user/caoqi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market analysts use this skill to scan public Polymarket multi-outcome markets for overbooked or underbooked pricing and generate a ranked opportunity report. It also supports scheduled local reports delivered through configured email or Telegram workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scripts fetch public Polymarket market data and write opportunities.json locally. <br>
Mitigation: Review the generated local output before using it for decisions and avoid committing opportunities.json if it contains operationally sensitive preferences. <br>
Risk: Email delivery uses the default Apple Mail account through local osascript automation. <br>
Mitigation: Set SMTP_TO deliberately, review the recipient before scheduling, and run the report manually before enabling recurring delivery. <br>
Risk: The optional cron setup can repeatedly run the scan and send reports without further review. <br>
Mitigation: Review the scripts and delivery settings before enabling a schedule, and monitor initial scheduled runs for failures or unexpected recipients. <br>
Risk: Telegram delivery is described by the skill but is not implemented in the provided scripts. <br>
Mitigation: Do not rely on Telegram delivery unless an implementation is added and reviewed separately. <br>


## Reference(s): <br>
- [Setup Guide](references/setup.md) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/caoqi/polymarket-opportunities-scanning) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown instructions, shell commands, JavaScript scripts, and JSON scan output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local opportunities.json file and formatted report text for email or Telegram delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
