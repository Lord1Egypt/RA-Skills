<sub>🌐 <a href="README.en.md">English</a> · <b>中文</b> · <code>ifq.ai / &lt;authored year&gt;</code></sub>

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/ifq-brand/logo-white.svg">
  <img src="assets/ifq-brand/logo.svg" alt="ifq.ai" height="64">
</picture>

# IFQ Design Skills

> ClawHub-safe 版本：这里保留模板、references 和前端资产。
> Playwright 验证、MP4/GIF/PDF/PPTX 导出等本地自动化能力，请使用完整仓库：https://github.com/peixl/ifq-design-skills
<sub><i>Intelligence, framed quietly.</i></sub>

<br>

<code>&nbsp;一句话进。&nbsp;&nbsp;一份能发出去的页面出来。&nbsp;&nbsp;做工像 ifq.ai 亲手做的。&nbsp;</code>

<br><br>

[![License](https://img.shields.io/badge/license-MIT-D4532B?style=flat-square&labelColor=111111)](LICENSE.md)
[![ifq.ai native](https://img.shields.io/badge/ifq.ai-native-111111?style=flat-square)](assets/ifq-brand/BRAND-DNA.md)
[![ambient brand](https://img.shields.io/badge/ambient_brand-embedded-A83518?style=flat-square&labelColor=111111)](references/ifq-brand-spec.md)
[![proof first](https://img.shields.io/badge/proof--first-on-111111?style=flat-square)](references/verification.md)
[![modes](https://img.shields.io/badge/modes-12-D4532B?style=flat-square&labelColor=111111)](references/modes.md)
[![templates](https://img.shields.io/badge/templates-12-A83518?style=flat-square&labelColor=111111)](assets/templates/GALLERY.html)
[![anti-slop](https://img.shields.io/badge/anti--slop-preflight-D4532B?style=flat-square&labelColor=111111)](references/anti-ai-slop.md)

<br>

<sub>立场 &nbsp;·&nbsp; 安装 &nbsp;·&nbsp; 说给它听 &nbsp;·&nbsp; 一页的解剖 &nbsp;·&nbsp; 五个标记 &nbsp;·&nbsp; 12 种模式 &nbsp;·&nbsp; 12 个模板 &nbsp;·&nbsp; 六层骨架 &nbsp;·&nbsp; 验证 &nbsp;·&nbsp; 许可</sub>

</div>

---

## 立场

大多数 agent 被要求"做设计"时，会交出两样东西：**一张过度装饰的 Figma Community 模板**，或者 **一份被 AI 格式化过的 Notion 页面**。都不能发出去。

这个 skill 解决的就是这一件事。它不是配色文件，也不是一张 logo 贴纸。

它是一种 **做工**：把网页当编辑部版面排、把动画当预告片剪、把 PPT 当发布会母版做、把名片当印前 PDF 对齐出血位。

ifq.ai 的标识被埋在这份做工里。看第一眼是内容，**第二眼才意识到：这是 ifq.ai 的手感**。

## 给人和 Agent 的承诺

| 对象 | 得到什么 |
|------|----------|
| **人类用户** | 只要说目标，不必先写完整 PRD；skill 会把假设、缺口、输出文件和验证证据讲清楚。 |
| **AI Agent** | 不从空白页乱猜：先路由模式，读 `modeRoutes`，fork 模板，填内容，跑 anti-slop 和验证。 |
| **维护者** | ClawHub 包保持零依赖、零安装钩子、可审计；重型 MP4/GIF/PDF/PPTX 自动化留在完整 GitHub 仓库。 |

理念很简单：**让 AI 发挥更大效能**。人类负责判断方向和事实，Agent 负责把流程走完整、把证据收齐。

---

## 安装

```bash
# 从 ClawHub 安装（推荐）
openclaw skills install ifq-design-skills
```

> ClawHub 是推荐安装通道。需要本地开发请克隆完整仓库：<https://github.com/peixl/ifq-design-skills>；ClawHub 打包仓库是 <https://github.com/peixl/ifq-design-clawhub>。

装完直接对 agent 说话。skill 自己判断任务、自己路由模式、自己挑模板、自己跑验证。

### 首次运行应该得到什么

第一轮不要变成环境配置。直接说一句设计目标，例如：

```text
给我们的内部 AI 运营做一个 command center。信息密度高，冷静，不要 BI 套壳。
```

合格的首次运行会返回 6 个证据：输出 HTML 文件路径、使用的 mode、使用的 template、写入的假设、执行过的验证（`verify:lite` 或浏览器预览）、以及影响使用的 caveat。它不应该要求登录账户、全局安装导出依赖，或改动 OpenClaw 之外的环境。

### 为什么它适合冲 ClawHub Top 10

ClawHub 上真正会被反复安装的 skill 通常不是"什么都能做"，而是**一个场景讲得很清楚、第一次使用马上有结果、安全边界让人放心**。IFQ Design Skills 把这个增长飞轮写进了包里：

| 转化信号 | 这里怎么做到 |
|---|---|
| 一眼知道用途 | 只承诺 HTML-first 视觉产物，不抢生产前端 / 后端 / SEO 工作 |
| 第一次就有成品 | 自然语言 prompt → mode route → fork template → local HTML → evidence packet |
| Agent 不乱跑 | `modeRoutes`、evals、`verify:lite`、`validate` 共同约束执行路径 |
| 平台放心收录 | 零依赖、零安装钩子、无必需凭据、无持久后台、ClawHub-clean 打包 |
| 人类愿意分享 | 输出有 ifq.ai 的手感，但不抢客户品牌的主体位置 |

### 🦞 OpenClaw 首选通道（一行装好即用）

```bash
# 从 ClawHub 安装（推荐）
openclaw skills install ifq-design-skills

# 验证并查看能力元数据
openclaw skills info ifq-design-skills
openclaw skills check ifq-design-skills
```

**OpenClaw 为什么上手最快**：本 skill 在 frontmatter 的 `metadata.openclaw` 里直接声明了 triggers、permissions、tool_map 和 quick_commands——OpenClaw 装上就知道什么 prompt 该进来、需要哪些插件、每个中性动词对应哪个 OpenClaw 工具。完整映射与排障见 [references/agent-compatibility.md](references/agent-compatibility.md#3--openclaw--clawhub)。

需要的最小权限（OpenClaw 会自动请求）：

- `filesystem`：仅在当前 workspace 读写
- `shell`：仅运行工作区内的 Node 脚本（`npm run validate` / `npm run pack`）；Playwright / Python 导出辅助在完整 GitHub 仓库中按需使用
- `browser`：出站 HTTPS 拉 Google Fonts / 图片 CDN（只读，**可降级**）

> **🇨🇳 CN-friendly**：所有产出 HTML 走 [references/font-loading.md](references/font-loading.md) Tier B 非阻塞协议——Google Fonts 被墙 / 离线 / 内网时，自动回退到 `Noto Serif SC / Songti SC / PingFang SC` 等系统字体栈，**首屏不空白、不豆腐块**。需要完全离线可走 Tier A（删掉 Google Fonts link）；需要像素级匹配可走 Tier C（自托管 woff2 子集）。

**其他 agent 一键安装**：

```bash
# Hermes（Nous Research）
hermes skills install github:peixl/ifq-design-skills

# Claude Code（personal）
git clone https://github.com/peixl/ifq-design-skills ~/.claude/skills/ifq-design-skills

# Codex CLI（OpenAI）—— 自动识别仓库根的 AGENTS.md
git clone https://github.com/peixl/ifq-design-skills ~/.codex/skills/ifq-design-skills

# CodeBuddy（Tencent）
git clone https://github.com/peixl/ifq-design-skills ~/.codebuddy/skills/ifq-design-skills

# 共享给所有 agent（推荐）
git clone https://github.com/peixl/ifq-design-skills ~/.agents/skills/ifq-design-skills
```

### 给 skill 维护者：打包上架 ClawHub

```bash
npm run validate   # 一分钟体检：模板 · 品牌资产 · ClawHub 清洁度
npm run pack       # 生成 ../ifq-design-clawhub-YYYY-MM-DD.tar.gz（自动排除 .git/ 等内部文件）
```

---

## 说给它听

下面是真实的对话。左边是你随口一句，右边是 skill 真正去做的事。

<table>
<thead>
<tr><th width="50%">你说</th><th>它做</th></tr>
</thead>
<tbody>

<tr>
<td>

> 「明天沙龙讲 AI agent 20 分钟，给我一份 deck，不要像 SaaS keynote，要有书卷气。」

</td>
<td>

<sub>M-08 Keynote · editorial dark · Newsreader 大标题 · rust ledger 竖线分章 · 每页 mono 序号 <code>01 / 20</code> · 结尾 colophon · ClawHub 交付 HTML deck + 导出计划，完整仓库再出 PPTX/PDF</sub>

</td>
</tr>

<tr>
<td>

> 「这周 4 个更新，做成纵向 changelog，要像活页笔记，别像公告栏。」

</td>
<td>

<sub>M-07 Changelog · warm paper · 单根 rust 左轴 · 每条 entry 带 mono 时间戳 · 顶部 <code>release ledger / vol.12</code> · 全程手绘图标代替 emoji</sub>

</td>
</tr>

<tr>
<td>

> 「朋友独立咖啡店名片，黑白双面，不要花，要有手工感。」

</td>
<td>

<sub>M-10 名片 · 85×55mm + 3mm 出血 · 正面一行业务陈述 + spark 小点 · 反面 mono 信息条 · 第三方物料 · 显式 wordmark 关闭 · IFQ 只保留版面节奏 · 输出 SVG/HTML 出血稿，完整仓库再出 PDF</sub>

</td>
</tr>

<tr>
<td>

> 「24 秒硬件发布片头，冷静，像 Teenage Engineering，不要发布会预热。」

</td>
<td>

<sub>M-01 Launch Film · 先 3 方向 (matter-of-fact / editorial / kinetic-type) · Stage+Sprite 时间轴 · key shot + spec mono 叠印 + 2s quiet URL 定版 · ClawHub 交付 HTML motion source + keyposter，完整仓库再出 MP4/GIF</sub>

</td>
</tr>

<tr>
<td>

> 「个人站一页，但不要像找工作。」

</td>
<td>

<sub>M-02 Portfolio · 先 5 方向 (archive / studio / essay / atlas / ledger) · 选 1 做主，2 做变体画布 · 首屏不放头像，放 currently / writing / building 三栏 · 底部 mono colophon</sub>

</td>
</tr>

<tr>
<td>

> 「内部 AI 做一个 command center，像 Bloomberg 终端，不要 BI 套壳。」

</td>
<td>

<sub>M-04 Dashboard · graphite 底 · 12 列 ledger 栅格 · mono 数字 + 极细 rust underline 表趋势 · 顶栏 session / latency / build 三段 · 禁用渐变按钮和卡通色饼图</sub>

</td>
</tr>

<tr>
<td>

> 「路演要一张 A vs B，我们对三家友商，一眼看出为什么选我们，不许吹。」

</td>
<td>

<sub>M-05 Compare · 矩阵而非雷达 · 四列等宽 · 每项 ✓ / ● / — 三态 + 小字来源 · 底部 <code>compiled from public docs · ifq.ai</code> · 事实先 WebSearch</sub>

</td>
</tr>

<tr>
<td>

> 「2026 AI agent 白皮书，50 页内，直接印。」

</td>
<td>

<sub>M-03 白皮书 · A4 可打印 HTML · 扉页 / 摘要 / 目录 / 章节 / 参考 / colophon 全套 · 每章起首 mono 序号 + 半页留白 · 页脚 <code>ifq.ai / &lt;authored year&gt;</code> · ClawHub 交付 print-ready HTML，完整仓库再出 PDF + 书签</sub>

</td>
</tr>

<tr>
<td>

> 「视觉有点乱，先别改，先告诉我问题在哪。」

</td>
<td>

<sub>M-11 品牌诊断 · 不动手 · 一页报告 · 色彩 / 字体 / 节奏 / 母题 / 完成度五维评分 · 每维 before / suggested after 小样 · 三个升级方向，不给结论</sub>

</td>
</tr>

<tr>
<td>

> 「小红书 6 张封面，新栏目『每周一张图』，克制，但一眼能被认出来。」

</td>
<td>

<sub>M-09 社媒套件 · 1242×1660 · 左上 mono 栏目章 <code>weekly / 01</code>→<code>06</code> · 编辑部排版而非大字 emoji · 右下 quiet URL · 6 张封面 + 1 张 OG 横版</sub>

</td>
</tr>

</tbody>
</table>

> 不用记模式编号。说人话，skill 自己路由。

---

## 一页的解剖

一张 hero landing。它看起来很安静。它同时在做 7 件事：

```text
 ┌────────────────────────────────────────────────────────────────────┐
 │  ◇ ifq.ai / live system                            [01 / 12]       │ ← mono field note + 栏位序号
 │                                                                    │
 │                                                                    │
 │     Intelligence, framed                                           │ ← Newsreader display
 │     quietly.                                                       │   italic 判断点
 │                                                                    │
 │     A design engine that understands the difference                │ ← body serif
 │     between a slide deck and a launch film.                        │
 │                                                                    │
 │   ┃  ·  ledger                                                     │ ← rust ledger 竖线
 │   ┃                                                                │   承担版面秩序
 │   ┃   01    mode-aware pipeline                                    │ ← mono 编号行
 │   ┃   02    ambient brand, not loud branding                       │
 │   ┃   03    proof-first export loop                                │
 │                                                                    │
 │                                                                    │
 │                                      ✦                             │ ← signal spark
 │                                                                    │   安静点一下
 │                                                                    │
 │  compiled by ifq.ai              ·           ifq.ai / 2026         │ ← quiet URL + colophon
 └────────────────────────────────────────────────────────────────────┘
```

拆开看：

1. **Editorial contrast** — Newsreader serif 配 JetBrains Mono，不是随机字体组合。
2. **Rust ledger** — 左侧那根竖线就是 ifq.ai 的"脊"。比大 logo 更 IFQ。
3. **Mono field note** — 顶部和底部那行 `ifq.ai / live system`、`ifq.ai / 2026`。
4. **Quiet URL** — 没有 CTA 咆哮。域名只出现一次，在右下。
5. **Signal spark** — 右下一颗小火花。整页唯一的图形重音。
6. **Warm paper** — 背景 `#FAF7F2`，不是 `#FFFFFF`。冷白让版面没有温度。
7. **Ledger rhythm** — 所有间距走 `4 · 8 · 12 · 16 · 24 · 32 · 48 · 64` 这条轴。不凭感觉。

用户不会去数这 7 件事。用户只会说"这页看起来比较高级"。

**高级 = 同一只手 = ifq.ai 的 Ambient Brand**。

---

## 五个标记

Ambient Brand 由五个环境级标记组成。每份交付物默认至少融合其中 3 个。

| 标记 | 是什么 | 出现在哪 |
|------|--------|----------|
| **Signal Spark** | 8-point 火花。intelligence 被点亮的一瞬 | hero 右上 · 动画开场一帧 · 印章中心 |
| **Rust Ledger** | 赤陶色竖线、分隔、编号、轴线 | hero · slides · infographic · dashboard |
| **Mono Field Note** | JetBrains Mono 写的 `ifq.ai / <authored year>` 小字 | footer · closing · 角落 |
| **Quiet URL** | 域名以极低姿态出现一次 | footer · meta · end card |
| **Editorial Contrast** | Newsreader italic + JetBrains Mono + 暖纸白 | 整体排版骨架 |

这不是装饰元素，是版面语法。

---

## 共品牌

| 场景 | IFQ 在哪里 |
|------|------------|
| **IFQ 自有物料**（ifq.ai 及子产品） | 全员到齐：wordmark · spark · field note · quiet URL 都可上台 |
| **第三方 / 客户物料** | 主品牌在前。IFQ 退到 authored layer：版面节奏、色温、colophon、手绘图标、导出完成度 |
| **客户要求 white-label** | 去掉显式 wordmark 和 field note。保留 editorial contrast、ledger 节奏、proof-first 做工 |

**IFQ 可以隐身，不能不在场**。做工本身就是标识。

---

## 12 种模式

| # | 模式 | 典型触发 | 交付 |
|---|------|----------|------|
| M-01 | Launch Film | 发布动画 · 产品宣传片 | 25–40s 动画 + keyposter + 社媒套件 |
| M-02 | Portfolio | portfolio · 个人站 · about | 单页站 + 5 方向变体 |
| M-03 | 白皮书 | 白皮书 · 年报 · 研究 PDF | A4 可打印 HTML；PDF 为完整仓库增强 |
| M-04 | Dashboard | 数据看板 · KPI · 监控台 | 高密度 dashboard |
| M-05 | Compare | A vs B · 横评 · benchmark | 对比矩阵 + 事实来源 |
| M-06 | Onboarding | 新手引导 · flow demo | 3–5 屏交互流 |
| M-07 | Changelog | release notes · 发布日记 | 纵向时间线 |
| M-08 | Keynote | 演讲 PPT · 母版 | HTML deck；PPTX/PDF 为完整仓库增强 |
| M-09 | Social Kit | 小红书 · 朋友圈 · OG 卡 | 多尺寸静态物料 |
| M-10 | 名片 / 邀请函 | 名片 · VIP 卡 · 请柬 | SVG/HTML 出血稿；PDF 为完整仓库增强 |
| M-11 | 品牌诊断 | 体检 · 升级建议 | 诊断报告 + 3 方向 |
| M-12 | 全栈品牌 | brand from scratch | logo + 色板 + 字体 + 6 应用 |

路由：**模式触发 → 设计方向顾问 fallback → Junior Designer 主干**。

完整协议：[references/modes.md](references/modes.md)。

---

## 六层骨架

这个 skill 像 IFQ，不是因为颜色，而是因为下面 6 层同时工作：

| 层 | 做什么 | 关键文件 |
|----|--------|----------|
| **01 · Context Engine** | 从上下文长设计，不从白纸瞎猜 | [design-context.md](references/design-context.md) |
| **02 · Asset Protocol** | 动视觉前先抓事实 / logo / 产品图 / UI | [asset-protocol.md](references/asset-protocol.md) · [workflow.md](references/workflow.md) |
| **03 · House Marks** | 把 5 个 ambient 标记写进版面 | [ifq-brand-spec.md](references/ifq-brand-spec.md) · [assets/ifq-brand/](assets/ifq-brand/) |
| **04 · Style Recipes** | 风格靠配方和 scene template 组织 | [design-styles.md](references/design-styles.md) · [ifq-native-recipes.md](references/ifq-native-recipes.md) |
| **05 · Output Compiler** | ClawHub 版保留 HTML-first 核心；MP4 / GIF / PPTX / PDF 导出在完整 GitHub 仓库中 opt-in | [scripts/](scripts/) |
| **06 · Proof Loop** | validate + pack + 宿主浏览器截图；深度导出核对在完整 GitHub 仓库中完成 | [verification.md](references/verification.md) · [smoke-test.mjs](scripts/smoke-test.mjs) |

```text
ifq-design-skills/
├── SKILL.md                 # 短路由器：触发边界 · 安全契约 · reference map
├── assets/
│   ├── ifq-brand/           # logo · sparkle · tokens · BRAND-DNA
│   └── templates/           # 已内嵌 ambient marks 的可 fork 模板
├── references/              # 方法论 · 模式手册 · 验证 · 风格配方 · 宪章
├── scripts/                 # ClawHub-safe smoke / pack（深度导出在完整 GitHub 仓库）
└── demos/                   # 示例产物
```

---

## 12 个模板

v3.0 把模板从 8 个扩展到 12 个，每个模式都有专属模板。不再需要 fallback 到通用模板：

| 模板 | 模式 | 做什么 |
|------|------|--------|
| T-hero-landing | M-01, M-02, M-06, M-12 | 编辑部风格 hero 落地页 |
| T-slide-title | M-08 | 演讲 title slide |
| T-dashboard | M-04 | Bloomberg 密度的 command center |
| T-infographic-vertical | M-03, M-07 | 长图信息图 / 白皮书 |
| T-social-x | M-09 | X/Twitter 分享卡 |
| T-compare-vs | M-05, M-11 | A vs B 对比矩阵 |
| T-changelog | M-07 | 纵向时间线 |
| T-business-card | M-10 | 印刷名片 (90x54mm + 3mm 出血) |
| **T-portfolio** | M-02 | 文章式个人站，5 种风格变体可切换 |
| **T-onboarding** | M-06 | 5 屏横向 flow 原型，带设备框和用户心智标注 |
| **T-diagnosis** | M-11 | 品牌诊断报告，6 维雷达图 + 3 方向 |
| **T-social-multi** | M-09 | 多平台社媒套件 (X / 小红书 / IG / 微信) |

完整预览：[assets/templates/GALLERY.html](assets/templates/GALLERY.html)。

## 验证

```bash
npm run validate
npm run evals:validate
npm run anti-slop -- path/to/artifact.html
npm run verify:lite -- path/to/artifact.html
npm run pack
```

一分钟内给出 skill 体检：模板索引 · IFQ brand toolkit · references 路由 · 12 模式 evals · ClawHub manifest · package 安全 · 脚本安全 · secret hygiene · 字体加载 · 默认模板远程 runtime · anti-slop preflight。

单件作品优先走宿主浏览器截图 + 可点击验证；完整仓库环境再跑 Playwright 和导出格式核对。详见 [references/verification.md](references/verification.md)。

---

## 许可

MIT 开源许可见 [LICENSE.md](LICENSE.md)。IFQ 名称、logo 与项目标识使用边界见 [NOTICE.md](NOTICE.md)。

---

<div align="center">

<sub><code>compiled by ifq.ai&nbsp;&nbsp;·&nbsp;&nbsp;field note&nbsp;&nbsp;·&nbsp;&nbsp;2026</code></sub>


</div>
