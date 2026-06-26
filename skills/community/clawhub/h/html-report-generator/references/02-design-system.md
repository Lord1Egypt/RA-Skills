# 02 · 设计系统与视觉模板

> **核心原则：** 先理解用户描述，自创专属模板；T1–T6 是参考库，不是选项菜单。

---

## 🤖 第零步：自创报告专属模板（每次生成必须执行）

> ⚠ **强制要求**：在规划任何页面之前，AI 必须先完成此步骤。禁止直接套用 T1–T6。

### 执行流程

```
输入：用户的报告主题 / 风格描述 / 情感诉求
  ↓
Step A · 分析用户意图
  - 主题属于哪类（技术/商业/风险/数据/创意/…）
  - 用户有无隐含风格偏好（"专业""炫酷""简洁""科技感"…）
  - 是暗色系还是亮色系？强视觉冲击还是内容主导？
  ↓
Step B · 从 T1–T6 提取基因（混合/变形/新建）
  - 识别最匹配的 1–2 个基础模板作为"父模板"
  - 提取其背景方案 / 卡片结构 / 页眉风格 / 字体策略
  - 根据用户主题差异点，决定哪些基因要"变异"
  ↓
Step C · 声明本次报告专属模板 Tc（Custom）
  - 命名：Tc · [描述性名称]（[英文副标题]）
  - 明确写出：气质 / 适用 / 背景 / 卡片 / 字体 / 页眉 / CSS核心片段
  ↓
输出：Tc 模板定义 → 后续所有页面以 Tc 为主模板生成
```

### Tc 模板定义模板（AI 填写）

```
【本次报告专属模板 Tc】

名称：Tc · ___（___）
父模板：基于 T_（___）× T_（___）变形
气质定位：___、___、___
适用场景：___

背景方案：
  - 主背景：___
  - 纹理/光效：___

卡片风格：
  - 形状/圆角：___
  - 边框：___
  - 阴影/特效：___

字体搭配：
  - 展示字体：___
  - 正文字体：___

页眉形式：___

核心 CSS 变量：
  --bg: ___; --card: ___; --p: ___; --t: ___; --mt: ___;

CSS 核心片段（body / .card / .display-title）：
[AI 生成实际 CSS]
```

---

## 🎨 主题一致性规则

### 步骤 1 · 确定报告主基调

在 Tc 确定后，再根据主题选择配色主基调：

| 主题类型 | 主基调 | 核心配色 | 辅助配色 | 视觉模板倾向 |
|---------|--------|---------|---------|-------------|
| 技术/架构/原理 | 专业科技 | 方案 1 蓝 / 方案 5 紫 / 方案 6 青 | 方案 7 粉（展望） | T1/T3 系 |
| 风险/威胁/攻击 | 警示严肃 | 方案 2 红 / 方案 3 橙 | 方案 6 青（数据） | T1/T2 系 |
| 防御/安全/优化 | 积极正面 | 方案 4 绿 / 方案 1 蓝 | 方案 5 紫（技术） | T1/T4 系 |
| 数据/统计/分析 | 中性客观 | 方案 6 青 / 方案 1 蓝 | 方案 5 紫（强调） | T4 系 |
| 趋势/展望/预测 | 活力创新 | 方案 7 粉 / 方案 6 青 | 方案 1 蓝（数据） | T2/T5 系 |

> **🤖 AI 自扩展（主基调）：**
> - **若主题跨类型**，混合主基调：权重最大的类型为主，次要类型取辅助配色。
> - **若主题不在上表**，AI 自行推断情感倾向，在框架内创建新行，明确写出主基调/核心配色/辅助配色/推荐模板系，再执行。
>
> | 主题类型 | 主基调 | 核心配色 | 辅助配色 | 视觉模板倾向 |
> |---------|--------|---------|---------|-------------|
> | 合规/法律/监管 | 权威正式 | 方案 1 蓝（深）/ 方案 3 橙（警示） | 方案 6 青（细节） | T1/T5 系 |
> | 品牌/营销/传播 | 活力感性 | 方案 7 粉 / 方案 3 橙 | 方案 6 青（数据） | T2/T5 系 |
> | 金融/投资/商业 | 稳健专业 | 方案 1 蓝 / 方案 4 绿（增长） | 方案 2 红（风险） | T4/T1 系 |
> | *(AI 遇到新主题时在此追加)* | … | … | … | … |

