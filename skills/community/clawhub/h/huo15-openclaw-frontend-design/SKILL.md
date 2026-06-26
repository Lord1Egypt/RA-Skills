---
name: huo15-openclaw-frontend-design
displayName: 火一五前端设计技能
description: 高保真 Web UI / 移动 H5 / iOS / Android / HarmonyOS / 微信 + 支付宝 + 抖音 + 快手 四端小程序 原生风格原型 + 大胆美学方向 + 反 AI Slop 硬红线 + 8 流派 design tokens（含 motion）系统化（CSS vars / Tailwind / Figma 三导出） + 多流派并行对比 + WCAG 2.2 AA 无障碍自动审计 + 动效 tokens + 2026 微趋势补丁（Editorial Tech / Spatial Web / AI-Backlash / Brutalist 2026）。用于构建网站、落地页、仪表盘、APP 移动端、小程序（四端）、React/Vue 组件、HTML 海报、产品详情页、信息图、设计系统、无障碍合规页面、动效系统。配套 6 大美学流派 + 4 条 2026 微趋势 + 小程序子集、15 条硬红线、Junior/Full 两趟渲染、design tokens（color / typography / spacing / radius / shadow / motion）；自验证 Claude in Chrome MCP 优先 + 多路线 fallback + axe-core / Lighthouse a11y 审计；多流派对比与 design-director v3.x 联动。触发词：做网站、做落地页、做 UI、做 APP、做 H5、做小程序、做设计系统、design tokens、做动效、motion tokens、wxml、axml、ttml、ksml、做组件、HTML 原型、页面设计、移动端设计、前端设计、做海报、做详情页、iOS 风格、安卓风格、鸿蒙风格、微信小程序、支付宝小程序、抖音小程序、快手小程序、几个方向对比、风格提案、无障碍、a11y、WCAG、Lighthouse 审计、动画时长、easing、缓动函数、Editorial Tech、Spatial Web、AI-Backlash、Brutalist 2026、2026 微趋势。
version: 4.7.0
aliases:
  - 火一五前端设计技能
  - 火一五Web设计技能
  - 火一五APP设计技能
  - 火一五移动端设计技能
  - 火一五H5设计技能
  - 火一五小程序设计技能
  - 火一五抖音小程序技能
  - 火一五快手小程序技能
  - 火一五无障碍审计技能
  - 火一五动效技能
  - 火一五设计系统技能
  - 火一五落地页技能
  - 火一五UI设计技能
  - 火一五海报设计技能
  - 火一五前端设计
  - 前端设计
  - UI 设计
  - 页面设计
  - HTML 原型
  - 落地页设计
  - 海报设计
  - Web 设计
  - APP 设计
  - 移动端设计
  - H5 设计
  - 小程序设计
  - 微信小程序
  - 支付宝小程序
  - 抖音小程序
  - 快手小程序
  - 无障碍
  - a11y
  - WCAG
  - 动效
  - motion tokens
  - 动画 tokens
  - design tokens
  - 设计 tokens
  - 设计系统
---

# 火一五前端设计技能 v4.7

> 高保真 Web UI + 移动端 / APP / H5 + 微信 / 支付宝 / 抖音 / 快手 四端小程序 + design tokens（含 motion）系统化 + 多流派并行对比 + WCAG 2.2 AA 无障碍审计 + 动效 tokens + Tailwind v4 `@theme` 适配 + **2026 微趋势补丁** 原型生成 — 青岛火一五信息科技有限公司
> 设计理念对标 Anthropic `frontend-design` skill 与 2026 社区共识，本土化改写、不拷贝官方内容
> v2.0 起：5 流派 starter HTML（`examples/`）+ 配色 / 字体 / 灵感三件套（`references/`）+ 反 AI Slop 红线扩到 11 条
> v2.1 起：第 6 流派 `MOBILE-NATIVE`（iOS HIG / Material Design 3 / HarmonyOS 三套 starter）+ 移动端红线 2 条（共 13 条）+ 触发词覆盖 APP / H5 / 移动端
> v2.2 起：微信小程序 + 支付宝小程序 starter（归 MOBILE-NATIVE 子集）+ 小程序红线 2 条（共 15 条）+ 字体豁免说明 + 触发词覆盖 wxml / axml
> v3.0 起：自验证工作流升级 — Claude in Chrome MCP 优先，Playwright CLI / 微信开发者工具 / 支付宝 IDE 三路线 fallback；新增 [`references/self-verify.md`](references/self-verify.md) 操作手册
> v4.0 起：design tokens 系统化 — 8 个流派统一 [`tokens/<slug>.json`](tokens/) 扁平 schema（color / colorHex / typography / spacing / radius / shadow），三导出器 jq 一行转 CSS variables / Tailwind config / Figma Tokens Studio
> v4.1 起：多流派并行对比 — 新增 [`tokens/_compare-matrix.md`](tokens/_compare-matrix.md) 8 流派横向对比矩阵 + [`references/multi-genre-compare.md`](references/multi-genre-compare.md) 与 `huo15-openclaw-design-director` 联动手册
> v4.2 起：小程序三端齐 — 抖音 starter；红线 #14 UI 库列表扩展
> v4.3 起：小程序四端齐 — 快手 starter；触发词扩到快手小程序 / ksml
> v4.4 起：a11y 自动审计 — WCAG 2.2 AA 30 条速查 + axe-core MCP 注入 + Lighthouse CLI fallback
> v4.5 起：动效 tokens — 8 流派 motion 字段差异化动效原则
> v4.6 起：Tailwind v4 `@theme {}` 块导出 + oklch 原生支持
> **v4.7 起**：2026 微趋势补丁 — 新增 §三补 4 条 2026 当代微趋势（Editorial Tech 编辑科技 / Spatial / Depth Web 半 3D / AI-Aesthetic Backlash 反 AI 范式 / Brutalist 2026 克制版），不动 §三 6 流派主表，作为流派之上的「年代感锚点层」，与 design-director v3.0 的 §四 2026 趋势池 1:1 对应；红线没变（继续 15 条），但加 `era_anchor` 元字段到 [`tokens/<slug>.json`](tokens/) 让流派和 2026 趋势 hybridize；[`references/inspirations.md`](references/inspirations.md) 顶部加 §0 当代标杆指南 (linear.app / vercel.com / stripe.press / are.na / nothing.tech / aesop.com 等真实 URL 锚点)

