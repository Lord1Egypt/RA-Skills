---
reportTypeId: sbGrossAndInvalids
adProduct: SPONSORED_BRANDS
officialDocUrl: https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types/gross-and-invalid-traffic
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

# SB 毛量与无效流量

毛量与无效流量报告向 Sponsored Products、Sponsored Brands 和 Sponsored Display 广告主提供其广告活动流量性质的透明度。本报告涵盖所请求广告类型的所有广告活动，并提供所请求日期内广告活动级别的毛量与无效流量指标。例如，Sponsored Products 毛量与无效流量报告会返回在所选日期内获得曝光的所有 Sponsored Products 广告活动的毛量与无效流量指标。

## 配置

| 配置项 | 值 |
|---|---|
| reportTypeId | sbGrossAndInvalids |
| 最大日期范围 | 365 天 |
| 数据保留期 | 365 天 |
| timeUnit | SUMMARY 或 DAILY |
| groupBy | campaign |
| format | GZIP_JSON 或 CSV |

> Sponsored Products、Sponsored Brands 和 Sponsored Display 对毛量与无效流量报告支持相同的列与配置。

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

**额外指标**: 无

**过滤条件**:
- campaignStatus（取值：ENABLED, PAUSED, ARCHIVED）
