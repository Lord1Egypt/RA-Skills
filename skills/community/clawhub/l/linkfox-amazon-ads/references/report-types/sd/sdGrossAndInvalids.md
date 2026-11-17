---
reportTypeId: sdGrossAndInvalids
adProduct: SPONSORED_DISPLAY
officialDocUrl: https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types/gross-and-invalids
timeUnit: [SUMMARY, DAILY]
groupBy: [campaign]
format: [GZIP_JSON, CSV]
filters:
  - name: campaignStatus
    values: [ENABLED, PAUSED, ARCHIVED]
    applicableWhenGroupBy: [campaign]
dateRange:
  maxSpanDays: 365
  dataRetentionDays: 365
---

# SD 总流量与无效流量（Gross and Invalid Traffic）

总流量与无效流量报表为 Sponsored Display 广告主提供广告系列流量性质的透明度。该报表包含所请求广告类型的全部广告系列，并在广告系列层面提供所请求日期内的总流量与无效流量指标。

> **注意**
> Sponsored Products、Sponsored Brands 与 Sponsored Display 对总流量与无效流量报表支持相同的列与配置。

## 配置

| 配置项 | 取值 |
|---|---|
| reportTypeId | sdGrossAndInvalids |
| 最大日期范围 | 365 天 |
| 数据保留期 | 365 天 |
| timeUnit | SUMMARY 或 DAILY |
| groupBy | campaign |
| format | GZIP_JSON 或 CSV |

## 基础指标

| 字段 |
|------|
| campaignName |
| campaignStatus |
| clicks |
| date |
| endDate |
| grossClickThroughs |
| grossImpressions |
| impressions |
| invalidClickThroughRate |
| invalidClickThroughs |
| invalidImpressionRate |
| invalidImpressions |
| startDate |

## 按 campaign 分组

**额外指标**：无

**过滤器**：
- campaignStatus（取值：ENABLED, PAUSED, ARCHIVED）

## 调用示例

### 总流量与无效流量汇总报表

```bash
curl --location 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxxxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxxx' \
--data '{
    "name": "SD Gross and Invalid Traffic",
    "startDate": "2025-03-05",
    "endDate": "2025-03-10",
    "configuration": {
        "adProduct": "SPONSORED_DISPLAY",
        "groupBy": ["campaign"],
        "columns": [
            "campaignName",
            "grossImpressions",
            "grossClickThroughs",
            "invalidClickThroughs",
            "invalidClickThroughRate",
            "startDate",
            "endDate"
        ],
        "reportTypeId": "sdGrossAndInvalids",
        "timeUnit": "SUMMARY",
        "format": "CSV"
    }
}'
```
