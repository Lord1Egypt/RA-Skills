# 领星新广告基础数据接口参考（newAd/baseData）

所有接口均为 POST 请求，域名：`https://openapi.lingxing.com`
所有接口均为**只读查询**，令牌桶容量 10（`sbDivideAsinReports` 为 1）。
`sid` 与 `profile_id` 二选一必填（`dspAccountList` 除外）。

---

## dspAccountList - 查询广告账号列表

**路径**: `/basicOpen/baseData/account/list`（特殊路径）

**参数**:
| 参数 | 必填 | 类型 | 说明 |
|------|------|------|------|
| type | 是 | string | `dsp` / `seller` / `vendor` |
| offset | 否 | int | 分页偏移，默认 0 |
| length | 否 | int | 每页条数，默认 20 |

**关键返回字段**: profile_id, sid, name, type, country_code, currency_code, status(-1删除/0停止/1正常/2授权异常)

---

## portfolios - 广告组合

**路径**: `/pb/openapi/newad/portfolios`

**参数**: sid/profile_id, offset, length, next_token

**关键返回字段**: portfolio_id, profile_id, name, state, budget(amount/policy/startDate/endDate), in_budget, serving_status

---

## SP 广告基础数据（6个）

### spCampaigns - SP广告活动

**路径**: `/pb/openapi/newad/spCampaigns`

**参数**: sid/profile_id, state(enabled/paused/archived), offset, length, next_token

**关键返回字段**: campaign_id, profile_id, name, targeting_type(auto/manual), state, serving_status, daily_budget, start_date, end_date, bidding(strategy/adjustments), portfolio_id, tags

---

### spAdGroups - SP广告组

**路径**: `/pb/openapi/newad/spAdGroups`

**参数**: sid/profile_id, state, campaign_id(可选), offset, length, next_token

**关键返回字段**: ad_group_id, campaign_id, profile_id, name, default_bid, state, serving_status, bid_optimization

---

### spProductAds - SP广告商品

**路径**: `/pb/openapi/newad/spProductAds`

**参数**: sid/profile_id, state, ad_group_id(可选), offset, length, next_token

**关键返回字段**: ad_id, campaign_id, ad_group_id, profile_id, sku, asin, state, serving_status

---

### spKeywords - SP关键词

**路径**: `/pb/openapi/newad/spKeywords`

**参数**: sid/profile_id, state, campaign_id(可选), ad_group_id(可选), offset, length, next_token

**关键返回字段**: keyword_id, campaign_id, ad_group_id, profile_id, keyword_text, match_type(exact/phrase/broad), bid, state, serving_status

---

### spTargets - SP商品定位

**路径**: `/pb/openapi/newad/spTargets`

**参数**: sid/profile_id, state, campaign_id(可选), ad_group_id(可选), offset, length, next_token

**关键返回字段**: target_id, campaign_id, ad_group_id, profile_id, expression_type(auto/manual), expression, resolved_expression, bid, state, serving_status

---

### spNegativeTargetsOrKeywords - SP否定投放

**路径**: `/pb/openapi/newad/spNegativeTargetsOrKeywords`

**参数**: sid/profile_id, campaign_id(可选), ad_group_id(可选), offset, length, next_token

**关键返回字段**: campaign_id, ad_group_id, profile_id, negative_type(negativeKeyword/negativeAsin/negativeBrand), negative_text, negative_match_type, state

---

## SB 广告基础数据（5个）

### hsaCampaigns - SB广告活动

**路径**: `/pb/openapi/newad/hsaCampaigns`

**参数**: sid/profile_id, state, offset, length, next_token

**关键返回字段**: campaign_id, profile_id, name, budget, budget_type, state, serving_status, start_date, landing_page, bid_multiplier

---

### hsaAdGroups - SB广告组

**路径**: `/pb/openapi/newad/hsaAdGroups`

**参数**: sid/profile_id, state, campaign_id(可选), offset, length, next_token

**关键返回字段**: ad_group_id, campaign_id, profile_id, name, state, serving_status

---

### hsaProductAds - SB广告创意

**路径**: `/pb/openapi/newad/hsaProductAds`

**参数**: sid/profile_id, offset, length, next_token

**关键返回字段**: ad_id, campaign_id, ad_group_id, profile_id, state, creative(广告创意结构)

---

### sbTargeting - SB广告投放

**路径**: `/pb/openapi/newad/sbTargeting`

**参数**: sid/profile_id, ads_type(SB/SBV/ALL), state, offset, length, next_token

**关键返回字段**: campaign_id, ad_group_id, keyword_id, keyword_text, keyword_bid, match_type, target_id, expression, target_bid, target_state, resolved_expression

---

### hsaNegativeKeywords - SB否定关键词

**路径**: `/pb/openapi/newad/hsaNegativeKeywords`

**参数**: sid/profile_id, state, campaign_id(可选), offset, length, next_token

**关键返回字段**: keyword_id, campaign_id, ad_group_id, profile_id, keyword_text, match_type, state

---

### hsaNegativeTargets - SB否定商品投放

**路径**: `/pb/openapi/newad/hsaNegativeTargets`

**参数**: sid/profile_id, state, campaign_id(可选), offset, length, next_token

**关键返回字段**: target_id, campaign_id, ad_group_id, profile_id, expression_type, expression, resolved_expression, state

---

### sbDivideAsinReports - SB分摊

**路径**: `/pb/openapi/newad/sbDivideAsinReports`
**令牌桶容量**: 1

**参数**: profile_id(必填，不支持sid), report_date(Y-m-d), offset, length, next_token

---

## SD 广告基础数据（5个）

### sdCampaigns - SD广告活动

**路径**: `/pb/openapi/newad/sdCampaigns`

**参数**: sid/profile_id, state, offset, length, next_token

**关键返回字段**: campaign_id, profile_id, name, tactic(T00001/T00020/T00030), cost_type, budget_type, budget, state, serving_status, start_date

---

### sdAdGroups - SD广告组

**路径**: `/pb/openapi/newad/sdAdGroups`

**参数**: sid/profile_id, state, campaign_id(可选), offset, length, next_token

**关键返回字段**: ad_group_id, campaign_id, profile_id, name, default_bid, state, serving_status, bid_optimization

---

### sdProductAds - SD广告商品

**路径**: `/pb/openapi/newad/sdProductAds`

**参数**: sid/profile_id, state, ad_group_id(可选), offset, length, next_token

**关键返回字段**: ad_id, ad_group_id, campaign_id, profile_id, sku, asin, state, serving_status

---

### sdTargets - SD商品定位

**路径**: `/pb/openapi/newad/sdTargets`

**参数**: sid/profile_id, state, campaign_id(可选), offset, length, next_token

**关键返回字段**: target_id, campaign_id, ad_group_id, profile_id, expression_type, expression, resolved_expression, bid, state, serving_status

---

### sdNegativeTargets - SD否定商品定位

**路径**: `/pb/openapi/newad/sdNegativeTargets`

**参数**: sid/profile_id, state, campaign_id(可选), offset, length, next_token

**关键返回字段**: target_id, campaign_id, ad_group_id, profile_id, expression_type, expression, resolved_expression, state

---

## 通用说明

- `state` 过滤：`enabled` / `paused` / `archived`，不传返回全部
- `next_token` 分页游标：与 `offset` 同时传时以 `next_token` 为准，推荐优先用 `next_token`
- `sbDivideAsinReports` 仅支持 `profile_id`，不支持 `sid`，且令牌桶容量仅 1，需串行调用
