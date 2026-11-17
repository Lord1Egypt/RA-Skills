---
reportTypeId: spPurchasedProduct
adProduct: SPONSORED_PRODUCTS
officialDocUrl: https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types/purchased-product
timeUnit: [SUMMARY, DAILY]
groupBy: [asin]
format: [GZIP_JSON]
filters: []
dateRange:
  maxSpanDays: 31
  dataRetentionDays: 95
---

# SP 购买商品报告

Sponsored Products 购买商品报告包含被购买但未作为广告投放的商品的绩效数据。购买商品报告同时包含投放表达式与关键词 ID。收到报告后，可按 `keywordType` 过滤，以区分投放表达式与关键词。

## 配置

| 配置项 | 取值 |
|---|---|
| reportTypeId | spPurchasedProduct |
| 最大日期范围 | 31 天 |
| 数据保留 | 95 天 |
| timeUnit | SUMMARY 或 DAILY |
| groupBy | asin |
| format | GZIP_JSON |

## 基础指标

| 字段 |
|------|
| date |
| startDate |
| endDate |
| addToList |
| addToListFromClicks |
| qualifiedBorrows |
| qualifiedBorrowsFromClicks |
| royaltyQualifiedBorrows |
| royaltyQualifiedBorrowsFromClicks |
| portfolioId |
| campaignName |
| campaignId |
| adGroupName |
| adGroupId |
| keywordId |
| keyword |
| keywordType |
| advertisedAsin |
| purchasedAsin |
| advertisedSku |
| campaignBudgetCurrencyCode |
| matchType |
| unitsSoldClicks1d |
| unitsSoldClicks7d |
| unitsSoldClicks14d |
| unitsSoldClicks30d |
| sales1d |
| sales7d |
| sales14d |
| sales30d |
| purchases1d |
| purchases7d |
| purchases14d |
| purchases30d |
| unitsSoldOtherSku1d |
| unitsSoldOtherSku7d |
| unitsSoldOtherSku14d |
| unitsSoldOtherSku30d |
| salesOtherSku1d |
| salesOtherSku7d |
| salesOtherSku14d |
| salesOtherSku30d |
| purchasesOtherSku1d |
| purchasesOtherSku7d |
| purchasesOtherSku14d |
| purchasesOtherSku30d |
| kindleEditionNormalizedPagesRead14d |
| kindleEditionNormalizedPagesRoyalties14d |

## 按 asin 分组

**附加指标**：无

**筛选条件**：无

## 调用示例

```bash
curl --location --request POST 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxxxxx' \
--data-raw '{
    "name":"SP purchased product report 7/5-7/10",
    "startDate":"2022-07-05",
    "endDate":"2022-07-10",
    "configuration":{
        "adProduct":"SPONSORED_PRODUCTS",
        "groupBy":["asin"],
        "columns":["purchasedAsin","advertisedAsin","adGroupName","campaignName","sales14d","campaignId","adGroupId","keywordId","keywordType","keyword"],
        "reportTypeId":"spPurchasedProduct",
        "timeUnit":"SUMMARY",
        "format":"GZIP_JSON"
    }
}'
```
