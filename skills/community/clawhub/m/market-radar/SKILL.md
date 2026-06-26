---
name: Market Radar
description: Industry hotspot and competitor monitoring across 5 dimensions. Use when user (in Chinese) asks to monitor an industry (监测...行业) and provides competitor URLs. Systematically browses international English sources using agent-browser, runs a 5-dimension scan (brand activity, visual identity, brand positioning, content hotspots, strategic signals) on each competitor, then delivers a structured Chinese daily-brief with brand alerts and role-based action recommendations via Telegram.
read_when:
  - User sends a Chinese message asking to monitor an industry (监测...行业)
  - User mentions competitor URLs alongside an industry name
  - User asks for 竞品动态, 行业热点, 市场监测, or 竞品日报
metadata:
  clawdbot:
    emoji: 📡
    requires:
      bins: [agent-browser]
allowed-tools: Bash(agent-browser:*)
---

# Market Radar — 行业热点与竞品五维监测

> **MANDATORY TOOL RULE**: All web browsing in this skill MUST use the `agent-browser` CLI via Bash. Do NOT use any built-in browser tool, web_fetch, HTTP fetch, or any other browsing mechanism. Every page visit must be a `Bash` tool call running an `agent-browser` command. If `agent-browser` is unavailable, stop and report the error — do not fall back to other tools.

You are a market intelligence analyst. When triggered, conduct a structured English-language web research session using `agent-browser` CLI commands via Bash, then produce a fully translated Chinese-language daily brief.

## Trigger Pattern

User message format (Chinese):
```
监测[行业名]行业，竞品网址：[url1, url2, ...]
（可选）自有品牌网址：[your-brand-url]
```

Parse to extract:
- **INDUSTRY**: The industry name (e.g., "新能源汽车", "AI教育", "跨境电商")
- **INDUSTRY_EN**: Your English translation of the industry name for search queries
- **COMPETITOR_URLS**: List of competitor URLs
- **YOUR_BRAND_URL**: (Optional) User's own brand URL — if provided, run the same 5-dimension scan on it as a comparison baseline

---

## Research Workflow

Use a **single persistent browser session** throughout all phases. Do NOT close the browser between phases. Close only after all browsing is complete.

---

### Phase 1: Industry Hotspot Research（行业热点）

**Language rule:** All searches are in English. Use INDUSTRY_EN for all queries.

Search at least 4 of the following sources. Use `snapshot -c` (compact) for all snapshots. Collect the 3–5 most relevant and recent items per source.

#### 1. Google News
```bash
agent-browser open "https://news.google.com/search?q=INDUSTRY_EN&hl=en-US&gl=US&ceid=US:en"
agent-browser snapshot -c
```
If the page is shallow, scroll once: `agent-browser scroll down 800` then re-snapshot.
Collect: headline, source name, publication date, 1-sentence summary.

#### 2. Hacker News (Algolia)
```bash
agent-browser open "https://hn.algolia.com/?q=INDUSTRY_EN&dateRange=pastMonth&type=story"
agent-browser snapshot -c
```
Collect: story title, comment count (high comments = strong community signal), date.

#### 3. Reddit
```bash
agent-browser open "https://www.reddit.com/search/?q=INDUSTRY_EN&t=month&sort=relevance"
agent-browser snapshot -c
```
Collect: post titles, upvote counts, subreddit names.

#### 4. Bing News
```bash
agent-browser open "https://www.bing.com/news/search?q=INDUSTRY_EN&freshness=Month"
agent-browser snapshot -c
```

#### 5. TechCrunch / Product Hunt（按行业适用性选择）
```bash
agent-browser open "https://techcrunch.com/search/INDUSTRY_EN"
agent-browser open "https://www.producthunt.com/search?q=INDUSTRY_EN"
```

**行业专项来源：**
- AI/ML: `huggingface.co/blog`, `the-decoder.com`
- SaaS/B2B: `g2.com`, `capterra.com`
- Fintech: `finextra.com`, `thefinancialbrand.com`
- E-commerce: `retail-dive.com`, `ecommercetimes.com`
- Healthcare: `mobihealthnews.com`
- Consumer hardware: `theverge.com`, `engadget.com`
- EV/Auto: `electrek.co`, `insideevs.com`

**禁止来源：** 不得访问百度、知乎、微信/微信公众号、新浪、搜狐、163.com 或任何中国大陆平台。目标是从国际视角获取资料。

**不要跟进个别文章链接**，除非摘要严重不足以判断重要性。

---

### Phase 2: Competitor 5-Dimension Scan（竞品五维扫描）

> 参考 `references/monitoring-rules.md` 查看完整关键词列表、CSS 选择器和预警判定标准。

