---
reportTypeId: sdTargeting
adProduct: SPONSORED_DISPLAY
officialDocUrl: https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types/targeting
timeUnit: [SUMMARY, DAILY]
groupBy: [targeting, matchedTarget]
format: [GZIP_JSON]
filters: []
dateRange:
  maxSpanDays: 31
  dataRetentionDays: 65
---

# SD 投放定向（Targeting）

定向报表包含按投放定向表达式拆分的绩效指标。对于 Sponsored Display，定向报表还可按 `matchedTarget` 分组以呈现实际匹配到的 ASIN。

## 配置

| 配置项 | 取值 |
|---|---|
| reportTypeId | sdTargeting |
| 最大日期范围 | 31 天 |
| 数据保留期 | 65 天 |
| timeUnit | SUMMARY 或 DAILY |
| groupBy | targeting 或 matchedTarget |
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
| targetingExpression |
| targetingId |
| targetingText |
| unitsSold |
| unitsSoldClicks |
| videoCompleteViews |
| videoFirstQuartileViews |
| videoMidpointViews |
| videoThirdQuartileViews |
| videoUnmutes |
| viewabilityRate |
| viewClickThroughRate |

## 按 targeting 分组

**额外指标**：adKeywordStatus, newToBrandDetailPageViewClicks, newToBrandDetailPageViewRate, newToBrandDetailPageViews, newToBrandDetailPageViewViews, newToBrandECPDetailPageView

**过滤器**：无

## 按 matchedTarget 分组

**额外指标**：matchedTargetAsin

**过滤器**：无

## 调用示例

### 按 targeting 分组的定向汇总报表

```bash
curl --location 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxx' \
--data '{
    "name": "SD targeting report",
    "startDate": "2025-03-05",
    "endDate": "2025-03-10",
    "configuration": {
        "adProduct": "SPONSORED_DISPLAY",
        "groupBy": ["targeting"],
        "columns": [
            "adGroupId",
            "campaignId",
            "targetingId",
            "targetingText",
            "targetingExpression",
            "impressions",
            "clicks",
            "cost",
            "purchases",
            "sales",
            "startDate",
            "endDate"
        ],
        "reportTypeId": "sdTargeting",
        "timeUnit": "SUMMARY",
        "format": "GZIP_JSON"
    }
}'
```

### 按 matchedTarget 分组的定向报表

```bash
curl --location 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxx' \
--data '{
    "name": "SD targeting matched-target report",
    "startDate": "2025-03-05",
    "endDate": "2025-03-10",
    "configuration": {
        "adProduct": "SPONSORED_DISPLAY",
        "groupBy": ["matchedTarget"],
        "columns": [
            "adGroupId",
            "campaignId",
            "matchedTargetAsin",
            "impressions",
            "clicks",
            "cost",
            "purchases",
            "sales",
            "startDate",
            "endDate"
        ],
        "reportTypeId": "sdTargeting",
        "timeUnit": "SUMMARY",
        "format": "GZIP_JSON"
    }
}'
```
