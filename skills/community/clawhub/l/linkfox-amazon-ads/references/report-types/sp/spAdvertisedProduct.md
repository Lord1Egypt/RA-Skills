---
reportTypeId: spAdvertisedProduct
adProduct: SPONSORED_PRODUCTS
officialDocUrl: https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types/advertised-product
timeUnit: [SUMMARY, DAILY]
groupBy: [advertiser]
format: [GZIP_JSON]
filters:
  - name: adCreativeStatus
    values: [ENABLED, PAUSED, ARCHIVED]
dateRange:
  maxSpanDays: 31
  dataRetentionDays: 95
---

# SP 已推广商品（Advertised Product）

已推广商品报表包含作为广告系列一部分进行推广的商品的绩效数据。

## 配置

| 配置项 | 取值 |
|---|---|
| reportTypeId | spAdvertisedProduct |
| 最大日期范围 | 31 天 |
| 数据保留期 | 95 天 |
| timeUnit | SUMMARY 或 DAILY |
| groupBy | advertiser |
| format | GZIP_JSON |

## 基础指标

| 字段 |
|------|
| date |
| startDate |
| endDate |
| campaignName |
| campaignId |
| adGroupName |
| adGroupId |
| adId |
| addToList |
| qualifiedBorrows |
| royaltyQualifiedBorrows |
| portfolioId |
| impressions |
| clicks |
| costPerClick |
| clickThroughRate |
| cost |
| spend |
| campaignBudgetCurrencyCode |
| campaignBudgetAmount |
| campaignBudgetType |
| campaignStatus |
| advertisedAsin |
| advertisedSku |
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
| salesOtherSku7d |
| unitsSoldSameSku1d |
| unitsSoldSameSku7d |
| unitsSoldSameSku14d |
| unitsSoldSameSku30d |
| unitsSoldOtherSku7d |
| kindleEditionNormalizedPagesRead14d |
| kindleEditionNormalizedPagesRoyalties14d |
| acosClicks7d |
| acosClicks14d |
| roasClicks7d |
| roasClicks14d |

## 按 advertiser 分组

额外指标：无

## 过滤器

- adCreativeStatus（取值：ENABLED, PAUSED, ARCHIVED）

## 调用示例

**端点**：`POST https://advertising-api.amazon.com/reporting/reports`

**请求头**：
```
Content-Type: application/vnd.createasyncreportrequest.v3+json
Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxxxx
Amazon-Advertising-API-Scope: xxxxxxx
Authorization: Bearer Atza|xxxxxxxxxxxxx
```

**请求体**：
```json
{
    "name": "SP advertised product report 7/5-7/10",
    "startDate": "2022-07-05",
    "endDate": "2022-07-10",
    "configuration": {
        "adProduct": "SPONSORED_PRODUCTS",
        "groupBy": ["advertiser"],
        "columns": ["impressions", "clicks", "cost", "campaignId", "advertisedAsin"],
        "reportTypeId": "spAdvertisedProduct",
        "timeUnit": "SUMMARY",
        "format": "GZIP_JSON"
    }
}
```
