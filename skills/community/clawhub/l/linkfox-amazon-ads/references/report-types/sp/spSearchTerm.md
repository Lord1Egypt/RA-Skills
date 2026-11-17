---
reportTypeId: spSearchTerm
adProduct: SPONSORED_PRODUCTS
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
  dataRetentionDays: 65
---

# SP 搜索词报告

搜索词报告包含按投放表达式与关键词细分的搜索词绩效指标。注意，搜索词报告仅包含至少产生一次广告点击的展示。可使用 `keywordType` 筛选条件，在报告中只包含投放表达式或关键词。

> **注意**
> 如果某个商品详情页上的展示位置没有关联的搜索关键词，则报告中的搜索词将显示为星号 `*`。

## 配置

| 配置项 | 取值 |
|---|---|
| reportTypeId | spSearchTerm |
| 最大日期范围 | 31 天 |
| 数据保留 | 65 天 |
| timeUnit | SUMMARY 或 DAILY |
| groupBy | searchTerm |
| format | GZIP_JSON |

## 基础指标

| 字段 |
|------|
| impressions |
| addToList |
| qualifiedBorrows |
| royaltyQualifiedBorrows |
| clicks |
| costPerClick |
| clickThroughRate |
| cost |
| purchases1d |
| purchases7d |
| purchases14d |
| purchases30d |
| purchasesSameSku1d |
| purchasesSameSku7d |
| purchasesSameSku14d |
| purchasesSameSku30d |
| unitsSoldClicks1d |
| unitsSoldClicks7d |
| unitsSoldClicks14d |
| unitsSoldClicks30d |
| sales1d |
| sales7d |
| sales14d |
| sales30d |
| attributedSalesSameSku1d |
| attributedSalesSameSku7d |
| attributedSalesSameSku14d |
| attributedSalesSameSku30d |
| unitsSoldSameSku1d |
| unitsSoldSameSku7d |
| unitsSoldSameSku14d |
| unitsSoldSameSku30d |
| kindleEditionNormalizedPagesRead14d |
| kindleEditionNormalizedPagesRoyalties14d |
| salesOtherSku7d |
| unitsSoldOtherSku7d |
| acosClicks7d |
| acosClicks14d |
| roasClicks7d |
| roasClicks14d |
| keywordId |
| keyword |
| campaignBudgetCurrencyCode |
| date |
| startDate |
| endDate |
| portfolioId |
| searchTerm |
| campaignName |
| campaignId |
| campaignBudgetType |
| campaignBudgetAmount |
| campaignStatus |
| keywordBid |
| adGroupName |
| adGroupId |
| keywordType |
| matchType |
| targeting |
| adKeywordStatus |

## 按 searchTerm 分组

**附加指标**：adKeywordStatus

**筛选条件**：
- keywordType（取值：BROAD、PHRASE、EXACT、TARGETING_EXPRESSION、TARGETING_EXPRESSION_PREDEFINED）

## 调用示例

### 仅投放表达式

```bash
curl --location --request POST 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxxxx' \
--data-raw '{
    "name":"SP search term report 7/5-7/10",
    "startDate":"2022-07-05",
    "endDate":"2022-07-10",
    "configuration":{
        "adProduct":"SPONSORED_PRODUCTS",
        "groupBy":["searchTerm"],
        "columns":["impressions","clicks","cost","campaignId","adGroupId","date","targeting","searchTerm","keywordType","keywordId"],
        "filters": [
            {
                "field": "keywordType",
                "values": [
                    "TARGETING_EXPRESSION",
                    "TARGETING_EXPRESSION_PREDEFINED"
                ]
            }
        ],
        "reportTypeId":"spSearchTerm",
        "timeUnit":"DAILY",
        "format":"GZIP_JSON"
    }
}'
```

### 仅关键词

```bash
curl --location --request POST 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxxxx' \
--data-raw '{
    "name":"SB search terms report 7/5-7/10",
    "startDate":"2022-07-05",
    "endDate":"2022-07-10",
    "configuration":{
        "adProduct":"SPONSORED_PRODUCTS",
        "groupBy":["searchTerm"],
        "columns":["impressions","clicks","cost","campaignId","adGroupId","startDate","endDate","keywordType","keyword","matchType","keywordId","searchTerm"],
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
        "reportTypeId":"spSearchTerm",
        "timeUnit":"SUMMARY",
        "format":"GZIP_JSON"
    }
}'
```