### 步骤 2 · 70-20-10 配色分配原则

```
70% 页面 → 使用主基调配色（可微调，如方案 1 蓝 ↔ 方案 6 青）
20% 页面 → 使用对比色配色（逻辑转折/强调内容）
10% 页面 → 使用特殊场景配色（纯黑/纯白/渐变色）
```

### 步骤 3 · 背景一致性约束

| 报告类型 | 背景规则 | 禁止行为 |
|---------|---------|---------|
| 暗色报告 | 全部页面使用暗色背景 | 禁止混入亮色版纯白 |
| 亮色报告 | 全部页面使用亮色背景 | 禁止混入深色 |
| 混合报告 | 按章节划分，同一章节内背景一致 | 禁止无规律的明暗跳跃 |

### 步骤 4 · 页眉设计语言统一

整份报告页眉应保持统一的设计语言：
- 字体大小层级一致（如 eyebrow 永远 9.5px）
- 元素位置一致（如页码永远在右侧）
- 装饰元素一致（如状态灯/分割线风格）

---

## 🚫 禁止清单

生成每页前对照，有一条违反立即推翻重写：

```
❌ 跳过第零步，直接套用 T1–T6 未经任何定制
❌ Tc 模板未明确写出 CSS 核心片段就开始生成
❌ 整份报告没有明确的主基调配色（随机分配）
❌ 主基调配色使用率 < 50%
❌ 背景色在章节内不一致（无逻辑的明暗跳跃）
❌ 所有页面用同一种布局结构（左图 + 右 3 格出现超过 3 次）
❌ 卡片全部是同款：深色底 + 蓝色边框 + border-radius:6px
❌ 背景纯色无任何纹理、渐变、分割、光晕
❌ 页眉永远是"小字报告名 | 大字主题 | 右侧标签 + 页码"同一形式
❌ SVG 雷达图每页必有（最容易滥用的装饰性图表）
❌ font-family 永远是 'PingFang SC','Microsoft YaHei'
```

---

## 📚 T1–T6 基础模板参考库

> **定位：** 这是 AI 创建 Tc 时的"基因库"，提供可复用的 CSS 片段和设计语言。
> 每次生成不是从这里"选一个用"，而是从这里"提取基因重组"。

---

### T1 · 暗色精品（Dark Luxury）

**气质：** 科技感、高端精致、深夜实验室
**适用：** 执行摘要、技术原理、趋势展望

#### CSS 片段

```css
/* 引入展示字体 */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

body { background: #05080f; font-family: 'DM Sans','PingFang SC',sans-serif; }

/* 噪点纹理 */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:100;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)' opacity='0.035'/%3E%3C/svg%3E");
}

/* 环境光晕 */
.glow {
  position:absolute; border-radius:50%; pointer-events:none;
  background: radial-gradient(ellipse, rgba(R,G,B,0.09) 0%, transparent 65%);
}

/* 展示标题 */
.display-title {
  font-family: 'Syne','PingFang SC',sans-serif;
  font-size: 38px; font-weight: 800;
  letter-spacing: -1.5px; line-height: 1.0;
  background: linear-gradient(135deg, #e2e8f0 30%, ACCENT_COLOR);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 卡片 */
.card {
  background: rgba(13,17,30,0.8);
  border: 1px solid rgba(255,255,255,0.06);
  backdrop-filter: blur(8px);
  border-radius: 8px; padding: 14px 16px;
  display: flex; flex-direction: column; gap: 5px;
}
.card::before {            /* 顶部高光线 */
  content:''; display:block; height:1px; flex-shrink:0;
  background: linear-gradient(90deg, transparent, rgba(ACCENT,0.4), transparent);
  margin: -14px -16px 10px;
}
.card-bar {                /* 左侧色条 */
  position:absolute; left:0; top:14px; bottom:14px;
  width:2px; border-radius:2px;
}

/* 页眉风格 */
.hd-eyebrow {
  font-size: 9.5px; letter-spacing: 2.5px;
  text-transform: uppercase; color: #374151;
}
.status-dot {
  width:5px; height:5px; border-radius:50%;
  box-shadow: 0 0 8px rgba(R,G,B,0.9);
}

/* 统计数字行 */
.stat-num {
  font-family: 'Syne', sans-serif;
  font-size: 42px; font-weight: 800;
  line-height: 1; letter-spacing: -2px;
  background: linear-gradient(135deg, COLOR_A, COLOR_B);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}
.stat-divider {
  position:absolute; left:0; top:8%; height:84%; width:1px;
  background: linear-gradient(180deg, transparent, rgba(ACCENT,0.3), transparent);
}
```

