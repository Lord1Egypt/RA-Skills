## Description:

银行卡类型及真伪查询；输入银行卡号可查询卡类型、卡名称、卡 BIN、发卡行、银行官网和客服电话，也支持查询银行列表。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to look up bank-card type, issuing bank, BIN, support phone, official website, and bank-list information through Jike Data. It is intended for explicit user-requested card or bank lookups, with masked card output by default.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles full payment-card numbers and sends lookup requests to an external API service.

Mitigation: Use the skill only with explicit user intent, prefer masked text output, and avoid submitting real card numbers unless the deployment has approved that data flow.

Risk: JSON output for card lookups can expose raw response fields and may be captured by downstream logs.

Mitigation: Avoid JSON output for card lookups unless logging, retention, and access controls are appropriate for payment-card-related data.

Risk: The API key and submitted card numbers may appear in service or proxy URL logs because requests include query parameters.

Mitigation: Keep API keys in controlled environment variables, rotate keys if logs are exposed, and route traffic only through trusted networks and services.

Risk: Changing JIKE_API_BASE_URL can redirect card numbers and API keys to a non-standard endpoint.

Mitigation: Leave JIKE_API_BASE_URL unset in normal use and set it only for trusted testing environments.

## Reference(s):

- [ClawHub skill release: jike-bank-card-query](https://clawhub.ai/jikeapi-cn/skills/jike-bank-card-query)
- [Publisher profile: jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)
- [Jike Data homepage](https://www.jikeapi.cn/)
- [Jike bank-card query API endpoint](https://api.jikeapi.cn/v1/bank/card/query)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Terminal text or JSON from Python CLI commands, with Markdown usage guidance in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Card numbers are masked in text output by default; JSON output may include raw service response fields.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
