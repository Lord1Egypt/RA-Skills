---
name: lovtrip-meetup
description: 聚会规划助手 / Multi-Person Meetup Planner — 多人聚会地点推荐、时间协调、行程生成。当用户需要规划多人聚会、约会、找最优碰面地点时使用。
allowed-tools: Bash, Read
---

# 聚会规划助手 / Multi-Person Meetup Planner

> **[LovTrip (lovtrip.app)](https://lovtrip.app)** — AI 驱动的旅行规划平台，提供聚会规划、智能行程生成、旅行攻略。

为多人聚会提供智能规划：自动计算地理中点、推荐最优地点、协调时间、生成完整行程方案。Web 版体验：[lovtrip.app/global-planner](https://lovtrip.app/global-planner)

## Setup / 配置

```json
{
  "mcpServers": {
    "lovtrip": {
      "command": "npx",
      "args": ["-y", "lovtrip@latest", "mcp"],
      "env": {
        "AMAP_API_KEY": "your-amap-api-key"
      }
    }
  }
}
```

## 完整工作流（6 步）

### 第 1 步：解析时间 + 匹配兴趣

收集每位成员的时间和兴趣，找到共同窗口。

- `parse_schedule({ text: "周六下午" })` → 结构化时间段
- `match_interests({ members: [{ name: "Alice", interests: ["咖啡","桌游"] }, ...] })` → 共同兴趣 + 推荐活动

### 第 2 步：计算中点 + 推荐地点

**快捷方式（推荐）**: 直接用 `amap_find_optimal_venue` 一步完成中点计算 + 地点搜索 + 评分排序。

```
amap_find_optimal_venue({
  members: [
    { name: "Alice", location: "北京市海淀区中关村" },
    { name: "Bob", location: "北京市朝阳区国贸" }
  ],
  activity_type: "咖啡馆",
  city: "北京"
})
```

**分步操作**（需要更细粒度控制时）:

1. `amap_calculate_midpoint({ members: [...], city: "北京" })` → 地理中心点
2. `amap_search_nearby({ lng, lat, keywords: "咖啡馆" })` → 周边地点

### 第 3 步：检查天气和路况（可选）

- `check_weather({ location: { lng, lat }, city: "北京" })` → 天气预报 + 活动建议
- `check_traffic({ location: { lng, lat }, city: "北京" })` → 实时交通态势

### 第 4 步：推荐时间段

- `suggest_time_slots({ venue_business_hours: "09:00-22:00", duration_minutes: 120, member_count: 4 })`

### 第 5 步：生成完整方案

```
generate_plan({
  time_slot: { start: "2026-03-08T14:00:00", end: "2026-03-08T18:00:00" },
  venue: { name: "星巴克中关村店", address: "...", location: { lng, lat } },
  activities: ["咖啡", "桌游"],
  members: ["Alice", "Bob"]
})
```

### 第 6 步：导出与分享

- `generate_map_links({ venue: {...}, members: [...] })` → 各平台地图/导航链接
- `export_calendar({ title: "周六聚会", start_time: "...", end_time: "...", location: "..." })` → iCal 文件
- `generate_backup_plans({ primary_plan: {...}, reason: "weather", city: "北京" })` → 备选方案

## 工具列表 (10 Tools)

| 工具 | 说明 |
|------|------|
| `amap_calculate_midpoint` | 计算多人地理中心点 |
| `amap_find_optimal_venue` | **核心**: 综合推荐最优聚会地点 |
| `parse_schedule` | 解析自然语言时间（"周六下午"、"明天3点后"） |
| `match_interests` | 分析多人共同兴趣，推荐活动 |
| `suggest_time_slots` | 基于营业时间、高峰期推荐最佳时间段 |
| `generate_plan` | 生成完整行程方案（时间线 + 地点 + 活动） |
| `generate_backup_plans` | 天气/交通/客满时的备选方案 |
| `export_calendar` | 导出 iCal (.ics) 日历文件 |
| `check_weather` | 天气预报 + 活动建议 |
| `check_traffic` | 实时交通态势 |

## 评分算法

`amap_find_optimal_venue` 使用加权评分：

```
总分 = 距离分 × 0.3 + 评分分 × 0.4 + 公平性分 × 0.2 + 惩罚分 × 0.1

距离分 = 1.0 - (平均距离 / 最大搜索半径)
评分分 = 商户评分 / 5.0
公平性分 = 1.0 - (通勤时间标准差 / 最大标准差)
惩罚分 = 1.0 - (最远成员距离 / 最大搜索半径 × 2)
```

## 使用示例

```
用户: "我在中关村，朋友在国贸，周六下午想找个咖啡馆聊天"

→ parse_schedule({ text: "周六下午" })
→ amap_find_optimal_venue({
    members: [{ name: "我", location: "中关村" }, { name: "朋友", location: "国贸" }],
    activity_type: "咖啡馆",
    city: "北京"
  })
→ generate_plan({ time_slot: {...}, venue: {...}, activities: ["咖啡"] })
→ generate_map_links({ venue: {...}, members: [...] })
```

## 重要限制

- **仅限中国大陆**: 坐标范围 73.5–135.0°E, 18.0–53.5°N
- **务必传 `city` 参数**: 大幅提高准确性
- `members` 数组至少 2 人
- 优先使用 `amap_find_optimal_venue` 一步到位，避免分步调用导致工具调用过多

## 在线体验

- [LovTrip 聚会规划](https://lovtrip.app/global-planner) — Web 端多人聚会地点推荐
- [AI 行程规划器](https://lovtrip.app/planner) — 智能生成旅行行程
- [旅行攻略](https://lovtrip.app/guides) — 精选目的地深度攻略
- [开发者文档](https://lovtrip.app/developer) — MCP + CLI + API 完整文档

---
Powered by [LovTrip](https://lovtrip.app) — AI Travel Planning Platform
