## Description: <br>
Deploy an autonomous warehouse orchestration setup with four agents for robot fleet coordination, inventory tracking, pick-wave optimization, and dock scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teoslayer](https://clawhub.ai/user/teoslayer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to configure a multi-agent warehouse setup that coordinates robot fleets, inventory state, pick assignments, and dock events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup can install downstream Pilot skills and change local Pilot configuration for warehouse agents. <br>
Mitigation: Review the role manifest and each downstream pilot-* skill before installation, especially skills that handle escrow or webhook behavior. <br>
Risk: Agent handshakes could connect warehouse coordination flows to unintended peers. <br>
Mitigation: Handshake only with known trusted peer hostnames and verify trust state before publishing operational messages. <br>


## Reference(s): <br>
- [Pilot Protocol](https://pilotprotocol.network) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown with shell commands and JSON manifest snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes role-specific hostnames, peer handshakes, and Pilot manifest content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
