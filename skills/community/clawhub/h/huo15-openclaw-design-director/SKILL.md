---
name: huo15-openclaw-design-director
displayName: 火一五设计方向顾问技能
description: 当用户没给明确方向时，基于 6 大美学流派 × 24 设计哲学库（每条带视觉三元组：hex 配色 + 字体组合 + 当代标杆作品锚点）× 3 档审美档位（Junior / Senior / Master）× 2026 当代趋势锚点池，生成 3 个反差方向的硬核 brief 对比（不是抽象描述，是可直接执行的配色 + 字体 + 视觉钩子三件套），帮用户快速定流派、定基调、定差异点。配 anti-pattern 警示和 5 组高分混血组合。配合 huo15-openclaw-frontend-design v4.x 使用，直接读取其 tokens / compare-matrix / redLineWaiver / multi-genre-compare 接力入口。触发词：帮我选设计方向、做几个方向对比、三个风格对比、design direction、设计选型、风格提案、APP 选风格、移动端选方向、iOS 还是安卓、跨端方案选型、Master 档设计、风格混血、aesthetic tier。
version: 3.0.0
aliases:
  - 火一五设计方向技能
  - 火一五设计方向顾问技能
  - 火一五风格提案技能
  - 火一五方向选型技能
  - 火一五跨端方案技能
  - 火一五设计方向
  - 设计方向
  - 方向选型
  - 风格提案
  - design direction
  - 选风格
  - APP 选风格
  - 跨端选型
  - Master 档设计
  - 风格混血
  - aesthetic tier
  - 当代趋势锚点
---

# 火一五设计方向顾问技能 v3.0

> 多方向设计提案生成 — 青岛火一五信息科技有限公司
> **v3.0 起**：审美升级。24 条设计哲学库改写为「视觉三元组」（hex 配色 + 字体组合 + 当代标杆锚点）+ 3 档审美档位（Junior / Senior / Master）+ 2026 当代趋势锚点池 + 反差三方向出硬核 brief（可直接执行）+ 6 类 anti-pattern 警示 + 5 组高分混血组合。
> **v2.0 起**：从 5 流派扩到 6 流派含 mobile-native 子集；与 `huo15-openclaw-frontend-design` v4.x 全量接力（tokens / compare-matrix / multi-genre-compare / redLineWaiver / a11y-checklist）

---

## 一、触发场景

当用户要做一个页面 / 产品 / 品牌 / APP / 小程序，但**没明确美学方向**时：

- "帮我选个设计方向"
- "做三个风格对比"
- "这个 APP 应该做成什么风格"
- "iOS / 安卓 / 鸿蒙 选哪种平台风"
- "做一个 Master 档的设计方案" ⭐v3.0
- "我想要风格混血" ⭐v3.0
- 或在 `huo15-openclaw-frontend-design §三` 被用户选"让你决定"时自动触发

**产出**：3 个反差方向的**硬核 brief**（可直接拿去执行，不是抽象描述）+ 五维对比矩阵 + 推荐方向 + Master 档可选升级路径，按接力消息格式移交给 `frontend-design` 做并行 Junior pass。

---

## 二、24 条设计哲学库（v3.0 视觉三元组化）

每条哲学不再是抽象名字，而是「**hex 配色 / 字体组合 / 当代标杆锚点**」可直接落地的三元组。

### 2.1 极简主义派（5 条）

