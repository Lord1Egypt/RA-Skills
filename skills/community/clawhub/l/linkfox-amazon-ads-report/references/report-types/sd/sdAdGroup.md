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

# SD Ad Group

Ad group reports contain performance data broken down at the ad group level. Ad group reports include all campaigns of the requested sponsored ad type that have performance activity for the requested days. For Sponsored Display, ad group reports can also be grouped by `matchedTarget` for more granular data.

## Configuration

| Configuration | Value |
|---|---|
| reportTypeId | sdAdGroup |
| Maximum date range | 31 days |
| Data retention | 65 days |
| timeUnit | SUMMARY or DAILY |
| groupBy | adGroup or matchedTarget |
| format | GZIP_JSON |

## Base metrics

| Field |
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

## Group by adGroup

**Additional metrics**: cumulativeReach, impressionsFrequencyAverage, newToBrandDetailPageViewClicks, newToBrandDetailPageViewRate, newToBrandDetailPageViews, newToBrandDetailPageViewViews, newToBrandECPDetailPageView

**Filters**: N/A

## Group by matchedTarget

**Additional metrics**: matchedTargetAsin

**Filters**: N/A

## Sample calls

### Ad group summary report grouped by ad group

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
