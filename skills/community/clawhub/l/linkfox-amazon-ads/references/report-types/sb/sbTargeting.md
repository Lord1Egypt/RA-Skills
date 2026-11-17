---
reportTypeId: sbTargeting
adProduct: SPONSORED_BRANDS
officialDocUrl: https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types/targeting
timeUnit: [SUMMARY, DAILY]
groupBy: [targeting]
format: [GZIP_JSON]
filters:
  - name: adKeywordStatus
    values: [ENABLED, PAUSED, ARCHIVED]
    applicableWhenGroupBy: [targeting]
  - name: keywordType
    values: [BROAD, PHRASE, EXACT, TARGETING_EXPRESSION, TARGETING_EXPRESSION_PREDEFINED, THEME]
    applicableWhenGroupBy: [targeting]
dateRange:
  maxSpanDays: 31
  dataRetentionDays: 60
---

# SB 定向

定向报告包含按定向表达式和关键词拆分的绩效指标。

> **注意**
> 定向报告不支持 Sponsored TV 的非 endemic 广告主。

## 请求关键词与定向目标

若只需定向表达式，将 keywordType 过滤器设为 TARGETING_EXPRESSION 和 TARGETING_EXPRESSION_PREDEFINED。若只需关键词，将 keywordType 过滤器设为 BROAD、PHRASE 和 EXACT。

> **注意**
> 本报告目前为预览版。预览期间，isMultiAdGroupsEnabled=False 的 Sponsored Brands 广告活动相关数据不可用。待 v3 报告支持所有 Sponsored Brands 广告活动后，我们将在发布说明中宣布正式可用。

## 配置

| 配置项 | 值 |
|---|---|
| reportTypeId | sbTargeting |
| 最大日期范围 | 31 天 |
| 数据保留期 | 60 天 |
| timeUnit | SUMMARY 或 DAILY |
| groupBy | targeting |
| format | GZIP_JSON |

## 基础指标

| 字段 |
|------|
| addToCart |
| addToCartClicks |
| addToCartRate |
| adGroupId |
| adGroupName |
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
| keywordBid |
| keywordId |
| adKeywordStatus |
| keywordText |
| keywordType |
| matchType |
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
| targetingExpression |
| targetingId |
| targetingText |
| targetingType |
| topOfSearchImpressionShare |
| unitsSold |

## 按 targeting 分组

**额外指标**: 无

**过滤条件**:
- adKeywordStatus（取值：ENABLED, PAUSED, ARCHIVED）
- keywordType（取值：BROAD, PHRASE, EXACT, TARGETING_EXPRESSION, TARGETING_EXPRESSION_PREDEFINED, THEME）

## 调用示例

### 仅关键词

```bash
curl --location 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxx' \
--data '{
    "name": "SB keywords report 9/5-9/10",
    "startDate": "2023-09-05",
    "endDate": "2023-09-10",
    "configuration": {
        "adProduct": "SPONSORED_BRANDS",
        "groupBy": [
            "targeting"
        ],
        "columns": [
            "adGroupId",
            "campaignId",
            "keywordId",
            "matchType",
            "keywordText",
            "impressions",
            "clicks",
            "cost",
            "startDate",
            "endDate"
        ],
        "filters": [
            {
                "field": "keywordType",
                "values": [
                    "BROAD",
                    "PHRASE",
                    "EXACT"
                ]
            }
        ],
        "reportTypeId": "sbTargeting",
        "timeUnit": "SUMMARY",
        "format": "GZIP_JSON"
    }
}'
```
