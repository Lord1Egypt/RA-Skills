## Description: <br>
Deploy a log analytics system with four agents for collection, parsing, alerting, and visualization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to set up a four-agent log analytics workflow for centralized collection, parsing, anomaly alerting, dashboards, and reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Child skills installed by the setup, especially webhook and Slack bridge skills, may forward log data to external destinations. <br>
Mitigation: Review the installed child skills before use and configure only Slack channels or webhook destinations the operator controls. <br>
Risk: Log reports and examples may include secrets, personal data, or sensitive operational details. <br>
Mitigation: Redact secrets and personal data from logs, alerts, reports, and sample payloads before sharing or forwarding them. <br>
Risk: The setup writes a local manifest at ~/.pilot/setups/log-analytics.json, which may overwrite an existing setup file. <br>
Mitigation: Check whether the manifest path already exists before running the manifest creation step. <br>


## Reference(s): <br>
- [Pilot Protocol homepage](https://pilotprotocol.network) <br>
- [ClawHub skill page](https://clawhub.ai/teoslayer/pilot-log-analytics-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown with bash commands and JSON manifest templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl, clawhub, the pilot-protocol skill, and a running daemon.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
