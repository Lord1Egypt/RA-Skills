## Description: <br>
Deploy a status page pipeline with 3 agents that automate service monitoring, status aggregation, and public incident communication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to configure a three-agent status page workflow for health checks, status aggregation, and incident notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup depends on pilotctl, clawhub, and multiple role-specific pilot-* skills. <br>
Mitigation: Confirm those tools and skills are trusted and expected before installation or execution. <br>
Risk: The setup manifest write step may replace existing status page setup data. <br>
Mitigation: Inspect or back up ~/.pilot/setups/status-page.json before writing the role-specific manifest. <br>
Risk: Incident notifications may expose internal hostnames, private endpoints, secrets, or unnecessary outage details. <br>
Mitigation: Review and minimize incident payloads before publishing to status pages, subscriber emails, or Slack channels. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON manifest templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires pilotctl, clawhub, the referenced pilot-* skills, and a running daemon.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
