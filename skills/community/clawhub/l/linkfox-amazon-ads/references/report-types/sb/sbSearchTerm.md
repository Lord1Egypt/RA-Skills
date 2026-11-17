---
reportTypeId: sbSearchTerm
adProduct: SPONSORED_BRANDS
officialDocUrl: https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types/search-term
timeUnit: [SUMMARY, DAILY]
groupBy: [searchTerm]
format: [GZIP_JSON]
filters:
  - name: keywordType
    values: [BROAD, PHRASE, EXACT, TARGETING_EXPRESSION, TARGETING_EXPRESSION_PREDEFINED]
    applicableWhenGroupBy: [searchTerm]
dateRange:
  maxSpanDays: 31
  dataRetentionDays: 60
---

# SB 搜索词

搜索词报告包含按定向表达式和关键词拆分的搜索词绩效指标。注意，搜索词报告仅包含至少产生一次广告点击的曝光。使用 keywordType 过滤器可在报告中包含定向表达式或关键词。

> **注意**
> 如果某个投放位置在商品详情页上没有关联的搜索关键词，报告中的搜索词将显示为星号 `*`。

> **注意**
> 本报告目前为预览版。预览期间，isMultiAdGroupsEnabled 设为 FALSE 的 Sponsored Brands 广告活动相关数据不可用。待 v3 报告支持所有 Sponsored Brands 广告活动后，我们将在发布说明中宣布正式可用。

## 配置

| 配置项 | 值 |
|---|---|
| reportTypeId | sbSearchTerm |
| 最大日期范围 | 31 天 |
| 数据保留期 | 60 天 |
| timeUnit | SUMMARY 或 DAILY |
| groupBy | searchTerm |
| format | GZIP_JSON |

## 基础指标

| 字段 |
|------|
| adGroupId |
| adGroupName |
| addToList |
| addToListFromClicks |
| qualifiedBorrows |
| qualifiedBorrowsFromClicks |
| royaltyQualifiedBorrows |
| royaltyQualifiedBorrowsFromClicks |
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
| endDate |
| impressions |
| keywordBid |
| keywordId |
| keywordText |
| kindleEditionNormalizedPagesRead14d |
| kindleEditionNormalizedPagesRoyalties14d |
| matchType |
| purchases |
| purchasesClicks |
| sales |
| salesClicks |
| searchTerm |
| startDate |
| unitsSold |
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

## 按 searchTerm 分组

**额外指标**: adKeywordStatus

**过滤条件**:
- keywordType（取值：BROAD, PHRASE, EXACT, TARGETING_EXPRESSION, TARGETING_EXPRESSION_PREDEFINED）

## 调用示例

```bash
curl --location 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxxx' \
--data '{
    "name": "SP search terms report 9/5-9/10",
    "startDate": "2023-09-05",
    "endDate": "2023-09-10",
    "configuration": {
        "adProduct": "SPONSORED_BRANDS",
        "groupBy": [
            "searchTerm"
        ],
        "columns": [
            "impressions",
            "clicks",
            "cost",
            "campaignId",
            "adGroupId",
            "startDate",
            "endDate",
            "matchType",
            "keywordId",
            "searchTerm"
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
        "reportTypeId": "sbSearchTerm",
        "timeUnit": "SUMMARY",
        "format": "GZIP_JSON"
    }
}'
```
