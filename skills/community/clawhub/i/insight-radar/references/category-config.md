# Category Configuration Guide

如何为 insight-radar 添加自定义新闻类别。

---

## 📋 通过 news-source-manager 添加

**推荐方式** (对话式):

```
用户: "添加新闻类别: 产品设计"

汤圆: "好的！为 '产品设计' 类别设置关键词。
建议: product design, UX, UI, user experience

你可以直接确认，或者自定义关键词（用逗号分隔）"

用户: "确认"

汤圆: "推荐信息源（产品设计类）:
1. Nielsen Norman Group (nngroup.com)
2. UX Design (uxdesign.cc)
3. Smashing Magazine (smashingmagazine.com)

回复 '确认' 使用推荐，或 '自定义' 手动输入"

用户: "确认"

汤圆: "✅ 已添加 '产品设计' 类别，明天开始生效。"
```

---

## 🛠️ 手动编辑 news-sources.json

**文件位置**: `~/.openclaw/workspace/memory/news-sources.json`

**添加新类别**:

```json
{
  "categories": [
    {
      "name": "Product Design",
      "keywords": ["product design", "UX", "UI", "user experience"],
      "sources": [
        {"name": "Nielsen Norman Group", "url": "nngroup.com", "priority": 1},
        {"name": "UX Design", "url": "uxdesign.cc", "priority": 2}
      ],
      "active": true,
      "search_params": {
        "freshness": "day",
        "count": 3
      }
    }
  ],
  "last_updated": "2026-03-23T15:23:00+08:00",
  "user_confirmed": true
}
```

---

## 🎨 自定义类别模板

### 示例1: 游戏行业

```json
{
  "name": "Gaming Industry",
  "keywords": ["video games", "esports", "gaming industry", "game development"],
  "sources": [
    {"name": "GameSpot", "url": "gamespot.com", "priority": 1},
    {"name": "IGN", "url": "ign.com", "priority": 2},
    {"name": "Polygon", "url": "polygon.com", "priority": 2}
  ],
  "active": true,
  "search_params": {
    "freshness": "day",
    "count": 5
  }
}
```

### 示例2: 教育科技

```json
{
  "name": "EdTech",
  "keywords": ["edtech", "education technology", "online learning", "MOOC"],
  "sources": [
    {"name": "EdSurge", "url": "edsurge.com", "priority": 1},
    {"name": "Inside Higher Ed", "url": "insidehighered.com", "priority": 2}
  ],
  "active": true,
  "search_params": {
    "freshness": "day",
    "count": 3
  }
}
```

### 示例3: 太空探索

```json
{
  "name": "Space Exploration",
  "keywords": ["SpaceX", "NASA", "space exploration", "rockets", "satellites"],
  "sources": [
    {"name": "Space.com", "url": "space.com", "priority": 1},
    {"name": "Ars Technica Space", "url": "arstechnica.com/space", "priority": 1}
  ],
  "active": true,
  "search_params": {
    "freshness": "week",  // 太空新闻更新慢，可以用一周
    "count": 3
  }
}
```

---

## 📊 字段说明

| 字段 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `name` | ✅ | 类别名称（英文，用于标识） | "AI/Tech" |
| `keywords` | ✅ | 覆盖度评估关键词（insight-radar 用于判断搜索结果是否覆盖了该类别的主要子领域，不直接作为搜索词） | ["AI", "machine learning", "semiconductor"] |
| `sources` | ✅ | 信息源列表 | 见下表 |
| `active` | ✅ | 是否启用 | true / false |
| `search_params` | ⭕ | 搜索参数（可选） | 见下表 |

**sources 字段**:

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | ✅ | 信息源名称 |
| `url` | ✅ | 域名（用于过滤搜索结果） |
| `priority` | ⭕ | 优先级（1最高，默认2） |

**search_params 字段**:

| 字段 | 默认值 | 说明 |
|------|--------|------|
| `count` | 5 | 每次搜索返回结果数量 |

---

## ✅ 最佳实践

### 1. Keywords 选择（用于覆盖度评估）

keywords 不是搜索词，而是 insight-radar 搜索后评估"结果是否覆盖了该类别的主要子领域"的标准。如果某个子领域在搜索结果中缺失，AI 会自动补搜。

**好的关键词**:
- ✅ 覆盖该类别的 3-4 个不同子领域
- ✅ 行业术语："DeFi", "biotech", "semiconductor"
- ✅ 5-8 个关键词，每个子领域 1-2 个代表词

**不好的关键词**:
- ❌ 太宽泛："news", "technology"
- ❌ 全部集中在同一个子领域
- ❌ 太少（<3）导致无法评估覆盖度

### 2. Sources 选择

**优质信息源特征**:
- ✅ 权威性（行业公认）
- ✅ 更新频率稳定
- ✅ 不是纯聚合器（有原创分析）
- ✅ 无付费墙或付费墙友好

**如何找信息源**:
1. Google: "best [your topic] news sources"
2. 问同行推荐
3. 试运行几天，淘汰低质量源

### 3. Priority 设置

- **Priority 1**: 核心权威源（如 Nature, McKinsey）
- **Priority 2**: 补充源（如 TechCrunch）
- 系统会优先抓取 Priority 1 的内容

---

## 🧪 测试新类别

添加新类别后，测试是否生效：

```
用户: "生成今天的新闻早报"

汤圆: [如果配置正确，会包含新类别的新闻]
```

**调试**:
- 如果没有新类别的新闻 → 检查 `active: true`
- 如果搜索结果质量差 → 调整 keywords
- 如果信息源不匹配 → 检查 url 是否正确

---

## 🔄 更新类别

**修改关键词**:
```
用户: "把 AI/Tech 的关键词改为更具体的"

汤圆: [调用 news-source-manager，交互式修改]
```

**禁用类别** (不删除配置):
```json
{
  "name": "Finance/Crypto",
  "active": false  // 暂时不关注，但保留配置
}
```

---

*Last updated: 2026-03-27*
