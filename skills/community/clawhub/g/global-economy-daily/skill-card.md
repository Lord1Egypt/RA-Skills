## Description: <br>
Automatically generates daily global economic insight reports with market data, geopolitical event summaries, and outlook commentary for QQ or Feishu delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[markdown777](https://clawhub.ai/user/markdown777) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operators use this skill to generate a daily market and geopolitical briefing, then send or schedule it through QQ or Feishu. It is intended for recurring economic summary workflows that combine live Yahoo Finance price pulls with templated commentary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can present live price pulls together with static or templated commentary as a real-time analysis report. <br>
Mitigation: Review and rewrite analysis sections before relying on them, and clearly distinguish live prices from templated commentary. <br>
Risk: The artifact includes broad outbound-send instructions and a preconfigured QQ target. <br>
Mitigation: Confirm or replace all QQ and Feishu recipients, and add an explicit confirmation step before any external message is sent. <br>
Risk: The documentation describes installing a LaunchAgent for recurring external messages. <br>
Mitigation: Create the LaunchAgent only when recurring delivery is intended and after recipients, timing, and content have been reviewed. <br>


## Reference(s): <br>
- [Global Economy Daily artifact documentation](SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/markdown777/global-economy-daily) <br>
- [Yahoo Finance chart API endpoint](https://query1.finance.yahoo.com/v8/finance/chart) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style daily report text with optional shell commands and launchd configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live market prices, static or templated analysis, and outbound message delivery settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
