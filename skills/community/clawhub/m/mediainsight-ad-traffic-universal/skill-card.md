## Description:

查询广告投放流量分布与趋势的数据分析技能。支持按行业、地域、媒体（OTT/移动端）、目标受众等多维度分析广告曝光数据，适用于媒体策略评估、竞品投放监测、行业广告趋势研究等场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[nonorongrong-design](https://clawhub.ai/user/nonorongrong-design)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, media planners, and marketing teams use this skill to submit MediaInsight ad-traffic analysis tasks, resolve permitted industry/media/audience dimensions, estimate coin cost, and download completed report files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated remote actions can submit MediaInsight tasks and consume account credits.

Mitigation: Use --dry-run first and review the resolved payload and coin estimate before creating a task.

Risk: The shared demo token has limited permissions, may expire, and is not appropriate for sensitive or proprietary analysis.

Mitigation: Use a private MEDIAINSIGHT_MCP_TOKEN, --token, or --token-file for stable access and sensitive work.

Risk: Custom --mcp-url or --base-url values can receive credential-bearing requests.

Mitigation: Use the default endpoints unless the replacement endpoint is fully trusted.

Risk: Session cookies are persisted on disk.

Mitigation: Use a deliberate --session-file location when needed and delete generated session files after use.

Risk: Downloaded archives can be extracted with --extract-dir without strong resource limits.

Mitigation: Extract only expected reports into a dedicated directory and remove generated files after inspection.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nonorongrong-design/skills/mediainsight-ad-traffic-universal)
- [2024 annual media ad traffic market analysis report](https://doc.weixin.qq.com/pdf/d3_AGwAzwarAPECNP0jI9V9pRkKJrYtL?scode=ANEAJwfLAAokGeAoaDAGwAzwarAPE)
- [2025 annual media ad traffic market analysis report](https://doc.weixin.qq.com/pdf/d3_AGwAzwarAPECNaOYYZMA6R0ymjf1M?scode=ANEAJwfLAAoF9heh5bAGwAzwarAPE)
- [MediaInsight MCP server](https://open-api-mediainsight.cn.miaozhen.com/mcp_server/mcp)
- [MediaInsight API endpoint](https://mediainsight.cn.miaozhen.com/api_v2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with shell commands; scripts emit JSON status, resolved payloads, and downloaded ZIP/CSV report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report availability, visible dimensions, media expansion, and output files depend on the active MediaInsight token permissions.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
