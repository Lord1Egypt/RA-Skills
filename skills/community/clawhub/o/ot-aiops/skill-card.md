## Description: <br>
Vendor-neutral industrial/OT data tap and troubleshooting router for reading and, with gated controls, writing to PLCs, controllers, machine tools, and IIoT brokers across common industrial protocols. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zw008](https://clawhub.ai/user/zw008) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, OT engineers, and reliability teams use this skill to route industrial protocol requests to an OT AIOps MCP server for data collection, diagnostics, asset inventory, and controlled troubleshooting actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes high-impact OT and industrial write capabilities that can affect controllers, brokers, or equipment when used against live systems. <br>
Mitigation: Use write tools only with formal authorization, keep dry-run and double-confirm controls in place, and avoid production control systems unless the change is approved. <br>
Risk: Industrial endpoint credentials and the OT AIOps master password could provide broad access if mishandled. <br>
Mitigation: Use least-privilege endpoint credentials, protect the master password, and review the MCP server implementation before using live equipment. <br>
Risk: Behavior validated in preview, mock, or simulated environments may not match live industrial equipment. <br>
Mitigation: Verify configuration and diagnostics against the target equipment in a controlled environment before relying on results or taking action. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline commands, configuration paths, protocol tool names, and safety guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include protocol-specific diagnostics and gated write cautions for OT environments.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
