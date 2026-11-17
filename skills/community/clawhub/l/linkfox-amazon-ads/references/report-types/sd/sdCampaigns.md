---
reportTypeId: sdCampaigns
adProduct: SPONSORED_DISPLAY
officialDocUrl: https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types/campaign
timeUnit: [SUMMARY, DAILY]
groupBy: [campaign, matchedTarget]
format: [GZIP_JSON]
filters: []
dateRange:
  maxSpanDays: 31
  dataRetentionDays: 65
---

# SD 广告系列（Campaigns）

广告系列报表包含按广告系列维度拆分的绩效数据。广告系列报表包含所请求的赞助广告类型中，在所请求日期内有绩效活动的全部广告系列。对于 Sponsored Display，广告系列报表还可按 `matchedTarget` 分组以获取更细粒度的数据。

> **注意**
> 只能使用报表配置中所有 groupBy 值都支持的过滤器。对于广告系列报表，过滤器仅在仅包含单个 groupBy 值时才被支持。

## 配置

| 配置项 | 取值 |
|---|---|
| reportTypeId | sdCampaigns |
| 最大日期范围 | 31 天 |
| 数据保留期 | 65 天 |
| timeUnit | SUMMARY 或 DAILY |
| groupBy | campaign 或 matchedTarget |
| format | GZIP_JSON |

## 基础指标

| 字段 |
|------|
| addToCart |
| addToCartClicks |
| addToCartRate |
| addToCartViews |
| addToList |
| addToListFromClicks |
| addToListFromViews |
| qualifiedBorrows |
| qualifiedBorrowsFromClicks |
| qualifiedBorrowsFromViews |
| royaltyQualifiedBorrows |
| royaltyQualifiedBorrowsFromClicks |
| royaltyQualifiedBorrowsFromViews |
| brandedSearches |
| brandedSearchesClicks |
| brandedSearchesViews |
| brandedSearchRate |
| campaignBudgetCurrencyCode |
| campaignId |
| campaignName |
| clicks |
| cost |
| date |
| detailPageViews |
| detailPageViewsClicks |
| eCPAddToCart |
| eCPBrandSearch |
| endDate |
| impressions |
| impressionsViews |
| kindleEditionNormalizedPagesRead |
| kindleEditionNormalizedPagesReadFromClicks |
| kindleEditionNormalizedPagesReadFromViews |
| kindleEditionNormalizedPagesRoyalties |
| kindleEditionNormalizedPagesRoyaltiesFromClicks |
| kindleEditionNormalizedPagesRoyaltiesFromViews |
| newToBrandPurchases |
| newToBrandPurchasesClicks |
| newToBrandSalesClicks |
| newToBrandUnitsSold |
| newToBrandUnitsSoldClicks |
| purchases |
| purchasesClicks |
| purchasesPromotedClicks |
| sales |
| salesClicks |
| salesPromotedClicks |
| startDate |
| unitsSold |
| unitsSoldClicks |
| videoCompleteViews |
| videoFirstQuartileViews |
| videoMidpointViews |
| videoThirdQuartileViews |
| videoUnmutes |
| viewabilityRate |
| viewClickThroughRate |

## 按 campaign 分组

**额外指标**：campaignBudgetAmount, campaignStatus, costType, cumulativeReach, impressionsFrequencyAverage, longTermSales, longTermROAS, newToBrandDetailPageViewClicks, newToBrandDetailPageViewRate, newToBrandDetailPageViews, newToBrandDetailPageViewViews, newToBrandECPDetailPageView, newToBrandSales

**过滤器**：无

## 按 matchedTarget 分组

**额外指标**：matchedTargetAsin

**过滤器**：无

## 调用示例

### 按广告系列分组的广告系列汇总报表

```bash
curl --location 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxxxxx' \
--data '{
    "name": "SD campaigns report",
    "startDate": "2025-03-05",
    "endDate": "2025-03-10",
    "configuration": {
        "adProduct": "SPONSORED_DISPLAY",
        "groupBy": ["campaign"],
        "columns": [
            "impressions",
            "clicks",
            "cost",
            "campaignId",
            "campaignName",
            "startDate",
            "endDate"
        ],
        "reportTypeId": "sdCampaigns",
        "timeUnit": "SUMMARY",
        "format": "GZIP_JSON"
    }
}'
```