| # | 哲学 | hex 配色（主+辅+强调） | 字体组合 | 当代标杆锚点 |
|---|------|----------------|---------|-------------|
| 1 | **原研哉 / 无印良品** | `#FAF7EB` 米白 + `#1A1A1A` 黑 + `#7F0019` 朱红印 | Noto Serif SC display + Hiragino Sans body | muji.net / 原研哉「白」展册 / 真山正纪杂志 |
| 2 | **Dieter Rams 十诫** | `#F0F0F0` 浅灰 + `#1B1B1B` 近黑 + `#E45D2D` Braun 橙 | Akzidenz-Grotesk / GT America | Braun T1000 收音机 / vitsoe.com / Apple Calculator(2026) |
| 3 | **Swiss Design / 国际主义** | `#FFFFFF` + `#000000` + `#D4181F` 红 | Helvetica Neue / Neue Haas Grotesk | Müller-Brockmann《Grid Systems》/ Swissted poster 系列 |
| 4 | **Apple 后乔布斯** | `#FFFFFF` + `#1D1D1F` 黑灰 + `#0071E3` 链接蓝 | SF Pro Display + SF Pro Text | apple.com/iphone/ / Apple WWDC 2024 keynote 单帧 |
| 5 | **Stripe 极简科技** | `#FFFFFF` + `#0A2540` 海军蓝 + `#635BFF` 亮紫 | Sohne / Sohne Mono | stripe.com 首屏 / stripe.press（电子书 site） |

→ 对应 frontend-design 流派：**bold-minimal**

### 2.2 编辑杂志派（4 条）

| # | 哲学 | hex 配色 | 字体组合 | 当代标杆锚点 |
|---|------|---------|---------|-------------|
| 6 | **NYT / 纽约客** | `#FFFFFF` + `#121212` 深黑 + `#D0021B` 报头红 | Cheltenham / NYT Imperial / Karnak | nytimes.com/section/style / The New Yorker 封面 |
| 7 | **Monocle 杂志** | `#F2EBDC` 米色 + `#1F2A1F` 深绿 + `#A56B33` 棕 | Plantin MT + Helvetica | monocle.com / Monocle Films 字幕 |
| 8 | **Pentagram 平面** | `#000000` + `#FFFFFF` + `#FF6347` 番茄 | Founders Grotesk / Caslon | pentagram.com / Paula Scher Citibank logo / NYT Magazine 改版 |
| 9 | **Stripe Press / Linear blog** ⭐v3.0 编辑科技 | `#FAF8F5` 米色 + `#0F0F0F` 黑 + `#FF5733` 橙 | GT Sectra serif + Sohne sans | press.stripe.com / linear.app/blog / Mono Issue 杂志 |

→ 对应 frontend-design 流派：**editorial**

### 2.3 前卫实验派（4 条）

| # | 哲学 | hex 配色 | 字体组合 | 当代标杆锚点 |
|---|------|---------|---------|-------------|
| 10 | **Sagmeister 观念先锋** | `#F4D03F` 黄 + `#1A1A1A` + `#FF1744` 警示红 | Knockout / Acumin Pro | sagmeisterwalsh.com / "Things I Have Learned in My Life So Far" |
| 11 | **David Carson 破坏排版** | `#000000` + `#FFFFFF` + `#FF6B35` 焦橙 | Adobe Garamond + 错位的任何字 | Ray Gun 杂志 / "The End of Print" |
| 12 | **Brutalist 2026** ⭐v3.0 升级 | `#FAFAFA` 不再纯白 + `#0A0A0A` + `#FFE600` 警告黄 | JetBrains Mono / Iosevka / Departure Mono | are.na / nothing.tech / Plain English Podcast / Tylko |
| 13 | **Y2K / Vaporwave 复古未来** | `#FF00FF` 品红 + `#00FFFF` 青 + `#9D4EDD` 紫 | Druk Wide / Bitstream Vera Sans Mono | A.G. Cook / PC Music / Cyberpunk 2077 UI / Nothing Phone OS |

→ 对应 frontend-design 流派：**brutalist** / **retro-future**

### 2.4 东方 / 有机派（4 条）