---

## 一、触发场景

当用户要构建以下任一，触发本技能：

- 网站 / 落地页 / 官网 / 仪表盘
- React / Vue / HTML / Svelte 组件
- 营销海报 / 产品详情页 / 信息图
- **移动 H5 落地页 / APP 风格原型**（iOS / 安卓 / 鸿蒙 风格 H5，对应 §三 第 6 流派 MOBILE-NATIVE）
- **微信 / 支付宝 / 抖音 / 快手小程序原型** ⭐v2.2 起，v4.3 补齐四端（归 MOBILE-NATIVE 子集，见 `examples/mini-program/`）
- 任何"美化页面 / 优化 UI"类请求

**不触发**（归其他技能）：

- PPT 演示稿 → `huo15-openclaw-ppt`
- Word / PDF 文档 → `huo15-openclaw-office-doc`
- 纯数据分析图表 → 常规 matplotlib / echarts 即可

**产出**：可直接运行的 HTML/CSS/JS（或 React/Vue）代码 + 3 行设计说明 + 可选截图验证命令。

---

## 二、设计思考（动手前必答四问）

| 维度 | 要回答 |
|------|--------|
| 目的 | 这个界面解决什么问题？谁是使用者？ |
| 基调 | 选一个**极端**方向（见 §三） |
| 约束 | 技术栈 / 性能 / 可访问性 / 目标设备 |
| 差异点 | 用户会记住**哪一件**事？ |

**硬规则**：**承诺一个极端方向**。极简和极繁同样有效，关键是意图明确，**不要骑墙**。

---

## 三、六大美学流派（必选其一）

| 流派 | 关键特征 | 适合场景 | 参考 |
|------|---------|---------|------|
| **BOLD-MINIMAL** 勇敢极简 | 大字号、大留白、2 色系、无装饰 | 科技产品、B 端 SaaS、个人作品集 | Stripe / Linear / Apple |
| **EDITORIAL** 编辑杂志 | 衬线字、纵向栅格、引号装饰、杂志版式 | 品牌故事、深度内容、报告 | NYT Style / The Verge |
| **BRUTALIST** 野兽派 | 等宽字、粗黑线、打破网格、刻意粗糙 | 独立工作室、Web3、先锋作品 | Bloomberg / early craigslist |
| **RETRO-FUTURE** 复古未来 | 像素字、CRT 光晕、80s 霓虹配色 | 游戏、音乐、娱乐 | Vaporwave / Cyberpunk 2077 |
| **ORGANIC** 有机自然 | 手绘感、暖色、不规则形状、柔边 | 食品、母婴、健康 | Medium 早期 / Notion |
| **MOBILE-NATIVE** 移动原生 ⭐v2.1 | 遵循平台规范的移动设计：iOS HIG / Material Design 3 / HarmonyOS | APP 原型、H5 落地页、移动 webview | Apple HIG / m3.material.io / 鸿蒙设计指南 |

**如果用户没给方向 ⭐v4.1 升级**：走多流派并行对比流程，详见 [`references/multi-genre-compare.md`](references/multi-genre-compare.md)。
- **首选**：让 `huo15-openclaw-design-director` 选 3 流派（它有 20 条设计哲学 + 五维矩阵）
- **次选**：从 [`tokens/_compare-matrix.md`](tokens/_compare-matrix.md) §反差对位选一组（理性/感性/实验、冷峻/温暖/复古、桌面/移动/跨端等）
- 3 个 Junior pass **必须并行**（用 Explore subagent 隔离 context，不要串行）
- 截图后由 director 打分推荐 / design-critique 5 维评分 / 用户人眼挑，三选一
- 用户敲定 → 删掉其他草稿 → 单流派走阶段 3 Full Pass

**MOBILE-NATIVE 的三选一**：用户说"做 APP / 做 H5"时，先问目标平台 — iOS（用 `examples/mobile-native/ios/`）/ Android（用 `examples/mobile-native/md3/`）/ HarmonyOS（用 `examples/mobile-native/harmony/`）。多平台需求 → 三套 starter 都给，但产出文件夹分开。

**小程序场景** ⭐v2.2 起，v4.3 补齐四端：归 MOBILE-NATIVE 子集，**不另立第 7 流派**（避免膨胀）。
- 微信小程序：`examples/mini-program/wechat/`（wxml + wxss + JSON 配置三件套）
- 支付宝小程序：`examples/mini-program/alipay/`（axml + acss + 配置）
- 抖音小程序 ⭐v4.2：`examples/mini-program/douyin/`（ttml + ttss + 配置）
- 快手小程序 ⭐v4.3：`examples/mini-program/kuaishou/`（ksml + 标准 css 后缀 + 配置）
- **四端同步迭代姿势**：先做微信 → 复制到抖音改 `wx:` → `tt:` → 复制到快手改 `wx:` → `ks:`（两者最相近，各 3 分钟）→ 复制到支付宝改 `wx:` → `a:` / `bindtap` → `onTap`（差异最大，5 分钟）。完整对照表见 [`examples/mini-program/README.md`](examples/mini-program/README.md)。

---

## 三补、2026 微趋势补丁 ⭐v4.7

