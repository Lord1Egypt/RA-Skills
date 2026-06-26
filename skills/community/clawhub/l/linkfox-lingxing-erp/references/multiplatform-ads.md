# 领星多平台广告接口参考

所有接口均为 POST 请求，域名：`https://openapi.lingxing.com`

---

## TikTok 推广广告

### queryAdvertiserList - 查询广告账号

**路径**: `/basicOpen/multiplatform/ads/queryAdvertiserList`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| startDate | 是 | string | 开始日期，yyyy-MM-dd，间隔不超过31天 |
| endDate | 是 | string | 结束日期，yyyy-MM-dd |
| length | 是 | int | 每页条数，小于2000 |
| page | 是 | int | 页码 |
| advertiserIds | 否 | array | 广告账号ID列表 |
| status | 否 | array | STATUS_ENABLE/SYSTEM_STATUS_IN_REVIEW/SYSTEM_STATUS_NOT_PASS/STATUS_LIMIT/STATUS_DISABLE |
| currencies | 否 | array | 币种列表，如 ["USD","CNY"] |
| orderField | 否 | string | 排序字段（驼峰） |
| orderType | 否 | string | ASC/DESC |
| searchType | 否 | string | advertiser_name/ad_group_name/campaign_name/ad_name |
| searchValue | 否 | array | 搜索值 |

**关键返回字段**: advertiserId, advertiserName, spend, impressions, clicks, ctr, cpc, orders, revenue, roas

---

### queryCommonAdvertiserList - 查询推广广告账号（通用）

**路径**: `/basicOpen/multiplatform/ads/queryCommonAdvertiserList`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| internalStatus | 否 | string | ENABLE/DISABLE/DELETE |
| hasGmvStore | 否 | int | 1=只返回有GMV店铺的账号 |

**关键返回字段**: 广告账号基础信息列表

---

### queryTiktokCampaignList - 查询广告系列

**路径**: `/basicOpen/multiplatform/ads/queryTiktokCampaignList`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| startDate | 是 | string | 开始日期，yyyy-MM-dd，间隔不超过31天 |
| endDate | 是 | string | 结束日期 |
| length | 是 | int | 每页条数，小于2000 |
| page | 是 | int | 页码 |
| advertiserIds | 否 | array | 广告账号ID列表 |
| campaignIds | 否 | array | 广告活动ID列表 |
| objectiveType | 否 | array | REACH/TRAFFIC/VIDEO_VIEWS/LEAD_GENERATION/ENGAGEMENT/APP_PROMOTION/WEB_CONVERSIONS/PRODUCT_SALES |
| status | 否 | array | STATUS_ENABLE/STATUS_DISABLE 等 |
| summaryCurrency | 否 | string | 汇总币种 |

**关键返回字段**: campaignId, campaignName, spend, impressions, clicks, orders, revenue, roas, status

---

### queryTiktokAdGroupList - 查询广告组

**路径**: `/basicOpen/multiplatform/ads/queryTiktokAdGroupList`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| startDate | 是 | string | 开始日期，yyyy-MM-dd，间隔不超过31天 |
| endDate | 是 | string | 结束日期 |
| length | 是 | int | 每页条数，小于2000 |
| page | 是 | int | 页码 |
| advertiserIds | 否 | array | 广告账号ID列表 |
| campaignIds | 否 | array | 广告活动ID列表 |
| status | 否 | array | STATUS_ENABLE/STATUS_DISABLE 等 |
| searchType | 否 | string | ad_group_name 等 |

**关键返回字段**: adGroupId, adGroupName, campaignId, spend, impressions, clicks, orders, roas

---

### queryTiktokAdList - 查询广告