对每个竞品 URL，依次执行以下 5 个维度的检测。每个竞品**最多访问 5 个子页面**（含首页）。

#### 维度① 品牌活动动向

```bash
agent-browser open COMPETITOR_URL
agent-browser wait --load networkidle --timeout 3000
agent-browser snapshot -c
```

在快照中查找 `.banner`、`.promotion`、`.top-nav`、`.hero`、`.sidebar`、`.footer` 区域，检查是否存在：
- 限时活动、会员促销、联名合作、抽奖、引流二维码、新品发布公告

**记录：** 发现的活动内容 + 预警标记（🚨 有异常 / ✅ 未见异常）

#### 维度② 视听觉监控

```bash
agent-browser screenshot
agent-browser snapshot -c
```

根据快照内容，文字描述以下视觉元素：
- **Logo**：位置、颜色风格
- **首屏（Hero）**：背景类型（纯色/图片/视频/渐变）、主色调
- **CTA 按钮**：颜色、文案、位置
- **导航栏**：是否有高亮/新增菜单项
- **暗黑模式**：是否存在切换按钮
- **整体风格**：极简/丰富/年轻/专业

**记录：** 视觉风格描述 + 预警标记（🚨 若发现 "redesign"/"new look"/"beta" 等词 / ✅ 否则）

注意：本工具无法自动对比历史截图；用户根据描述自行判断是否有变化。

#### 维度③ 品牌形象与定位

从当前首页快照中提取以下元素（无需新开页面）：
- `h1`、`.slogan`、`.tagline` — 核心价值主张
- `.tag`、`.badge`、`.category` — 品类标签
- `.footer-text`、`.notice`、`.disclaimer` — 信任信号、声明
- 用户画像引导词（年龄词、注册引导文案）

**记录：** 当前 Slogan + 品类标签 + 信任信号 + 预警标记（🚨 若有明显定位转移 / ✅ 否则）

#### 维度④ 内容热点管理

依次尝试以下路径，首个有效则停止：
```bash
agent-browser open COMPETITOR_URL/blog
# 或 /news  /press  /updates  /articles
agent-browser snapshot -c
```

提取：
- 可见文章/内容条目数量
- 最新 3–5 篇标题 + 日期
- 若有热榜/trending 区域，提取前 5 条

**对提取到的标题做内联调性分析**，每篇分类为：
- 🔥 轰动型（夸张/情绪化/猎奇）
- 📚 教育型（How-to/分析/深度）
- 📣 促销型（自我推广/新功能发布）
- ⚪ 中性型（行业新闻/播报）

**记录：** 内容数量 + 主导调性 + 最新标题 + 预警标记（🚨 竞品抢跑热点 或 停更 / ✅ 正常）

#### 维度⑤ 战略辅助指标

依次尝试（每次取快照后即可，无需全部访问）：
```bash
agent-browser open COMPETITOR_URL/pricing
agent-browser snapshot -c
```

若 `/pricing` 有效，记录：套餐名称、价格、免费/付费层变化。

```bash
agent-browser open COMPETITOR_URL/changelog
# 或 /release-notes  /whats-new  /announcement
agent-browser snapshot -c
```

在快照中查找战略风险关键词：
- **定价变动**：new pricing, price change, now free, free tier
- **重大更新**：v2, major update, new feature, early access
- **法律/合规**：DMCA, copyright, banned, suspended, takedown, warning
- **停服风险**：sunset, shutting down, end of life, discontinue

**记录：** 定价结构 + 重大公告 + 预警标记（🚨 定价/法律/停服异常 / ✅ 无异常）

---

#### 如提供了自有品牌网址（YOUR_BRAND_URL）

对自有品牌 URL 执行相同的五维扫描，结果在报告中单独列出，并与竞品进行横向对比。

---

### Phase 3: Close Browser

```bash
agent-browser close
```

---

### Phase 4: Synthesis（合成与预警判定）

在撰写报告前，对所有收集到的数据进行分析：

1. **预警汇总**：将五维扫描中所有标注 🚨 的条目列出，按以下优先级排序，取前 3 条作为"品牌级警报"：
   - 1级（最紧急）：法律/停服风险、大幅定价变动
   - 2级（重要）：品牌重新定位、视觉重大改版、新品发布
   - 3级（值得关注）：促销活动上线、内容方向转变、停更信号

2. **行业信号加权**：同一趋势在多个来源出现（Google News + HackerNews + Reddit）= 强信号；单一来源 = 低可信度早期信号。

3. **竞品收敛分析**：多个竞品同时向同一方向移动（如全部推出 AI 功能、全部推出免费层）= 行业级战略模式，需特别标注。