| # | 哲学 | hex 配色 | 字体组合 | 当代标杆锚点 |
|---|------|---------|---------|-------------|
| 14 | **东方禅意（侘寂）** | `#FDFBF5` 宣纸 + 墨分五色 `#1A1A1A` `#404040` `#7A7A7A` `#B0B0B0` `#E0E0E0` + `#A62828` 朱砂 | Noto Serif SC + Hiragino Mincho | 龙安寺枯山水 / 杉本博司「海景」/ 安藤忠雄住吉之家 |
| 15 | **日本民艺（Mingei）** | `#E8DCC4` 米黄 + `#5C4033` 棕 + `#7A8B5A` 苔绿 | DNP 秀英明朝 + Noto Sans JP | 柳宗悦民艺馆 / 日本民艺馆 web / 中川政七商店 |
| 16 | **Field.io 动态几何** | `#000000` + `#00FF94` 荧光绿 + `#FF006E` 品 | GT America Mono / Söhne | field.io / 资生堂 The Ginza / OFFF 主视觉 |
| 17 | **Organic / 有机自然** | `#FFFBF5` 奶白 + `#3D2817` 棕墨 + `#9AAB9C` 莫兰迪绿 | Tiempos / Druk + Söhne | aesop.com / oatly.com / Notion 早期 |

→ 对应 frontend-design 流派：**organic**

### 2.5 信息 / 功能派（3 条）

| # | 哲学 | hex 配色 | 字体组合 | 当代标杆锚点 |
|---|------|---------|---------|-------------|
| 18 | **Tufte 数据可视化** | `#FFFFFF` + `#1A1A1A` + 单一 `#D0021B` accent | ETBembo / Gill Sans | edwardtufte.com / The Visual Display of Quantitative Information |
| 19 | **Bauhaus 功能主义** | `#D32F2F` 红 + `#FFD600` 黄 + `#1565C0` 蓝 + `#FAFAFA` 象牙 | Futura / Bauhaus 93（克制使用）+ Helvetica | Herbert Bayer 海报 / Bauhaus Dessau / IBM Rebus（Paul Rand） |
| 20 | **Bloomberg 编辑信息密度** ⭐v3.0 | `#000000` + `#FF6900` Bloomberg 橙 + `#1A1A1A` | AvantGarde / Tungsten + Roboto Mono | bloomberg.com/businessweek / Tobias Frere-Jones 字体作品 |

→ 对应 frontend-design 流派：B 端 dashboard 场景常 mix **bold-minimal** + 数据组件

### 2.6 移动平台派（4 条）

| # | 哲学 | hex 配色 | 字体组合 | 当代标杆锚点 |
|---|------|---------|---------|-------------|
| 21 | **Apple HIG (iOS 26)** | `#FFFFFF` + `#000000` + `#0A84FF` 系统蓝 | SF Pro Display + SF Pro Text + SF Mono | iOS 26 Settings / Apple Notes / Shortcuts |
| 22 | **Material Design 3 dynamic** | seed 派生 primary/secondary/tertiary container | Roboto / Roboto Flex variable | Pixel Launcher / Gmail Android 2025 / m3.material.io |
| 23 | **HarmonyOS 灵动色块** | 4 色同明度（L≈0.78）多色相 + 大圆角胶囊（24-48px） | HarmonyOS Sans + 鸿蒙黑体 | HarmonyOS 4 设置 / 鸿蒙音乐 / 华为新闻 app |
| 24 | **微信小程序 Native** | 系统暗/亮 + 各 brand 自定 | PingFang SC（系统）+ 不能 @font-face | 滴滴小程序 / 美团点餐 / 微信电商 |

→ 对应 frontend-design 流派：**mobile-native-ios** / **mobile-native-md3** / **mobile-native-harmony** + 小程序四端（微信 / 支付宝 / 抖音 / 快手）

---

## 三、审美档位（Junior / Senior / Master）⭐v3.0 新增

**同一个流派，三档品味差距巨大**。直接在 brief 里声明档位，下游 frontend-design 才知道交付到哪一层。