**路径**: `/basicOpen/multiplatform/ads/queryTiktokAdList`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| startDate | 是 | string | 开始日期，yyyy-MM-dd，间隔不超过31天 |
| endDate | 是 | string | 结束日期 |
| length | 是 | int | 每页条数，小于2000 |
| page | 是 | int | 页码 |
| advertiserIds | 否 | array | 广告账号ID列表 |
| campaignIds | 否 | array | 推广系列ID列表 |
| adgroupIds | 否 | array | 广告组ID列表 |
| adIds | 否 | array | 广告ID列表 |

**关键返回字段**: adId, adName, adGroupId, campaignId, spend, impressions, clicks, orders, roas, status

---

## TikTok GMV Max

### queryGmvStoreList - 查询 GMV MAX 店铺列表

**路径**: `/basicOpen/multiplatform/ads/queryGmvStoreList`
**参数**: 无必填参数

**关键返回字段**: advertiserId, storeId, storeName

---

### queryGmvAdvertiserReportList - 查询 GMV MAX 广告账号报告

**路径**: `/basicOpen/multiplatform/ads/queryGmvAdvertiserReportList`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| startDate | 是 | string | 开始日期，yyyy-MM-dd，间隔不超过31天 |
| endDate | 是 | string | 结束日期 |
| length | 是 | int | 每页条数，小于2000 |
| page | 是 | int | 页码，从1开始 |
| advertiserIds | 否 | array | 广告账号ID列表 |
| gmvMaxPromotionTypeCodes | 否 | array | PRODUCT/LIVE |
| storeIds | 否 | array | 店铺ID列表 |
| summaryCurrency | 否 | string | 汇总币种，默认USD |

**关键返回字段**: subjectId, reportDate, cost, orders, roi, grossRevenue（唯一键：subjectId+reportDate）

---

### queryGmvCampaignReportList - 查询 GMV MAX 推广系列报告

**路径**: `/basicOpen/multiplatform/ads/queryGmvCampaignReportList`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| startDate | 是 | string | 开始日期，yyyy-MM-dd，间隔不超过31天 |
| endDate | 是 | string | 结束日期 |
| length | 是 | int | 每页条数，小于2000 |
| page | 是 | int | 页码，从1开始 |
| advertiserIds | 否 | array | 广告账号ID列表 |
| campaignIds | 否 | array | 推广系列ID列表 |
| gmvMaxPromotionTypeCodes | 否 | array | PRODUCT/LIVE |
| status | 否 | array | ENABLE/DISABLE/DELETE |

**关键返回字段**: subjectId, campaignId, reportDate, cost, orders, roi（唯一键：subjectId+reportDate）

---

### queryGmvItemGroupReportList - 查询 GMV MAX 广告商品报告

**路径**: `/basicOpen/multiplatform/ads/queryGmvItemGroupReportList`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| startDate | 是 | string | 开始日期，yyyy-MM-dd，间隔不超过31天 |
| endDate | 是 | string | 结束日期 |
| length | 是 | int | 每页条数，小于2000 |
| page | 是 | int | 页码 |
| advertiserIds | 否 | array | 广告账号ID列表 |
| itemGroupIds | 否 | array | 广告商品ID列表 |
| status | 否 | array | available/unavailable |

**关键返回字段**: subjectId, reportDate, grossRevenue, cost, orders, roi（唯一键：subjectId+reportDate）

---

## 沃尔玛广告 - SP 广告

### queryCampaignSpList - 查询 SP 广告活动

**路径**: `/basicOpen/multiplatform/ads/queryCampaignSpList`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| advertiserIds | 是 | array | 广告账号ID列表 |
| campaignType | 是 | array | sponsoredProducts-manual/sponsoredProducts-auto（SP必须且只能用这两个） |
| day | 是 | int | 归因天数：3/14/30 |
| startDate | 是 | string | 开始日期，yyyy-MM-dd，间隔不超过31天 |
| endDate | 是 | string | 结束日期 |
| operationSourceType | 是 | string | openapi调用传 gateway |
| pageNum | 是 | int | 页码，从1开始 |
| pageSize | 是 | int | 每页大小，小于2000 |
| paging | 是 | boolean | openapi必填 true |
| campaignIds | 否 | array | 广告活动ID列表 |
| status | 否 | array | enabled/paused/live/completed 等 |

