## Description: <br>
Uses the MachineCommander MCP service to query real-time data, status, location, alerts, project information, and movement history for construction machinery and vessels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sandofree](https://clawhub.ai/user/sandofree) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to answer operational questions about construction equipment and vessels, including counts, locations, work status, fuel, alarms, project membership, and recent activity. The artifact also documents command dispatch through the MachineCommander MCP service, which should be used only with appropriate operational controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documents command dispatch to real construction machines, and the security evidence does not show clear safety controls. <br>
Mitigation: Use only with trusted MachineCommander MCP access that is authenticated, tenant or project scoped, logged, and gated by explicit human approval before any machine command is executed. <br>
Risk: The skill depends on live operational data from the MachineCommander MCP service. <br>
Mitigation: Install only when the service is trusted and operational control is needed; verify access scope and review returned data before acting on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sandofree/machine-commander-query) <br>
- [Publisher profile](https://clawhub.ai/user/sandofree) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON responses from MCP calls with markdown guidance and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Large result sets may require reviewing only the first key records.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
