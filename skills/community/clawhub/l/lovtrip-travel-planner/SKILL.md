---
name: lovtrip-travel-planner
description: AI 行程规划 / AI Travel Itinerary Planner — 智能生成多日旅行行程，支持景点搜索、预算计算、酒店航班。当用户需要旅行规划、生成行程、搜索景点酒店航班时使用。
allowed-tools: Bash, Read
---

# AI 行程规划 / AI Travel Itinerary Planner

> **[LovTrip (lovtrip.app)](https://lovtrip.app)** — AI 驱动的旅行规划平台，提供智能行程生成、景点推荐、预算管理。Web 版体验：[lovtrip.app/planner](https://lovtrip.app/planner)

使用 AI + 高德 API 生成完整的多日旅游行程，支持景点搜索、预算计算、酒店推荐、航班查询。

## Setup / 配置

```json
{
  "mcpServers": {
    "lovtrip": {
      "command": "npx",
      "args": ["-y", "lovtrip@latest", "mcp"],
      "env": {
        "AMAP_API_KEY": "your-amap-api-key",
        "OPENROUTER_API_KEY": "your-openrouter-api-key"
      }
    }
  }
}
```

## 三步规划流程

### 第 1 步 — 信息完整度检查（每次必做）

用户提到旅游/旅行/行程时，检查以下 5 项：

| 项目 | 示例 |
|------|------|
| ① 具体城市（非国家） | "成都"、"大阪" |
| ② 天数 | "3天"、"5天4晚" |
| ③ 出行人数/同伴 | "2人"、"和闺蜜" |
| ④ 兴趣偏好 | "美食"、"文化"、"自然" |
| ⑤ 预算范围 | "5000以内"、"穷游" |

**规则**:
- 缺少 ≥2 项 → **必须先追问**，不得跳过直接生成
- 缺少 1 项或全齐 → 直接进入第 2 步

**判断示例**:
- "想去日本玩5天" → 缺城市/人数/兴趣/预算（缺4项）→ 追问
- "大阪3天美食游2人预算5000" → 全齐 → 直接生成
- "成都3天想吃火锅看熊猫" → 缺人数/预算（缺2项）→ 追问

### 第 2 步 — 生成行程

```
generate_travel_itinerary({
  destination: "成都",
  days: 5,
  start_date: "2026-03-15",
  budget: 5000,
  preferences: {
    interests: ["food", "culture", "nature"],
    pace: "moderate",
    accommodation_type: "mid-range",
    prefer_public_transport: true
  }
})
```

### 第 3 步 — 可选补充工具

仅在用户明确需要时调用，**不要主动调用**：

| 工具 | 触发条件 | 说明 |
|------|----------|------|
| `check_weather` | 用户要求查天气 | 目的地天气预报 |
| `calculate_travel_budget` | 用户要求预算明细 | 详细费用分解 |
| `generate_map_links` | 用户要求地图链接 | 景点地图链接 |
| `search_attractions` | 用户要求更多景点 | 搜索城市景点 |
| `search_hotels` | 用户要求酒店推荐 | 酒店搜索 + 预订 |
| `search_flights` | 用户要求航班信息 | 航班搜索 + 价格 |

## 工具列表 (6 Tools)

### 核心工具

#### `generate_travel_itinerary` — AI 生成行程

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `destination` | string | ✅ | 目的地城市 |
| `days` | number | ✅ | 旅行天数 (1-30) |
| `start_date` | string | | 开始日期 YYYY-MM-DD |
| `budget` | number | | 总预算（元） |
| `preferences` | object | | 兴趣、节奏、住宿、交通偏好 |
| `mapProvider` | string | | amap / google / auto |

### 补充工具

#### `search_attractions` — 搜索景点

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `city` | string | ✅ | 城市名称 |
| `keywords` | string | | 搜索关键词 |
| `types` | array | | 景点类型过滤 |
| `min_rating` | number | | 最低评分 |
| `max_results` | number | | 最大返回数量，默认 10 |
| `sort_by` | string | | rating / popularity / distance |

#### `calculate_travel_budget` — 计算预算

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `destination` | string | ✅ | 目的地 |
| `days` | number | ✅ | 天数 |
| `budget_total` | number | | 总预算 |
| `accommodation_cost` | number | | 住宿费 |
| `transportation_cost` | number | | 交通费 |
| `daily_food_budget` | number | | 每日餐饮 |
| `activities` | array | | 活动费用列表 |

#### `search_hotels` — 搜索酒店

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `city` | string | ✅ | 城市 |
| `check_in` | string | ✅ | 入住日期 |
| `check_out` | string | ✅ | 退房日期 |
| `guests` | number | | 住客数 |
| `min_price` / `max_price` | number | | 价格范围 |
| `star_rating` | number | | 星级 (3/4/5) |
| `location_preference` | string | | 位置偏好 |

#### `search_flights` — 搜索航班

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `origin` | string | ✅ | 出发城市 |
| `destination` | string | ✅ | 目的城市 |
| `departure_date` | string | ✅ | 出发日期 |
| `return_date` | string | | 返程日期 |
| `passengers` | number | | 乘客数 |
| `cabin_class` | string | | economy / premium_economy / business / first |
| `max_price` | number | | 最高价格 |
| `direct_only` | boolean | | 仅直飞 |

#### `optimize_daily_route` — 日程路线优化

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `start_point` | string | ✅ | 起点地址 |
| `waypoints` | array | ✅ | 途径点列表 |
| `city` | string | ✅ | 城市 |
| `end_point` | string | | 终点地址 |
| `start_time` | string | | 出发时间 HH:mm |
| `travel_mode` | string | | transit / driving / walking |

## 关键规则

1. **工具调用限制**: `generate_travel_itinerary`（1次）+ 可选工具（最多2次）= 最多 3 次
2. **禁止为每个景点单独调用工具** — 会导致调用爆炸
3. **工具参数不含 emoji** — `{ "destination": "成都" }` 而非 `{ "destination": "📍 成都" }`
4. **多轮对话调整**: 记住上文，根据用户修改重新生成行程
5. **地图链接格式化**: 从 JSON 中提取 URL 生成 Markdown 链接 `[高德地图](url)`

## 支持的兴趣标签

`nature` | `culture` | `food` | `shopping` | `nightlife` | `adventure`

## 支持的旅行节奏

- `relaxed`: 每天 2-3 个景点，充足休息
- `moderate`: 每天 3-4 个景点，适中节奏
- `fast`: 每天 4-5 个景点，紧凑安排

## 在线体验

- [LovTrip AI 行程规划器](https://lovtrip.app/planner) — Web 端智能行程生成
- [国际行程规划](https://lovtrip.app/international-planner) — Google Maps + AI 国际行程
- [旅行攻略](https://lovtrip.app/guides) — 精选目的地深度攻略
- [热门目的地](https://lovtrip.app/destinations) — 发现你的下一个旅行目的地
- [行程方案](https://lovtrip.app/itineraries) — 现成行程模板，即查即用
- [开发者文档](https://lovtrip.app/developer) — MCP + CLI + API 完整文档

---
Powered by [LovTrip](https://lovtrip.app) — AI Travel Planning Platform
