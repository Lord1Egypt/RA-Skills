## Description:

股票多条件筛选、热门因子管理、Jiuyan 数据查询和抖音热点分析。提供 17 个 CLI 工具覆盖四大模块。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent query stock filters, stock details, comparison data, hot-factor presets, Jiuyan stock analysis, and Douyin hotspot data through a configured stock API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends requests and an API key to the configured stock API endpoint.

Mitigation: Install only for trusted stock API endpoints, use HTTPS for remote servers, and scope STOCK_API_KEY to the minimum permissions needed.

Risk: Preset update, delete, use, and sort tools can change server-side hot-factor preset data.

Mitigation: Review preset-changing requests before execution and avoid giving the agent API keys with preset write permissions unless those actions are intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shenghoo123-png/skills/kay-stock-filter)
- [Publisher profile](https://clawhub.ai/user/shenghoo123-png)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON returned by CLI tools, with setup and invocation guidance in Markdown documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, STOCK_API_BASE_URL, and STOCK_API_KEY; optional STOCK_API_TIMEOUT controls request timeout.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
