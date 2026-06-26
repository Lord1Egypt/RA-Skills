## Description: <br>
Deploy an expense tracking pipeline with three agents that automate receipt collection, categorization, and report generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, finance operations teams, and agent administrators use this skill to configure a three-agent Pilot Protocol expense workflow that turns receipts into categorized reports for approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Expense data may be shared with downstream Pilot skills, webhook destinations, Slack channels, and peer agents. <br>
Mitigation: Confirm the approved webhook destination, Slack workspace or channel, and peer handshakes before sending real employee or financial data. <br>
Risk: Archived receipts and report payloads may contain sensitive employee, vendor, or payment information. <br>
Mitigation: Set retention expectations for archived receipts and avoid including unnecessary personal or financial details in test or production events. <br>
Risk: The setup depends on Pilot tooling, downstream pilot-* skills, and local binaries. <br>
Mitigation: Install only if the Pilot tooling and required downstream skills are trusted and available in the deployment environment. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/teoslayer/pilot-expense-tracker-setup) <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash commands and JSON manifest templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes role-specific setup manifests for collector, categorizer, and reporter agents.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