| 档位 | 特征 | 信号词 | bold-minimal 例子 |
|------|------|-------|-------------------|
| **Junior pass** | 占位文案 + 占位图 + 跑通骨架 | Tailwind 默认色板、Inter 字体、shadcn 卡片 | 一个能用的 hero + features + footer |
| **Senior 落地** | 字体定制、自家配色、自家组件 | OKLCH 主色、display+body 反差、骨架定制 | Stripe 落地页质感 |
| **Master 级** | 单一签名钩子 / 反工业范式 / 时代感强 | 自定字距 / 微版式 / 反 cliché 选择 | linear.app 的 hero gradient + 版本号 / Vercel Ship 单帧 |

**对标范本**（Master 档每流派 2-3 个，建议读完原网页再做）：

| 流派 | Master 档对标 |
|------|---------------|
| bold-minimal | linear.app · vercel.com · stripe.press · raycast.com |
| editorial | nytimes.com（深度专题）· monocle.com · linear.app/blog · stripe.press |
| brutalist | are.na · nothing.tech · plainenglishpodcast.com · tylko.com |
| retro-future | nothing.tech ROM · A.G. Cook 网站 · OFFF Festival 主视觉 |
| organic | aesop.com · oatly.com · Notion 早期 · cosmos.so |
| mobile-native-ios | iOS 26 Settings · Apple Notes 真机截图 · Day One iOS · Things 3 |
| mobile-native-md3 | Pixel Launcher · Gmail Android · Calculator(Android 14+) |
| mobile-native-harmony | HarmonyOS 4 Settings · 鸿蒙音乐 · 华为新闻 |

**判断流程**（director 在 brief 中显式标注）：

```
用户预算 / 时间充裕 + 目标是品牌官网 / 投融资路演 / 单页 KV → Master 档
中等预算 + 目标是产品落地页 / 完整功能页 → Senior 落地
快速验证 / 内部工具 / 抢时间 → Junior pass
```

---

## 四、2026 当代趋势锚点池 ⭐v3.0 新增

每年都有新潮流。下面是**截至 2026 年 4 月**真实在火、可作为参考的当代趋势池，**不是过期的（如紫色渐变）也不是过早期的（如 2018 玻璃拟态）**。director 在反差三方向时，可从中选 1 条作为"反差方向"。

| 趋势 | 视觉签名 | 真实在火的理由 | 锚点 |
|------|---------|---------------|------|
| **Editorial Tech 编辑科技** | 米色或近黑底 + 衬线 display + 等宽 caption + 长篇排版 | 反 SaaS 千篇一律，回归阅读质感 | linear.app/blog · stripe.press · cosmos.so · pirsch.io |
| **Spatial / Depth Web** | 半 3D / WebGL 浅景深 / OKLab spotlight + 鼠标跟随阴影 | Apple Vision OS 推动 + 浏览器 GPU 进步 | apple.com/vision-pro/ · onform.fm · igloo.inc |
| **AI-Aesthetic Backlash 反 AI 范式** | 手绘 + 真实摄影 + 不规则形 + 严禁紫粉渐变 / glassmorphism | 2024-2025 紫渐变烂大街后的反弹 | are.na · plain-english.com · oatly.com 改版 |
| **Brutalist 2026** | 灰白 + 黑 + 警示黄 / 警示红 + 等宽字 + 极少装饰 | nothing.tech / 极简硬件品牌带火 | nothing.tech · tylko.com · plainenglishpodcast.com |
| **Modern Memphis 新孟菲斯** | 80s 几何 + 但更克制 + 莫兰迪化（不是糖果色） | 韦斯安德森电影回流 + 新生代复古 | wesanderson.com · The Grand Budapest Hotel UI |
| **Organic Tech 有机科技** | OKLCH 暖灰 + 不规则圆角 + 手作字体 + spring 动效 | 反"机器感" SaaS，强调温度 | aesop.com · cosmos.so · obvious.studio |
| **Editorial Mono 等宽编辑** | 全等宽字 + 单色 + 大留白 + 文档感 | Are.na / Plain English / 独立播客带动 | are.na · plainenglishpodcast.com · craft.do |
| **大字 + 大照片** ⭐ Apple 时代 | 100pt+ display + 撑满全屏照片 + 极少文案 | Apple 一直在做、社媒小红书也跟上 | apple.com 任意产品页 / Vercel Ship |

