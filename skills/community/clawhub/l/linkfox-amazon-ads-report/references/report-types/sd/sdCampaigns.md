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

# SD Campaigns

Campaign reports contain performance data broken down at the campaign level. Campaign reports include all campaigns of the requested sponsored ad type that have performance activity for the requested days. For Sponsored Display, campaign reports can also be grouped by `matchedTarget` for more granular data.

> **Note**
> You can only use a filter that is supported by all groupBy values included in a report configuration. For campaign reports, this means that filters are only supported when you include a single groupBy value.

## Configuration

| Configuration | Value |
|---|---|
| reportTypeId | sdCampaigns |
| Maximum date range | 31 days |
| Data retention | 65 days |
| timeUnit | SUMMARY or DAILY |
| groupBy | campaign or matchedTarget |
| format | GZIP_JSON |

## Base metrics

| Field |
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

## Group by campaign

**Additional metrics**: campaignBudgetAmount, campaignStatus, costType, cumulativeReach, impressionsFrequencyAverage, longTermSales, longTermROAS, newToBrandDetailPageViewClicks, newToBrandDetailPageViewRate, newToBrandDetailPageViews, newToBrandDetailPageViewViews, newToBrandECPDetailPageView, newToBrandSales

**Filters**: N/A

## Group by matchedTarget

**Additional metrics**: matchedTargetAsin

**Filters**: N/A

## Sample calls

### Campaign summary report grouped by campaign

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
