# Data Contract

本文档定义 `property-advisor` 的编排层如何消费房源数据，以及如何保留原始快照。

核心原则：

- 上游房源数据尽量原样保留
- 编排层可以新增派生字段，但不能丢原始字段
- 最终展示和 join 逻辑必须优先依赖原始链接和标识符
- 同一份 contract 同时适用于 `ok-core-skill` 和 `gt-core-skill`

## 1. ListingList

房源搜索返回的最小列表结构。

```json
{
  "total": 25,
  "listings": [
    {
      "id": "listing_001",
      "listing_id": "123456",
      "title": "The Archive, Southbank",
      "price": "A$786/wk",
      "location": "Southbank VIC",
      "url": "https://example.test/archive",
      "image_url": "https://example.test/archive.jpg"
    }
  ]
}
```

### 必保字段

| 字段 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| `title` | string | 是 | 房源标题 |
| `price` | string | 是 | 原始价格文本 |
| `location` | string | 是 | 区域或地址文本 |
| `url` | string | 是 | 原帖链接 |
| `image_url` | string \| null | 否 | 封面图 |
| `listing_id` | string \| null | 否 | 平台唯一 ID |
| `id` | string \| null | 否 | 编排层可用的稳定 ID |

## 2. ListingDetail

详情页补全后允许增加：

- `description`
- `images`
- `seller_name`
- `posted_time`
- `category`
- `address`
- `lat`
- `lng`
- `geo_precision`
- `attributes`
- `bedrooms_text`
- `bathrooms_text`
- `property_type`
- `date_available`
- `seller_type`

详情补全失败时，编排层必须保留原列表数据并显式标记 `detail_fetched=false`。
如果是 GT API 降级链路，必须额外保留 `detail_degraded_reason`。

## 3. RawListingSnapshot

编排层在搜索后必须落原始房源快照。

```json
{
  "id": "listing_archive",
  "listing_id": null,
  "title": "The Archive, Southbank",
  "price": "A$786/wk",
  "location": "Southbank VIC",
  "url": "https://example.test/archive",
  "image_url": "https://example.test/archive.jpg",
  "images": ["https://example.test/archive.jpg"],
  "description": "1 bedroom apartment with study...",
  "detail_fetched": true,
  "monthly_price_value": 3403.38,
  "inferred_bedrooms": 1
}
```

### RawListingSnapshot 必保字段

| 字段 | 说明 |
| --- | --- |
| `id` | 编排层 join 主键 |
| `listing_id` | 上游平台 ID |
| `title` | 原始标题 |
| `price` | 原始价格文本 |
| `location` | 原始位置文本 |
| `url` | 原帖链接 |
| `image_url` / `images` | 原始图片信息 |
| `description` | 详情描述 |
| `detail_fetched` | 是否成功补齐详情 |
| `raw` | 原始 payload 回显 |

### 允许的派生字段

- `monthly_price_value`
- `price_value`
- `price_currency`
- `price_period`
- `inferred_bedrooms`
- `image_count`
- `has_placeholder_image`

### 市场 / source 来源字段

- `request.resolved_market`: `ok` 或 `gt`
- `request.resolved_source_id`: 当前实际路由到的 source adapter；第一版 OK/GT adapter 分别委托 `ok-core-skill` / `gt-core-skill`
- `raw.source_market`: 上游来源市场
- `raw.source_runtime_mode`: `ok` / `bridge` / `api`
- `raw.source_routing_reason`: 路由命中原因

注意：`property-advisor` 自身不内建各平台爬虫。source 字段表示编排层选择了哪个 adapter；真实抓取能力来自对应上游 skill / plugin / client。

## 4. Join 规则

编排层把房源结果与地图结果合并时，固定按下面顺序 join：

1. `id`
2. `listing_id`
3. `url`
4. `title + location` 仅作为最后兜底

如果原帖链接缺失：

- 仍可保留在 `raw_listing_snapshots`
- 但不能进入最终候选表点名展示

## 5. CandidateDecisionRow

最终展示层消费的固定结构：

```json
{
  "candidate_name": "The Archive, Southbank",
  "status": "可继续关注",
  "price": "A$786/wk",
  "location": "Southbank VIC",
  "satisfied": ["预算内", "已补齐房源详情"],
  "missing_or_unknown": ["面积待确认", "卫浴数待确认"],
  "elimination_or_risk": ["环境风险偏高，需重点核对主路/轨道/工业干扰。"],
  "listing_url": "https://example.test/archive"
}
```

### 固定 8 列

| 字段 | 说明 |
| --- | --- |
| `candidate_name` | 候选房源 |
| `status` | 推荐 / 可继续关注 / 待补地图 / 待人工复核 / 淘汰 |
| `price` | 原始价格文本 |
| `location` | 原始位置文本 |
| `satisfied` | 已满足项 |
| `missing_or_unknown` | 缺失/未知项 |
| `elimination_or_risk` | 淘汰原因或风险 |
| `listing_url` | 原帖链接 |

## 6. Fail-Closed 规则

- 缺少原帖链接的候选不能点名展示
- 这类候选必须进入 `hidden_candidates`
- `hidden_candidates` 只能汇总提示，不能伪装成正常候选行