**反趋势 / 已死的视觉**（director 应主动避免推荐 + 加入 anti-pattern 警示）：
- ❌ 紫渐变 + glassmorphism（2023-2024 AI slop 标志）
- ❌ Material You 默认配色（默认 token 不改）
- ❌ Skeuomorphism 重型仿物（除非客户明确要"轻拟物 iOS 26 风"）
- ❌ Hero + 3 features + CTA + footer 模板化骨架
- ❌ 默认 Inter / Roboto + 默认 Tailwind 圆角 16px

---

## 五、3 方向生成法（v3.0 升级出硬核 brief）

### 5.1 方向选取规则

**不要选 3 个相似方向**。从以下五维反差对位中任选一组，或自由组合：

| 命题 | 流派组合 | 主推场景 |
|---|---|---|
| 理性 vs 感性 vs 实验 | bold-minimal × organic × brutalist | 早期品牌选型 |
| 冷峻 vs 温暖 vs 复古 | editorial × organic × retro-future | 内容产品 |
| 桌面 vs 移动 vs 跨端 | bold-minimal × mobile-native-ios × mobile-native-harmony | APP 选型 |
| 极简 vs 编辑 vs 装饰 | bold-minimal × editorial × retro-future | 杂志型品牌 |
| **2026 三新趋势** ⭐v3.0 | Editorial Tech × Spatial × Brutalist 2026 | 想要前卫品味 |

或按"经典 + 反差 + 时代感"自由组合：
- **1 个经典稳妥**（bold-minimal / editorial）
- **1 个有性格反差**（brutalist / retro-future / 移动平台派任一）
- **1 个 2026 当代锚点**（从 §四 趋势池选一）

### 5.2 每个方向必给的「**硬核 brief**」（v3.0 8 件套，可直接执行）

```
### 方向 N：<流派名> · <Junior/Senior/Master 档位>

- **一句话定位**（≤ 25 字）：[ 为谁做 + 什么感觉 + 一个差异钩子 ]

- **配色硬核**（直接给 hex，不要"温暖色调"这种废话）：
  - 主色：#XXXXXX（OKLCH: oklch(L% C H)）
  - 文字：#XXXXXX 在 #XXXXXX 上，对比度 ≥ 4.5:1
  - accent：#XXXXXX（点缀 5-10%，警示色 / 品牌色）
  - 中性：3-5 级灰阶 hex

- **字体硬核**（不要"现代无衬线"这种废话）：
  - display：<具体字体名> + 字号区间 + 字距 % + 行高
  - body：<具体字体名> + 字号 + 行高
  - mono（如有）：<具体字体名>

- **签名钩子**（用户会记住的「那一件事」，必须具体到一个动作）：
  例：「hero 大字 144pt + -3% 字距 + 单一 OKLCH 渐变文字」
  或：「左下永远显示 BUILD · 2026.4.28 等宽版本戳」
  或：「scrollytelling 时段落随 scroll 进度淡入」

- **当代标杆锚点**：1-2 个具体 URL / 网站名（从 §二 视觉三元组的"锚点"列直接抄）

- **frontend-design 资产路径**：
  - tokens：`../huo15-openclaw-frontend-design/tokens/<slug>.json`
  - example：`../huo15-openclaw-frontend-design/examples/<dir>/index.html`

- **redLineWaiver 提醒**：本流派的合规豁免（避免误判违规）

- **anti-pattern 警示**（v3.0 必填）：本方向最容易做差的 1-2 点，从 §六 抄
```

### 5.3 五维对比矩阵（v3.0 加品味档位维度）

