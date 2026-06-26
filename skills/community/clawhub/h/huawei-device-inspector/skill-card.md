## Description: <br>
Inspects Huawei switches and routers over SSH, collects status, alarm, resource, and security-risk data, and generates a Markdown health report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[v585](https://clawhub.ai/user/v585) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and network operations engineers use this skill for routine inspections, troubleshooting, and security audit checks of Huawei network devices. It helps collect device state, resource usage, active alarms, and issue summaries for operational reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports live-looking router and switch login details in the skill artifact. <br>
Mitigation: Remove hardcoded device details, rotate any credential that may have been real, and require operators to provide secrets through an approved secure channel. <br>
Risk: The security evidence reports unsafe SSH guidance, including disabled host-key checking. <br>
Mitigation: Verify SSH host keys before connecting and only run inspections against devices the operator is explicitly authorized to assess. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/v585/huawei-device-inspector) <br>
- [Publisher profile](https://clawhub.ai/user/v585) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with tables and inline command or code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include device diagnostics, alarm summaries, and recommendations; credentials and host details should be supplied securely by the operator.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
