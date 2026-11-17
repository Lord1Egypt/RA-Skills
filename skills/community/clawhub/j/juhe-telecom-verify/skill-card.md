## Description:

三网手机实名认证。验证手机号、姓名、身份证三要素是否一致，支持移动、联通、电信三网。使用场景：用户说"实名认证"、"手机号实名验证"、"验证三要素"、"手机号和姓名是否匹配"、"身份证和手机号一致性"等。通过聚合数据（juhe.cn）API 实时核验，免费注册每天免费调用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to verify whether a Chinese mobile number, real name, and identity card number match across China Mobile, China Unicom, and China Telecom through Juhe Data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles highly sensitive identity data and sends names, mobile numbers, and identity card values to Juhe for verification.

Mitigation: Use only when the user explicitly requests Juhe telecom real-name verification and warn that identity data will be sent to Juhe.

Risk: API keys or identity values can be exposed through command-line history, process listings, or logs.

Mitigation: Prefer the JUHE_TELECOM_KEY environment variable or a protected .env file, avoid passing secrets or identity data on the command line, and do not run where stdout is logged unless raw JSON output is removed or sanitized.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juhemcp/skills/juhe-telecom-verify)
- [Juhe telecom real-name verification API](https://www.juhe.cn/docs/api/id/208)
- [Juhe Data](https://www.juhe.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and masked verification results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API response fields and masked personal identifiers.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
