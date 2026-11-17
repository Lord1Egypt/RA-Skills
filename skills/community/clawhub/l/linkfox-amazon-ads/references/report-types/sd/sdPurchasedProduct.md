---
reportTypeId: sdPurchasedProduct
adProduct: SPONSORED_DISPLAY
officialDocUrl: https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types/purchased-product
timeUnit: [SUMMARY, DAILY]
groupBy: [asin]
format: [GZIP_JSON]
filters: []
dateRange:
  maxSpanDays: 31
  dataRetentionDays: 65
---

# SD 已购商品（Purchased Product）

Sponsored Display 已购商品报表包含与广告系列品牌光环（brand-halo）活动相关、已被购买的商品的绩效数据（被购买的 ASIN 与被推广的 ASIN 不同）。

## 配置

| 配置项 | 取值 |
|---|---|
| reportTypeId | sdPurchasedProduct |
| 最大日期范围 | 31 天 |
| 数据保留期 | 65 天 |
| timeUnit | SUMMARY 或 DAILY |
| groupBy | asin |
| format | GZIP_JSON |

## 基础指标

| 字段 |
|------|
| adGroupId |
| adGroupName |
| asinBrandHalo |
| addToList |
| addToListFromClicks |
| qualifiedBorrowsFromClicks |
| royaltyQualifiedBorrowsFromClicks |
| addToListFromViews |
| qualifiedBorrows |
| qualifiedBorrowsFromViews |
| royaltyQualifiedBorrows |
| royaltyQualifiedBorrowsFromViews |
| campaignBudgetCurrencyCode |
| campaignId |
| campaignName |
| conversionsBrandHalo |
| conversionsBrandHaloClicks |
| date |
| endDate |
| kindleEditionNormalizedPagesRead |
| kindleEditionNormalizedPagesReadFromClicks |
| kindleEditionNormalizedPagesReadFromViews |
| kindleEditionNormalizedPagesRoyalties |
| kindleEditionNormalizedPagesRoyaltiesFromClicks |
| kindleEditionNormalizedPagesRoyaltiesFromViews |
| promotedAsin |
| promotedSku |
| salesBrandHalo |
| salesBrandHaloClicks |
| startDate |
| unitsSoldBrandHalo |
| unitsSoldBrandHaloClicks |

## 按 asin 分组

**额外指标**：无

**过滤器**：无

## 调用示例

### 已购商品汇总报表

```bash
curl --location --request POST 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxxxxx' \
--data-raw '{
    "name": "SD purchased product report",
    "startDate": "2025-03-05",
    "endDate": "2025-03-10",
    "configuration": {
        "adProduct": "SPONSORED_DISPLAY",
        "groupBy": ["asin"],
        "columns": [
            "promotedAsin",
            "asinBrandHalo",
            "adGroupName",
            "campaignName",
            "salesBrandHalo",
            "conversionsBrandHalo",
            "campaignId",
            "adGroupId"
        ],
        "reportTypeId": "sdPurchasedProduct",
        "timeUnit": "SUMMARY",
        "format": "GZIP_JSON"
    }
}'
```
