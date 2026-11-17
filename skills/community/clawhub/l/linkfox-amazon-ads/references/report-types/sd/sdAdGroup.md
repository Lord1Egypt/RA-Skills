---
reportTypeId: sdAdGroup
adProduct: SPONSORED_DISPLAY
officialDocUrl: https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types/ad-group
timeUnit: [SUMMARY, DAILY]
groupBy: [adGroup, matchedTarget]
format: [GZIP_JSON]
filters: []
dateRange:
  maxSpanDays: 31
  dataRetentionDays: 65
---

# SD 广告组（Ad Group）

广告组报表包含按广告组维度拆分的绩效数据。广告组报表包含所请求的赞助广告类型中，在所请求日期内有绩效活动的全部广告系列。对于 Sponsored Display，广告组报表还可按 `matchedTarget` 分组以获取更细粒度的数据。

## 配置

| 配置项 | 取值 |
|---|---|
| reportTypeId | sdAdGroup |
| 最大日期范围 | 31 天 |
| 数据保留期 | 65 天 |
| timeUnit | SUMMARY 或 DAILY |
| groupBy | adGroup 或 matchedTarget |
| format | GZIP_JSON |

## 基础指标

| 字段 |
|------|
| addToCart |
| addToCartClicks |
| addToCartRate |
| addToCartViews |
| adGroupId |
| adGroupName |
| addToList |
| addToListFromClicks |
| addToListFromViews |
| qualifiedBorrows |
| qualifiedBorrowsFromClicks |
| qualifiedBorrowsFromViews |
| royaltyQualifiedBorrows |
| royaltyQualifiedBorrowsFromClicks |
| royaltyQualifiedBorrowsFromViews |
| bidOptimization |
| brandedSearches |
| brandedSearchesClicks |
| brandedSearchesViews |
| brandedSearchRate |
| campaignBudgetCurrencyCode |
| campaignId |
| campaignName |
| clicks |
| cost |
| cumulativeReach |
| date |
| detailPageViews |
| detailPageViewsClicks |
| eCPAddToCart |
| eCPBrandSearch |
| endDate |
| impressions |
| impressionsViews |
| newToBrandPurchases |
| kindleEditionNormalizedPagesRead |
| kindleEditionNormalizedPagesReadFromClicks |
| kindleEditionNormalizedPagesReadFromViews |
| kindleEditionNormalizedPagesRoyalties |
| kindleEditionNormalizedPagesRoyaltiesFromClicks |
| kindleEditionNormalizedPagesRoyaltiesFromViews |
| newToBrandPurchasesClicks |
| newToBrandSales |
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

## 按 adGroup 分组

**额外指标**：cumulativeReach, impressionsFrequencyAverage, newToBrandDetailPageViewClicks, newToBrandDetailPageViewRate, newToBrandDetailPageViews, newToBrandDetailPageViewViews, newToBrandECPDetailPageView

**过滤器**：无

## 按 matchedTarget 分组

**额外指标**：matchedTargetAsin

**过滤器**：无

## 调用示例

### 按广告组分组的广告组汇总报表

```bash
curl --location 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxxxxxx' \
--data '{
    "name": "SD ad group report",
    "startDate": "2025-03-05",
    "endDate": "2025-03-10",
    "configuration": {
        "adProduct": "SPONSORED_DISPLAY",
        "groupBy": ["adGroup"],
        "columns": [
            "impressions",
            "clicks",
            "cost",
            "campaignId",
            "adGroupId",
            "adGroupName",
            "startDate",
            "endDate"
        ],
        "reportTypeId": "sdAdGroup",
        "timeUnit": "SUMMARY",
        "format": "GZIP_JSON"
    }
}'
```
