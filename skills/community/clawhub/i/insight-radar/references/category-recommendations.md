# Category Recommendations (常见类别推荐信息源)

为 insight-radar 提供常见类别的信息源推荐。当用户添加新类别时，优先从这里选择。

---

## 📂 科技 & 互联网

### AI/Tech (默认)
- **Keywords**: AI, machine learning, LLM, tech trends
- **Sources**: TechCrunch, The Verge, Ars Technica, Hacker News
- **适合人群**: 科技从业者、创业者、投资人

### Gaming (游戏)
- **Keywords**: video games, esports, gaming industry, game development, metaverse
- **Sources**: 
  - IGN (游戏评测+新闻)
  - GameSpot (行业新闻)
  - Polygon (深度报道)
  - GamesIndustry.biz (商业视角)
- **适合人群**: 游戏开发者、玩家、投资人

### Social Media (社交媒体)
- **Keywords**: social media, Twitter, TikTok, Instagram, content creator
- **Sources**:
  - Social Media Today
  - The Verge (科技社交)
  - TechCrunch (社交产品)
- **适合人群**: 内容创作者、营销人员、产品经理

---

## 💼 商业 & 金融

### Business Strategy (默认)
- **Keywords**: M&A, business model, disruption
- **Sources**: Stratechery, The Information, WSJ
- **适合人群**: 创业者、投资人、高管

### Finance/Crypto (默认)
- **Keywords**: markets, crypto, DeFi, trading
- **Sources**: Yahoo Finance, CoinDesk, The Block
- **适合人群**: 投资人、交易员、Web3从业者

### E-Commerce (电商)
- **Keywords**: e-commerce, retail, Amazon, Shopify, D2C
- **Sources**:
  - Retail Dive
  - Digital Commerce 360
  - Modern Retail
- **适合人群**: 电商从业者、品牌方、投资人

### Real Estate (房地产)
- **Keywords**: real estate, property, housing market, construction
- **Sources**:
  - The Real Deal
  - Housing Wire
  - Commercial Observer
- **适合人群**: 房地产投资人、开发商

---

## 🏥 健康 & 生活

### Health/Bio (默认)
- **Keywords**: biotech, pharma, health tech, medical
- **Sources**: STAT News, The Lancet, Fierce Biotech, MedTech Dive
- **适合人群**: 医疗从业者、投资人、患者

### Fitness/Wellness (健身健康)
- **Keywords**: fitness, wellness, mental health, nutrition
- **Sources**:
  - Well+Good
  - Men's Health / Women's Health
  - Healthline
- **适合人群**: 健身爱好者、教练、健康产品从业者

### Food/Beverage (餐饮)
- **Keywords**: food industry, restaurants, beverage, culinary
- **Sources**:
  - Food Dive
  - Restaurant Business
  - Eater (餐饮文化)
- **适合人群**: 餐饮从业者、美食爱好者

---

## 🎨 创意 & 设计

### Design/UX (产品设计)
- **Keywords**: product design, UX, UI, user experience
- **Sources**:
  - Nielsen Norman Group
  - UX Design (uxdesign.cc)
  - Smashing Magazine
- **适合人群**: 设计师、产品经理

### Fashion (时尚)
- **Keywords**: fashion, luxury, apparel, style
- **Sources**:
  - Vogue Business
  - Business of Fashion (BoF)
  - Fashionista
- **适合人群**: 时尚从业者、品牌方、投资人

### Entertainment/Media (娱乐媒体)
- **Keywords**: entertainment, Hollywood, streaming, music industry
- **Sources**:
  - The Hollywood Reporter
  - Variety
  - Billboard (音乐)
- **适合人群**: 娱乐从业者、内容创作者

---

## 🌍 社会 & 环境

### Energy/Climate (默认)
- **Keywords**: renewable energy, climate tech, carbon
- **Sources**: Canary Media, Energy Monitor, Utility Dive
- **适合人群**: 能源从业者、投资人、环保人士

### Policy/Regulation (默认)
- **Keywords**: AI regulation, antitrust, policy
- **Sources**: Politico, Protocol Policy, Techdirt
- **适合人群**: 政策研究者、律师、企业合规

### Education (教育)
- **Keywords**: edtech, education, online learning, MOOC
- **Sources**:
  - EdSurge
  - Inside Higher Ed
  - The Chronicle of Higher Education
- **适合人群**: 教育从业者、EdTech创业者

### Space (太空探索)
- **Keywords**: SpaceX, NASA, space exploration, rockets, satellites
- **Sources**:
  - Space.com
  - Ars Technica Space
  - SpaceNews
- **适合人群**: 航天爱好者、投资人

---

## 🚗 交通 & 制造

### Automotive (汽车)
- **Keywords**: electric vehicles, Tesla, autonomous driving, auto industry
- **Sources**:
  - Automotive News
  - Electrek (电动车)
  - The Drive
- **适合人群**: 汽车从业者、投资人、车主

### Transportation/Logistics (交通物流)
- **Keywords**: logistics, supply chain, transportation, delivery
- **Sources**:
  - FreightWaves
  - Supply Chain Dive
  - Transport Topics
- **适合人群**: 物流从业者、供应链管理

### Manufacturing (制造业)
- **Keywords**: manufacturing, industrial, automation, robotics
- **Sources**:
  - Manufacturing Dive
  - IndustryWeek
  - Automation World
- **适合人群**: 制造业从业者、工程师

---

## 💡 使用建议

### 如何选择信息源

1. **看用户身份**:
   - 从业者 → 选行业垂直媒体（如 Fierce Biotech）
   - 普通爱好者 → 选大众媒体（如 The Verge）
   - 投资人 → 选商业视角（如 Business of Fashion）

2. **看更新频率**:
   - Daily news 需求 → 选新闻类媒体（如 TechCrunch）
   - 深度分析需求 → 选分析类媒体（如 Stratechery）

3. **避免付费墙**:
   - ❌ Bloomberg, FT, McKinsey（有付费墙）
   - ✅ Yahoo Finance, The Verge（免费）

4. **平衡观点**:
   - 至少包含1个"批判视角"媒体（如 Techdirt）
   - 避免全是"行业吹捧"类媒体

---

## 🔄 快速添加模板

**游戏类别示例**:
```json
{
  "name": "Gaming",
  "keywords": ["video games", "esports", "gaming industry", "game development"],
  "sources": [
    {"name": "IGN", "url": "ign.com", "priority": 1},
    {"name": "GameSpot", "url": "gamespot.com", "priority": 1},
    {"name": "Polygon", "url": "polygon.com", "priority": 2},
    {"name": "GamesIndustry.biz", "url": "gamesindustry.biz", "priority": 2}
  ],
  "active": true,
  "search_params": {
    "freshness": "day",
    "count": 3
  }
}
```

---

*Last updated: 2026-03-27*
