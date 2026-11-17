---
reportTypeId: sbPurchasedProduct
adProduct: SPONSORED_BRANDS
officialDocUrl: https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types/purchased-product
timeUnit: [SUMMARY, DAILY]
groupBy: [purchasedAsin]
format: [GZIP_JSON]
filters: []
dateRange:
  maxSpanDays: 731
  dataRetentionDays: 731
---

# SB 已购商品

Sponsored Brands 已购商品报告包含因你的广告活动而产生购买的商品的绩效数据。

## 配置

| 配置项 | 值 |
|---|---|
| reportTypeId | sbPurchasedProduct |
| 最大日期范围 | 731 天 |
| 数据保留期 | 731 天 |
| timeUnit | SUMMARY 或 DAILY |
| groupBy | purchasedAsin |
| format | GZIP_JSON |

## 基础指标

| 字段 |
|------|
| campaignId |
| adGroupId |
| date |
| startDate |
| endDate |
| campaignBudgetCurrencyCode |
| campaignName |
| campaignPriceTypeCode |
| adGroupName |
| attributionType |
| purchasedAsin |
| ordersClicks14d |
| productName |
| productCategory |
| sales14d |
| salesClicks14d |
| orders14d |
| unitsSold14d |
| newToBrandSales14d |
| newToBrandPurchases14d |
| newToBrandUnitsSold14d |
| newToBrandSalesPercentage14d |
| newToBrandPurchasesPercentage14d |
| newToBrandUnitsSoldPercentage14d |
| unitsSoldClicks14d |
| kindleEditionNormalizedPagesRead14d |
| kindleEditionNormalizedPagesRoyalties14d |

## 按 purchasedAsin 分组

**额外指标**: 无

**过滤条件**: 无

## 调用示例

```bash
curl --location --request POST 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxxxxx' \
--data-raw '{
    "name":"SB purchased product report 7/5-7/10",
    "startDate":"2022-07-05",
    "endDate":"2022-07-10",
    "configuration":{
        "adProduct":"SPONSORED_BRANDS",
        "groupBy":["purchasedAsin"],
        "columns":["purchasedAsin","attributionType","adGroupName","campaignName","sales14d","startDate","endDate"],
        "reportTypeId":"sbPurchasedProduct",
        "timeUnit":"SUMMARY",
        "format":"GZIP_JSON"
    }
}'
```
