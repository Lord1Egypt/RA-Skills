---
reportTypeId: sdAdvertisedProduct
adProduct: SPONSORED_DISPLAY
officialDocUrl: https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types/advertised-product
timeUnit: [SUMMARY, DAILY]
groupBy: [advertiser]
format: [GZIP_JSON]
filters: []
dateRange:
  maxSpanDays: 31
  dataRetentionDays: 65
---

# SD Advertised Product

Advertised product reports contain performance data for products that are advertised as part of your Sponsored Display campaigns.

## Configuration

| Configuration | Value |
|---|---|
| reportTypeId | sdAdvertisedProduct |
| Maximum date range | 31 days |
| Data retention | 65 days |
| timeUnit | SUMMARY or DAILY |
| groupBy | advertiser |
| format | GZIP_JSON |

## Base metrics

| Field |
|------|
| addToCart |
| addToCartRate |
| addToCartViews |
| addToCartClicks |
| adGroupId |
| adGroupName |
| adId |
| addToList |
| addToListFromClicks |
| qualifiedBorrows |
| royaltyQualifiedBorrows |
| addToListFromViews |
| qualifiedBorrowsFromClicks |
| qualifiedBorrowsFromViews |
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
| impressionsFrequencyAverage |
| impressionsViews |
| kindleEditionNormalizedPagesRead |
| kindleEditionNormalizedPagesReadFromClicks |
| kindleEditionNormalizedPagesReadFromViews |
| kindleEditionNormalizedPagesRoyalties |
| kindleEditionNormalizedPagesRoyaltiesFromClicks |
| kindleEditionNormalizedPagesRoyaltiesFromViews |
| newToBrandDetailPageViewClicks |
| newToBrandDetailPageViewRate |
| newToBrandDetailPageViews |
| newToBrandDetailPageViewViews |
| newToBrandECPDetailPageView |
| newToBrandPurchases |
| newToBrandPurchasesClicks |
| newToBrandSales |
| newToBrandSalesClicks |
| newToBrandUnitsSold |
| newToBrandUnitsSoldClicks |
| promotedAsin |
| promotedSku |
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

## Group by advertiser

**Additional metrics**: N/A

**Filters**: N/A

## Sample calls

### Advertised product summary report

```bash
curl --location --request POST 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxxxxxxxx' \
--data-raw '{
    "name": "SD advertised product report 3/5-3/10",
    "startDate": "2025-03-05",
    "endDate": "2025-03-10",
    "configuration": {
        "adProduct": "SPONSORED_DISPLAY",
        "groupBy": ["advertiser"],
        "columns": [
            "impressions",
            "clicks",
            "cost",
            "campaignId",
            "newToBrandSalesClicks",
            "detailPageViews"
        ],
        "reportTypeId": "sdAdvertisedProduct",
        "timeUnit": "SUMMARY",
        "format": "GZIP_JSON"
    }
}'
```
