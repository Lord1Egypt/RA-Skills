# 领星新广告-报告接口参考

所有接口均为 POST 请求，请求域名：`https://openapi.lingxing.com`

## 通用请求头

| 标签 | 必填 | 说明 |
|------|------|------|
| X-API-VERSION | 是 | 固定传 `2`（offset 为偏移量，从0开始） |

## 通用参数规律

- `sid` 或 `profile_id` 二选一必填（部分接口仅需其中一个）
- `report_date`：报告日期，格式 `Y-m-d`，多数报表类接口必填
- `offset`：分页偏移量，从 0 开始，默认 0
- `length`：每页条数，默认 15，建议传 100

---

## SP 广告报表

### spCampaignReports - SP广告活动报表
**路径**: `/pb/openapi/newad/spCampaignReports`
**参数**:
| 参数 | 必填 | 说明 |
|------|------|------|
| sid | 是* | 店铺ID |
| profile_id | 是* | 广告账号ID（与sid二选一） |
| report_date | 是 | 报告日期 Y-m-d |
| show_detail | 否 | 1=返回1d/7d/14d/30d归因期数据 |
| offset | 否 | 分页偏移量 |
| length | 否 | 每页条数 |

**关键返回字段**: targeting_type, impressions, clicks, cost, same_orders, orders, same_sales, sales, units, same_units, campaign_id, profile_id, report_date

---

### campaignPlacementReports - SP广告位报告
**路径**: `/pb/openapi/newad/campaignPlacementReports`
**参数**: 与 spCampaignReports 相同
**关键返回字段**: placement（广告位），impressions, clicks, cost, orders, sales, units, campaign_id

---

### spAdGroupReports - SP广告组报表
**路径**: `/pb/openapi/newad/spAdGroupReports`
**参数**: 与 spCampaignReports 相同
**关键返回字段**: ad_group_id, campaign_id, impressions, clicks, cost, orders, sales, units

---

### spProductAdReports - SP广告商品报表
**路径**: `/pb/openapi/newad/spProductAdReports`
**参数**: 与 spCampaignReports 相同，新增可选 `ad_group_id`
**关键返回字段**: ad_id, asin, sku, ad_group_id, campaign_id, impressions, clicks, cost, orders, sales, units

---

### spKeywordReports - SP关键词报表
**路径**: `/pb/openapi/newad/spKeywordReports`
**参数**: 与 spCampaignReports 相同
**关键返回字段**: keyword_id, keyword_text, match_type, ad_group_id, campaign_id, impressions, clicks, cost, orders, sales

---

### spTargetReports - SP商品定位报表
**路径**: `/pb/openapi/newad/spTargetReports`
**参数**: 与 spCampaignReports 相同
**关键返回字段**: target_id, targeting_expression, targeting_type, ad_group_id, campaign_id, impressions, clicks, cost, orders, sales

---

### asinReports - SP已购买商品报表
**路径**: `/pb/openapi/newad/asinReports`
**参数**: sid/profile_id, report_date, offset, length
**关键返回字段**: asin, other_asin, campaign_id, ad_group_id, impressions, clicks, purchases_1d/7d/14d/30d, sales_1d/7d/14d/30d

---

### queryWordReports - SP用户搜索词报表
**路径**: `/pb/openapi/newad/queryWordReports`
**参数**: 与 spCampaignReports 相同
**关键返回字段**: query, keyword_id, targeting_id, match_type, impressions, clicks, cost, orders, sales, units

---

## SB 广告报表

### hsaCampaignReports - SB广告活动报表
**路径**: `/pb/openapi/newad/hsaCampaignReports`
**参数**: sid/profile_id, report_date, offset, length
**关键返回字段**: campaign_id, impressions, clicks, cost, attributedOrdersNewToBrand14d, attributedSales14d

---

### hsaCampaignPlacementReports - SB广告活动-广告位报告
**路径**: `/pb/openapi/newad/hsaCampaignPlacementReports`
**参数**: sid/profile_id, report_date, offset, length
**关键返回字段**: placement, campaign_id, impressions, clicks, cost, dpv, orders, sales

---

### hsaAdGroupReports - SB广告组报表
**路径**: `/pb/openapi/newad/hsaAdGroupReports`
**参数**: sid/profile_id, report_date, offset, length
**关键返回字段**: ad_group_id, campaign_id, impressions, clicks, cost

---

### listHsaTargetingReport - SB广告的投放报告
**路径**: `/pb/openapi/newad/listHsaTargetingReport`
**参数**: sid/profile_id, report_date, offset, length
**关键返回字段**: keyword_id/target_id, keyword_text, match_type, campaign_id, impressions, clicks, cost, dpv, orders, sales

---

### hsaQueryWordReports - SB用户搜索词报表
**路径**: `/pb/openapi/newad/hsaQueryWordReports`
**参数**: 与 spCampaignReports 相同
**关键返回字段**: query, impressions, clicks, cost, orders_14d, sales_14d

---

### hsaPurchasedAsinReports - SB广告归因于广告的购买报告
**路径**: `/pb/openapi/newad/hsaPurchasedAsinReports`
**参数**: sid/profile_id, report_date, offset, length
**关键返回字段**: asin, promoted_asin, campaign_id, purchases_14d, sales_14d, units_14d

---

### listHsaProductAdReport - SB广告创意报告
**路径**: `/pb/openapi/newad/listHsaProductAdReport`
**参数**: sid/profile_id, report_date, offset, length
**关键返回字段**: ad_id, asin, ad_group_id, campaign_id, impressions, clicks, cost, orders_14d, sales_14d

