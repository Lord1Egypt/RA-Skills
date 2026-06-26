## Description: <br>
股票多条件筛选、热门因子管理、Jiuyan 数据查询和抖音热点分析。提供 17 个 CLI 工具覆盖四大模块。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query a configured stock-data API for stock screening, search, detail lookup, comparisons, factor preset management, Jiuyan analysis, and Douyin hotspot data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends requests and credentials to the configured STOCK_API_BASE_URL. <br>
Mitigation: Use only a trusted backend URL and provide a scoped STOCK_API_KEY appropriate for the intended access. <br>
Risk: Factor preset create, update, delete, and sort tools mutate backend state. <br>
Mitigation: Confirm the requested mutation with the user before running those tools. <br>
Risk: The hot_factor_delete operation is documented as irreversible. <br>
Mitigation: Verify the exact preset ID before deletion and avoid broad or ambiguous delete requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shenghoo123-png/kay-stock-filter) <br>
- [README.md](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [JSON text returned by Node.js CLI tools] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, STOCK_API_BASE_URL, and typically STOCK_API_KEY; requests are sent to a configured /api/v1 backend.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
