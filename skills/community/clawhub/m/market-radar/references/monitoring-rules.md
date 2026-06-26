# 五维监测规则详细参考

本文件供 agent 在执行 Phase 2 竞品五维扫描时查阅。包含每个维度的完整关键词列表、CSS 选择器、判断标准。

---

## 维度① 品牌活动动向

### 需检查的页面区域（选择器优先级顺序）
```
.banner, .top-banner, .announcement-bar
.hero, .hero-section, .above-fold
.promotion, .activity, .campaign, .event
.top-nav, .nav-bar, header nav
.sidebar, .widget
.footer, footer
```

### 活动类关键词（国际站英文为主）
| 类别 | 关键词 |
|------|--------|
| 会员/付费 | membership, VIP, premium, paywall, unlock, subscribe, paid plan, pro plan |
| 限时活动 | limited time, flash sale, expires, countdown, ends soon, today only |
| 联名/合作 | collaboration, collab, partnership, co-branded, x [brand] |
| 抽奖/福利 | giveaway, raffle, contest, win, prize, reward |
| 引流/跳转 | QR code, scan, redirect, download app, get the app, mini program |
| 新品发布 | new launch, just launched, introducing, announcing, available now |

### 预警判定
- 首页出现上述任意关键词所在的**新增区块**（非固定导航）→ 标注 🚨（品牌活动）
- 如仅为常规注册/订阅入口，非异常，标注 ✅

---

## 维度② 视听觉统一监控

### 截图操作
```bash
agent-browser screenshot
```
截图后，agent 根据快照内容（snapshot -c）对以下元素做文字描述：

### 需描述的视觉元素清单
| 元素 | 描述内容 |
|------|----------|
| Logo | 位置、颜色、是否含文字、与品牌名关系 |
| 首屏（Hero） | 背景类型（纯色/图片/视频/渐变）、主色调、是否有动效 |
| CTA 按钮 | 颜色、文案、数量、位置 |
| 导航栏 | 菜单项数量、是否有高亮/新增项 |
| 暗黑模式 | 是否存在切换按钮，或默认深色背景 |
| 整体风格 | 极简/丰富/年轻/专业/等 |

### 预警判定
- 本工具**不能自动对比历史截图**（无持久化状态）
- agent 描述当前视觉风格；用户根据自身记忆或历史报告判断是否有变化
- 若快照文字中出现"beta", "new look", "redesign", "refresh" 等词 → 标注 🚨（视听觉）
- 否则标注 ✅ 并附简短描述

---

## 维度③ 品牌形象与定位

### 需提取的文字元素（选择器）
```
h1, h2
.slogan, .tagline, .headline
.tag, .label, .badge, .category
.footer-text, footer p
.notice, .disclaimer, .trust-badge
.announcement, .alert-bar
[class*="trust"], [class*="verified"], [class*="safe"]
```

### 需关注的信号类型
| 信号类别 | 说明 |
|----------|------|
| 定位语言 | h1/tagline 中的核心价值主张，是否有品类转移迹象 |
| 信任信号 | "AI-generated", "human-reviewed", "privacy-first", "no ads", "certified" 等 |
| 用户画像引导 | 年龄引导词（18+, teens, students, professionals）、注册引导弹窗文案 |
| 声明/公告 | 隐私政策更新、内容政策变更、DMCA/版权声明 |

### 预警判定
- h1 或 tagline 文案与上次已知内容**明显不同** → 标注 🚨（品牌形象）
- 新增信任信号或声明页面 → 标注 🚨
- 无变化或常规内容 → 标注 ✅

---

## 维度④ 内容热点管理

### 需访问的路径（顺序尝试，首个有效则停止）
```
/blog  /news  /press  /updates  /feed  /articles  /stories
```

### 需提取的信息
```
.post-list article, .list-item, .entry, .card
.hot-list, .top10, .trending, .popular, .featured
```

| 指标 | 提取内容 |
|------|----------|
| 文章数量 | 当前页面可见文章/内容条目数量 |
| 最新内容 | 最新 3–5 篇标题 + 发布日期 |
| 热榜/推荐 | 若有热榜/trending 区域，提取前 5 条 |

### 情绪/调性内联分析标准
agent 对提取到的标题进行分类，每篇归入以下之一：

| 类型 | 特征 |
|------|------|
| 🔥 轰动型 | 夸张标题、数字噱头、情绪化词汇（shocking, exposed, secret, leaked） |
| 📚 教育型 | How-to、Guide、Tutorial、分析类、深度内容 |
| 📣 促销型 | 包含品牌自我推广、新产品发布、功能介绍 |
| ⚪ 中性型 | 新闻播报、行业动态、无明显情绪 |

输出格式：「近期内容以 [X型] 为主（占比约 X%），最新发布：[标题] [日期]」

### 预警判定
- 与行业热点高度重合，且早于竞争对手发布 → 标注 🚨（内容热点：竞品抢跑）
- 近 30 天内容数量为 0 → 标注 🚨（内容热点：停更，战略信号）
- 正常更新节奏 → 标注 ✅

---

## 维度⑤ 战略辅助指标

### 需访问的路径
```
/pricing  /plans  /upgrade  （定价）
/changelog  /release-notes  /whats-new  （版本更新）
/announcement  /blog/announcement  （公告）
```

### 战略风险关键词
| 类别 | 关键词 |
|------|--------|
| 定价变动 | new pricing, price change, now free, free tier, starting at, per month |
| 产品更新 | v2, version 2, major update, new feature, now available, early access |
| 应用/平台 | iOS app, Android app, desktop app, browser extension, API access |
| 法律/合规风险 | DMCA, copyright, content removal, banned, suspended, warning, takedown |
| 停服风险 | sunset, shutting down, end of life, discontinue, migrate |

### 预警判定
- 出现定价变动（新增/取消免费层、大幅涨价）→ 标注 🚨（战略信号：定价）
- 出现法律/停服关键词 → 标注 🚨（战略信号：风险）
- 出现重大产品更新 → 标注 🚨（战略信号：产品）
- 无异常 → 标注 ✅

---

## 预警优先级排序（用于 Phase 4 汇总 Top3）

```
1级（最紧急）：法律/停服风险、大幅定价变动
2级（重要）：品牌重新定位（Slogan 变更）、重大视觉改版、新品发布
3级（值得关注）：促销活动上线、内容方向转变、停更信号
```