---

### listHsaKeywordPlacementReport - SB关键词-广告位报告
**路径**: `/pb/openapi/newad/listHsaKeywordPlacementReport`
**参数**: sid/profile_id, report_date, offset, length
**关键返回字段**: keyword_id, placement, campaign_id, impressions, clicks, cost

---

## SD 广告报表

### sdCampaignReports - SD广告活动报表
**路径**: `/pb/openapi/newad/sdCampaignReports`
**参数**: sid/profile_id, report_date, tactic（可选，T00001/T00002/T00003), offset, length
**关键返回字段**: campaign_id, tactic, impressions, clicks, cost, orders, sales, view_impressions

---

### sdAdGroupReports - SD广告组报表
**路径**: `/pb/openapi/newad/sdAdGroupReports`
**参数**: 与 sdCampaignReports 相同
**关键返回字段**: ad_group_id, campaign_id, tactic, impressions, clicks, cost, orders, sales

---

### sdProductAdReports - SD广告商品报表
**路径**: `/pb/openapi/newad/sdProductAdReports`
**参数**: 与 sdCampaignReports 相同
**关键返回字段**: ad_id, asin, sku, ad_group_id, campaign_id, impressions, clicks, cost, orders, sales

---

### sdTargetReports - SD商品定位报表
**路径**: `/pb/openapi/newad/sdTargetReports`
**参数**: sid/profile_id, report_date, offset, length
**关键返回字段**: target_id, ad_group_id, campaign_id, impressions, clicks, cost, orders, sales

---

### sdAsinReports - SD已购买商品报表
**路径**: `/pb/openapi/newad/sdAsinReports`
**参数**: sid/profile_id, report_date, tactic, offset, length
**关键返回字段**: asin, promoted_asin, other_asin, campaign_id, purchases_1d/7d/14d/30d

---

### sdMatchTargetReports - SD匹配的目标报表
**路径**: `/pb/openapi/newad/sdMatchTargetReports`
**参数**: 与 sdCampaignReports 相同
**关键返回字段**: targeting_expression, targeting_type, targeting_text, target_id, ad_group_id, campaign_id

---

## 小时数据接口（SP/SB/SD）

所有小时数据接口参数格式一致：

| 参数 | 必填 | 说明 |
|------|------|------|
| sid 或 profile_id | 是* | 店铺ID或广告账号ID |
| report_date | 是 | 报告日期 Y-m-d |
| offset | 否 | 分页偏移量 |
| length | 否 | 每页条数 |

| 接口名 | 路径 | 说明 |
|--------|------|------|
| spCampaignHourData | /pb/openapi/newad/spCampaignHourData | SP广告活动小时数据 |
| spAdPlacementHourData | /pb/openapi/newad/spAdPlacementHourData | SP广告位小时数据 |
| spAdGroupHourData | /pb/openapi/newad/spAdGroupHourData | SP广告组小时数据 |
| spAdvertiseHourData | /pb/openapi/newad/spAdvertiseHourData | SP广告小时数据 |
| spTargetHourData | /pb/openapi/newad/spTargetHourData | SP投放小时数据 |
| sbCampaignHourData | /pb/openapi/newad/sbCampaignHourData | SB广告活动小时数据 |
| sbAdGroupHourData | /pb/openapi/newad/sbAdGroupHourData | SB广告组小时数据 |
| sbTargetHourData | /pb/openapi/newad/sbTargetHourData | SB投放小时数据 |
| sbAdPlacementHourData | /pb/openapi/newad/sbAdPlacementHourData | SB广告位小时数据 |
| sdCampaignHourData | /pb/openapi/newad/sdCampaignHourData | SD广告活动小时数据 |
| sdAdGroupHourData | /pb/openapi/newad/sdAdGroupHourData | SD广告组小时数据 |
| sdAdvertiseHourData | /pb/openapi/newad/sdAdvertiseHourData | SD广告小时数据 |
| sdTargetHourData | /pb/openapi/newad/sdTargetHourData | SD投放小时数据 |

**小时数据关键返回字段**: `hour`（0-23的小时段），加各指标数据

---

## 其他接口

### dspReportOrderList - 查询DSP报告列表-订单
**路径**: `/basicOpen/dspReport/order/list`
**参数**:
| 参数 | 必填 | 说明 |
|------|------|------|
| profile_id | 是 | DSP广告账号ID（仅支持profile_id，不支持sid） |
| start_date | 是 | 开始日期 Y-m-d |
| end_date | 是 | 结束日期 Y-m-d |
| offset | 否 | 分页偏移量 |
| length | 否 | 每页条数（默认20） |

---

### ProductAnalysisList - 出单时段分析-产品
**路径**: `/basicOpen/adReport/productOrderAnalysis/list`
**参数**:
| 参数 | 必填 | 说明 |
|------|------|------|
| sid 或 profile_id | 是* | 店铺ID或广告账号ID |
| start_date | 是 | 开始日期 Y-m-d |
| end_date | 是 | 结束日期 Y-m-d |
| msku | 否 | MSKU 筛选 |
| asin | 否 | ASIN 筛选 |
| offset | 否 | 分页偏移量 |
| length | 否 | 每页条数 |

---

## 通用返回结构

```json
{
  "code": 0,
  "message": "操作成功",
  "error_details": [],
  "request_id": "xxx",
  "response_time": "2024-01-01 12:00:00",
  "total": 100,
  "data": [...]
}
```

`code=0` 为成功，其他为失败。
