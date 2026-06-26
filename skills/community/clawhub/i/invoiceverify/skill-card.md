## Description: <br>
按发票代码、号码、日期、金额等查验发票真伪与详情。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to verify Chinese invoice authenticity and retrieve invoice details from JisuAPI using invoice number, issue date, amount, code, check code, and related fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice details, which can include personal, tax, or sensitive business information, are sent to JisuAPI for verification. <br>
Mitigation: Use the skill only when authorized to share the relevant invoice information with JisuAPI and confirm before submitting sensitive invoice details. <br>
Risk: The skill requires a JisuAPI credential and may consume paid or quota-limited API calls. <br>
Mitigation: Use a dedicated API key and monitor quota, billing, and service permissions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jisuapi/invoiceverify) <br>
- [JisuAPI Invoice Verification API](https://www.jisuapi.com/api/invoiceverify/) <br>
- [JisuAPI](https://www.jisuapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON responses and concise agent summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; invoice verification calls send invoice details to JisuAPI.] <br>

## Skill Version(s): <br>
1.0.4 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
