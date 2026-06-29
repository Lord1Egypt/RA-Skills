---
name: inspiration-app-recommend
description: >-
  灵感应用推荐助手。自动从 Product Hunt、GitHub Trending、Hacker News、36Kr、少数派、即刻、V2EX
  等平台聚合最新热门应用/产品/开源项目，按类别智能分类，提炼可借鉴的创意灵感点与商业模式分析，
  生成交互式 HTML 可视化推荐报告。解决"不知道做什么产品/应用"的创意枯竭痛点。
  Triggers: 灵感推荐, 做什么应用, 产品灵感, 创意推荐, 热门应用, 最新产品,
  有什么好想法, 做点什么, app inspiration, 应用灵感, 项目灵感, 有啥好项目,
  新产品创意, product ideas, 灵感报告, 想做点什么, 找灵感, 创意枯竭.
agent_created: true
---

# 灵感应用推荐助手

从互联网聚合最新热门应用/产品/项目，提供创意灵感与可执行的产品方向建议。

## 何时使用

当用户表达以下意图时触发：
- "推荐一些灵感/创意/好项目"
- "不知道做什么应用/产品"
- "最近有什么热门新应用"
- "想看看有什么好想法/好方向"
- "帮我找找灵感"
- "最近 XXX 领域有什么新产品"

## 核心工作流程

### Phase 1: 需求理解

从用户输入中提取以下信息（缺失则使用默认值）：

1. **关注领域** — 如 AI 工具、电商、SaaS、社交、效率工具、开源项目、移动 App、硬件等。默认：全覆盖
2. **平台偏好** — 如 Web、小程序、移动端、桌面端。默认：全平台
3. **目标用户** — 如 C 端/B 端/开发者/创作者。默认：不限
4. **灵感数量** — 默认推荐 15-20 个产品
5. **数据源偏好** — 海外为主/国内为主/全球混合。默认：全球混合

### Phase 2: 多源数据采集

并行搜索以下数据源（根据用户偏好选择 6-8 个来源，至少覆盖国内外各 2 个）：

**海外源**（至少选 3 个）：
- Product Hunt 今日/本周热门 (`producthunt.com`)
- GitHub Trending 本周 (`github.com/trending`)
- Hacker News Show HN (`news.ycombinator.com/show`)
- BetaList 最新创业项目 (`betalist.com`)
- AlternativeTo 新工具 (`alternativeto.net`)

**国内源**（至少选 3 个）：
- 36Kr 最新项目/快讯 (`36kr.com`)
- 少数派 新 App 推荐 (`sspai.com`)
- 即刻 热门话题 (`okjike.com`)
- V2EX 分享创造/创意节点 (`v2ex.com`)
- 掘金/CSDN 新技术实践

**垂直源**（按用户领域选择）：
- AI 工具：`theresanaiforthat.com`, `futuretools.io`
- 开源：`ossinsight.io`, `gitstar-ranking.com`
- 设计：`dribbble.com`, `producthunt.com`
- 独立开发：`indiehackers.com`

使用 `WebSearch` 工具进行关键词搜索，格式：
```
site:producthunt.com trending products this week
site:github.com/trending this week
```

使用 `WebFetch` 工具抓取具体页面内容，提取：
- 产品名称
- 一句话描述
- 核心功能/亮点
- 技术栈（如有）
- 用户反馈/热度指标（upvotes, stars, 评论数）
- 商业模式/定价（如有）
- 发布时间

### Phase 3: 智能分类与灵感提炼

将采集的产品按以下维度分类：

1. **领域分类**：AI/LLM 工具、效率工具、开发者工具、设计创意、社交社区、电商零售、教育学习、健康健身、金融科技、内容创作、企业服务、硬件 IoT、游戏娱乐、其他

2. **创新等级**：
   - 🔥 **颠覆式** — 全新品类，解决之前无人解决的问题
   - 💡 **微创新** — 在现有品类上有显著差异化
   - 📈 **趋势跟进** — 跟进当前热门方向
   - 🔄 **跨界融合** — 两个领域的交叉创新

3. **可行性评估**（为每个产品评估）：
   - 技术难度：低/中/高
   - 时间投入：1 周 / 1 月 / 3 月 / 半年+
   - 市场规模：小众/垂直/大众
   - 变现路径：订阅/广告/交易抽成/增值服务/开源+企业版