| 维度 | 方向 1 | 方向 2 | 方向 3 |
|------|--------|--------|--------|
| 美学震撼 | ★★★☆☆ | ★★★★★ | ★★☆☆☆ |
| 可用性 | ★★★★★ | ★★★☆☆ | ★★★★☆ |
| 品牌辨识 | ★★☆☆☆ | ★★★★★ | ★★★☆☆ |
| 实现成本 | 低 | 高 | 中 |
| 风险 | 低 | 高（可能不被客户接受） | 中 |
| **品味档位上限** ⭐v3.0 | Senior | Master | Senior |
| **a11y 友好度** | 见 [`a11y-checklist.md §流派对照`](../huo15-openclaw-frontend-design/references/a11y-checklist.md) |

### 5.4 推荐表态

**必须**给出一个推荐（不能骑墙）：

```
### 推荐
选 **方向 N · <档位>**，理由：[结合用户的目的、受众、约束的三句话推理]

### 次选
方向 M（<档位>），适用场景：[如果方向 N 不被接受的退路]

### 反对
不选方向 K，原因：[为什么这条不合适]

### 升级建议（可选）⭐v3.0
如果预算 / 时间允许，方向 N 可从 Senior 升到 Master：补 [具体 1-2 个签名钩子]
```

---

## 六、6 类审美 anti-pattern ⭐v3.0 新增

每个方向必标 1-2 条相关 anti-pattern。Director 也用这个清单做"反趋势 / 已死视觉"自检。

| # | anti-pattern | 哪个流派最易犯 | 体现 |
|---|--------------|--------------|------|
| 1 | **极简变性冷淡** | bold-minimal | 全白 + 灰文字 + 没有 accent，无温度无品牌 → 加一个鲜明 accent / 一个签名钩子 |
| 2 | **有机变幼稚** | organic | 全圆角 + 莫兰迪粉 + 手绘 emoji 图标 → 砍 emoji + 用真摄影 + 字体加重 |
| 3 | **复古变土味** | retro-future | 直接堆 80s 霓虹粉 + Comic Sans + 像素字 → 用 Druk Wide 等当代复古字 + 单一霓虹 accent |
| 4 | **杂志变 Word 文档** | editorial | 衬线 + 左对齐 + 没结构感 → 加纵向栅格、引号装饰、栏宽控制 |
| 5 | **野兽变脏乱差** | brutalist | 等宽 + 黑底 + 红字一键命中 = 原始网吧风 → Brutalist 2026 用浅灰 + 警示黄克制装饰 |
| 6 | **AI Slop 全家桶** | 任何流派 | 紫粉渐变 / 玻璃拟态 / 默认 Tailwind / Inter 字体 + Hero+Features+CTA → 直接判废，重选方向 |

---

## 七、5 组高分混血 ⭐v3.0 新增

6 流派 × 6 流派 = 36 组 pair，绝大部分会"对冲"互相削弱。下面是 5 组**经测试品味互补、不打架**的混血：

| 混血组合 | 配比 | 用法 | 标杆锚点 |
|---------|------|------|---------|
| **editorial × bold-minimal** | 70%E + 30%BM | 阅读型品牌（书店 / 媒体 / 内容产品）| stripe.press · linear.app/blog |
| **organic × bold-minimal** | 60%O + 40%BM | 健康 / 食品 / 母婴的高品质版（不要可爱化） | aesop.com · oatly.com |
| **brutalist 2026 × editorial** | 50%/50% | 独立工作室 / 编辑型 SaaS / 思想类播客 | are.na · plainenglishpodcast.com |
| **retro-future × bold-minimal** | 30%RF + 70%BM | 科技品牌想要"一点点性格"（避免全盘霓虹） | nothing.tech · raycast.com |
| **mobile-native-ios × organic** | 50%/50% | 高品质生活类 APP / 内容向 APP | Day One iOS · Things 3 · Reeder |

**混血必须遵守**：
- **挑一个为主导**（70%/30% 或 60%/40%），不要 50%/50% 除非两个流派天然互补（如上表第 3、5 组）
- **配色取主导流派**，副流派只贡献 1-2 个签名元素
- **字体绝不混用 4 套**，最多 display + body + mono 三种