**关键返回字段**: campaignId, campaignName, adSpend, numAdsShown, numAdsClicks, attributedSales, attributedOrders, acos, roas, cpc, ctr, status

---

### queryGroupSpList - 查询 SP 广告组

**路径**: `/basicOpen/multiplatform/ads/queryGroupSpList`
**参数**: 同 queryCampaignSpList（campaignIds 改为可选筛选项）

**关键返回字段**: adGroupId, adGroupName, campaignId, adSpend, attributedSales, acos, roas, status

---

### queryPageTypeSPList - 查询 SP 广告页面类型

**路径**: `/basicOpen/multiplatform/ads/queryPageTypeSPList`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| startDate | 否 | string | 开始日期，yyyy-MM-dd |
| endDate | 否 | string | 结束日期 |
| advertiserIds | 否 | array | 广告账号ID列表 |
| campaignType | 否 | array | 广告类型列表 |
| campaignIds | 否 | array | 广告活动ID列表 |
| day | 否 | int | 归因天数 |
| pageNum | 否 | int | 页码 |
| pageSize | 否 | int | 每页大小 |

**关键返回字段**: pageType, adSpend, numAdsShown, numAdsClicks, attributedSales, acos, roas

---

### reportAdItemSpList - 查询 SP 广告

**路径**: `/basicOpen/multiplatform/ads/reportAdItemSpList`
**参数**: 与 queryCampaignSpList 相同必填参数，另可加 adGroupIds 筛选

**关键返回字段**: adId, adGroupId, campaignId, adSpend, attributedSales, acos, roas, status

---

### reportKeywordSpList - 查询 SP 关键词

**路径**: `/basicOpen/multiplatform/ads/reportKeywordSpList`
**参数**: 与 queryCampaignSpList 相同必填参数

**关键返回字段**: keywordId, keywordText, matchType, adGroupId, adSpend, attributedSales, acos, roas

---

### reportPlatformSpList - 查询 SP 平台

**路径**: `/basicOpen/multiplatform/ads/reportPlatformSpList`
**参数**: 与 queryCampaignSpList 相同必填参数

**关键返回字段**: platform, adSpend, numAdsShown, numAdsClicks, attributedSales, acos, roas

---

## 沃尔玛广告 - SB 广告

### reportCampaignSbList - 查询 SB 广告活动

**路径**: `/basicOpen/multiplatform/ads/reportCampaignSbList`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| advertiserIds | 是 | array | 广告账号ID列表 |
| campaignType | 是 | array | ["sba"]（SB必须且只能用sba） |
| startDate | 是 | string | 开始日期，yyyy-MM-dd |
| endDate | 是 | string | 结束日期 |
| campaignIds | 否 | array | 广告活动ID列表 |
| day | 否 | int | 归因天数，默认14 |
| pageNum | 否 | int | 页码 |
| pageSize | 否 | int | 每页大小，最大200 |

**关键返回字段**: campaignId, campaignName, adSpend, attributedSales, acos, roas, ntbOrders, ntbRevenue, status

---

### reportAdGroupSbList - 查询 SB 广告组

**路径**: `/basicOpen/multiplatform/ads/reportAdGroupSbList`
**参数**: 与 reportCampaignSbList 相同必填参数，加 campaignIds 筛选

**关键返回字段**: adGroupId, adGroupName, campaignId, adSpend, attributedSales, acos, roas

---

### reportAdItemSbList - 查询 SB 广告

**路径**: `/basicOpen/multiplatform/ads/reportAdItemSbList`
**参数**: 与 reportAdGroupSbList 相同，加 adGroupIds 筛选

**关键返回字段**: adId, adGroupId, campaignId, adSpend, attributedSales, acos, roas

---

### reportKeywordSbList - 查询 SB 关键词