---

### T2 · 编辑分割（Editorial Split）

**气质：** 杂志感、强叙事、视觉冲击、对比强烈
**适用：** 攻击原理、案例分析、防御方案、风险评估

#### CSS 片段

```css
/* 分割背景三层 */
.bg-dark {
  position:absolute; top:0; left:0; width:1017px; height:720px;
  background: #111827;
}
.bg-light {
  position:absolute; top:0; right:0; width:650px; height:720px;
  background: #f8f7f3;
  clip-path: polygon(60px 0, 100% 0, 100% 100%, 0 100%);
}
.accent-stripe {
  position:absolute; top:0; left:322px; width:28px; height:720px;
  background: linear-gradient(180deg, COLOR_TOP, COLOR_BOTTOM);
  clip-path: polygon(0 0, 100% 0, calc(100% - 28px) 100%, 0 100%);
}

/* 左栏超大标题 */
.big-title {
  font-size: 48px; font-weight: 900;
  line-height: 0.92; letter-spacing: -2px;
  color: #f9fafb;
}

/* 左栏统计项 */
.ls-item {
  border-left: 2px solid ACCENT;
  padding: 3px 0 3px 14px;
}
.ls-num { font-size: 30px; font-weight: 900; line-height: 1; letter-spacing: -1px; }

/* 右栏白底卡片 */
.card-light {
  background: #fff; border-radius: 6px;
  box-shadow: 0 1px 2px rgba(0,0,0,.06), 0 0 0 1px rgba(0,0,0,.04);
  padding: 12px 14px;
}

/* 右栏深色卡片 */
.card-dark { background: #1e293b; border-radius: 6px; padding: 12px 14px; }

/* 右栏彩色卡片（强调） */
.card-accent { background: ACCENT; border-radius: 6px; padding: 12px 14px; }

/* 标签 */
.tag-accent {
  display:inline-block; padding:2px 7px; border-radius:2px;
  font-size:9px; font-weight:700; letter-spacing:.3px;
  background: ACCENT; color: #fff;
}
```

---

### T3 · 终端代码（Terminal / Code Audit）

**气质：** 技术极客、审计报告、真实感、开发者专属
**适用：** 技术实现、工具框架、检测评估、漏洞分析

#### CSS 片段

