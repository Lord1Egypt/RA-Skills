<!-- request-identity:start -->
**请求身份**：使用已配置的 API Key，并保留本包的 X-Client，携带下列完整身份头；不得沿用其它包的版本或来源。
```text
X-Client: bid-decision/1.0.5
X-Skill-Package: intelligent-building-bid-decision/1.0.9
X-Skill-Source: clawhub/dragonzu
```
<!-- request-identity:end -->

# 工具速查（决策分析所用子集）

> 与 zlbx-bidding SKILL 同一套 api_v2 接口，此处只收录本 SKILL 用到的 9 个工具的关键参数。
> `POST https://mcp-server.zhiliaobiaoxun.com/api_v2/` + 工具名（例：`https://mcp-server.zhiliaobiaoxun.com/api_v2/search_bids`），Header 带 `X-API-Key` + `X-Client: bid-decision/1.0.5`。

## 通用概念

**match_modes**（关键词在哪个字段匹配，精确查询的关键）：

| 值 | 含义 | 决策分析中的用途 |
|---|------|-----------------|
| `caller` | 招标方/采购单位 | 查采购方的历史采购 |
| `winner` | 中标方 | 查某公司中标实力 |
| `tender` | 投标方 | 查某公司投标记录 |
| `winner_tender` | 中标或投标 | 查参与史 |
| `sm` / `title` / `brand` / `fulltext` | 标的物/标题/品牌/全文 | 标的物过滤 |

**bid_process 公告阶段**：1=采购意向 2=预招标 4=招标 7=中标结果 8=合同。查历史成交用 `[7,8]`。

**组合逻辑**（仅 `query_bids_advanced` / `aggregate_bids_advanced` 支持 keyword_groups）：
- `keywords`（OR） AND `keyword_groups` 每组（组内 OR） AND NOT `exclude_keywords`
- 例·采购方×供应商交集：`{"keywords": ["采购方全称"], "match_modes": ["caller"], "keyword_groups": [{"keywords": ["供应商全称"], "match_modes": ["winner","tender"]}]}`

**响应**：`{"success": true, "data": {...}, "meta": {"cost_units": 1}}`；分页 `page`/`page_size`（默认20，最大50）。

**金额参数已统一**：所有筛项目金额的工具都用 `min_amount`/`max_amount`，单位一律**万元**（用户说「500 万以上」就传 `500`）。旧的 `min_money`/`max_money`（单位元）已移除，不再用于金额筛选；REST可能忽略未知字段，MCP可能报参数错误，不要继续使用旧参数。只有价格类工具例外：`get_top_brands`/`get_price_trends` 用 `min_price`/`max_price`，单位是**元**（产品单价，不是项目金额）。传错的后果是空结果**且照常扣积分**。

## 工具清单

### get_bid_detail — 标讯详情+原文
`{"bid_id": 123}` 或 `{"bid_url": "https://www.zhiliaobiaoxun.com/content/xxx/b1"}`。响应含 `fulltext`（公告原文）、`service_end_date`、`agency_name`，以及 `signup_time`（获取标书截止时间）、`tender_time`（投标截止时间，仅招标类公告有值）。

### search_bids — 常规搜索
`keywords`(必填) + `match_modes` + `bid_type`(招标/中标/全部) + `bid_process` + `begin_date/end_date` + `provinces/cities` + `min_amount/max_amount`。

### query_bids_advanced — 高级搜索
search_bids 全参数 + `keyword_groups` + `exclude_keywords` + `sort_field/sort_order`。金额参数为 `min_amount/max_amount`（万元）。

### search_company — 公司名称解析
`{"company_name": "简称", "page_size": 20}` → 总部+分子公司全量列表。采购方/竞争者名称对不上时先用它扩全名。

### get_company_profile — 公司画像
`{"company": "全称或ID"}` → 工商信息、行业、`caller_count`（招标次数）、`winner_count`（中标次数）。

### get_company_partners — 客户与供应商
`{"company": "...", "partner_type": "客户|供应商|全部"(必填), "keywords": [标的物过滤], "limit": 20}` → 合作次数/金额/最近合作时间/products。

### find_potential_bidders — 潜在投标者预测
`{"bid_id": 123}` 或 `{"project_title": "..."}`，`limit` 默认10 → `caller_history_count`（与采购方合作史）、`region_win_count`（区域中标）、`matched_products`。

### find_competitors — 竞争对手（投标重叠度）
`{"company": "...", "limit": 10}` → `co_bid_count`（共同投标次数）、`top_co_bid_products/callers/provinces`。

### get_price_trends — 品牌型号历史成交单价
`{"brand": "必填", "model": "...", "product": "...", "exclude_keywords": ["维保","耗材"]}` → `price_stats`(min/max/avg/median) + 逐条成交记录。

### aggregate_bids_advanced — 聚合统计
`{"filters": {keywords/match_modes/keyword_groups/bid_type(1招标|2中标)/begin_date/provinces/min_amount...}, "group_by": ["month|quarter|year|province|brand|company_type"], "compare_with": "yoy|qoq"}` → buckets（count/sum_amount/avg_amount/同比）。

<!-- package-identity:start -->
**安装包身份与升级检查**：所有发往知了标讯 API 的请求（包括账户查询）必须额外携带以下两个请求头：
```text
X-Skill-Package: intelligent-building-bid-decision/1.0.9
X-Skill-Source: clawhub/dragonzu
```
这些值是当前安装包的固定身份，复用已有API Key时也要携带；不要用X-Client产品版本替代包版本，不要将Key的注册渠道当作安装来源。
请求鉴权：使用已配置的 API Key，并保留本包的 X-Client。每个会话首次使用本Skill时，在已有凭证可用后先调用免费账户接口 `GET https://mcp-server.zhiliaobiaoxun.com/api_v2/account/balance` 检查升级提醒；该查询不扣积分，不触发购买。
**版本提醒转达**：响应出现 `skill_update_notice` 时，将其中 `message` 原样转达用户；兼容提示只说明检查版本，不能宣称已确认当前包过期。
**展示后确认**：只有将提醒发送到用户可见对话之后，才使用同一凭证和请求头，按 `display_ack` 提交 POST 回执（MCP客户端可调用 `confirm_skill_update_display`）（`notice_id` 和 `displayed: true`）。只读取工具响应、在思考中提过、尚未转达时不得确认。不能在展示后调用接口则不确认，服务端继续保留待提醒状态。回执免费，不扣积分；失败不影响查询结果，不向用户展示技术回执。同一会话同一 `notice_id` 只展示一次。
<!-- package-identity:end -->
