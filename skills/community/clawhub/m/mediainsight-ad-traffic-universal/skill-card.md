## Description: <br>
查询广告投放流量分布与趋势的数据分析技能。支持按行业、地域、媒体（OTT/移动端）、目标受众等多维度分析广告曝光数据，适用于媒体策略评估、竞品投放监测、行业广告趋势研究等场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nonorongrong-design](https://clawhub.ai/user/nonorongrong-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Media planners, advertisers, and analysts use this skill to submit MediaInsight advertising traffic analysis tasks, resolve visible campaign dimensions, and download completed ZIP/CSV reports for exposure distribution and trend review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create real remote MediaInsight tasks and consume account credits. <br>
Mitigation: Run dry-run first, inspect the resolved payload and coin cost, and submit only after confirming the task matches the intended account and analysis scope. <br>
Risk: Session JSON files can contain reusable authentication cookies. <br>
Mitigation: Treat generated session files as sensitive, delete them after use, and avoid sharing them with reports or logs. <br>
Risk: A personal MediaInsight token expands account access and may switch tenant context. <br>
Mitigation: Use the minimum necessary token, avoid tenant switching unless intended, and keep MEDIAINSIGHT_MCP_TOKEN out of committed files. <br>
Risk: The public demo token has limited permissions and may be rate-limited or unavailable. <br>
Mitigation: Use it only for initial evaluation; use an owned token for production analysis or broader media and industry coverage. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nonorongrong-design/mediainsight-ad-traffic-universal) <br>
- [MediaInsight MCP Server](https://open-api-mediainsight.cn.miaozhen.com/mcp_server/mcp) <br>
- [MediaInsight API Endpoint](https://mediainsight.cn.miaozhen.com/api_v2) <br>
- [2024 Media Advertising Traffic Market Analysis Report](https://doc.weixin.qq.com/pdf/d3_AGwAzwarAPECNP0jI9V9pRkKJrYtL?scode=ANEAJwfLAAokGeAoaDAGwAzwarAPE) <br>
- [2025 Media Advertising Traffic Market Analysis Report](https://doc.weixin.qq.com/pdf/d3_AGwAzwarAPECNaOYYZMA6R0ymjf1M?scode=ANEAJwfLAAoF9heh5bAGwAzwarAPE) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Files, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands, JSON task responses, and downloadable ZIP/CSV report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.10+, network access to MediaInsight endpoints, and optionally MEDIAINSIGHT_MCP_TOKEN for broader or more stable analysis.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
