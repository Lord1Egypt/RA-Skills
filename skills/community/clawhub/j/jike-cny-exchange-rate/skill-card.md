## Description: <br>
人民币汇率查询，支持外汇牌价币种列表、人民币外汇牌价查询和汇率转换，数据由即刻数据（jikeapi.cn）开放接口提供。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and end users use this skill to list supported foreign currencies, query RMB exchange-rate quotes, and convert amounts between currencies through the Jike API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Currency lookup requests and the Jike API key are sent to jikeapi.cn. <br>
Mitigation: Install only if that data sharing is acceptable, and use a scoped API key where available. <br>
Risk: Supplying the API key on the command line can expose it through shell history or process listings. <br>
Mitigation: Prefer the JIKE_CNY_EXCHANGE_RATE_KEY or JIKE_APPKEY environment variable instead of the --key argument. <br>
Risk: Changing JIKE_API_BASE_URL redirects requests and credentials to another host. <br>
Mitigation: Set JIKE_API_BASE_URL only to hosts the operator explicitly trusts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/jike-cny-exchange-rate) <br>
- [Publisher profile](https://clawhub.ai/user/jikeapi-cn) <br>
- [Jike API homepage](https://www.jikeapi.cn/) <br>
- [CNY exchange-rate query endpoint](https://api.jikeapi.cn/v1/cny_exchange_rate/query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text or JSON from a Python command-line script, with Markdown usage guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a JIKE_CNY_EXCHANGE_RATE_KEY or JIKE_APPKEY credential.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
