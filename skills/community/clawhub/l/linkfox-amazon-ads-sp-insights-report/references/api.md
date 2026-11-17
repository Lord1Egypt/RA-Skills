# Amazon Ads SP 洞察报告 API 参考

本 Skill 统一封装 Sponsored Products Audience 与 Search Term Impression Share/Rank 两类 Reporting API v1 beta 报告。

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/amazonAds/developerProxy`
- **请求方式**：POST JSON
- **认证方式**：Header `Authorization: <api_key>`；优先读取 `LINKFOX_AGENT_API_KEY`，回退 `LINKFOXAGENT_API_KEY`
- **请求头**：`Content-Type: application/json`、`User-Agent: LinkFox-Skill/2.0`，透传 `SESSION_ID` / `MODE_ID` / `APP_NAME`
- **超时**：网关请求和报告分片下载均为 150 秒
- **默认网关**：`https://tool-gateway.linkfox.com`
- **Amazon Token**：调用方只传 `profileId`；后端选择并刷新 Token。禁止在参数中传入任何 Amazon 凭证
- **成熟度**：Reporting API v1 当前为 Amazon open beta
- **生成时间**：异步报告通常约 2–10 分钟，偶尔可能更久；脚本约 5 分钟输出一次进度提示，达到客户端等待窗口不等于报告失败

## 入口与参数

| 报告 | 入口 | 专用参考 |
|---|---|---|
| Sponsored Products Audience | `scripts/get_sp_audience_report.py` | `sp-audience-reporting-v1.md` |
| Sponsored Products Search Term Impression Share/Rank | `scripts/get_sp_search_impression_share.py` | `sp-search-impression-share-v1.md` |

共同参数：`profileId`、`region`、`startDate`、`endDate`、`timeUnit`、`advertiserAccountId`、`pollInterval`、`maxAttempts`、`reportId`。Audience 额外接受 `detailLevel`；Search Impression Share 不接受自定义维度或字段。

## 内部调用链

三个路径都通过同一 LinkFox `developerProxy` 转发：

1. `POST adsApi/v1/query/advertiserAccounts`：把 `profileId` 映射到唯一 `advertiserAccountId`。
2. `POST adsApi/v1/create/reports`：创建固定官方字段组合的 CSV 报告。
3. `POST adsApi/v1/retrieve/reports`：按 `reportId` 查询状态；完成后下载全部 `completedReportParts[]`。

Ads v1 请求不发送 `Amazon-Advertising-API-Scope`；`profileId` 仅供后端选择当前用户已授权的 Token。

## developerProxy 请求示例

```bash
curl -X POST "${LINKFOX_TOOL_GATEWAY}/amazonAds/developerProxy" \
  -H "Authorization: ${LINKFOX_AGENT_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "User-Agent: LinkFox-Skill/2.0" \
  -d '{
    "region":"NA",
    "path":"adsApi/v1/retrieve/reports",
    "method":"POST",
    "profileId":1234567890,
    "body":"{\"reportIds\":[\"REPORT_ID\"]}",
    "contentType":"application/json"
  }'
```

业务调用应优先执行入口脚本，不要手工拼装三个阶段。

## 成功响应

```json
{
  "success": true,
  "status": "COMPLETED",
  "reportId": "report-id",
  "reportKind": "audience",
  "profileId": 1234567890,
  "advertiserAccountId": "account-id",
  "totalRows": 42,
  "dataFiles": [{"part":1,"path":"C:/.../part-01.csv","rowCount":42}],
  "preview": [{"audienceSegment.name":"In-market ..."}],
  "pollAttempts": 2,
  "elapsedSeconds": 60.2
}
```

`reportKind` 为 `audience` 或 `search-impression-share`。`success=true` 且 `totalRows=0` 是合法空报告。

## 未完成与缓存

轮询窗口耗尽返回 `status=STILL_PROCESSING`、`message`、`reportId`、`resumeHint.mode=poll-only`、`resumeHint.params` 和 `_cacheable=false`。这表示 Amazon 仍在生成而不是报告失败；继续时必须复用同一 `reportId`，不要创建重复报告。失败和未完成结果不缓存；成功结果缓存 24 小时，并校验 `dataFiles[].path` 仍存在。缓存按 `SESSION_ID`、报告类型和参数隔离；`--no-cache` 强制刷新。

## 错误

| 状态/错误 | 含义 | 处理 |
|---|---|---|
| 400 | 日期、字段组合或请求体非法 | 查看 `details`，修正一次后再调 |
| 401 | LinkFox Key 或 Amazon Token 失效 | LinkFox 401 走 onboarding；Amazon 401 刷新 Ads 授权 |
| 402 | LinkFox 套餐或余额问题 | 走 `references/onboarding.md` |
| 403 | v1 权限未开放 | 检查 Amazon Ads 应用和授权账号权限 |
| 404 | reportId 不存在或不可访问 | 不自动重建 |
| 429 | Amazon 限流 | 降低轮询频率，不密集重试 |
| `FAILED` | 报告生成失败 | 透传失败详情 |
| exit 42 | Ads Auth Skill 未安装 | 安装 `linkfox-amazon-ads-auth` |

## Feedback API

`POST https://skill-api.linkfox.com/api/v1/public/feedback`

```json
{"skillName":"linkfox-amazon-ads-sp-insights-report","sentiment":"NEUTRAL","category":"SUGGESTION","content":"..."}
```
