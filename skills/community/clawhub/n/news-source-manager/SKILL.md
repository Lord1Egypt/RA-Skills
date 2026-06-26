---
name: news-source-manager
description: Manages user's news category preferences and information sources. Stores in news-sources.json, supports add/remove/list operations. Use when (1) user wants to customize news categories, (2) user mentions "add news source" or "change news preferences", (3) insight-radar skill needs to load news config.
---

# News Source Manager (信息源管理器)

**Purpose**: 集中管理用户的新闻兴趣类别和信息源。纯配置管理，不涉及搜索执行。

---

## 📂 Data Structure

Stores in: `~/.openclaw/workspace/memory/news-sources.json`

```json
{
  "categories": [
    {
      "name": "AI/Tech",
      "keywords": ["AI", "machine learning", "LLM", "GPT", "tech trends", "AI agents", "semiconductor"],
      "sources": [
        {"name": "TechCrunch", "url": "techcrunch.com", "priority": 1},
        {"name": "MIT Technology Review", "url": "technologyreview.com", "priority": 1},
        {"name": "Ars Technica", "url": "arstechnica.com", "priority": 2}
      ],
      "active": true,
      "search_params": {
        "freshness": "day",
        "count": 5
      }
    }
  ],
  "last_updated": "2026-03-23T15:20:00+08:00",
  "user_confirmed": true
}
```

**字段说明**:
- `keywords`: 类别关键词，用于搜索后**覆盖度评估**——insight-radar 用它们判断宽泛搜索是否遗漏了重要子领域，决定是否补搜
- `sources`: 优先信息源，priority 1 = 核心权威，priority 2 = 补充
- `search_params.count`: 每次搜索返回结果数

---

## 🔧 Operations

### 1. Initialize (首次使用)

**When**: 用户首次使用 insight-radar，或 news-sources.json 不存在

**Steps**:
1. 检测 config 缺失
2. 询问用户关注的类别：
   ```
   我为你准备了常见类别：
   1. AI/Tech (AI、科技趋势)
   2. Business Strategy (商业战略、管理)
   3. Finance/Crypto (金融、加密货币)
   4. Health/Bio (医疗、生物科技)
   5. Energy/Climate (能源、气候科技)
   6. Policy/Regulation (政策、监管)
   7. Product Design (产品设计、UX)

   你对哪些感兴趣？(多选用逗号分隔，如: 1,2,3)
   或者告诉我你的自定义类别。
   ```
3. 用户选择后，从 `references/keyword-templates.json` 加载对应类别的默认 keywords、sources 和 search_hints
4. 展示推荐信息源，用户确认或修改
5. 写入 `news-sources.json`
6. 确认: "✅ 配置已保存！"

---

### 2. List Current Config

**Trigger**: "我的新闻配置是什么" / "show my news sources"

**Steps**:
1. 读取 `news-sources.json`
2. 展示:
   ```
   📰 你的新闻配置

   ✅ AI/Tech (启用)
      搜索提示: latest AI technology news LLM agents
      信息源: TechCrunch, MIT Tech Review, Ars Technica

   ⏸️ Finance/Crypto (未启用)
      信息源: Bloomberg, CoinDesk

   最后更新: 2026-03-23
   ```
3. 询问是否需要修改

---

### 3. Add Category

**Trigger**: "添加新闻类别: 产品设计" / "add category: UX design"

**Steps**:
1. 提取类别名
2. 如果匹配默认模板（`references/keyword-templates.json`），加载默认 keywords 和 sources
3. 如果是自定义类别，引导用户设置:
   - keywords（用于搜索后覆盖度评估，建议涵盖该类别的 3-4 个子领域）
   - sources（推荐信息源）
4. 用户确认后写入 `news-sources.json`
5. 确认: "✅ 已添加 '产品设计' 类别。"

**keywords 编写指南**:
- 覆盖该类别的主要子领域（3-4 个方向）
- insight-radar 用 keywords 评估搜索结果覆盖度，发现盲区后自动补搜
- 示例 (AI/Tech): AI, LLM, AI agents, semiconductor, robotics, AI safety

---

### 4. Remove Category

**Trigger**: "删除类别: Finance" / "disable crypto news"

**Steps**:
1. 找到匹配类别
2. 确认: "⚠️ 确认删除 'Finance/Crypto' 类别吗？"
3. 用户确认后设置 `active: false`（或删除）
4. 确认: "✅ 已删除。"

---

### 5. Modify Sources

**Trigger**: "TechCrunch质量不行，换成The Verge" / "add source: Hacker News"

**Steps**:
1. 解析意图: 移除/添加/替换
2. 找到受影响类别
3. 展示 before/after 对比
4. 用户确认后更新 `news-sources.json`
5. 确认: "✅ 信息源已更新。"

---

### 6. Export Config (供 insight-radar 调用)

**Trigger**: insight-radar 加载配置时调用

**Steps**:
1. 读取 `news-sources.json`
2. 过滤 `active: true` 的类别
3. 返回结构化数据:
   ```json
   {
     "active_categories": [
       {
         "name": "AI/Tech",
         "keywords": ["AI", "machine learning", "LLM", "AI agents", "semiconductor"],
         "sources": ["TechCrunch", "MIT Tech Review"],
         "search_params": {"count": 5}
       }
     ]
   }
   ```

---

## 🧠 Default Category Templates

完整关键词和信息源列表见 [keyword-templates.json](references/keyword-templates.json)。

以下为各类别摘要:

| Category | 核心关键词（用于覆盖度评估） | Default Sources |
|----------|---------------------------|-----------------|
| **AI/Tech** | AI, LLM, AI agents, semiconductor, robotics, AI safety | TechCrunch, MIT Tech Review, The Verge |
| **Business Strategy** | M&A, disruption, SaaS, digital transformation, startup | McKinsey, HBR, WSJ, Bloomberg |
| **Finance/Crypto** | VC, IPO, bitcoin, DeFi, macroeconomics, fintech | Bloomberg, CoinDesk, FT, Reuters |
| **Health/Bio** | biotech, clinical trials, CRISPR, digital health, medical AI | STAT News, Nature, NEJM, Fierce Biotech |
| **Energy/Climate** | renewable, battery, EV, carbon capture, hydrogen, nuclear | Canary Media, CleanTechnica, Carbon Brief |
| **Policy/Regulation** | AI regulation, antitrust, GDPR, AI Act, cybersecurity | Politico, Bloomberg Gov, Lawfare |
| **Product Design** | UX, UI, design system, accessibility, Figma, user research | Nielsen Norman, Smashing Magazine |

**keywords 角色**: insight-radar 搜索后用 keywords 评估覆盖度，发现盲区自动补搜。不再作为搜索词。
