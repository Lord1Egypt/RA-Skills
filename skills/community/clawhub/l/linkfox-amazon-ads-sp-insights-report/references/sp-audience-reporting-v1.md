# Sponsored Products Audience（Reporting API v1）参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/amazonAds/developerProxy`
- **请求方式**：POST，`Content-Type: application/json`
- **认证方式**：Header `Authorization: <api_key>`；优先读取 `LINKFOX_AGENT_API_KEY`，回退 `LINKFOXAGENT_API_KEY`
- **User-Agent**：`LinkFox-Skill/2.0`
- **超时**：网关请求和报告分片下载均为 150s
- **默认生产网关**：`https://tool-gateway.linkfox.com`
- **Amazon 认证**：调用方只传 `profileId`；后端按 profile 选择 access token。参数中禁止出现 access token、refresh token 或 LWA 密钥
- **上游成熟度**：Amazon 官方当前把 Reporting API v1 标为 open beta；账号可能尚未开放，字段/限流可能调整，不应按 GA 稳定性承诺
- **生成时间**：异步报告通常约 2–10 分钟，偶尔可能更久；约 5 分钟仍未完成时脚本会提示继续等待

入口脚本：`python scripts/get_sp_audience_report.py '<JSON 参数>' [--inline] [--no-cache]`

## 请求参数

| 参数 | 类型 | 必填 | 默认 | 说明 |
|---|---|---:|---|---|
| `profileId` | integer/string | 是 | - | 正整数；来自 Ads 授权 Skill |
| `region` | string | 是 | - | `NA` / `EU` / `FE` |
| `startDate` | string | 创建模式是 | - | `YYYY-MM-DD` |
| `endDate` | string | 创建模式是 | - | `YYYY-MM-DD`；不得晚于今天 |
| `timeUnit` | string | 否 | `DAILY` | `DAILY` / `SUMMARY` |
| `detailLevel` | string | 否 | `ACCOUNT` | `ACCOUNT` / `CAMPAIGN` / `AD_GROUP` |
| `advertiserAccountId` | string | 否 | 自动映射 | Ads v1 account ID；仅用于映射失败后的显式恢复 |
| `pollInterval` | integer | 否 | `60` | 5–300 秒；官方建议每分钟一次 |
| `maxAttempts` | integer | 否 | `10` | 1–120 |
| `reportId` | string | 否 | - | 传入后跳过账户查询和创建，进入仅轮询模式 |

## 内部 Ads v1 调用链

三步均通过同一个 LinkFox `developerProxy` 转发；v1 请求不发送 `Amazon-Advertising-API-Scope`，`profileId` 只用于服务端选取授权记录/token。

### 1. 映射 advertiser account

`POST adsApi/v1/query/advertiserAccounts`

脚本先查询 global accounts，再用下面的 non-global filter 查询，并跟随 `nextToken`（包括返回空页但仍有 token 的情况）：

```json
{"isGlobalAccountFilter":{"include":[false]}}
```

从 `alternateIds` 中匹配当前 `profileId`，得到唯一 `advertiserAccountId`。若显式传入 `advertiserAccountId`，跳过本步。

### 2. 创建 SP Audience 报告

`POST adsApi/v1/create/reports`

```json
{
  "accessRequestedAccounts": [{"advertiserAccountId": "ACCOUNT_ID"}],
  "reports": [{
    "format": "CSV",
    "periods": [{"datePeriod": {"startDate": "2026-08-01", "endDate": "2026-08-07"}}],
    "query": {
      "fields": [
        "date.value", "advertiserAccount.id", "adProduct.value",
        "audienceSegment.id", "audienceSegment.name", "audienceSegment.type",
        "audienceSegment.classCode", "audienceSegment.source",
        "audienceSegmentCountry.code", "budgetCurrency.value",
        "metric.impressions", "metric.clicks",
        "metric.totalCost", "metric.purchases", "metric.sales", "metric.roas"
      ],
      "filter": {"on": {
        "field": "adProduct.value", "comparisonOperator": "EQUALS",
        "not": false, "values": ["SPONSORED_PRODUCTS"]
      }}
    }
  }]
}
```

