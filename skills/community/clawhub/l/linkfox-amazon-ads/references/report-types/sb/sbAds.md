---
reportTypeId: sbAds
adProduct: SPONSORED_BRANDS
officialDocUrl: https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types/ad
timeUnit: [SUMMARY, DAILY]
groupBy: [ads]
format: [GZIP_JSON]
filters:
  - name: adStatus
    values: [ENABLED, PAUSED, ARCHIVED]
    applicableWhenGroupBy: [ads]
dateRange:
  maxSpanDays: 31
  dataRetentionDays: 60
---

# SB 广告

被推广商品报告包含按广告维度拆分的广告活动绩效数据。

> **注意**
> 本报告目前为预览版。预览期间，isMultiAdGroupsEnabled 设为 FALSE 的 Sponsored Brands 广告活动相关数据不可用。待 v3 报告支持所有 Sponsored Brands 广告活动后，我们将在发布说明中宣布正式可用。

## 配置

| 配置项 | 值 |
|---|---|
| reportTypeId | sbAds |
| 最大日期范围 | 31 天 |
| 数据保留期 | 60 天 |
| timeUnit | SUMMARY 或 DAILY |
| groupBy | ads |
| format | GZIP_JSON |

## 基础指标

| 字段 |
|------|
| addToCart |
| addToCartClicks |
| addToCartRate |
| addToList |
| qualifiedBorrows |
| royaltyQualifiedBorrows |
| addToListFromClicks |
| qualifiedBorrowsFromClicks |
| royaltyQualifiedBorrowsFromClicks |
| adGroupId |
| adGroupName |
| adId |
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
| viewableImpressions |

## 按 ads 分组

**额外指标**: 无

**过滤条件**:
- adStatus（取值：ENABLED, PAUSED, ARCHIVED）

## 调用示例

```bash
curl --location 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxxxxxx' \
--data '{
    "name":"SB advertised product report 9/5-9/10",
    "startDate":"2023-09-05",
    "endDate":"2023-09-10",
    "configuration":{
        "adProduct":"SPONSORED_BRANDS",
        "groupBy":["ads"],
        "columns":["impressions","clicks","cost","campaignId","adId","adGroupId"],
        "reportTypeId":"sbAds",
        "timeUnit":"SUMMARY",
        "format":"GZIP_JSON"
    }
}'
```