**6 流派是骨架（决定字体 / 配色 / 排版的基本性格），2026 微趋势是年代感锚点层（决定看起来是不是当下流行）。** 一个高品味的 brief 通常是「主流派 × 1 条 2026 微趋势」的混合，而不是单一流派。

与 [`huo15-openclaw-design-director`](../huo15-openclaw-design-director/SKILL.md) v3.0 §四 2026 趋势池 1:1 对应，director 选趋势 → frontend-design 落地实现。

### 三补.1 Editorial Tech（编辑科技）

**视觉签名**：米色或近黑底 + 衬线 display + 等宽 caption + 长篇排版 + 无千篇一律 hero/features 骨架

**适配的主流派**：bold-minimal / editorial（混血）

**实现锚点**：
- 字体组合：GT Sectra / Tiempos serif display + Söhne / Inter sans body + JetBrains Mono caption
- 配色：`#FAF8F5` 米色底 + `#0F0F0F` 黑文 + `#FF5733` 单一橙 accent
- 关键钩子：长段落（72 字符宽）+ 引号装饰 + drop cap 首字母 + 永久 metadata（作者 / 时间 / Reading Time）

**当代标杆**：press.stripe.com · linear.app/blog · cosmos.so · pirsch.io · craft.do/blog

**适用场景**：内容型品牌（书店 / 媒体 / 思想类 SaaS / 投资基金 / 思想型公司 blog）

### 三补.2 Spatial / Depth Web（半 3D）

**视觉签名**：WebGL 浅景深 / OKLab spotlight / 鼠标跟随阴影 / parallax / 浮空层叠

**适配的主流派**：bold-minimal / mobile-native-ios（Vision OS Web 风）

**实现锚点**：
- WebGL：Three.js / OGL 做轻量 GPU 几何（不要满屏 3D，只在 hero 用 spotlight）
- CSS：`backdrop-filter` + `mask-image` 做 OKLab 光斑 + `transform: perspective(1000px) translateZ(...)` 浮空
- 鼠标跟随：CSS variable + `mousemove` 注入 `--mouse-x` `--mouse-y` 控制阴影 / 高光位置
- 关键钩子：hero 的"鼠标移动看到不同角度"或"scroll 时元素小幅 Z 轴偏移"

**当代标杆**：apple.com/vision-pro/ · onform.fm · igloo.inc · paper.design · readymag.com

**适用场景**：科技品牌（AI / 硬件 / 操作系统 / 高端 SaaS）想要「未来感」但不要赛博朋克霓虹

**警示**：和红线 #11（AI 渐变模糊）容易撞 — 用 OKLab 真 spotlight 不是 blur 大色块。

### 三补.3 AI-Aesthetic Backlash（反 AI 范式）

**视觉签名**：手绘 + 真实摄影 + 不规则形 + **严禁紫粉渐变 / glassmorphism** + 反 SaaS 千篇一律

**适配的主流派**：organic / brutalist 2026

**实现锚点**：
- 字体：avoid Inter / Roboto / system-ui；用 Tiempos / Druk / Söhne / GT America
- 配色：暖灰 + 深棕 + 不超过 2 色 accent；严禁紫色渐变 / 大色块 blur
- 元素：用 SVG 手绘线 + 真摄影（Unsplash / 自家素材，**禁** AI 生图）+ 不规则圆角（`border-radius: 24px 8px 32px 12px`）
- 关键钩子：「这看起来明显不是 AI 生成的」一眼可辨

**当代标杆**：are.na · plain-english.com · oatly.com 改版 · obvious.studio · cosmos.so

**适用场景**：独立品牌 / 高端食品 / 文化机构 / 想反工业 SaaS 范式的产品

**警示**：和红线 #2（紫色渐变）/ #11（AI 渐变模糊）/ #10（玻璃形态）强联动，违反任一直接 AI Slop 判废。

### 三补.4 Brutalist 2026（克制版野兽派）

**视觉签名**：灰白 / 米白 + 黑 + 警示黄 / 警示红 + 等宽字 + 极少装饰 + 永久 metadata

**适配的主流派**：brutalist

**实现锚点**：
- 字体：JetBrains Mono / Iosevka / Departure Mono 单字体打天下（display + body 都用 mono）
- 配色：`#FAFAFA` 灰白底（不是纯白） + `#0A0A0A` 黑 + `#FFE600` 警示黄（仅用于 accent / 状态标记，不是装饰）
- 元素：1px 黑描边 / 0 圆角 / 永久 BUILD · 日期戳 / 文档感版式（像 README）
- 关键钩子：「看起来像 GitHub README 但是品牌官网」/ 信息密度大但克制装饰

**当代标杆**：nothing.tech · tylko.com · plainenglishpodcast.com · are.na

**适用场景**：硬件品牌（极简硬件 / DevTool / 独立工作室）/ 思想型博客 / 反工业 SaaS

**警示**：和老 Brutalist（Bloomberg Terminal / craigslist 风）的区别 — 2026 版**克制装饰、强调信息层级**，不是原始网吧风。

### 三补 与红线 / tokens / director 的关系

- **红线（§四 15 条）不变**：2026 微趋势依然要遵守 15 条硬红线
- **tokens（§五.6）加可选 `era_anchor` 元字段**：标记本流派 token 默认对应哪条 2026 趋势（如 brutalist token 默认对应"Brutalist 2026"）
- **director（v3.0 §四）选 1 条趋势 → 本 skill 落地**：接力消息 `briefs.<genre>.eraAnchor` 字段填趋势名（"Editorial Tech" / "Spatial Web" / "AI-Backlash" / "Brutalist 2026"），渲染时拉本节锚点配色 / 字体 / 关键钩子做 starter 改写

---

## 四、反 AI Slop 硬红线（违反任一直接判废）

