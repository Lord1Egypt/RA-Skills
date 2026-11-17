# Sponsored Products Search Term Impression Share（Reporting API v1）参考

## 调用规范

- **请求地址**：`${LINKFOX_TOOL_GATEWAY}/amazonAds/developerProxy`
- **请求方式**：POST，`Content-Type: application/json`
- **认证方式**：Header `Authorization: <api_key>`；优先读取 `LINKFOX_AGENT_API_KEY`，回退 `LINKFOXAGENT_API_KEY`
- **User-Agent**：`LinkFox-Skill/2.0`
- **超时**：网关请求和报告分片下载均为 150s
- **默认生产网关**：`https://tool-gateway.linkfox.com`
- **Amazon 认证**：只传 `profileId`；后端选择 token。参数中禁止出现 access/refresh token
- **上游成熟度**：Amazon 官方当前把 Reporting API v1 标为 open beta；账号可能尚未开放，字段/限流可能调整，不应按 GA 稳定性承诺
- **生成时间**：异步报告通常约 2–10 分钟，Search Impression Share 偶尔可能更久；约 5 分钟仍未完成时脚本会提示继续等待

入口脚本：`python scripts/get_sp_search_impression_share.py '<JSON 参数>' [--inline] [--no-cache]`

## 请求参数

| 参数 | 类型 | 必填 | 默认 | 说明 |
|---|---|---:|---|---|
| `profileId` | integer/string | 是 | - | 正整数；来自 Ads 授权 Skill |
| `region` | string | 是 | - | `NA` / `EU` / `FE` |
| `startDate` | string | 创建模式是 | - | `YYYY-MM-DD` |
| `endDate` | string | 创建模式是 | - | `YYYY-MM-DD`；不得晚于今天 |
| `timeUnit` | string | 否 | `DAILY` | `DAILY` / `SUMMARY` |
| `advertiserAccountId` | string | 否 | 自动映射 | Ads v1 account ID；仅用于映射失败后的显式恢复 |
| `pollInterval` | integer | 否 | `60` | 5–300 秒；官方建议每分钟一次 |
| `maxAttempts` | integer | 否 | `10` | 1–120 |
| `reportId` | string | 否 | - | 传入后跳过账户查询和创建，进入仅轮询模式 |

本报告入口不接受 campaign/adGroup/target/keyword 等自定义维度，因为它们与 impression share/rank 的官方字段兼容规则冲突。

## 内部 Ads v1 调用链

所有调用均经 `${LINKFOX_TOOL_GATEWAY}/amazonAds/developerProxy` 转发。Ads v1 不发送 `Amazon-Advertising-API-Scope`；`profileId` 只用于后端选取授权记录/token。

### 1. 映射 advertiser account

`POST adsApi/v1/query/advertiserAccounts`

依次查询 `{}` 和 `{"isGlobalAccountFilter":{"include":[false]}}`，跟随 `nextToken`，从 `alternateIds` 匹配当前 profile，得到唯一 `advertiserAccountId`。

### 2. 创建 SP Search Term Impression Share 报告

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
        "searchTerm.value", "metric.impressionShare", "metric.impressionShareRank"
      ],
      "filter": {"on": {
        "field": "adProduct.value", "comparisonOperator": "EQUALS",
        "not": false, "values": ["SPONSORED_PRODUCTS"]
      }}
    }
  }]
}
```

`SUMMARY` 把 `date.value` 换成 `dateRange.value`。三个非时间维度是 impression share/rank 的官方必需字段，不能删；也不能追加 campaign/ad group/target。

### 3. 轮询并下载

`POST adsApi/v1/retrieve/reports`

```json
{"reportIds":["REPORT_ID"]}
```

按官方建议最多每分钟轮询。`COMPLETED` 后下载全部 `completedReportParts[].url`，支持 plain CSV 和 gzip-compressed CSV；预签名 URL 不输出。

## developerProxy 请求示例

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
  "reportKind": "search-impression-share",
  "profileId": 1234567890,
  "advertiserAccountId": "account-id",
  "totalRows": 2,
  "dataFiles": [{"part":1,"path":"C:/.../part-01.csv","rowCount":2}],
  "preview": [{
    "searchTerm.value":"wireless charger",
    "metric.impressionShare":"0.34",
    "metric.impressionShareRank":"3"
  }]
}
```

`success=true` 且 `totalRows=0` 是合法空报告，不应自动扩大日期或更换账号重试。

## 未完成响应

`status=STILL_PROCESSING` 表示客户端等待窗口结束但 Amazon 仍在生成，并非失败。响应包含 `message`、`reportId`、`resumeHint.mode=poll-only` 和 `resumeHint.params`。向用户确认后用这些参数与 `--no-cache` 继续轮询同一报告，不要创建新报告。未完成和失败响应不缓存。

## 错误处理

| 状态/错误 | 含义 | 建议 |
|---|---|---|
| 400 | 日期或字段组合非法 | 查看 `details.body`，不添加不兼容维度 |
| 401 | LinkFox key 或 Amazon token 失效 | LinkFox 401 走 onboarding；上游 401 刷新 Ads 授权 |
| 402 | LinkFox 余额/套餐问题 | 走 `references/onboarding.md` |
| 403 | Amazon Ads v1 权限不足 | 检查 Ads API 应用/授权账户权限 |
| 404 | reportId 不存在/不可访问 | 不自动重建 |
| 429 | 上游限流 | 降低轮询频率，不密集重试 |
| `FAILED` | Amazon 报告生成失败 | 透传失败详情 |

## 官方参考

- [Reporting API v1 overview](https://advertising.amazon.com/API/docs/en-us/guides/reporting/ads-v1/overview)
- [Reporting API v1 quickstart](https://advertising.amazon.com/API/docs/en-us/guides/reporting/ads-v1/quickstart)
- [Query advertiser accounts](https://advertising.amazon.com/API/docs/en-us/guides/account-management/query-advertiser-accounts)
- [Search term dimension](https://advertising.amazon.com/API/docs/en-us/guides/reporting/ads-v1/dimensions/targeting/search-term)
- [Search impression share metrics](https://advertising.amazon.com/API/docs/en-us/guides/reporting/ads-v1/metrics/impression-share/search)

## Feedback API

此端点与工具网关不同：`POST https://skill-api.linkfox.com/api/v1/public/feedback`。

```json
{"skillName":"linkfox-amazon-ads-sp-insights-report","sentiment":"NEUTRAL","category":"SUGGESTION","content":"..."}
```