4. **灵感提炼** — 为每个产品提炼 3 个可借鉴的创意点：
   - 核心洞察：这个产品解决了什么本质问题？
   - 可复制模式：什么做法可以迁移到其他领域？
   - 差异化机会：在这个方向上还有什么未被满足的需求？

### Phase 4: 趋势总结

从采集数据中提炼 3-5 个当前宏观趋势：
- 热门方向词云
- 资本关注领域
- 技术采用曲线（早期/增长/成熟）
- 国内 vs 海外差异分析

### Phase 5: 生成 HTML 报告

使用内置模板 `assets/report-template.html` 生成交互式报告。报告包含：

1. **概览仪表盘**：采集产品总数、覆盖来源数、热门趋势标签
2. **领域分布图**：饼图/柱状图展示各领域占比
3. **产品卡片流**：每个产品一张卡片，含分类标签、热度、来源、核心亮点、灵感点
4. **分类筛选器**：按领域、平台、创新等级、技术难度筛选
5. **趋势分析区**：Top 趋势 + 机会雷达
6. **灵感行动清单**：按可执行性排序的 Top 5 推荐方向

报告使用步骤：
1. 读取 `assets/report-template.html`
2. 将采集分析后的数据注入模板的 `<script>` 数据区域
3. 写入工作目录输出为 `inspiration-report.html`
4. 使用 `present_files` 展示给用户

### Phase 6: 后续交互

生成报告后，提示用户可以：
- "对某个产品深入分析" — 针对单个产品做详细竞品拆解
- "按 XXX 领域筛选" — 只看特定领域
- "生成行动计划" — 针对选中的灵感方向生成 MVP 开发计划
- "保存为灵感库" — 将本次结果追加到本地灵感库

## 数据注入格式

报告模板中的数据注入格式如下（替换模板中的 `REPORT_DATA_PLACEHOLDER`）：

```javascript
const reportData = {
  meta: {
    generatedAt: "2026-06-20T19:00:00+08:00",
    totalProducts: 18,
    sourcesCount: 8,
    focusAreas: ["AI工具", "效率工具", "SaaS"],
    topTrends: ["AI Agent", "Local First", "No-Code AI"]
  },
  products: [
    {
      id: 1,
      name: "产品名称",
      tagline: "一句话描述",
      url: "https://...",
      source: "Product Hunt",
      sourceIcon: "🚀",
      category: "AI工具",
      innovationLevel: "🔥",
      description: "详细描述...",
      highlights: ["亮点1", "亮点2"],
      techStack: ["Next.js", "OpenAI API"],
      metrics: { upvotes: 1234, stars: 567, comments: 89 },
      pricing: "Freemium, $19/mo",
      difficulty: "中",
      timeToMVP: "1月",
      marketSize: "大众",
      monetization: "订阅",
      inspirations: [
        { insight: "核心洞察", replicable: "可复制模式", opportunity: "差异化机会" }
      ]
    }
  ],
  trends: [
    { name: "趋势名", description: "描述", momentum: "上升", relatedProducts: [1,3,5] }
  ],
  topPicks: [1, 3, 7, 12, 15]
};
```

## 最佳实践

1. **并行搜索** — 使用多个 `WebSearch` 调用并行搜索不同数据源
2. **去重优先** — 如果同一产品出现在多个源，合并信息并标注多源验证
3. **中文优先** — 产品描述翻译为中文，保留原始名称
4. **实用导向** — 灵感提炼要具体可执行，避免空泛的"关注用户体验"
5. **时效性标注** — 标注每个产品首次出现的时间和新颖程度
6. **诚实标注** — 如果某产品数据不全，标注"信息有限"而非编造
7. **领域聚焦** — 如果用户指定了领域，70% 的产品应来自该领域，30% 为跨领域启发

## 错误处理

- 搜索无结果：扩大搜索范围或切换关键词，告知用户当前领域热度较低
- 页面抓取失败：标注数据来源为"搜索引擎摘要"，降低置信度标注
- 仅搜到 5 个以内产品：诚实告知覆盖面有限，建议更宽泛的关键词
