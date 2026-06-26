---
name: lovtrip-china-map
description: 高德地图助手 / Amap Map Tools for China — 地理编码、周边搜索、路线规划、地图链接生成。当用户需要中国大陆范围的地理编码、地点搜索、路线规划时使用。
allowed-tools: Bash, Read
---

# 高德地图助手 / Amap Map Tools for China

> **[LovTrip (lovtrip.app)](https://lovtrip.app)** — AI 驱动的旅行规划平台，提供智能行程生成、地图导航、旅行攻略。

通过 [LovTrip](https://lovtrip.app) MCP Server 调用高德地图 API，提供中国大陆范围内的地理编码、逆地理编码、周边搜索、路线规划、地点详情和地图链接生成能力。

## Setup / 配置

用户需先配置 MCP Server。在 Claude Code 的 MCP 设置中添加：

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

如果 MCP 不可用，可使用 `scripts/amap.sh` 作为兜底方案直接调用高德 REST API。

## 工具列表 (6 Tools)

### 1. `amap_geocode` — 地理编码

将中文地址转换为经纬度坐标。

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `address` | string | ✅ | 地址，如 "北京市海淀区中关村大街1号" |
| `city` | string | | 城市名称，提高精度，如 "北京" |

**示例**: `amap_geocode({ address: "北京市海淀区中关村大街1号", city: "北京" })`

### 2. `amap_reverse_geocode` — 逆地理编码

将经纬度坐标转换为详细地址。

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `lng` | number | ✅ | 经度 |
| `lat` | number | ✅ | 纬度 |

**示例**: `amap_reverse_geocode({ lng: 116.397428, lat: 39.90923 })`

### 3. `amap_search_nearby` — 周边搜索

搜索指定位置周边的 POI（兴趣点）。

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `lng` | number | ✅ | 中心点经度 |
| `lat` | number | ✅ | 中心点纬度 |
| `keywords` | string | ✅ | 搜索关键词，如 "咖啡馆"、"餐厅" |
| `radius` | number | | 搜索半径（米），默认 2000 |
| `types` | string | | POI 类型编码 |

### 4. `amap_calculate_route` — 路线规划

计算两点间的距离、时间和费用。

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `origin_lng` | number | ✅ | 起点经度 |
| `origin_lat` | number | ✅ | 起点纬度 |
| `destination_lng` | number | ✅ | 终点经度 |
| `destination_lat` | number | ✅ | 终点纬度 |
| `mode` | string | | transit / driving / walking，默认 transit |
| `city` | string | | 城市名称，默认 "北京" |

### 5. `get_venue_details` — 地点详情

查询 POI 的营业时间、价格、评分、照片等详细信息。

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `poi_id` | string | ✅ | POI ID，从搜索结果中获取 |

### 6. `generate_map_links` — 生成地图链接

为地点生成高德、腾讯、百度、Apple Maps 深度链接。

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `venue` | object | ✅ | `{ name, address, location: { lng, lat } }` |
| `members` | array | | 成员位置列表，用于生成导航链接 |
| `mode` | string | | drive / bus / walk / ride，默认 bus |

## 典型工作流

```
用户: "帮我查一下北京国贸附近的咖啡馆"

步骤 1: amap_geocode({ address: "北京国贸", city: "北京" })
        → 获得坐标 { lng: 116.461, lat: 39.909 }

步骤 2: amap_search_nearby({ lng: 116.461, lat: 39.909, keywords: "咖啡馆" })
        → 获得周边咖啡馆列表

步骤 3: get_venue_details({ poi_id: "B0FFFAB6J2" })
        → 获取感兴趣的咖啡馆详情

步骤 4: generate_map_links({ venue: { name: "...", address: "...", location: {...} } })
        → 生成各平台地图链接
```

## 重要限制

- **仅限中国大陆**: 坐标范围 73.5–135.0°E, 18.0–53.5°N
- **务必传 `city` 参数**: 大幅提高地理编码准确性
- **批量限制**: 单次最多 10 个地址
- 国际地点请使用 `lovtrip-global-planner` 技能（Google Places API）

## 在线体验

- [LovTrip 行程规划器](https://lovtrip.app/planner) — Web 端使用高德地图 AI 规划行程
- [聚会规划](https://lovtrip.app/global-planner) — 多人聚会地点推荐
- [开发者文档](https://lovtrip.app/developer) — MCP + CLI + API 完整文档

---
Powered by [LovTrip](https://lovtrip.app) — AI Travel Planning Platform