```css
body {
  background: #0d1117;
  font-family: 'Courier New', Consolas, monospace;
}

/* 扫描线 */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:100;
  background: repeating-linear-gradient(
    0deg, transparent, transparent 2px,
    rgba(0,255,65,0.012) 2px, rgba(0,255,65,0.012) 4px
  );
}

/* 细网格 */
body::after {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background-image:
    linear-gradient(rgba(0,255,65,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,255,65,0.03) 1px, transparent 1px);
  background-size: 40px 40px;
}

/* Terminal 标题栏（32px，在 .hd 之上，需调整四区：terminal-bar 32px + hd 40px + ct 608px + ft 40px = 720） */
.terminal-bar {
  height: 32px; background: #161b22;
  border-bottom: 1px solid #30363d;
  display: flex; align-items: center; padding: 0 16px; gap: 8px;
  flex-shrink: 0;
}
.term-dot { width:10px; height:10px; border-radius:50%; }

/* 代码卡片 */
.code-card { background: #161b22; border: 1px solid #30363d; border-radius: 6px; overflow:hidden; }
.code-card-header {
  background: #21262d; padding: 6px 12px;
  border-bottom: 1px solid #30363d;
  display: flex; align-items: center; gap: 8px;
}
.code-body { padding: 10px 12px; font-family: monospace; font-size: 10.5px; }
.line { line-height: 1.6; white-space: nowrap; overflow: hidden; }
.ln { color:#484f58; width:24px; display:inline-block; text-align:right; margin-right:12px; user-select:none; }

/* 语法高亮 */
.kw { color: #ff7b72; }   /* 关键字 */
.fn { color: #d2a8ff; }   /* 函数名 */
.st { color: #a5d6ff; }   /* 字符串 */
.nm { color: #79c0ff; }   /* 数字 */
.cm { color: #8b949e; }   /* 注释 */
.vr { color: #ffa657; }   /* 变量 */

/* 状态标签 */
.badge-ok   { background:rgba(63,185,80,.15);  color:#3fb950; border:1px solid rgba(63,185,80,.3);  }
.badge-warn { background:rgba(210,153,34,.15); color:#d29922; border:1px solid rgba(210,153,34,.3); }
.badge-err  { background:rgba(248,81,73,.15);  color:#f85149; border:1px solid rgba(248,81,73,.3);  }
.badge-info { background:rgba(88,166,255,.15); color:#58a6ff; border:1px solid rgba(88,166,255,.3); }
/* 公共 */
.badge-term { padding:1px 6px; border-radius:3px; font-size:9px; font-family:monospace; font-weight:600; }

/* 终端输出颜色 */
.t-ok   { color: #3fb950; }
.t-warn { color: #d29922; }
.t-err  { color: #f85149; }
.t-info { color: #58a6ff; }
.t-dim  { color: #8b949e; }
```

> **T3 四区调整：** terminal-bar 占 32px，需把原 `hd 72px` 拆为 `terminal-bar 32px + hd 40px`，`ct` 改为 `608px`，`ft` 改为 `40px`，总和仍 = 720px。

---

### T4 · 数据仪表盘（Dashboard Analytical）

**气质：** 数据驱动、BI 报表、专业分析
**适用：** 数据分析、检测统计、趋势对比、ROI 计算

#### CSS 片段

```css
/* 亮色版 */
body { background: #f0f4f8; color: #1e293b; }

/* KPI 卡片 */
.kpi {
  background: #fff; border-radius: 8px;
  padding: 12px 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,.08);
  border-top: 3px solid ACCENT;
}
.kpi-n {
  font-size: 32px; font-weight: 800;
  letter-spacing: -1px; line-height: 1;
}
.kpi-label { font-size: 9.5px; color: #9ca3af; text-transform: uppercase; letter-spacing: .5px; margin-top: 2px; }
.kpi-trend { font-size: 11px; margin-top: 3px; }
.kpi-trend.up   { color: #10b981; }
.kpi-trend.down { color: #ef4444; }

/* 图表容器卡片 */
.chart-card {
  background: #fff; border-radius: 8px;
  padding: 14px 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,.06);
}
.chart-title { font-size: 11.5px; font-weight: 700; color: #374151; margin-bottom: 8px; }

/* 数据表格 */
.data-table { width:100%; border-collapse:collapse; font-size: 10.5px; }
.data-table th { background:#f8fafc; color:#9ca3af; padding:5px 8px; text-align:left; font-weight:600; border-bottom:2px solid #e5e7eb; }
.data-table td { padding:5px 8px; border-bottom:1px solid #f1f5f9; color:#374151; }
```

---

### T5 · 极简文字（Editorial Minimal）

**气质：** 学术报告、深度长文、克制高级、内容为王
**适用：** 概念定义、风险摘要、趋势预测、观点陈述

#### CSS 片段