---

## 八、工作流（v3.0 升级）

### 阶段 1 · 需求分解
- 复述用户的：**目的 / 受众 / 约束 / 时间预算 / 平台 / 期望档位 ⭐v3.0**
- 平台维度决定要不要把 mobile-native 子集纳入候选
- **档位维度**：根据预算 / 时间 / 目标产物自动判定 Junior / Senior / Master，并在最终 brief 显式标注
- 如果以上任一缺失，先用一轮问答补齐

### 阶段 2 · 方向筛选
- 从 §二 24 条设计哲学库中挑 3 条（按 §5.1 规则组合）
- 至少 1 条来自 §四 2026 趋势池（强制保证有当代性）
- 跑过 §六 anti-pattern 自检 — 每个方向标记 1-2 条相关警示
- 检查混血必要性（§七）— 单流派够不够 hold 住目标？不够就推荐混血

### 阶段 3 · 硬核 brief 生成 ⭐v3.0 升级
本 skill **不直接出 HTML**，而是按下面接力消息格式发给 `frontend-design`，由它跑 [`multi-genre-compare.md`](../huo15-openclaw-frontend-design/references/multi-genre-compare.md) 流程并行出 3 份 Junior pass HTML。

但 brief 内容必须按 §5.2 8 件套写**死配色 hex / 死字体名 / 死签名钩子**，不要含糊。

### 阶段 4 · 对比 + 推荐
3 份 Junior pass 截图回流后（frontend-design 自验证用 Chrome MCP 路线），按 §5.3 + §5.4 出报告，**给出升级到 Master 档的具体建议**。

### 阶段 5 · 接力消息格式 ⭐v3.0 加 tier / anchor / antiPattern 字段

```jsonc
// director → frontend-design
{
  "task": "multi-genre-junior-pass",
  "genres": ["bold-minimal", "organic", "brutalist"],
  "tier": "senior",  // junior | senior | master ⭐v3.0
  "context": {
    "client": "<品牌名>",
    "scope": "<目标页面 / 组件类型>",
    "differentiator": "<差异点一句话>",
    "platform": "web | mobile | mini-program | cross"
  },
  "briefs": {
    "bold-minimal": {
      "positioning": "...",
      "palette": { "primary": "#0A2540", "text": "#1D1D1F", "accent": "#635BFF" },
      "typography": { "display": "Sohne 80pt -2%", "body": "Sohne 16pt 1.5", "mono": "Sohne Mono" },
      "signatureHook": "hero 大字带 OKLCH 单色渐变 + 永久 BUILD 戳",
      "anchor": "stripe.com 首屏 / linear.app",
      "antiPattern": "性冷淡（要加 accent + signature hook 反制）",
      "redLineWaiver": []
    },
    "organic": { /* 同上结构 */ },
    "brutalist": { /* 同上结构 */ }
  },
  "hybridSuggestion": null  // 或 { "primary": "editorial", "secondary": "bold-minimal", "ratio": "70/30" }
}

// frontend-design → director（截图回流）
{
  "task": "multi-genre-junior-pass-done",
  "outputs": [
    { "genre": "bold-minimal", "html": "<rel-path>", "screenshot": "<rel-path>" },
    { "genre": "organic", "html": "<rel-path>", "screenshot": "<rel-path>" },
    { "genre": "brutalist", "html": "<rel-path>", "screenshot": "<rel-path>" }
  ]
}
```

格式与 [`frontend-design/references/multi-genre-compare.md §6`](../huo15-openclaw-frontend-design/references/multi-genre-compare.md) 一致。

---

## 九、与其他 huo15 技能的分工

| 场景 | 归属 |
|------|------|
| 设计方向选型（3 方向对比 + 硬核 brief + 档位） | **本技能** |
| 选定方向后做 HTML 原型 | `huo15-openclaw-frontend-design` |
| 评审已有设计 + 审美档位识别 | `huo15-openclaw-design-critique` v2.0 |
| 抓品牌规范 brand-spec | `huo15-openclaw-brand-protocol` |
| Web / 移动 / 小程序四端 starter / tokens / a11y / motion | `huo15-openclaw-frontend-design` v4.x |
| 文生图风格预设 + aesthetic anchor | `huo15-img-prompt` v3.x |

