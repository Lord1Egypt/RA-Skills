## Description: <br>
访问猫棒后台（SmartAX MA5671A / OpenWrt SFP）抓取 GPON 状态和设备信息，以加图标的文本表格输出。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wowrouter](https://clawhub.ai/user/wowrouter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Network operators, device administrators, and technical users use this skill to retrieve GPON status and device information from a SmartAX MA5671A / OpenWrt SFP management interface and present the results as a readable Markdown status table. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill logs into a disclosed local device administration page and handles a session cookie. <br>
Mitigation: Use it only for devices you own or administer on a trusted local management network, and treat credentials, cookies, raw logs, and HTML responses as sensitive. <br>
Risk: The skill targets a fixed local management address by default. <br>
Mitigation: Confirm the target device and network before use to avoid accessing an unintended administration interface. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wowrouter/gpon-status) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance] <br>
**Output Format:** [Markdown table with icons] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes GPON status, device information, and warning indicators for signal or temperature values when applicable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