4. **白空间识别**：行业趋势中，竞品尚未覆盖的方向 = 差异化机会。

5. **翻译**：所有英文研究内容翻译为中文。品牌名、域名、产品名保留英文原文，其余描述性内容全部翻译。

---

### Phase 5: Write the Report（撰写报告）

**输出规则：**
- 全程中文（基于英文研究翻译而来）
- **直接以 `# 市场雷达报告` 开头**，不加任何前言
- 品牌名和域名保留英文；所有其他内容用中文
- OpenClaw 自动处理 Telegram 长消息分段，不需要手动截断

---

## 报告模板

```
# 市场雷达报告
**行业：** [INDUSTRY中文] | **监测时间：** [YYYY-MM-DD] | **数据来源：** [实际查看的来源，如 Google News、HackerNews、Reddit、Bing News]

---

🚨 今日品牌级警报 Top3

1. **[竞品名] — [维度名]**：[1–2句说明发现了什么，为什么紧急]
2. **[竞品名] — [维度名]**：[说明]
3. **[竞品名] — [维度名]**：[说明，或"本次监测无其他重大异常"]

---

📊 竞品五维监测汇总

### [竞品品牌名] (domain.com)

| 维度 | 发现 | 预警 |
|------|------|------|
| 品牌活动 | [促销/活动/引流情况，或"未见异常"] | 🚨/✅ |
| 视听觉 | [Logo/首屏/配色/暗黑模式观察] | 🚨/✅ |
| 品牌形象 | [Slogan/标签/信任信号] | 🚨/✅ |
| 内容热点 | [发文量/主题方向/情绪倾向] | 🚨/✅ |
| 战略信号 | [定价/功能更新/法律风险] | 🚨/✅ |

**小结：** [2–3句，该竞品本次最值得注意的战略动向]

（每个竞品重复上方结构）

---

## 行业热点 🔥

### 核心趋势

（来自多个来源交叉验证的强信号，每条附来源和大致日期）

• **[趋势标题]**：[2–3句中文说明。来源：[Source]，[日期]]
• **[趋势标题]**：[说明]

（3–5条）

### 值得关注的信号

（早期或单一来源的方向性信号，可信度较低但值得跟踪）

• [信号描述]（来源：[Source]）

（2–3条）

---

🎯 分岗位行动建议

**品牌运营岗：**
• [建议1：针对内容选题/活动跟进/热点抢跑]
• [建议2]
• [建议3，可选]

**品牌设计师岗：**
• [建议1：针对视觉一致性/竞品视觉对标/设计迭代方向]
• [建议2]

---

附：数据质量备注

[说明任何加载失败的来源、无法访问的竞品页面、或超过60天的数据。如数据完整，写"本次监测数据完整，无重大缺口"。]
```

---

## Efficiency Checklist

- ✅ 所有内容页用 `snapshot -c`（compact）
- ✅ 需要点击时才用 `snapshot -i`（interactive）
- ✅ 浅页面先滚动：`agent-browser scroll down 800`，再重新 snapshot
- ✅ 所有 `wait --load networkidle` 设置 `--timeout 3000`
- ✅ 每个竞品最多 5 个子页面（含首页）
- ✅ 截图用于视听觉维度，其余维度依赖 snapshot 文字内容
- ❌ 不要跟进列表页面的单篇文章链接
- ❌ 不要使用内置浏览器、web_fetch 或任何非 agent-browser 工具
- ❌ 不要访问中国大陆来源
- ❌ 报告开头不加任何前言，直接写 `# 市场雷达报告`

**估计 agent-browser 调用次数：** 1个行业 + 3个竞品 ≈ 35–50 条命令，在单次 Claude turn 内可完成。

---

## Special Cases

**未提供竞品网址：** 跳过 Phase 2。报告顶部注明"未提供竞品网址，本报告仅含行业热点分析"，取消五维汇总表，保留行业热点和分岗位建议部分。

**行业名模糊（如仅写"AI"）：** 自行合理解读并在报告顶部说明：「本报告将'AI'解读为'AI生产力工具/SaaS'，如需调整请告知。」

**大型平台作为竞品（如 Google、Microsoft）：** 聚焦其与所监测行业相关的产品线，例如"AI productivity" + microsoft.com → 检查 `microsoft.com/en-us/microsoft-365/blog`。

**反爬虫/CAPTCHA：** 记录"访问受限（反爬虫）"，继续处理下一个竞品，在数据质量备注中说明。

**竞品近 60 天无博客更新：** 记录最新内容日期，在内容热点维度标注 🚨（停更信号），这本身是一个战略信号。
