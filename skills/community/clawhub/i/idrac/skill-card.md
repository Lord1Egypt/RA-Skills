## Description: <br>
Monitor and manage Dell PowerEdge servers via the iDRAC Redfish API for hardware health, inventory, logs, and power operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eddygk](https://clawhub.ai/user/eddygk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and infrastructure administrators use this skill to configure iDRAC access, run Redfish helper commands, inspect PowerEdge health and inventory, and perform power operations with confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper can cache iDRAC credentials in ~/.idrac-credentials and source ~/.config/idrac-skill/config. <br>
Mitigation: Use a dedicated least-privilege iDRAC account, keep credential files mode 600, delete cached credentials when not needed, and review the config file before execution. <br>
Risk: The helper disables TLS certificate verification for iDRAC HTTPS connections. <br>
Mitigation: Run it only on a trusted management network unless it is modified to validate the iDRAC certificate. <br>
Risk: Power and BIOS-changing operations can disrupt real servers. <br>
Mitigation: Require explicit human approval before shutdown, restart, power, or BIOS-changing actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/eddygk/idrac) <br>
- [iDRAC Redfish API Endpoint Reference](references/endpoints.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with shell command examples, JSON API output, and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq on macOS or Linux; connects only to the configured iDRAC address and may manage cached local credentials.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
