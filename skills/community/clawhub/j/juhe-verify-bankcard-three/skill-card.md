## Description:

银行卡三要素核验。验证银行卡号、姓名、身份证号三要素是否一致。使用场景：用户说"验证银行卡"、"核验银行卡三要素"、"银行卡实名认证"、"检查银行卡号和身份证是否匹配"、"银行卡三元素检测"等。通过聚合数据（juhe.cn）API实时核验，支持单次查询和批量核验。

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check whether a bank card number, legal name, and Chinese ID number match for real-name authentication or risk-control workflows. It supports single checks and batch verification through a Python script backed by the Juhe API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes sensitive bank card, legal name, and ID number data through an external Juhe verification API.

Mitigation: Use only with explicit user consent, minimize retained data, and show masked identifiers in responses.

Risk: The artifact uses an HTTP API endpoint for verification traffic.

Mitigation: Do not use real personal or financial data unless the endpoint is changed to HTTPS or the transport security is otherwise verified.

Risk: API keys can be exposed when passed on the command line or stored in a repository-local .env file.

Mitigation: Prefer environment or secret-manager injection and keep credentials out of command histories and repositories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juhemcp/skills/juhe-verify-bankcard-three)
- [Juhe bank card three-element verification API](https://www.juhe.cn/docs/api/id/207)
- [Juhe data service platform](https://www.juhe.cn)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and masked JSON verification results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and JUHE_BANKCARD3_KEY; handles sensitive bank card, legal name, and ID number inputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
