## Description: <br>
发票查重技能。录入发票进行查重、查询查重记录。适用于验证发票是否重复录入的场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zxt](https://clawhub.ai/user/zxt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance, accounting, and invoice-processing users use this skill to submit invoice numbers and dates for duplicate-entry checks and to retrieve prior duplicate-check records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice metadata is sent to the named external service for duplicate-check processing. <br>
Mitigation: Confirm organizational approval for third-party invoice-data processing before use. <br>
Risk: The skill requires an API key and the evidence flags credential-handling concerns. <br>
Mitigation: Do not paste API keys into chat; use a dedicated secret store or a short-lived local environment variable such as ZXT_API_KEY. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zxt/invoice-dedup) <br>
- [Publisher profile](https://clawhub.ai/user/zxt) <br>
- [中兴通简税Skill平台](https://skill.quandianfapiao.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown/text responses with shell command examples and formatted invoice duplicate-check results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZXT_API_KEY and sends invoice metadata to https://skill.quandianfapiao.com.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
