## Description:

全球汇率查询与货币换算。根据货币代码查询实时汇率、换算金额。使用场景：用户说"查一下汇率"、"美元兑人民币"、"100美元等于多少人民币"、"USD兑换CNY"、"汇率多少"等。通过聚合数据（juhe.cn）API 实时查询，支持 120+ 种货币，数据仅供参考。

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to look up live exchange rates, convert amounts between currency codes, and list supported currencies through the Juhe exchange-rate API. Results are for reference and should not be treated as bank execution prices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required Juhe API key can be exposed through command-line arguments or local .env files.

Mitigation: Prefer the JUHE_EXCHANGE_KEY environment variable, use a low-privilege key, avoid --key on shared systems, and keep scripts/.env out of source control.

Risk: The artifact calls Juhe exchange endpoints over HTTP, which may expose API-key and query data in transit if secure transport is unavailable.

Mitigation: Confirm provider support for HTTPS or update the endpoints to secure transport before installing in sensitive environments.

Risk: Exchange-rate output is reference data and may differ from bank execution prices.

Mitigation: Use the result as informational guidance and verify transaction prices with the relevant financial institution before acting.

## Reference(s):

- [Juhe Exchange Rate API Documentation](https://www.juhe.cn/docs/api/id/80)
- [Juhe Data Platform](https://www.juhe.cn)
- [ClawHub Skill Page](https://clawhub.ai/juhemcp/skills/juhe-exchange-rate)
- [ClawHub Publisher Profile](https://clawhub.ai/user/juhemcp)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a JUHE_EXCHANGE_KEY credential; script output includes exchange-rate data, update time, errors, and optional converted amount.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