| # | 禁用项 | 为什么 |
|---|--------|--------|
| 1 | 默认 **Inter / Roboto / Arial / system-ui** 字体 | 字体即性格，系统字 = 没性格 |
| 2 | **紫色渐变**（尤其紫色渐变打白底） | 2023 以来 AI 最滥用的视觉陈词滥调 |
| 3 | **emoji 当图标** | 必须用 Lucide / Phosphor / Tabler / Heroicons 真图标 |
| 4 | **圆角卡片 + 左侧彩色竖条** | Tailwind 默认范式，设计师都看腻了 |
| 5 | **CSS 画的伪产品图** | 真产品图用 Unsplash/Picsum 占位，明确标注"待替换" |
| 6 | **默认暗黑 `#121212` + 紫色主题** | 懒，且和 #2 联动犯错 |
| 7 | **Hero + Features + CTA + Footer** 千篇一律骨架 | 按内容定制结构，不要模板化 |
| 8 | 全部用 `#007AFF` / `#FF3B30` 这类 iOS 系统色 | 没有记忆点 |
| 9 | **全局统一 16px / 12px `border-radius`** | Tailwind / shadcn 默认值，工业感 = 没设计 |
| 10 | 滥用 **`backdrop-blur` 玻璃形态**（每个卡片都磨砂） | 2024 后期开始烂大街，掩盖排版无能 |
| 11 | **AI 生成的渐变模糊背景**（紫粉 / 蓝青大色块 blur） | 与红线 #2 联动，是 AI Slop 最强信号 |
| 12 ⭐v2.1 | 移动端**直接套 UI 库默认皮**（Vant / Ant Mobile / NutUI 不改 token） | 没有 brand identity = 没有产品 |
| 13 ⭐v2.1 | 移动端**缺 `viewport-fit=cover` + `safe-area-inset`**（刘海 / Home indicator 被遮） | 客户拿真机一看就崩，硬 a11y 红线 |
| 14 ⭐v2.2 / v4.2 / v4.3 扩展 | 小程序**直接套 WeUI / Vant Weapp / TDesign-Mini / Lin-UI / TTUI / Tt-Mini-UI / KSUI / kuaishou-uikit 默认皮**（不改 token） | 四端 1 千个 demo 长一个样，没产品识别 |
| 15 ⭐v2.2 | 小程序**缺 `<page-meta>` + `safe-area-inset` + `rpx` 适配** | 真机一看顶部胶囊 / 底部 home indicator 重叠，硬适配红线 |

**小程序字体豁免说明** ⭐v2.2：小程序平台**不允许 `@font-face` 加载 web font**（出于性能与审核），无法套用红线 #1 推荐字体（Manrope / DM Sans / IBM Plex Sans）。小程序 wxss / acss 中 `font-family` 优先序：
1. **PingFang SC**（iOS / 微信）
2. **Source Han Sans CN** / **思源黑体**（Android / 支付宝端）
3. **Noto Sans SC** fallback
4. **禁** `-apple-system, BlinkMacSystemFont` 写法（红线 #1 仍生效，且这些 fallback 链在小程序里其实也只走系统中文字体）

数字 / 英文如需差异化字体，可用 wxss 内联 base64 字体子集（仅 0–9 + A–Z），或干脆**全部用 PingFang SC** 数字部分，靠**字号 / 字重**做区分。

---

## 五、美学要素清单（每项都要想过）

### 5.1 字体 Typography
- 主字（display）选有性格的：Playfair Display / IBM Plex Serif / Space Mono / Noto Serif SC / DM Serif / Rubik Mono One
- 副字（body）选考究的：IBM Plex Sans / Source Serif / 思源宋体 / Noto Sans SC
- **主副反差要大**，避免同字族

### 5.2 颜色 Color
- 主色 + 锐利强调色，CSS variables 统一管理
- 优先 **oklch** 色空间（感知均匀，避免灰调）
- 主色占 60-70%，强调色 5-10%，中性 20-30%
- 不要 evenly-distributed palette

### 5.3 动效 Motion
- **页面加载的 staggered reveal > 散落的微交互**
- `animation-delay` 做级联出场
- CSS 优先，React 用 Motion（framer-motion）
- 一个高质量的动效 > 十个微交互

### 5.4 空间 Spatial Composition
- 不对称 / 重叠 / 对角线 / 打破网格
- 留白充足 **或** 密集信息，二选一
- 避免居中对齐一统到底

### 5.5 氛围 Backgrounds & Texture
- 渐变网格 / 噪点 / 几何图案 / 戏剧阴影
- 装饰性边框 / 自定义光标 / grain overlay
- 不要纯色底（除非极简流派明确需要）

### 5.6 Design Tokens ⭐v4.0 / v4.5 加 motion
- 每个流派一份 [`tokens/<slug>.json`](tokens/)，扁平 1 层 schema：`color` / `colorHex` / `typography` / `spacing` / `radius` / `shadow` / **`motion` ⭐v4.5** / `examplePath` / `redLineWaiver?`
- **8 个流派**：`bold-minimal` / `editorial` / `brutalist` / `retro-future` / `organic` / `mobile-native-ios` / `mobile-native-md3` / `mobile-native-harmony`
- **三个导出器**（jq 一行）：[`tokens/exporters/to-css-vars.md`](tokens/exporters/to-css-vars.md) / [`tokens/exporters/to-tailwind.md`](tokens/exporters/to-tailwind.md) / [`tokens/exporters/to-figma.md`](tokens/exporters/to-figma.md)
- **使用流程**：先在 §六 阶段 3.5 选定流派 → 跑 jq 命令出 CSS vars / Tailwind config → Junior Pass starter HTML 直接 `var(--color-xxx)` / `var(--duration-fast)` 引用
- schema 详细见 [`tokens/_schema.md`](tokens/_schema.md)；横向对比见 [`tokens/_compare-matrix.md`](tokens/_compare-matrix.md)（含 v4.5 motion 哲学速查）

