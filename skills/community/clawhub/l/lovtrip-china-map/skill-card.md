## Description:

高德地图助手 / Amap Map Tools for China — 地理编码、周边搜索、路线规划、地图链接生成。当用户需要中国大陆范围的地理编码、地点搜索、路线规划时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lizhijun](https://clawhub.ai/user/lizhijun)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent geocode Chinese addresses, reverse-geocode coordinates, search nearby POIs, plan routes, retrieve venue details, and generate map or navigation links for mainland China travel workflows.

### Deployment Geography for Use:

Mainland China

## Known Risks and Mitigations:

Risk: The install path can execute unpinned package code through automatic npx usage.

Mitigation: Pin the LovTrip npm package to a reviewed exact version and avoid automatic npx -y execution where possible.

Risk: The fallback amap.sh script should not be used with untrusted addresses or keywords until its Python argument handling is fixed.

Mitigation: Prefer the reviewed MCP server path, or restrict fallback script inputs to trusted values until the argument handling is corrected.

Risk: Precise location data and map queries may be sent to external map services.

Mitigation: Run the MCP server with minimal filesystem and environment access and avoid sending sensitive location data unless approved.

## Reference(s):

- [LovTrip China Map skill page](https://clawhub.ai/lizhijun/skills/lovtrip-china-map)
- [LovTrip](https://lovtrip.app)
- [LovTrip developer documentation](https://lovtrip.app/developer)
- [LovTrip planner](https://lovtrip.app/planner)
- [Amap REST API base endpoint](https://restapi.amap.com/v3)
- [Amap tool parameter reference](reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON-formatted tool results with map and navigation links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AMAP_API_KEY for live Amap requests; generated links may target Amap, Tencent, Baidu, and Apple Maps.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
