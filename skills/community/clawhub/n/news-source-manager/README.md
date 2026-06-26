# News Source Manager (信息源管理器)

> **Centralized news preference management** for your AI's daily briefings.

[![ClawHub](https://img.shields.io/badge/ClawHub-Published-blue)](https://clawhub.ai)
[![Version](https://img.shields.io/badge/version-1.0.0-green)](https://github.com/your-repo)
[![License](https://img.shields.io/badge/license-MIT--0-lightgrey)](LICENSE)

---

## 🎯 What It Does

Manages your **news categories** and **trusted sources** in one place, so skills like `insight-radar` know what you care about.

**Key features**:
- 📂 Customizable categories (AI/Tech, Finance, Health, etc.)
- 🔍 Smart keyword matching
- 📰 Trusted source prioritization
- 🔄 Easy add/remove operations

---

## ⚡ Quick Start

### Install

```bash
# From ClawHub (recommended)
clawhub install news-source-manager

# Or manually
cp -r news-source-manager ~/.openclaw/workspace/skills/
```

### First Use

When you first use `insight-radar`, it will ask:

```
我需要了解你关注哪些新闻类别，方便帮你定制信息源。

我为你准备了常见类别：
1. AI/Tech (AI、科技趋势)
2. Business Strategy (商业战略、管理)
3. Finance/Crypto (金融、加密货币)
4. Health/Bio (医疗、生物科技)
5. Energy/Climate (能源、气候科技)
6. Policy/Regulation (政策、监管)

你对哪些感兴趣？(可以多选，用逗号分隔，如: 1,2,3)
```

That's it! Your AI will remember your preferences.

---

## 📊 How It Works

### Data Storage

Your preferences are stored in:  
`~/.openclaw/workspace/memory/news-sources.json`

**Example**:
```json
{
  "categories": [
    {
      "name": "AI/Tech",
      "keywords": ["AI", "machine learning", "LLM", "GPT"],
      "sources": [
        {"name": "TechCrunch", "url": "techcrunch.com", "priority": 1},
        {"name": "MIT Tech Review", "url": "technologyreview.com", "priority": 1}
      ],
      "active": true,
      "search_params": {
        "freshness": "day",
        "count": 5
      }
    }
  ]
}
```

### How Skills Use This

When `insight-radar` runs:
1. Calls `news-source-manager` → "What categories are active?"
2. Gets keywords + sources
3. Searches news using those keywords
4. Prioritizes results from your trusted sources

---

## 🛠️ Operations

### View Current Config

```
Ask your AI: "Show my news sources" or "我的新闻配置是什么"
```

**Output**:
```
📰 你的新闻配置

✅ AI/Tech (启用)
   关键词: AI, machine learning, LLM
   信息源: TechCrunch, MIT Tech Review
   更新频率: 每天

⏸️ Finance/Crypto (未启用)
   信息源: Bloomberg, CoinDesk

最后更新: 2026-03-23
```

---

### Add Category

```
Ask your AI: "添加新闻类别: 产品设计" or "add category: UX design"
```

Your AI will:
1. Ask for keywords (or suggest defaults)
2. Recommend trusted sources
3. Add to your config
4. Confirm: "✅ 已添加 '产品设计' 类别，明天开始生效。"

---

### Remove Category

```
Ask your AI: "删除类别: Finance" or "disable crypto news"
```

Your AI will ask for confirmation, then remove it.

---

### Modify Sources

```
Ask your AI: "TechCrunch质量不行，换成The Verge" or "add source: Hacker News"
```

Your AI will show before/after, then update config.

---

## 📂 Default Categories

When you select a category, we provide smart defaults:

| Category | Sample Keywords | Default Sources |
|----------|----------------|-----------------|
| **AI/Tech** | AI, machine learning, LLM, GPT, ChatGPT, Claude, generative AI, neural networks, OpenAI, Anthropic | TechCrunch, MIT Tech Review, The Verge, Hacker News |
| **Business Strategy** | M&A, disruption, competitive advantage, platform economics, SaaS, B2B, unit economics | McKinsey, HBR, WSJ, Financial Times, Bloomberg |
| **Finance/Crypto** | Bitcoin, crypto, DeFi, VC, IPO, startup funding, trading, markets | Bloomberg, CoinDesk, Financial Times, Reuters |
| **Health/Bio** | Biotech, pharma, clinical trials, CRISPR, telemedicine, medical AI | STAT News, Nature, Science, NEJM |
| **Energy/Climate** | Solar, wind, battery, EV, carbon capture, climate tech | Canary Media, CleanTechnica, Energy Storage News |
| **Policy/Regulation** | AI regulation, antitrust, GDPR, privacy law, tech policy | Politico, The Verge Policy, Axios, TechCrunch Policy |

*Full keyword lists available in SKILL.md*

---

## 🧠 Smart Search Strategy

We use a **4-level fallback** to ensure you always get news:

### Level 0: Grouped Parallel Search (Primary)
- Divide keywords into 3 business directions
- Search each direction independently
- Example (Finance): Trading/Markets, Funding/VC, Crypto/DeFi
- **Benefit**: Covers entire category spectrum

### Level 1: Core Hotwords (Fallback)
- Use 5 most popular keywords
- Example: `(private equity OR IPO OR crypto OR macroeconomics OR fintech) AND news`

### Level 2: Category Name (Fallback)
- Use broad category name
- Example: `"Finance news OR Crypto market news"`

### Level 3: Expand Time Range (Last Resort)
- Keep Level 2 query, expand from 24h → 7 days

**Result**: Even if one search fails, you still get news!

---

## 🚀 Use Cases

### 1. Personalized Daily Briefings
- **Who**: Professionals, investors, founders
- **How**: Set categories once → get tailored news forever
- **Value**: No more irrelevant news noise

### 2. Team Intelligence Sharing
- **Who**: Startups, research teams
- **How**: Configure categories for your industry
- **Value**: Everyone gets the same strategic intelligence

### 3. Multi-Domain Monitoring
- **Who**: Generalists, VCs, consultants
- **How**: Enable 3-5 categories (AI, Finance, Policy, etc.)
- **Value**: Stay informed across multiple industries

---

## 📂 File Structure

```
news-source-manager/
├── SKILL.md    # Configuration logic & keyword templates
└── README.md   # This file
```

Super lightweight. No dependencies.

---

## 🛠️ Troubleshooting

**"No news found for my category"**:
- Your keywords may be too niche
- Try Level 2 fallback (ask AI: "use broader search")
- Or add more keywords to the category

**"Too much irrelevant news"**:
- Refine keywords (remove generic terms like "tech", "business")
- Add negative keywords (future feature)

**"I want to reset to defaults"**:
```
Ask your AI: "重置新闻配置" or "reset news sources to default"
```

---

## 📜 License

MIT-0 (No Attribution Required)

---

## 🙌 Credits

Created by **汤圆 (Tangyuan)** for 雯姐's news intelligence workflow.

**Powers**:
- [`insight-radar`](https://clawhub.ai/skills/insight-radar) — Daily news briefings
- Future skills that need news category management

---

## 📣 Feedback

Found a bug? Want a new category template? Ping `@KeDOuPi` on ClawHub.

**Star this skill** if it keeps you informed! ⭐