### 5.7 Motion Tokens ⭐v4.5（动效原则）
动效不是装饰，是**时间维度的版式**。每个流派的动效原则与该流派静态视觉一致：
- **bold-minimal / editorial**：克制 / 稳重 — 单一 easing、决不弹跳
- **brutalist / retro-future**：硬切 / CRT 闪烁 — linear / step easing，禁缓动函数
- **organic**：弹性 — spring 1.56 超调，模拟手作回落
- **mobile-native iOS / MD3 / Harmony**：照搬平台 spec（iOS spring / MD3 12 档 emphasized / 鸿蒙 fluid）

**实现**：CSS 用 `transition: <prop> var(--duration-fast) var(--easing-standard)`；React 用 Motion（framer-motion）的 `transition={{ duration, ease }}`；列表级联用 `:nth-child(n) { animation-delay: calc(var(--stagger-normal) * (n - 1)) }`。

**禁忌**（继承 §四 红线）：
- 禁滥用 motion（每个元素都 hover scale → 头晕）
- 禁 `transition: all` —— 总是显式列 properties
- 禁忽略 `prefers-reduced-motion: reduce` —— 媒体查询关掉 stagger / spring

---

## 六、工作流（Junior → Full 两趟渲染）

### 阶段 1 · 理解（Understand）
- 复述需求 / 目的 / 受众
- 确认基调和流派
- 列出硬约束（技术栈、浏览器兼容、a11y）
- **多流派模式判断 ⭐v4.1**：用户没给明确流派 + 触发词命中"几个方向 / 三个风格 / 帮我选" → 走 [`references/multi-genre-compare.md`](references/multi-genre-compare.md) 流程；否则进单流派 Junior pass

### 阶段 2 · Junior Pass（假设占位，快速出骨架）
- **从 `examples/<流派>/index.html` 起手**，复制到目标文件再改 — 不要从空白起步
- 同时打开 `references/colors.md` 和 `references/typography.md` 锁配色 / 字体
- 用占位文案（Lorem Ipsum 或真实类似文案）+ 占位图片（Picsum/Unsplash 链接）
- 跑通**结构、栅格、主要交互**
- **诚实标注**每一块占位（`<!-- TODO: 真实文案 -->`）
- 让用户看到方向再继续

### 阶段 3 · Full Pass（补内容、调细节）
- 补真实文案（问用户要 或 用 `huo15-openclaw-brand-protocol` 抓品牌资源）
- 替换真实图片（需要下载时返回 CLI 命令，不用 child_process）
- 微调字号、行高、字距、间距、阴影层级
- 加动效

### 阶段 3.5 · Tokens 导出（可选）⭐v4.0
当用户要把设计落地到既有项目（已有 Tailwind / 已有 Figma 设计系统 / 多产品复用）：
- 选定流派 → 找到对应 [`tokens/<slug>.json`](tokens/)
- 跑 jq 一行转换：CSS vars（[`exporters/to-css-vars.md`](tokens/exporters/to-css-vars.md)）/ Tailwind extend（[`exporters/to-tailwind.md`](tokens/exporters/to-tailwind.md)）/ Figma Tokens Studio（[`exporters/to-figma.md`](tokens/exporters/to-figma.md)）
- 转换产物建议落到 `<用户项目>/generated/tokens/` 入仓
- **不强制**：纯一次性 H5 / 海报场景跳过本阶段，直接用 `examples/` 起手即可

### 阶段 4 · 自验证（Self-Verify）⭐v3.0 工作流升级

**优先路线**：**Claude in Chrome MCP**，由 Claude 直接驱动浏览器渲染并截图，不需要让用户跑命令。
- `mcp__Claude_in_Chrome__list_connected_browsers` → 检查浏览器连接
- `mcp__Claude_in_Chrome__navigate` → 打开 `file://` 或 URL
- `mcp__Claude_in_Chrome__computer({action:"screenshot", save_to_disk:true})` → 截图
- `mcp__Claude_in_Chrome__read_console_messages` → 抓 oklch fallback / 字体 404 / JS 报错
- 移动端用 `resize_window` 切到设备 viewport（393×852 / 412×915 / 396×858）

**Fallback 顺序**（按场景降级）：
1. **MCP 不可用**（`list_connected_browsers` 返 `[]`）→ Playwright CLI（return-cliCmd 让用户执行，延续禁 child_process 铁律）：
   ```bash
   # 桌面端
   npx playwright-core screenshot <URL 或 file:///绝对路径> ~/verify.png --viewport-size=1440,900
   # 移动端（MOBILE-NATIVE 流派必跑）
   npx playwright-core screenshot <URL> ~/verify-iphone.png --viewport-size=393,852
   npx playwright-core screenshot <URL> ~/verify-android.png --viewport-size=412,915
   ```
2. **微信小程序场景** → 微信开发者工具打开 `examples/mini-program/wechat/`，编译预览 / 真机调试扫码
3. **支付宝小程序场景** → 支付宝小程序 IDE 打开 `examples/mini-program/alipay/`，预览扫码
4. **抖音小程序场景 ⭐v4.2** → 抖音开发者工具打开 `examples/mini-program/douyin/`，编译预览 / 扫码用抖音 App 看真机
5. **快手小程序场景 ⭐v4.3** → 快手小程序开发者工具打开 `examples/mini-program/kuaishou/`，编译预览 / 扫码用快手 App 看真机

**完整决策树 + 命令清单 + 兼容性矩阵** 见 [`references/self-verify.md`](references/self-verify.md)（v3.0 新增手册）。

**评审接力**：截图回收后由用户人眼审，或调 `huo15-openclaw-design-critique` 5 维打分。MOBILE-NATIVE 流派额外检查：safe-area-inset 上下有效、tab-bar 触达高度 ≥ 44pt / 48dp；小程序检查 `<page-meta>` 存在 + tabBar native + rpx 适配。

