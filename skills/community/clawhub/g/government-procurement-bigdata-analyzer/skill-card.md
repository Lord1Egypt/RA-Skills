## Description: <br>
政府采购招标大数据查询与分析助手，用于搜索政府、事业单位和央国企采购公告，分析中标、供应商、价格趋势和政采商机。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and business development teams use this skill to query and analyze Chinese government procurement, bidding, award, contract, supplier, competitor, and pricing data. It helps identify sales opportunities, monitor expiring projects, evaluate procurement trends, and profile government buyers or winning suppliers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically register a device, send host identifiers to the provider, and store an API key in ~/.zlbx/config.json. <br>
Mitigation: Review before installing; prefer supplying a manually created ZLBX_API_KEY unless the user explicitly accepts automatic registration and local key storage. <br>
Risk: Recharge or login links, returned contact data, and stored API keys may be sensitive. <br>
Mitigation: Treat generated links, contact results, and local credentials as sensitive, and avoid sharing them in public logs or transcripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhiliaobiaoxun/skills/government-procurement-bigdata-analyzer) <br>
- [API search reference](references/api-search.md) <br>
- [Company analysis API reference](references/api-company.md) <br>
- [Market analysis API reference](references/api-market.md) <br>
- [Automatic registration reference](references/auto-register.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown responses with JSON API request examples and analytical summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use the ZLBX_API_KEY environment variable or a local ~/.zlbx/config.json API key; automatic registration may create and store an API key when no key is configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
