## Description: <br>
全国采购与招标信息查询与分析助手，帮助用户检索招标、中标、采购意向和合同公告，并分析企业画像、竞争对手、采购单位、中标单位、品牌、价格趋势和市场机会。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Procurement, sales, bidding, and market analysts use this skill to search nationwide Chinese procurement and bidding notices, review company participation, identify competitors or potential suppliers, and analyze pricing and market trends. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Automatic registration can send local device and user identifiers to a remote service. <br>
Mitigation: Prefer a manually supplied ZLBX_API_KEY; enable automatic registration only after explicit user consent and data-minimization review. <br>
Risk: The skill may store an API key in ~/.zlbx/config.json. <br>
Mitigation: Restrict local file access, avoid shared machines, and rotate or remove the key when it is no longer needed. <br>
Risk: Quota exhaustion can produce login or recharge links tied to the service account. <br>
Mitigation: Verify the zhiliaobiaoxun domain and user intent before following payment, recharge, or auto-login links. <br>
Risk: Procurement contacts and company relationship data may include sensitive business or personal information. <br>
Mitigation: Use retrieved data only for authorized procurement analysis and follow applicable privacy and data-handling obligations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhiliaobiaoxun/skills/national-procurement-bidding-net-chinabidding) <br>
- [标讯搜索类工具 API 详情](references/api-search.md) <br>
- [企业分析类工具 API 详情](references/api-company.md) <br>
- [市场分析类工具 API 详情](references/api-market.md) <br>
- [SKILL 自动注册详细流程](references/auto-register.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON API request examples and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call zhiliaobiaoxun APIs, store an API key in ~/.zlbx/config.json, and generate login or recharge links when automatic registration is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
