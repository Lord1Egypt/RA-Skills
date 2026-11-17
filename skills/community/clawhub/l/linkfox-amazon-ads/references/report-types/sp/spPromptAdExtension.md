---
reportTypeId: spPromptAdExtension
adProduct: SPONSORED_PRODUCTS
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

# SP Prompt 广告扩展（Prompt Ad Extension）

Prompt 广告扩展报表包含 Sponsored Products 和 Sponsored Brands 广告的绩效数据，其中涵盖由 AI 驱动的 prompt 广告相关指标。Prompt 旨在通过亚马逊上的对话式体验，借助智能建议和引导性问题呈现相关商品信息，帮助购物者发现商品。

## 关于 Prompt

Prompt 是一种新的广告格式，可集成到现有的 Sponsored Products 和 Sponsored Brands 广告系列中，无需额外设置。它们在购物者决策的关键时刻增强商品发现能力：

- 在购物者决策的关键时刻，规模化地展示你的商品专业能力
- 以相关商品信息吸引高意向购物者
- 预判并解答购物者关于你商品的疑问

带有点击的 prompt 会显示在现有的 Sponsored Products 或 Sponsored Brands 报表中，你也可以通过亚马逊广告控制台暂停单个 prompt。

## 配置

| 配置项 | 取值 |
|---|---|
| reportTypeId | spPromptAdExtension |
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
| advertisedSku |
| advertisedAsin |
| adId |
| creativeExtensionId |
| creativeExtensionType |
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

## 按 promptAdExtension 分组

**额外指标**：无

**过滤器**：
- marketplaceId（取值：US）

## 调用示例

```bash
curl --location 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxxxxxx' \
--data '{
    "name":"SP prompt ad extension report 11/1-1/23",
    "startDate":"2025-11-01",
    "endDate":"2026-01-23",
    "configuration":{
        "adProduct":"SPONSORED_PRODUCTS",
        "groupBy":["promptAdExtension"],
        "columns":["date","campaignId","campaignName","adGroupId","adGroupName","adId","creativeExtensionId","promptText","impressions","clicks","cost","purchases7d","sales7d"],
        "reportTypeId":"spPromptAdExtension",
        "timeUnit":"DAILY",
        "format":"GZIP_JSON"
    }
}'
```
