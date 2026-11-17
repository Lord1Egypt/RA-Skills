---
reportTypeId: sbCampaigns
adProduct: SPONSORED_BRANDS
officialDocUrl: https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types/campaign
timeUnit: [SUMMARY, DAILY]
groupBy: [campaign]
format: [GZIP_JSON]
filters:
  - name: campaignStatus
    values: [ENABLED, PAUSED, ARCHIVED]
    applicableWhenGroupBy: [campaign]
dateRange:
  maxSpanDays: 31
  dataRetentionDays: 60
---

# SB 广告活动

广告活动报告包含按广告活动维度拆分的绩效数据。广告活动报告涵盖所请求赞助广告类型中、在所请求日期内有绩效活动的所有广告活动。例如，Sponsored Products 广告活动报告会返回在所选日期内获得曝光的所有 Sponsored Products 广告活动的绩效数据。广告活动报告还可按广告组和投放位置分组，以获取更细粒度的数据。

> **注意**
> 只能使用被报告配置中所有 groupBy 值共同支持的过滤器。对于广告活动报告，这意味着仅当包含单个 groupBy 值时才支持过滤器。

> **注意**
> 本报告目前为预览版。预览期间，isMultiAdGroupsEnabled=False 的 Sponsored Brands 广告活动相关数据不可用。待 v3 报告支持所有 Sponsored Brands 广告活动后，我们将在发布说明中宣布正式可用。

## 配置

| 配置项 | 值 |
|---|---|
| reportTypeId | sbCampaigns |
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
| brandStorePageView |
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
| topOfSearchImpressionShare |
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

## 按 campaign 分组

**额外指标**: campaignBudgetAmount, campaignBudgetCurrencyCode, campaignBudgetType, longTermSales, longTermROAS, topOfSearchImpressionShare

**过滤条件**:
- campaignStatus（取值：ENABLED, PAUSED, ARCHIVED）

## 调用示例

### 按广告活动分组的广告活动汇总报告

```bash
curl --location 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxxxxx' \
--data '{
    "name": "SB campaigns report 9/5-9/10",
    "startDate": "2023-09-05",
    "endDate": "2023-09-10",
    "configuration": {
        "adProduct": "SPONSORED_BRANDS",
        "groupBy": [
            "campaign"
        ],
        "columns": [
            "impressions",
            "clicks",
            "cost",
            "campaignId",
            "startDate",
            "endDate"
        ],
        "reportTypeId": "sbCampaigns",
        "timeUnit": "SUMMARY",
        "format": "GZIP_JSON"
    }
}'
```
