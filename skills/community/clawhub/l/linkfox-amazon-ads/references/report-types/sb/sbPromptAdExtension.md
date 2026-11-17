---
reportTypeId: sbPromptAdExtension
adProduct: SPONSORED_BRANDS
officialDocUrl: https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types/prompt-ad-extension
timeUnit: [SUMMARY, DAILY]
groupBy: [promptAdExtension]
format: [GZIP_JSON, XLSX]
filters:
  - name: marketplaceId
    values: [US]
    applicableWhenGroupBy: [promptAdExtension]
dateRange:
  maxSpanDays: 90
  dataRetentionDays: 95
---

# SB Prompt 广告扩展

Prompt Ad Extension 报告包含 Sponsored Products 和 Sponsored Brands 广告的绩效数据，涵盖 AI 驱动的 prompt 广告指标。Prompt 旨在通过亚马逊上的对话式体验帮助买家发现商品，借助智能建议与引导性问题呈现相关商品信息。

## 关于 Prompt

Prompt 是一种新的广告格式，可零额外配置地集成到现有的 Sponsored Products 和 Sponsored Brands 广告活动中。它通过以下方式在买家关键决策点增强商品发现：

- 在买家关键决策时刻大规模展示你的商品专业能力
- 用相关商品信息吸引高意向买家
- 预判并回答买家关于你商品的提问

获得点击的 Prompt 会显示在现有的 Sponsored Products 或 Sponsored Brands 报告中，你可通过 Amazon Ads 控制台暂停单个 Prompt。

## 配置

| 配置项 | 值 |
|---|---|
| reportTypeId | sbPromptAdExtension |
| 最大日期范围 | 90 天 |
| 数据保留期 | 95 天 |
| timeUnit | SUMMARY 或 DAILY |
| groupBy | promptAdExtension |
| format | GZIP_JSON 或 XLSX |

## 基础指标

| 字段 |
|------|
| date |
| startDate |
| endDate |
| campaignId |
| campaignName |
| adGroupId |
| adGroupName |
| marketplaceId |
| adId |
| adName |
| creativeExtensionId |
| creativeExtensionType |
| portfolioName |
| campaignBudgetCurrencyCode |
| promptText |
| impressions |
| clicks |
| clickThroughRate |
| costPerClick |
| cost |
| spend |
| viewableImpressions |
| acosClicks7d |
| acosClicks14d |
| roasClicks7d |
| roasClicks14d |
| purchases1d |
| purchases7d |
| purchases14d |
| purchases30d |
| purchasesSameSku1d |
| purchasesSameSku7d |
| purchasesSameSku14d |
| purchasesSameSku30d |
| purchasesOtherSku1d |
| purchasesOtherSku7d |
| purchasesOtherSku14d |
| purchasesOtherSku30d |
| unitsSoldClicks1d |
| unitsSoldClicks7d |
| unitsSoldClicks14d |
| unitsSoldClicks30d |
| unitsSoldSameSku1d |
| unitsSoldSameSku7d |
| unitsSoldSameSku14d |
| unitsSoldSameSku30d |
| unitsSoldOtherSku1d |
| unitsSoldOtherSku7d |
| unitsSoldOtherSku14d |
| unitsSoldOtherSku30d |
| sales1d |
| sales7d |
| sales14d |
| sales30d |
| attributedSalesSameSku1d |
| attributedSalesSameSku7d |
| attributedSalesSameSku14d |
| attributedSalesSameSku30d |
| salesOtherSku1d |
| salesOtherSku7d |
| salesOtherSku14d |
| salesOtherSku30d |
| purchaseClickRate7d |
| purchaseClickRate14d |
| newToBrandPurchases |
| newToBrandPurchasesPercentage |
| newToBrandUnitsSold |
| newToBrandUnitsSoldPercentage |
| newToBrandSales |
| newToBrandSalesPercentage |

## 按 promptAdExtension 分组

**额外指标**: 无

**过滤条件**:
- marketplaceId（取值：US）

## 调用示例

```bash
curl --location 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxxxxxx' \
--data '{
    "name":"SB prompt ad extension report 4/13-4/16",
    "startDate":"2026-04-13",
    "endDate":"2026-04-16",
    "configuration":{
        "adProduct":"SPONSORED_BRANDS",
        "groupBy":["promptAdExtension"],
        "columns":["date","campaignId","campaignName","adGroupId","adGroupName","adId","adName","creativeExtensionId","promptText","impressions","clicks","cost","purchases7d","sales7d","newToBrandPurchases","newToBrandSales"],
        "reportTypeId":"sbPromptAdExtension",
        "timeUnit":"DAILY",
        "format":"GZIP_JSON"
    }
}'
```