**路径**: `/basicOpen/multiplatform/ads/reportKeywordSbList`
**参数**: 与 reportCampaignSbList 相同必填参数

**关键返回字段**: keywordText, matchType, adSpend, attributedSales, acos, roas

---

### reportPageTypeSbList - 查询 SB 页面类型

**路径**: `/basicOpen/multiplatform/ads/reportPageTypeSbList`
**参数**: 与 reportCampaignSbList 相同必填参数

**关键返回字段**: pageType, adSpend, attributedSales, acos, roas

---

### reportPlatformSbList - 查询 SB 平台

**路径**: `/basicOpen/multiplatform/ads/reportPlatformSbList`
**参数**: 与 reportCampaignSbList 相同必填参数

**关键返回字段**: platform, adSpend, attributedSales, acos, roas

---

## 沃尔玛广告 - SV 广告

### queryAdGroupSvList - 查询 SV 广告组

**路径**: `/basicOpen/multiplatform/ads/queryAdGroupSvList`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| advertiserIds | 是 | array | 广告账号ID列表 |
| campaignType | 是 | array | ["video"]（SV必须且只能用video） |
| dateKey | 是 | string | day/week/month |
| startDate | 是 | string | 开始日期，yyyy-MM-dd |
| endDate | 是 | string | 结束日期 |
| campaignIds | 否 | array | 广告活动ID列表 |
| status | 否 | array | enabled/disabled/delete |
| pageNum | 否 | int | 页码，从1开始 |
| pageSize | 否 | int | 每页大小 |

**关键返回字段**: adGroupId, adGroupName, campaignId, adSpend, numAdsShown, numAdsClicks, attributedSales, acos, roas, status

---

### queryReportPageTypeSvList - 查询 SV 页面类型

**路径**: `/basicOpen/multiplatform/ads/queryReportPageTypeSvList`
**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| advertiserIds | 是 | array | 广告账号ID列表 |
| campaignType | 是 | array | ["video"] |
| startDate | 是 | string | 开始日期，yyyy-MM-dd |
| endDate | 是 | string | 结束日期 |
| pageType | 否 | array | browse/item/search/topic/category/homepage/other |
| day | 否 | int | 归因天数，默认14 |

**关键返回字段**: pageType, adSpend, numAdsShown, numAdsClicks, attributedSales, acos, roas

---

### reportAdItemSvList - 查询 SV 广告

**路径**: `/basicOpen/multiplatform/ads/reportAdItemSvList`
**参数**: advertiserIds(是), campaignType=["video"](是), startDate(是), endDate(是)，其他选填

**关键返回字段**: adId, adGroupId, campaignId, adSpend, attributedSales, acos, roas

---

### reportCampaignSvList - 查询 SV 广告活动

**路径**: `/basicOpen/multiplatform/ads/reportCampaignSvList`
**参数**: advertiserIds(是), campaignType=["video"](是), startDate(是), endDate(是)，其他选填

**关键返回字段**: campaignId, campaignName, adSpend, attributedSales, acos, roas, status

---

### reportKeywordSvList - 查询 SV 关键词

**路径**: `/basicOpen/multiplatform/ads/reportKeywordSvList`
**参数**: advertiserIds(是), campaignType=["video"](是), startDate(是), endDate(是)

**关键返回字段**: keywordText, matchType, adSpend, attributedSales, acos, roas

---

### reportPlatformSvList - 查询 SV 平台

**路径**: `/basicOpen/multiplatform/ads/reportPlatformSvList`
**参数**: advertiserIds(是), campaignType=["video"](是), startDate(是), endDate(是)

**关键返回字段**: platform, adSpend, attributedSales, acos, roas

---

### reportSearchTrendsList - 查询搜索趋势

**路径**: `/basicOpen/multiplatform/ads/reportSearchTrendsList`
**参数**: advertiserIds(是), startDate(是), endDate(是)，其他选填

**关键返回字段**: searchTerm, impressions, clicks, adSpend, reportDate

---
