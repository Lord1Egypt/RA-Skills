## Description: <br>
三网手机实名认证。验证手机号、姓名、身份证三要素是否一致，支持移动、联通、电信三网。使用场景：用户说"实名认证"、"手机号实名验证"、"验证三要素"、"手机号和姓名是否匹配"、"身份证和手机号一致性"等。通过聚合数据（juhe.cn）API 实时核验，免费注册每天免费调用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juhemcp](https://clawhub.ai/user/juhemcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to verify whether a mobile number, real name, and Chinese ID card number match across China Mobile, China Unicom, and China Telecom using Juhe's API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles highly sensitive identity data and sends submitted details to Juhe for verification. <br>
Mitigation: Use it only with a legitimate need and user consent, and send only the minimum required identity details. <br>
Risk: API keys or identity details can be exposed through GET URLs, command-line arguments, logs, or raw JSON output. <br>
Mitigation: Prefer the script's POST flow, store the API key in JUHE_TELECOM_KEY, avoid command-line secrets, and redact or remove raw JSON before sharing or logging results. <br>


## Reference(s): <br>
- [Juhe Telecom Verification API Documentation](https://www.juhe.cn/docs/api/id/208) <br>
- [Juhe](https://www.juhe.cn) <br>
- [ClawHub skill page](https://clawhub.ai/juhemcp/juhe-telecom-verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and JSON result summaries with shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JUHE_TELECOM_KEY; formatted results mask mobile number, name, and ID card values.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
