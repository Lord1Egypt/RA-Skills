## Description: <br>
Tracks Strait of Hormuz shipping transit data from public shipping sites, records daily traffic and throughput metrics, and alerts when traffic recovery thresholds are met. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laigen](https://clawhub.ai/user/laigen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts, operators, and agents use this skill to monitor public shipping indicators around the Strait of Hormuz, persist transit observations, and surface recovery alerts for Middle East shipping disruption and oil-flow monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs Chrome/Selenium browser automation and uses webdriver-manager to download ChromeDriver. <br>
Mitigation: Install and run it only in environments where browser automation and driver downloads are approved. <br>
Risk: The skill writes local CSV history and may create debug screenshots or HTML files under ~/.openclaw/workspace/memory. <br>
Mitigation: Review local retention requirements and remove debug artifacts when they are no longer needed. <br>
Risk: Notification channels can send monitoring summaries outside the local runtime when enabled. <br>
Mitigation: Review the configured channel before enabling notifications and confirm that external sharing is acceptable. <br>


## Reference(s): <br>
- [Configuration Reference](references/config.json) <br>
- [Hormuz Strait Monitor Data Source](https://hormuzstraitmonitor.com/) <br>
- [ShipXY Hormuz Data Source](https://www.shipxy.com/special/hormuz) <br>
- [ClawHub Skill Page](https://clawhub.ai/laigen/hormuz-strait-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Configuration] <br>
**Output Format:** [Plain text runtime summaries and CSV rows, with Markdown setup instructions in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Appends timestamped transit metrics and alert messages to a local CSV file under ~/.openclaw/workspace/memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
