---
reportTypeId: sbCampaignPlacement
adProduct: SPONSORED_BRANDS
officialDocUrl: https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types/placement
timeUnit: [SUMMARY, DAILY]
groupBy: [campaign]
format: [GZIP_JSON]
filters: []
dateRange:
  maxSpanDays: 31
  dataRetentionDays: 60
---

# SB 广告活动投放位置

投放位置报告包含按广告投放位置维度拆分的绩效数据。

> **注意**
> Sponsored Products 没有独立的投放位置报告。可在广告活动报告中使用 campaignPlacement groupBy 获取投放位置级别数据。

> **注意**
> 本报告目前为预览版。预览期间，isMultiAdGroupsEnabled 设为 FALSE 的 Sponsored Brands 广告活动相关数据不可用。待 v3 报告支持所有 Sponsored Brands 广告活动后，我们将在发布说明中宣布正式可用。

## 配置

| 配置项 | 值 |
|---|---|
| reportTypeId | sbCampaignPlacement |
| 最大日期范围 | 31 天 |
| 数据保留期 | 60 天 |
| timeUnit | SUMMARY 或 DAILY |
| groupBy | campaign |
| format | GZIP_JSON |

## 基础指标

| 字段 |
|------|
| addToCart |
| addToCartClicks |
| addToCartRate |
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
| viewableImpressions |
| viewClickThroughRate |

## 按 campaignPlacement 分组

**额外指标**: placementClassification

## 按 campaign 分组

**额外指标**: 无

## 调用示例

### 广告活动投放位置汇总报告

```bash
curl --location 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxxx' \
--data '{
    "name": "SB placement report 9/5-9/10",
    "startDate": "2023-09-05",
    "endDate": "2023-09-10",
    "configuration": {
        "adProduct": "SPONSORED_BRANDS",
        "groupBy": [
            "campaignPlacement"
        ],
        "columns": [
            "impressions",
            "clicks",
            "cost",
            "campaignId",
            "placementClassification",
            "startDate",
            "endDate"
        ],
        "reportTypeId": "sbCampaignPlacement",
        "timeUnit": "SUMMARY",
        "format": "GZIP_JSON"
    }
}'
```
