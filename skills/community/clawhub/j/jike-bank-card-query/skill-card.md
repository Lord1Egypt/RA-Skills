## Description: <br>
输入银行卡号查询卡类型、卡名称、卡 BIN、发卡行、银行官网和客服电话，也支持按银行名称和类型查询银行列表。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up bank card issuer, card type, BIN, Luhn support, bank website, and customer service phone information, or to query supported banks by name and type. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends bank card numbers and an AppKey to an external jikeapi.cn service with under-disclosed controls. <br>
Mitigation: Install only when that service is trusted, prefer BIN-only or test values, and keep the API key low-privilege and rotatable. <br>
Risk: Full bank card numbers can be shown when users request unmasked output. <br>
Mitigation: Keep the default masked output and avoid exposing full card numbers unless the user explicitly requires it. <br>
Risk: Changing JIKE_API_BASE_URL can redirect sensitive queries to another destination. <br>
Mitigation: Do not set JIKE_API_BASE_URL unless the alternate API destination is intentional and trusted. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/jikeapi-cn/jike-bank-card-query) <br>
- [即刻数据 homepage](https://www.jikeapi.cn/) <br>
- [即刻数据 bank card query endpoint](https://api.jikeapi.cn/v1/bank/card/query) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Terminal text tables or JSON from Python CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bank card numbers are masked by default; --no-mask exposes full card numbers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