**a11y 审计 ⭐v4.4**：渲染完成后注入 axe-core 跑 WCAG 2.2 AA 检查（首选 Chrome MCP 路线，详见 [`references/self-verify.md`](references/self-verify.md) §1.5 + [`references/a11y-checklist.md`](references/a11y-checklist.md) 30 条速查）；机器测不出的主观 / 交互项（颜色非唯一信息载体、键盘陷阱、错误纠正建议等）人审兜底。violations 修完且 passes ≥ 90% 视为可发布。

### 阶段 5 · 可选 · 评审（Review）
调用 `huo15-openclaw-design-critique` 做 5 维评分 + Keep/Fix/Quick Wins。

---

## 七、产出清单（每次交付必含）

1. **代码文件**（`index.html` / `App.tsx` / `page.vue`），可直接运行
2. **3 行设计说明**：
   - 流派（从 §三 五选一）
   - 关键设计选择（字体 / 主色 / 动效三选一突出）
   - 差异点（用户会记住什么）
3. **（可选）截图验证 CLI 命令**
4. **（可选）已知限制**（占位图未替换 / 未测移动端等）

---

## 八、与其他 huo15 技能的分工

| 能力 | 归属技能 |
|------|---------|
| Web UI / HTML 原型 / 落地页 | **本技能** |
| 设计方向选择（多流派对比） | `huo15-openclaw-design-director` |
| 品牌规范抓取 + brand-spec | `huo15-openclaw-brand-protocol` |
| 设计评审 5 维打分 | `huo15-openclaw-design-critique` |
| PPT 演示稿 | `huo15-openclaw-ppt` |
| Word / PDF 文档 | `huo15-openclaw-office-doc` |

---

## 九、触发词

**Web 端**
- 做网站 / 做落地页 / 做官网 / 做仪表盘
- 做组件 / 做 React 组件 / 做 Vue 组件
- HTML 原型 / 页面原型 / 前端原型
- 美化页面 / 优化 UI / 前端设计 / Web 设计
- 做海报 / 做详情页 / 做信息图 / 产品页

**移动端 ⭐v2.1**
- 做 APP / 做 APP 原型 / 做 APP 落地页 / 做 APP UI
- 做 H5 / 做移动 H5 / 做移动落地页
- iOS 风格 / iOS HIG / iPhone 设计
- 安卓 / Android / Material Design / MD3 / 安卓风格
- 鸿蒙 / HarmonyOS / 鸿蒙设计

**小程序 ⭐v2.2 起，v4.3 补齐四端**
- 做小程序 / 做微信小程序 / 做支付宝小程序 / 做抖音小程序 / 做快手小程序
- 小程序原型 / 小程序落地页 / 小程序首页
- wxml / wxss / 微信小程序设计
- axml / acss / 支付宝小程序设计
- ttml / ttss / 抖音小程序设计 ⭐v4.2
- ksml / 快手小程序设计 ⭐v4.3
- 四端小程序 / 多端同步

**Design Tokens ⭐v4.0**
- design tokens / 设计 tokens / 设计 token / token 导出
- 做设计系统 / 设计系统 / design system
- Tailwind 配色 / Tailwind 主题 / 流派 token
- Figma tokens / Tokens Studio / Figma 主题
- jq 转 CSS variables / 多产品共享主题

**多流派对比 ⭐v4.1**
- 几个方向对比 / 三个风格对比 / 多流派对比
- 帮我选方向 / 帮我选流派 / 你定方向
- design direction / 设计方向 / 风格提案 / 方向选型
- 三套 Junior pass / 三方向草稿
- 五维矩阵 / 流派打分

**无障碍审计 ⭐v4.4**
- 无障碍 / a11y / WCAG / WCAG 2.2
- accessibility / 无障碍审计 / 无障碍合规
- Lighthouse / axe-core / axe 审计
- 屏幕阅读器 / 键盘可操作 / 焦点环
- 对比度 / 触达目标 / alt 文本 / 色盲

**动效 / Motion Tokens ⭐v4.5**
- 做动效 / 加动效 / 动画 / motion / animation
- motion tokens / 动效 token / 动画 token
- duration / easing / 缓动函数 / cubic-bezier
- spring / 弹簧动效 / staggered / 级联出场
- prefers-reduced-motion / 减少动效 / 无障碍动效

**2026 微趋势 ⭐v4.7**
- Editorial Tech / 编辑科技 / 编辑感 / 长篇排版
- Spatial Web / 半 3D / Vision OS Web / depth web
- AI-Backlash / 反 AI / 反 AI 范式 / 反 SaaS / 手作高保真
- Brutalist 2026 / 克制版野兽派 / 灰白警示黄
- 2026 微趋势 / 2026 当代风 / 当下流行什么 / era_anchor

---

## 十、版本历史

