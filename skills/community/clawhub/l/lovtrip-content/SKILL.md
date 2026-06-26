---
name: lovtrip-content
description: 旅行内容查询 / Travel Content Browser — 搜索攻略、目的地、行程，零 API Key。当用户需要搜索旅行攻略、浏览目的地、查看行程方案时使用。
allowed-tools: Bash, Read
---

# 旅行内容查询 / Travel Content Browser

> **[LovTrip (lovtrip.app)](https://lovtrip.app)** — AI 驱动的旅行规划平台，提供智能行程生成、旅行攻略、目的地推荐。

零 API Key 即可使用。通过 `lovtrip` CLI 或 `curl` 查询 [LovTrip](https://lovtrip.app) 平台的旅行攻略、目的地信息和行程方案。

## Setup / 配置

### 方式 1: CLI（推荐）

```bash
npx lovtrip@latest --help
```

无需任何 API Key 或环境变量。

### 方式 2: curl

直接调用 LovTrip 公开 API，无需安装任何工具。

## 命令 / API 映射

### 1. 搜索 — `search`

全文搜索攻略、目的地和行程。

**CLI**:
```bash
npx lovtrip search "京都3天"
npx lovtrip search "Bali beach" --json
```

**curl**:
```bash
curl -s "https://lovtrip.app/api/search?q=京都3天" | python3 -m json.tool
```

### 2. 攻略列表 — `guides`

浏览旅行攻略。

**CLI**:
```bash
npx lovtrip guides
npx lovtrip guides --destination "Tokyo"
```

**curl**:
```bash
curl -s "https://lovtrip.app/api/guides?limit=10" | python3 -m json.tool
curl -s "https://lovtrip.app/api/guides?destination=Tokyo&limit=10" | python3 -m json.tool
```

### 3. 攻略详情 — `guide`

查看单篇攻略的完整内容。

**CLI**:
```bash
npx lovtrip guide kyoto-3-day-food-tour
```

**curl**:
```bash
curl -s "https://lovtrip.app/api/guides/kyoto-3-day-food-tour" | python3 -m json.tool
```

### 4. 目的地 — `destinations`

浏览热门目的地。

**CLI**:
```bash
npx lovtrip destinations
npx lovtrip destinations --trending
```

**curl**:
```bash
curl -s "https://lovtrip.app/api/destinations?limit=20" | python3 -m json.tool
curl -s "https://lovtrip.app/api/destinations/trending" | python3 -m json.tool
```

### 5. 行程 — `itineraries`

浏览旅行行程方案。

**CLI**:
```bash
npx lovtrip itineraries
npx lovtrip itineraries --destination "Bali" --days 5
```

**curl**:
```bash
curl -s "https://lovtrip.app/api/itineraries?limit=10" | python3 -m json.tool
curl -s "https://lovtrip.app/api/itineraries?destination=Bali&days=5" | python3 -m json.tool
```

## CLI 全局选项

| 选项 | 说明 |
|------|------|
| `--json` | 输出 JSON 格式 |
| `--api-url <url>` | 覆盖 API 地址 |
| `--no-color` | 禁用颜色输出 |
| `--help` | 显示帮助 |
| `--version` | 显示版本 |

## 使用示例

```
用户: "有没有东京的美食攻略？"

→ 执行: npx lovtrip search "东京 美食"
→ 返回攻略列表，包含标题、摘要、链接

用户: "看看这篇的详情"

→ 执行: npx lovtrip guide tokyo-food-guide-2026
→ 返回完整攻略内容
```

## 进阶使用

查询结果可以配合其他 LovTrip 技能使用：
- 找到感兴趣的目的地 → 使用 `lovtrip-travel-planner` 生成定制行程
- 找到国内地点 → 使用 `lovtrip-china-map` 查看地图和导航
- 找到视频攻略 → 使用 `lovtrip-video2article` 转为文章

## 在线体验

直接访问 [lovtrip.app](https://lovtrip.app) 使用完整的 Web 版功能：
- [AI 行程规划器](https://lovtrip.app/planner) — 智能生成多日行程
- [旅行攻略](https://lovtrip.app/guides) — 精选目的地深度攻略
- [热门目的地](https://lovtrip.app/destinations) — 发现下一个旅行目的地
- [行程方案](https://lovtrip.app/itineraries) — 现成的行程模板，即查即用
- [聚会规划](https://lovtrip.app/global-planner) — 多人碰面地点推荐
- [开发者文档](https://lovtrip.app/developer) — MCP Server + CLI + API 文档

---
Powered by [LovTrip](https://lovtrip.app) — AI Travel Planning Platform
