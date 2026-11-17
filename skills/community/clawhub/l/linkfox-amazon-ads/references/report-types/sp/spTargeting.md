---
reportTypeId: spTargeting
adProduct: SPONSORED_PRODUCTS
officialDocUrl: https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types/targeting
timeUnit: [SUMMARY, DAILY]
groupBy: [targeting]
format: [GZIP_JSON]
filters:
  - name: adKeywordStatus
    values: [ENABLED, PAUSED, ARCHIVED]
    applicableWhenGroupBy: [targeting]
  - name: keywordType
    values: [BROAD, PHRASE, EXACT, TARGETING_EXPRESSION, TARGETING_EXPRESSION_PREDEFINED]
    applicableWhenGroupBy: [targeting]
dateRange:
  maxSpanDays: 31
  dataRetentionDays: 95
---

# SP 投放报告

投放报告包含按投放表达式与关键词细分的绩效指标。

> **注意**
> 投放报告不支持 Sponsored TV 非流行品类广告主。

## 请求关键词与投放目标

若只需查看投放表达式，将 `keywordType` 筛选条件设为 TARGETING_EXPRESSION 和 TARGETING_EXPRESSION_PREDEFINED。若只需查看关键词，将 `keywordType` 筛选条件设为 BROAD、PHRASE 和 EXACT。

## 配置

| 配置项 | 取值 |
|---|---|
| reportTypeId | spTargeting |
| 最大日期范围 | 31 天 |
| 数据保留 | 95 天 |
| timeUnit | SUMMARY 或 DAILY |
| groupBy | targeting |
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
| topOfSearchImpressionShare |

## 按 targeting 分组

**附加指标**：adKeywordStatus

**筛选条件**：
- adKeywordStatus（取值：ENABLED、PAUSED、ARCHIVED）
- keywordType（取值：BROAD、PHRASE、EXACT、TARGETING_EXPRESSION、TARGETING_EXPRESSION_PREDEFINED）

## 调用示例

### 仅投放表达式

```bash
curl --location 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxx' \
--data '{
    "name": "SP targeting report 9/5-9/10",
    "startDate": "2023-09-05",
    "endDate": "2023-09-10",
    "configuration": {
        "adProduct": "SPONSORED_PRODUCTS",
        "groupBy": [
            "targeting"
        ],
        "columns": [
            "adGroupId",
            "campaignId",
            "targeting",
            "keywordId",
            "matchType",
            "impressions",
            "clicks",
            "cost",
            "purchases1d",
            "purchases7d",
            "purchases14d",
            "purchases30d",
            "startDate",
            "endDate"
        ],
        "filters": [
            {
                "field": "keywordType",
                "values": [
                    "TARGETING_EXPRESSION",
                    "TARGETING_EXPRESSION_PREDEFINED"
                ]
            }
        ],
        "reportTypeId": "spTargeting",
        "timeUnit": "SUMMARY",
        "format": "GZIP_JSON"
    }
}'
```

### 仅关键词

```bash
curl --location 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxxxx' \
--data '{
    "name": "SP keywords report 9/5-9/10",
    "startDate": "2023-09-05",
    "endDate": "2023-09-10",
    "configuration": {
        "adProduct": "SPONSORED_PRODUCTS",
        "groupBy": [
            "targeting"
        ],
        "columns": [
            "adGroupId",
            "campaignId",
            "keywordId",
            "matchType",
            "keyword",
            "impressions",
            "clicks",
            "cost",
            "purchases1d",
            "purchases7d",
            "purchases14d",
            "purchases30d",
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
        "reportTypeId": "spTargeting",
        "timeUnit": "SUMMARY",
        "format": "GZIP_JSON"
    }
}'
```