- **v4.7.0（当前 · 2026-04-28）**：2026 微趋势补丁。**§三 6 流派主表不变**，新增 §三补「2026 微趋势补丁」4 条年代感锚点（Editorial Tech 编辑科技 / Spatial Web 半 3D / AI-Aesthetic Backlash 反 AI / Brutalist 2026 克制版），每条含视觉签名 + 适配主流派 + 实现锚点（字体 / 配色 / 元素 / 关键钩子）+ 当代标杆 URL（press.stripe.com / linear.app/blog / apple.com/vision-pro/ / are.na / nothing.tech 等真实可访问）+ 适用场景 + 警示；与 [`huo15-openclaw-design-director`](../huo15-openclaw-design-director/SKILL.md) v3.0 §四 2026 趋势池 1:1 对应（director 选趋势 → 本 skill 落地）；接力消息加 `briefs.<genre>.eraAnchor` 字段；建议 [`tokens/<slug>.json`](tokens/) 加可选 `era_anchor` 元字段标记默认对应趋势（不强制改 schema，渐进式）；触发词扩到 Editorial Tech / Spatial Web / AI-Backlash / Brutalist 2026 / 2026 微趋势。**红线 / 流派 / tokens / a11y / motion / 自验证 / 多流派对比均不变**，纯当代审美补丁层。
- **v4.6.0（2026-04-27）**：Tailwind v4 适配。[`tokens/exporters/to-tailwind.md`](tokens/exporters/to-tailwind.md) 在 v3 `theme.extend` 章节之上加 v4 `@theme {}` 块导出（推荐，2026 起 Tailwind 默认走这条）：jq 命令把 tokens.json 转成 CSS 内 `@theme` 块，token 命名前缀化（`--color-*` / `--spacing-*` / `--radius-*` / `--shadow-*` / `--duration-*` / `--ease-*`），utility class 由 Tailwind 自动生成无需配置；oklch 在 v4 原生支持不需要 `@property` polyfill；hex fallback 通过同名属性双写实现；保留 v3 `theme.extend` 章节作 legacy 项目兼容。**红线 / 流派 / a11y / motion / 自验证 / 多流派对比 / tokens schema 均不变**，纯 Tailwind 现代化适配。
- **v4.5.0（2026-04-27）**：动效 tokens。8 个 [`tokens/<slug>.json`](tokens/) 加 `motion` 字段（duration / easing / stagger / philosophy），每个流派差异化动效原则：bold-minimal 克制 / editorial 稳重 / brutalist 硬切 / retro-future CRT 闪烁 / organic 弹性 spring / mobile-native-ios HIG spring / mobile-native-md3 完整 12 档 + 4 emphasized / mobile-native-harmony fluid；3 导出器同步加 motion 转换段：`to-css-vars.md` 加 `--duration-* / --easing-* / --stagger-*` + `@property` 块平滑过渡 / `to-tailwind.md` 加 `transitionDuration` + `transitionTimingFunction` 注入 theme.extend / `to-figma.md` 加 cubicBezier 4 元数组 + Tokens Studio v2 兼容；[`tokens/_compare-matrix.md`](tokens/_compare-matrix.md) 加 motion 哲学速查表（含反差选 motion 命题）；[`tokens/_schema.md`](tokens/_schema.md) 加 motion 字段约定；SKILL.md §五 加 5.7 Motion Tokens 段（动效原则 + 实现方式 + `prefers-reduced-motion` 兜底禁忌）；触发词扩到做动效 / motion / duration / easing / spring / 级联出场。**红线 / 流派 / a11y / 自验证均不变**，纯动效 token 化升级。
- **v4.4.0（2026-04-26）**：a11y 自动审计。新增 [`references/a11y-checklist.md`](references/a11y-checklist.md) WCAG 2.2 AA 30 条速查（4 大类 Perceivable / Operable / Understandable / Robust + 场景优先级表 B 端 / 内容站 / 落地页 / 移动端 / 小程序 + 流派 a11y 友好度对照表 8 流派）；[`references/self-verify.md`](references/self-verify.md) §1.5 新增 axe-core MCP 注入路线（`mcp__Claude_in_Chrome__javascript_tool` 跑 axe.run wcag2aa+wcag22aa）+ Lighthouse CLI fallback（`npx lighthouse --only-categories=accessibility`）；§六 阶段 4 加 a11y 审计段（violations 修完 + passes ≥ 90% 可发布）；触发词扩到无障碍 / a11y / WCAG / Lighthouse / 对比度 / 焦点环 / 屏幕阅读器；标识 a11y 与红线的关系（红线 #13 与 a11y #16 触达交集，未引入新红线）。**红线 / 流派 / tokens / 多流派对比均不变**，纯无障碍审计能力补齐。
- **v4.3.0（2026-04-26）**：小程序四端齐。新增 [`examples/mini-program/kuaishou/`](examples/mini-program/kuaishou/) 快手小程序 starter（app.json + app.css + app.js + project.config.json + pages/index 4 件套：ksml + css + json + js），与微信端 95% 同源，仅前缀差异（`wx:` → `ks:` 机械替换），样式后缀用标准 `.css`（区别于微信 `.wxss` / 抖音 `.ttss`）；红线 #14 UI 库列表扩展 KSUI / kuaishou-uikit；触发词扩到快手小程序 / ksml / 四端小程序；[`examples/mini-program/README.md`](examples/mini-program/README.md) 升级四端对照表（推荐顺序：微信 → 抖音 → 快手 → 支付宝）+ 顶部胶囊形态四端对照（微信圆角 / 支付宝椭圆 / 抖音矩形 / 快手矩形）+ "何时该用 Taro / Uni-app 编译框架"提示；阶段 4 自验证补快手开发者工具流程；[`references/inspirations.md`](references/inspirations.md) §7.4 加快手参考、§7.5 通用参考从三端升为四端。**红线 / 流派 / 自验证 / tokens / 多流派对比均不变**，纯第四端补齐。
- **v4.2.0（2026-04-26）**：小程序三端齐。新增 [`examples/mini-program/douyin/`](examples/mini-program/douyin/) 抖音小程序 starter（app.json + app.ttss + app.js + project.config.json + pages/index 4 件套：ttml + ttss + json + js），与微信 / 支付宝端 95% 同源，仅前缀差异（`wx:` → `tt:` 机械替换）；红线 #14 UI 库列表扩展 TTUI / Tt-Mini-UI；触发词扩到抖音小程序 / ttml / ttss / 三端小程序 / 多端同步；[`examples/mini-program/README.md`](examples/mini-program/README.md) 升级三端对照表（微信 → 抖音 3 分钟 / 微信 → 支付宝 5 分钟）+ 真机扫码必查清单；阶段 4 自验证补抖音开发者工具流程；[`references/inspirations.md`](references/inspirations.md) §7.3 加抖音参考、§7.4 三端通用参考含 Taro / Uni-app 编译框架；§三 小程序场景说明双端 → 三端。**红线 / 流派 / 自验证 / tokens / 多流派对比均不变**，纯第三端补齐。
- **v4.1.0（2026-04-26）**：多流派并行对比。新增 [`tokens/_compare-matrix.md`](tokens/_compare-matrix.md) 8 流派横向对比矩阵（关键 token / 反差对位 / redLineWaiver 速查）；新增 [`references/multi-genre-compare.md`](references/multi-genre-compare.md) 多流派对比手册（流程总览 + 与 `huo15-openclaw-design-director` 协作接力 + 接力消息格式 + Explore subagent 并行 3 流派 Junior pass）；SKILL.md §三 改写"如果用户没给方向"段为 director 联动入口；§六 阶段 1 加多流派模式判断；触发词扩到几个方向对比 / design direction / 风格提案 / 五维矩阵 / 流派打分。**红线 / 流派 / 自验证 / tokens 系统均不变**，纯多流派编排升级。预留 director v2 升级时无需 frontend-design 再改的接力入口（tokens schema + compare matrix + redLineWaiver 已就位）。
- **v4.0.0（2026-04-26）**：design tokens 系统化。新增 `tokens/` 目录：8 个流派各一份扁平 1 层 JSON（`color` / `colorHex` / `typography` / `spacing` / `radius` / `shadow` / `examplePath` / `redLineWaiver?`），覆盖 BOLD-MINIMAL / EDITORIAL / BRUTALIST / RETRO-FUTURE / ORGANIC + MOBILE-NATIVE iOS HIG / MD3 / HarmonyOS；三个导出器手册（`tokens/exporters/{to-css-vars,to-tailwind,to-figma}.md`）— jq 一行转 CSS variables / tailwind.config.js extend / Tokens Studio v2 兼容 JSON；SKILL.md §五 加 5.6 Design Tokens 段、§六 加阶段 3.5 Tokens 导出（可选）；触发词扩到 design tokens / 设计系统 / Tailwind 配色 / Figma tokens；导出器延续禁 child_process 铁律（return-cliCmd）；`references/colors.md` 顶部加 tokens 路径指引。**红线 / 流派 / 自验证工作流均不变**，纯设计系统化升级。
- **v3.0.0（2026-04-26）**：自验证工作流升级。阶段 4 重写：**Claude in Chrome MCP 成为首选路线**（list_connected_browsers / navigate / screenshot / read_console_messages / resize_window 5 个 MCP 工具组合驱动）；MCP 不可用时降级到 Playwright CLI（保留 return-cliCmd 模式 + 禁 child_process 铁律）；小程序场景下沉到微信开发者工具 / 支付宝 IDE；新增 `references/self-verify.md` 完整操作手册（决策树 + 4 条路线命令清单 + 三路线兼容性矩阵 + 移动端检查清单 + 设计原则提醒）。**红线 / 流派 / 触发词均不变**，纯工作流升级。
- **v2.2.0（2026-04-26）**：小程序扩展。新增 `examples/mini-program/wechat/` + `examples/mini-program/alipay/` 双小程序 starter（pages/index 三件套 + app.json + project.config / mini.project 配置 + sitemap），归 MOBILE-NATIVE 子集，**不另立第 7 流派**；硬红线由 13 → 15 条（增 #14 禁直接套 WeUI / Vant Weapp / TDesign-Mini / Lin-UI 默认皮、#15 禁缺 `<page-meta>` + safe-area-inset + rpx 适配）；新增小程序字体豁免说明（平台不允许 `@font-face` 加载 web font，font-family 退到 PingFang SC / 思源黑体）；触发词扩到小程序 / wxml / axml / 微信 / 支付宝；阶段 4 自验证补微信开发者工具 + 支付宝 IDE 流程；`references/inspirations.md` 补小程序章节。
- **v2.1.0（2026-04-26）**：移动端扩展。新增第 6 流派 **MOBILE-NATIVE**，覆盖 iOS HIG / Material Design 3 / HarmonyOS 三套平台规范；新增 `examples/mobile-native/{ios,md3,harmony}/index.html` 三套 starter；硬红线由 11 → 13 条（增：禁直接套 Vant / Ant Mobile / NutUI 默认皮、禁缺 viewport-fit=cover + safe-area-inset）；触发词扩到 APP / H5 / 移动端 / iOS 风格 / 安卓 / 鸿蒙；阶段 4 自验证补移动端双截图（iPhone 16 Pro / Pixel 8 viewport）；`references/` 三件套补 mobile-native 章节。
- **v2.0.0（2026-04-26）**：对齐补 + 补料版。SKILL.md 与 clawhub 版本号对齐到 2.0；新建 `examples/` 5 流派 starter HTML（直接可在浏览器打开，oklch + Google Fonts，复制即起步）；新建 `references/` 三件套（`colors.md` / `typography.md` / `inspirations.md`）作为运行期资源；硬红线由 8 → 11 条（增：禁全局 16px 圆角、禁滥用 backdrop-blur、禁 AI 渐变模糊背景）；Junior Pass 工作流强制从 `examples/` 起手。删除空的 `presets/` 占位目录。
- **v1.0.0（2026-04-23）**：初始版本。对齐 Anthropic `frontend-design` 核心理念（BOLD 美学方向 + 反 AI slop），本土化中文改写，加入 5 流派选择、8 条硬红线、Junior/Full 两趟渲染工作流、Playwright 自验证 CLI、与火一五其他技能的分工边界。

---

**技术支持：** 青岛火一五信息科技有限公司
