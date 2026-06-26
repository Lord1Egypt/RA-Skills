# Map Context Contract

本文档定义 `property-advisor` 如何显式调用并消费 `public-osm-map-context-skill`。

## 1. 调用方式

父 skill 不应依赖 nested skill 自动发现。

推荐调用：

```bash
python3 public-osm-map-context-skill/scripts/cli.py analyze-batch \
  --input listings.json \
  --destination "Melbourne CBD VIC" \
  --city melbourne
```

## 2. 输入要求

地图 skill 接收房源列表，最少包含：

```json
{
  "listings": [
    {
      "id": "listing_archive",
      "listing_id": null,
      "title": "The Archive, Southbank",
      "price": "A$786/wk",
      "location": "Southbank VIC",
      "url": "https://example.test/archive",
      "image_url": "https://example.test/archive.jpg",
      "description": "1 bedroom apartment ..."
    }
  ]
}
```

如果 `address` 缺失，地图 skill 应继续基于 `title`、`location`、`description` 做 best-effort 地址提取。

## 3. 输出要求

地图 skill 必须继续保留原始上下文字段：

- `listing_ref`
- `geo`
- `amenities`
- `transit_access`
- `risk_signals`
- `verification_links`
- `limitations`

同时新增固定 `assessments` 结构：

```json
{
  "assessments": {
    "transport_access": {
      "conclusion": "交通条件已有地址级 OSM 证据，可用于首轮排序。",
      "evidence": ["到 OSM 记录的 Normanby Road Tram Stop 直线估算约 50-100m。"],
      "confidence": "medium",
      "limitations": ["straight_line_estimate_only"]
    },
    "daily_convenience": {
      "conclusion": "生活便利度中等，能满足基础日常需求。",
      "evidence": ["800m 范围内记录到超市 1 家。"],
      "confidence": "medium",
      "limitations": []
    },
    "environment_risk": {
      "conclusion": "环境风险偏高，需重点核对主路/轨道/工业干扰。",
      "evidence": ["最近主路信号约 94m。"],
      "confidence": "medium",
      "limitations": []
    },
    "area_maturity": {
      "conclusion": "区域成熟度中等。",
      "evidence": ["当前片区公开 OSM 记录到的常用配套总量约 5 项。"],
      "confidence": "medium",
      "limitations": []
    }
  }
}
```

## 4. 四个固定维度

### `transport_access`

必须覆盖：

- 最近站点
- 到目标地的估算
- 精度边界

### `daily_convenience`

必须把超市、药店、餐饮等统计转成便利度结论，不能只返回计数。

### `environment_risk`

必须把主路、铁路、工业用地信号转成风险结论，不能只返回 raw distance。

### `area_maturity`

用于描述片区成熟度。`precision=area` 时只能做片区判断，不能写成楼栋级结论。

## 5. 低置信和降级规则

### `precision=address`

- 可作为首轮排序依据
- 仍须保留 `straight_line_estimate` 的局限说明

### `precision=area`

- assessments 只能写片区级结论
- 不能输出楼栋级步行距离
- 编排层通常应把候选状态降级为 `待人工复核`

### `precision=missing`

- assessments 必须显式返回“自动定位失败，需要人工复核”
- 仍需提供 `verification_links.google_maps_manual`

## 6. 链接规则

- `listing_ref.url` 是原帖链接兜底
- `verification_links.google_maps_manual` 只能作为地图复核链接
- 任何被点名展示的候选都必须有原帖链接

如果地图结果带有 `original_listing_url_missing`：

- 编排层不得点名展示该候选
- 只能把它放进 `hidden_candidates`
