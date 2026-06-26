## Description: <br>
通过聚合数据（juhe.cn）API 核验银行卡号、姓名和身份证号三要素是否一致，并返回面向用户的核验结果。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juhemcp](https://clawhub.ai/user/juhemcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill for bank-card real-name verification and risk-control checks after collecting a bank-card number, legal name, ID number, and Juhe API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive bank-card, legal-name, ID-card, and API-key data may be sent to Juhe over an unencrypted HTTP endpoint. <br>
Mitigation: Use only test data or change the provider call to HTTPS before handling real customer data, and obtain explicit user approval before sending personal information to Juhe. <br>
Risk: The Juhe API key can be exposed if passed directly on the command line. <br>
Mitigation: Prefer JUHE_BANKCARD3_KEY from an environment variable or managed secret, and avoid command-line key arguments. <br>
Risk: Verification requests involve sensitive personal information that can be overexposed in agent responses. <br>
Mitigation: Return only the minimum result needed, mask bank-card and ID-card values, and remind users to handle the data securely. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/juhemcp/juhe-verify-bankcard-three) <br>
- [Juhe bank-card three-element verification API](https://www.juhe.cn/docs/api/id/207) <br>
- [Juhe data service platform](https://www.juhe.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON verification results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JUHE_BANKCARD3_KEY; verification output should mask bank-card and ID-card values.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
