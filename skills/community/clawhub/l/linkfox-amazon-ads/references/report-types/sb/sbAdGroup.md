---
reportTypeId: sbAdGroup
adProduct: SPONSORED_BRANDS
officialDocUrl: https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types/ad-group
timeUnit: [SUMMARY, DAILY]
groupBy: [adGroup]
format: [GZIP_JSON]
filters:
  - name: adStatus
    values: [ENABLED, PAUSED, ARCHIVED]
    applicableWhenGroupBy: [adGroup]
dateRange:
  maxSpanDays: 31
  dataRetentionDays: 60
---

# SB 广告组

广告组报告包含按广告组维度拆分的绩效数据。广告组报告涵盖所请求赞助广告类型中、在所请求日期内有绩效活动的所有广告活动。例如，Sponsored Brands 广告组报告会返回在所选日期内获得曝光的所有 Sponsored Brands 广告组的绩效数据。

> **注意**
> Sponsored Products 没有独立的广告组报告。可在广告活动报告中使用 adGroup groupBy 获取广告组级别数据。

> **注意**
> 本报告目前为预览版。预览期间，isMultiAdGroupsEnabled=False 的 Sponsored Brands 广告活动相关数据不可用。待 v3 报告支持所有 Sponsored Brands 广告活动后，我们将在发布说明中宣布正式可用。

## 配置

| 配置项 | 值 |
|---|---|
| reportTypeId | sbAdGroup |
| 最大日期范围 | 31 天 |
| 数据保留期 | 60 天 |
| timeUnit | SUMMARY 或 DAILY |
| groupBy | adGroup |
| format | GZIP_JSON |

## 基础指标

| 字段 |
|------|
| addToCart |
| addToCartClicks |
| addToCartRate |
| adGroupId |
| adGroupName |
| adStatus |
| addToList |
| addToListFromClicks |
| qualifiedBorrows |
| qualifiedBorrowsFromClicks |
| royaltyQualifiedBorrows |
| royaltyQualifiedBorrowsFromClicks |
| brandedSearches |
| brandedSearchesClicks |
| campaignBudgetAmount |
| campaignBudgetCurrencyCode |
| campaignBudgetType |
| campaignId |
| campaignName |
| campaignStatus |
| clicks |
| cost |
| costType |
| date |
| detailPageViews |
| detailPageViewsClicks |
| eCPAddToCart |
| endDate |
| impressions |
| kindleEditionNormalizedPagesRead14d |
| kindleEditionNormalizedPagesRoyalties14d |
| newToBrandDetailPageViewRate |
| newToBrandDetailPageViews |
| newToBrandDetailPageViewsClicks |
| newToBrandECPDetailPageView |
| newToBrandPurchases |
| newToBrandPurchasesClicks |
| newToBrandPurchasesPercentage |
| newToBrandPurchasesRate |
| newToBrandSales |
| newToBrandSalesClicks |
| newToBrandSalesPercentage |
| newToBrandUnitsSold |
| newToBrandUnitsSoldClicks |
| newToBrandUnitsSoldPercentage |
| purchases |
| purchasesClicks |
| purchasesPromoted |
| sales |
| salesClicks |
| salesPromoted |
| startDate |
| unitsSold |
| unitsSoldClicks |
| video5SecondViewRate |
| video5SecondViews |
| videoCompleteViews |
| videoFirstQuartileViews |
| videoMidpointViews |
| videoThirdQuartileViews |
| videoUnmutes |
| viewabilityRate |

## 按 adGroup 分组

**额外指标**: 无

**过滤条件**:
- adStatus（取值：ENABLED, PAUSED, ARCHIVED）

## 按 campaign 分组

**额外指标**: 无

## 调用示例

### 按广告组分组的广告组汇总报告

```bash
curl --location 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxxxxxx' \
--data '{
    "name": "SB ad group report 9/5-9/10",
    "startDate": "2023-09-05",
    "endDate": "2023-09-10",
    "configuration": {
        "adProduct": "SPONSORED_BRANDS",
        "groupBy": [
            "adGroup"
        ],
        "columns": [
            "impressions",
            "clicks",
            "cost",
            "campaignId",
            "adGroupId",
            "startDate",
            "endDate"
        ],
        "reportTypeId": "sbAdGroup",
        "timeUnit": "SUMMARY",
        "format": "GZIP_JSON"
    }
}'
```
