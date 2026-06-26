## Description: <br>
Provides real-time institutional options flow and momentum analysis for US equities using the OptionWhales API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssidharhubble](https://clawhub.ai/user/ssidharhubble) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and trading-system builders use this skill to fetch options flow, momentum rankings, abnormal trades, and ticker-specific flow signals for market analysis and alerting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OptionWhales API key and sends authenticated requests to OptionWhales. <br>
Mitigation: Use a scoped or revocable API key when available and avoid exposing the key in shell history, logs, or shared output. <br>
Risk: Options flow output may be forwarded into automated alerts, dashboards, or trading workflows. <br>
Mitigation: Review downstream piping, cron jobs, and alerting rules before using the data in automated financial decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ssidharhubble/options-flow-intelligence) <br>
- [OptionWhales API](https://optionwhales.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text command output with setup guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPTIONWHALES_API_KEY and network access to OptionWhales.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
