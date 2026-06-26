## Description: <br>
Generates a comprehensive local hardware inventory across macOS, Linux, and Windows, including system, CPU, memory, storage, GPU, display, network, battery, peripheral, sensor, and live status details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BraveHeartZJH](https://clawhub.ai/user/BraveHeartZJH) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, IT staff, and end users use this skill to gather and summarize local computer hardware details when troubleshooting, auditing device configuration, or answering hardware capability questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hardware reports can expose device identifiers such as serial numbers, UUIDs, MAC addresses, Activation Lock status, and other local inventory details. <br>
Mitigation: Review and redact the generated report before sharing it outside the local troubleshooting context. <br>
Risk: Some hardware commands may request sudo or administrator privileges for deeper device details. <br>
Mitigation: Decline elevated prompts unless the extra hardware detail is necessary and the command is expected for the current platform. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BraveHeartZJH/hardware-info) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/BraveHeartZJH) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Structured Markdown hardware report with command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sensitive local device identifiers such as serial numbers, UUIDs, MAC addresses, and battery or Activation Lock status when those commands return them.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
