---
reportTypeId: spCampaigns
adProduct: SPONSORED_PRODUCTS
officialDocUrl: https://advertising.amazon.com/API/docs/en-us/guides/reporting/v3/report-types/campaign
timeUnit: [SUMMARY, DAILY]
groupBy: [campaign, adGroup, campaignPlacement]
format: [GZIP_JSON]
filters:
  - name: campaignStatus
    values: [ENABLED, PAUSED, ARCHIVED]
    applicableWhenGroupBy: [campaign]
  - name: adStatus
    values: [ENABLED, PAUSED, ARCHIVED]
    applicableWhenGroupBy: [adGroup]
  - name: campaignSite
    values: [AmazonBusiness]
    applicableWhenGroupBy: [campaignPlacement]
dateRange:
  maxSpanDays: 31
  dataRetentionDays: 95
---

# SP 广告系列（Campaigns）

广告系列报表包含按广告系列维度拆分的绩效数据。广告系列报表包含所请求的赞助广告类型中，在所请求日期内有绩效活动的全部广告系列。例如，Sponsored Products 广告系列报表会返回所选日期内获得曝光的全部 Sponsored Products 广告系列的绩效数据。广告系列报表还可按广告组和投放位置分组以获取更细粒度的数据。

> **注意**
> 只能使用报表配置中所有 groupBy 值都支持的过滤器。对于广告系列报表，过滤器仅在仅包含单个 groupBy 值时才被支持。

## 配置

| 配置项 | 取值 |
|---|---|
| reportTypeId | spCampaigns |
| 最大日期范围 | 31 天 |
| 数据保留期 | 95 天 |
| timeUnit | SUMMARY 或 DAILY |
| groupBy | campaign、adGroup 或 campaignPlacement |
| format | GZIP_JSON |

## 基础指标

| 字段 |
|------|
| impressions |
| addToList |
| qualifiedBorrows |
| royaltyQualifiedBorrows |
| clicks |
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
| date |
| startDate |
| endDate |
| campaignBiddingStrategy |
| costPerClick |
| clickThroughRate |
| spend |

## 按 campaign 分组

**额外指标**：campaignName, campaignId, campaignStatus, campaignBudgetAmount, campaignBudgetType, campaignRuleBasedBudgetAmount, campaignApplicableBudgetRuleId, campaignApplicableBudgetRuleName, campaignBudgetCurrencyCode, topOfSearchImpressionShare

**过滤器**：
- campaignStatus（取值：ENABLED, PAUSED, ARCHIVED）

## 按 adGroup 分组

**额外指标**：adGroupName, adGroupId, adStatus

**过滤器**：
- adStatus（取值：ENABLED, PAUSED, ARCHIVED）

## 按 campaignPlacement 分组

**额外指标**：placementClassification, campaignName, campaignId, campaignStatus, campaignBudgetAmount, campaignBudgetType, campaignRuleBasedBudgetAmount, campaignApplicableBudgetRuleId, campaignApplicableBudgetRuleName, campaignBudgetCurrencyCode, topOfSearchImpressionShare

**过滤器**：
- campaignSite（取值：AmazonBusiness）

> **注意**
> Amazon Business 绩效数据仅从 2024 年 9 月 5 日起可用。
>
> Sponsored Products 的 Amazon Business 竞价调整与报表功能即将支持 Bulksheets。
>
> 除 campaignPlacement 外的其他 groupBy 参数均不支持。

## 调用示例

### 按广告系列和广告组分组的广告系列日报表

```bash
curl --location --request POST 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxxxx' \
--data-raw '{
    "name":"SP campaigns report 7/5-7/10",
    "startDate":"2022-07-05",
    "endDate":"2022-07-10",
    "configuration":{
        "adProduct":"SPONSORED_PRODUCTS",
        "groupBy":["campaign","adGroup"],
        "columns":["impressions","clicks","cost","campaignId","adGroupId","date"],
        "reportTypeId":"spCampaigns",
        "timeUnit":"DAILY",
        "format":"GZIP_JSON"
    }
}'
```

### 按广告系列和投放位置分组的广告系列汇总报表

```bash
curl --location --request POST 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxxxxxx' \
--data-raw '{
    "name":"SP campaigns report 7/5-7/10",
    "startDate":"2022-07-05",
    "endDate":"2022-07-10",
    "configuration":{
        "adProduct":"SPONSORED_PRODUCTS",
        "groupBy":["campaign","campaignPlacement"],
        "columns":["impressions","clicks","cost","campaignId","placementClassification","startDate","endDate"],
        "reportTypeId":"spCampaigns",
        "timeUnit":"SUMMARY",
        "format":"GZIP_JSON"
    }
}'
```

### Amazon Business 按投放位置分组的广告系列汇总报表

```bash
curl --location --request POST 'https://advertising-api.amazon.com/reporting/reports' \
--header 'Content-Type: application/vnd.createasyncreportrequest.v3+json' \
--header 'Amazon-Advertising-API-ClientId: amzn1.application-oa2-client.xxxxxxxx' \
--header 'Amazon-Advertising-API-Scope: xxxxxxxx' \
--header 'Authorization: Bearer Atza|xxxxxxxxxxx' \
--data-raw '{
     "name":"SP campaigns report 9/07-9/10",
     "startDate":"2024-09-07",
     "endDate":"2024-09-10",
     "configuration":{
         "adProduct":"SPONSORED_PRODUCTS",
         "groupBy":["campaignPlacement"],
         "columns":["impressions","clicks","cost","campaignId","placementClassification","startDate","endDate"],
         "filters": [{"field":"campaignSite","values":["AmazonBusiness"]}],
         "reportTypeId":"spCampaigns",
         "timeUnit":"SUMMARY",
         "format":"GZIP_JSON"
    }
}'
```

> **注意**
> 仅按 campaignPlacement 分组生成的报表，与按 campaign 加 campaignPlacement 分组生成的报表相同。
