---
name: product-hunt-cn
description: "Product Hunt 热门产品监控 | Product Hunt Trending Products. 获取每日热门新产品、科技产品发布、创业项目 | Get daily trending products, tech launches, startup projects. 触发词：Product Hunt、PH、新产品、launch."
metadata:
  openclaw:
    emoji: "🚀"
    category: "startup"
    tags: ["producthunt", "ph", "startup", "launch", "product"]
    requires:
      bins: ["python3", "curl"]
---

# Product Hunt 热门产品监控

Product Hunt 每日热门产品监控，支持产品发现、趋势分析。

## 功能

### 热门产品
- **今日热门** - 今日 Top 产品
- **本周最佳** - 本周热门产品
- **本月精选** - 本月最佳产品

### 分类浏览
- **Tech** - 科技产品
- **Games** - 游戏
- **Books** - 书籍
- **Podcasts** - 播客

### 产品发现
- **新品发现** - 新上线产品
- **AI Tools** - AI 工具合集
- **Developer Tools** - 开发者工具

## 使用方式

### 获取今日热门

```
获取 Product Hunt 今日 Top 10
```

返回：
```json
[
  {"rank": 1, "name": "AI Writer Pro", "tagline": "AI 写作助手", "upvotes": 856, "comments": 234, "url": "https://..."},
  {"rank": 2, "name": "Code Assistant", "tagline": "智能编程助手", "upvotes": 743, "comments": 189, "url": "https://..."},
  {"rank": 3, "name": "Design Kit", "tagline": "设计工具套件", "upvotes": 621, "comments": 156, "url": "https://..."}
]
```

### 按分类筛选

```
获取 Product Hunt AI 类别热门
```

### 关键词搜索

```
在 Product Hunt 搜索 "note taking"
```

## 输出格式

### 产品列表
```
🚀 Product Hunt 今日热门

1. AI Writer Pro
   📝 AI 写作助手
   👍 856 | 💬 234
   https://...

2. Code Assistant
   📝 智能编程助手
   👍 743 | 💬 189
   https://...
```

---

*Product Hunt，发现下一个爆款* 🚀
