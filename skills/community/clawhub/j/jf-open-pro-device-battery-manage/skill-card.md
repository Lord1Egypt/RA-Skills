## Description: <br>
杰峰低功耗设备电池管理技能（开发版）。支持查询低电量阈值范围、设置低电量模式阈值等电池管理功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jftech](https://clawhub.ai/user/jftech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators who manage JF low-power or solar-powered devices use this skill to query supported low-battery threshold ranges, inspect the current threshold, and set a new low-battery mode threshold. <br>

### Deployment Geography for Use: <br>
China Mainland, Asia, Europe, and North America, according to the documented JF API endpoint regions. <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive JF app credentials and device tokens. <br>
Mitigation: Keep secrets out of shared terminals and CI logs, and rotate any app secret or device token that may have been printed or logged. <br>
Risk: The skill can change live low-battery behavior on managed devices. <br>
Mitigation: Use it only for JF devices you manage, verify the supported threshold range and current value, and review the requested threshold before setting it. <br>
Risk: Endpoint selection affects where device API calls are sent. <br>
Mitigation: Set JF_ENDPOINT only to an official JF API host for the intended region. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jftech/jf-open-pro-device-battery-manage) <br>
- [JF Open Platform documentation](https://docs.jftech.com) <br>
- [Get low-battery threshold range configuration](https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=9bf993f3140ad9f9b4390fee750ba740&lang=zh) <br>
- [Set low-battery threshold configuration](https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=b246b44faa8c4d41a3f10e3de95b892a&lang=zh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands, environment variables, and API parameters.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JF credentials, a bound device, a device token, and an official JF API endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata.version: 1.4.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