`SUMMARY` 把 `date.value` 换成 `dateRange.value`。`CAMPAIGN` 增加 `campaign.id/name`；`AD_GROUP` 再增加 `adGroup.id/name`。`budgetCurrency.value` 是 `metric.totalCost` 与 `metric.sales` 的官方必需依赖，不能删除。

### 3. 轮询并下载

`POST adsApi/v1/retrieve/reports`

```json
{"reportIds":["REPORT_ID"]}
```

状态：`PENDING` / `PROCESSING` / `COMPLETED` / `FAILED`。完成响应中的 `completedReportParts[]` 可能包含多个 `url`；脚本下载全部分片，支持 plain CSV 和 gzip-compressed CSV。预签名 URL 不写入最终响应。

## developerProxy 请求示例

脚本对每一步构造：

```json
{
  "region": "NA",
  "path": "adsApi/v1/create/reports",
  "method": "POST",
  "profileId": 1234567890,
  "body": "{...Amazon JSON body...}",
  "contentType": "application/json"
}
```

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
  "preview": [{"audienceSegment.name":"In-market ...","metric.impressions":"1000"}],
  "pollAttempts": 2,
  "elapsedSeconds": 60.2
}
```

`success=true` 且 `totalRows=0` 是合法空报告，不应自动改变参数重试。

## 未完成响应

```json
{
  "success": false,
  "status": "STILL_PROCESSING",
  "reportId": "report-id",
  "resumeHint": {"params": {
    "profileId": 1234567890, "region": "NA", "reportId": "report-id",
    "pollInterval": 60, "maxAttempts": 20
  }},
  "_cacheable": false
}
```

`STILL_PROCESSING` 表示客户端等待窗口结束但 Amazon 仍在生成，并非报告失败。响应会明确给出 `message`、`resumeHint.mode=poll-only` 和续跑参数；继续时复用同一 `reportId`，不要重复创建。未完成和失败响应不写 24h cache。

## 错误处理

| 状态/错误 | 含义 | 建议 |
|---|---|---|
| 400 | 日期、字段组合或 body 非法 | 查看 `details.body`，修正一次后再调 |
| 401 | LinkFox key 或 Amazon token 失效 | LinkFox 401 走 onboarding；上游 401 刷新 Ads 授权 |
| 402 | LinkFox 余额/套餐问题 | 走 `references/onboarding.md` |
| 403 | Amazon Ads v1 权限不足 | 检查 Ads API 应用/授权账户权限 |
| 404 | reportId 不存在/不可访问 | 不自动重建；向用户说明 |
| 429 | 上游限流 | 尊重 Retry-After/降低轮询频率，不密集重试 |
| `FAILED` | Amazon 报告生成失败 | 透传失败详情 |

## 官方参考

- [Reporting API v1 overview](https://advertising.amazon.com/API/docs/en-us/guides/reporting/ads-v1/overview)
- [Reporting API v1 quickstart](https://advertising.amazon.com/API/docs/en-us/guides/reporting/ads-v1/quickstart)
- [Query advertiser accounts](https://advertising.amazon.com/API/docs/en-us/guides/account-management/query-advertiser-accounts)
- [Audience segment dimension](https://advertising.amazon.com/API/docs/en-us/guides/reporting/ads-v1/dimensions/audience/audience-segment)
- [Costs metrics: total cost](https://advertising.amazon.com/API/docs/en-us/guides/reporting/ads-v1/metrics/costs-and-fees/costs#total-cost)
- [Purchase metrics: sales and ROAS](https://advertising.amazon.com/API/docs/en-us/guides/reporting/ads-v1/metrics/amazon-retail-conversions/purchases#sales)

## Feedback API

此端点与工具网关不同：`POST https://skill-api.linkfox.com/api/v1/public/feedback`。

```json
{"skillName":"linkfox-amazon-ads-sp-insights-report","sentiment":"NEUTRAL","category":"SUGGESTION","content":"..."}
```
