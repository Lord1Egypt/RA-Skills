## Description:

身份证实名认证。验证姓名与身份证号是否一致，支持全国居民身份证。使用场景：用户说"身份证认证"、"实名认证"、"验证身份证"、"姓名和身份证是否匹配"、"身份证二要素核验"等。通过聚合数据（juhe.cn）API 实时核验，免费注册每天免费调用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to verify whether a person's name and Chinese Resident Identity Card number match through Juhe's ID card verification API. It supports agent-guided setup, command execution, and concise presentation of verification results.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill processes legal names and national ID numbers.

Mitigation: Use it only with informed consent and avoid retaining identity data beyond the verification task.

Risk: The bundled script uses plaintext HTTP for the Juhe ID card query endpoint.

Mitigation: Change the script to use HTTPS before handling real identity data.

Risk: Sensitive values may be exposed in URLs or full JSON output.

Mitigation: Avoid putting credentials or identity data in URLs where possible and mask or suppress raw JSON output before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/juhemcp/skills/juhe-idcard-verify)
- [Juhe ID Card Verification API](https://www.juhe.cn/docs/api/id/103)
- [Juhe](https://www.juhe.cn)
- [Juhe ID Card Query Endpoint](http://op.juhe.cn/idcard/query)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with shell commands and formatted text or JSON verification results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JUHE_IDCARD_VERIFY_KEY; results should be masked before display.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