```css
body { background: #fafaf8; color: #111827; }

/* 超大标题 */
.hero-title {
  font-size: 56px; font-weight: 900;
  letter-spacing: -2.5px; line-height: 0.92;
  color: #111827;
}
.hero-accent { color: ACCENT; }     /* 单一强调色 */

/* 细分隔线 */
.divider-thin {
  height: 1px;
  background: linear-gradient(90deg, #e5e7eb, transparent);
  margin: 12px 0;
}

/* 极简卡片（无背景色，仅左侧色条） */
.minimal-item {
  border-left: 3px solid ACCENT;
  padding: 6px 0 6px 14px;
}
.minimal-item-title { font-size: 12px; font-weight: 700; color: #111827; }
.minimal-item-body  { font-size: 11.5px; color: #6b7280; line-height: 1.5; margin-top: 3px; }

/* 大号引用 */
.pull-quote {
  font-size: 18px; font-weight: 600; color: #111827;
  line-height: 1.4; letter-spacing: -0.3px;
  border-left: 3px solid ACCENT;
  padding-left: 16px;
}
```

---

### T6 · 霓虹赛博（Neon Cyberpunk）

**气质：** 高饱和、夜间城市、未来感、极度视觉冲击
**适用：** 威胁情报、攻击溯源、黑产分析、极客演讲

#### CSS 片段

```css
body { background: #080010; color: #e0e0ff; font-family: 'Courier New', monospace; }

/* 霓虹光晕 */
.neon-glow-pink  { text-shadow: 0 0 8px #ff2d78, 0 0 20px rgba(255,45,120,0.4); color: #ff2d78; }
.neon-glow-cyan  { text-shadow: 0 0 8px #00ffe7, 0 0 20px rgba(0,255,231,0.4); color: #00ffe7; }
.neon-glow-purple{ text-shadow: 0 0 8px #bf5fff, 0 0 20px rgba(191,95,255,0.4); color: #bf5fff; }

/* 赛博卡片 */
.cyber-card {
  background: rgba(10,0,30,0.85);
  border: 1px solid NEON_COLOR;
  box-shadow: 0 0 12px rgba(NEON_R,NEON_G,NEON_B,0.25), inset 0 0 20px rgba(0,0,0,0.5);
  border-radius: 4px; padding: 14px 16px;
}

/* 闪烁光标 */
.cursor::after {
  content: '█'; animation: blink 1s step-end infinite;
}
@keyframes blink { 50% { opacity: 0; } }
```

---

## 模板排版参数汇总

| 模板 | 显示字体 | 正文字体 | 页面主标题字号 | 页眉形式 |
|------|---------|---------|-------------|---------|
| T1 暗色精品 | Syne 800 | DM Sans 300/400 | 32–42px 渐变裁剪 | 小大写 + 圆点灯 + monospace 页码 |
| T2 编辑分割 | 系统黑体 900 | 系统黑体 300 | 44–54px 白/黑 | 无横向页眉，融入左栏 |
| T3 终端代码 | monospace | monospace | 无大标题 | terminal-bar + 路径命令行 |
| T4 数据仪表 | 系统黑体 700 | 系统黑体 400 | 14–18px | 简洁 左标题 右日期 + 页码 |
| T5 极简文字 | 系统黑体 900 | 系统黑体 300 | 48–64px | 仅细线 + 页码 |
| T6 霓虹赛博 | monospace / Syne 800 | monospace | 28–40px 霓虹辉光 | 赛博路径格式 + 光标 |
| Tc 自创模板 | AI 根据主题自定 | AI 根据主题自定 | AI 根据主题自定 | AI 根据主题自定 |

**Google Fonts 引入（T1 及 Tc 需要时，放在 `<head>` 第一行）：**

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
```

---

## 多样性核查（在一致性前提下）

生成完所有页后对照：

```
□ 已完成第零步，Tc 模板有完整定义？
□ 主基调配色使用率 ≥ 60%？
□ 视觉模板变化 ≥ 2 种？
□ 没有连续 3 页使用完全相同的布局 + 配色组合？
□ 背景色在章节内保持一致？
□ 没有连续 3 页使用同一种模板？
□ 同一种卡片组合（背景色 + 圆角 + 边框）没有出现超过 4 次？
```