---

## 十、触发词

- 帮我选设计方向 / 选个方向 / 定方向
- 做三个风格对比 / 做几个方向对比 / 出几个风格
- 这个产品应该做成什么风格
- design direction / design proposal
- 设计选型 / 风格提案
- APP 选风格 / 移动端选方向 / iOS 还是安卓 / 跨端方案选型 / 鸿蒙还是 iOS
- 小程序选哪个风格 / 多端做什么风
- **Master 档设计 / 想做品牌官网级 / 想要顶级设计** ⭐v3.0
- **风格混血 / 混血组合 / 流派混合** ⭐v3.0
- **2026 当代风 / 当下流行什么 / aesthetic tier** ⭐v3.0

---

## 十一、版本历史

- **v3.0.0（当前 · 2026-04-28）**：审美升级。**§二 24 条设计哲学库改写为视觉三元组**（hex 配色 / 字体组合 / 当代标杆锚点）— 不再是抽象大师名，每条直接落地到可用配色 hex + 具体字体名 + 真实可访问的标杆作品 / 网站锚点；新增 §三 **3 档审美档位**（Junior pass / Senior 落地 / Master 级）+ 每流派 Master 档对标范本表；新增 §四 **2026 当代趋势锚点池**（Editorial Tech / Spatial Web / AI-Backlash / Brutalist 2026 / Modern Memphis / Organic Tech / Editorial Mono / 大字大照片）+ 反趋势 / 已死视觉清单；§五 反差三方向 §5.2 升级为 **8 件套硬核 brief**（一句话定位 / 死 hex 配色 / 死字体名 / 签名钩子 / 当代锚点 / tokens 路径 / redLineWaiver / anti-pattern），不再写"留白美学"这种抽象描述；§5.3 五维矩阵加品味档位上限维度；§5.4 推荐表态加升级到 Master 的具体建议；新增 §六 **6 类审美 anti-pattern**（极简变性冷淡 / 有机变幼稚 / 复古变土味 / 杂志变 Word / 野兽变脏乱 / AI Slop 全家桶）；新增 §七 **5 组高分混血**（editorial×bold-minimal / organic×bold-minimal / brutalist 2026×editorial / retro-future×bold-minimal / mobile-native-ios×organic）+ 混血规则；§八 工作流加档位维度 + 强制至少 1 条 2026 趋势 + anti-pattern 自检；§五 阶段 5 接力消息格式加 `tier` / `anchor` / `antiPattern` / `hybridSuggestion` 字段；触发词扩到 Master 档 / 风格混血 / 2026 当代风。**与 frontend-design v4.x 接力路径不变**，纯审美品味升级。
- **v2.0.0（2026-04-27）**：跨端 + 接力升级。流派从 5 扩到 6（加 MOBILE-NATIVE 含 iOS HIG / Material Design 3 / HarmonyOS / 小程序四端）；设计哲学库从 20 条扩到 24 条（新增 §2.6 移动平台派 4 条）；§3.1 方向选取规则加"桌面 / 移动 / 跨端"+"Web / iOS / 鸿蒙"两组反差对位；§3.2 每个方向必给从 5 件扩到 6 件；§3.3 五维矩阵加 a11y 友好度；§4 工作流阶段 5 移交正式格式化为接力消息 JSON；与 frontend-design v4.x 全量接力。
- **v1.0.0（2026-04-23）**：初始版本。20 条设计哲学库（5 派分类）+ 3 方向生成规则（1 保守 + 1 反差 + 1 中间）+ 五维对比矩阵 + 强制推荐表态（不骑墙）。

---

**技术支持：** 青岛火一五信息科技有限公司
