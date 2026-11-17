## Description:

通过按次付费的 okdata API 查询微信搜一搜公开内容、公众号、小程序、推荐词和微信指数。

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要研究微信公开内容的用户和开发者，用关键词查找公众号文章、视频号内容和小程序，查看微信指数走势及搜索推荐词。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rated the skill benign with medium confidence, but scan coverage is incomplete because several references could not be resolved.

Mitigation: Review the skill and decide whether you trust the okdata.online service before installing or configuring its API key.

Risk: Calls that reach the data source are billed even when results are empty or the request fails upstream.

Mitigation: Estimate the number and cost of calls before using the skill, set a maximum price, and check billing details in the response.

## Reference(s):

- [okdata 微信 API 文档](https://okdata.online/zh/apis/wechat/)
- [okdata Remote MCP endpoint](https://api.okdata.online/mcp)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured API results with concise text summaries or guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public WeChat search and index data; API calls are billed per call.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
