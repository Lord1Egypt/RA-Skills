## Description: <br>
使用积智数据 4S价 API，通过配件编码列表查询汽车配件的 4S价信息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[polaris2013](https://clawhub.ai/user/polaris2013) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query 4S pricing for automotive parts from a VIN and one or more parts codes, then summarize returned price fields such as sale and net prices with and without tax. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: VINs, parts codes, and the JZ_API_KEY are sent to a third-party pricing API. <br>
Mitigation: Use the skill only when authorized to share the vehicle and parts data with JZ/积智数据, and use a dedicated API key where possible. <br>
Risk: Returned pricing may be unavailable, outdated, or rejected for invalid VINs or missing data. <br>
Mitigation: Check API error objects and confirm important pricing results against the authoritative service before making business decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/polaris2013/price4s) <br>
- [JZ 4S price API endpoint](https://erp.qipeidao.com/jzOpenClaw/getPrice4s) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JZ_API_KEY; the helper script prints JSON returned by the pricing API or an error object.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
