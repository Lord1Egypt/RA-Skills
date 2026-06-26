---
name: huo15-openclaw-ppt
displayName: 火一五演示稿技能
description: 基于 design tokens 的 PPT 生成技能。内置 21 套生产级审美方案（Apple 发布会 / Apple.com / Apple macOS 26 Liquid Glass 玻璃 / 原研哉极简 / 中国水墨 / 国风故宫 / 赛博朋克绚彩 / 梵高油画 / 达芬奇手稿 / 小红书时尚奶油胶片 / 莫兰迪高级灰 / 孟菲斯 80s / 包豪斯 / 韦斯安德森 / 科技霓虹 / Vercel/Linear 极简）+ 11 个语义化页面模板。自动 fit 防 CJK 溢出，玻璃风自带七彩光球+磨砂卡，水墨/国风自带朱砂方印+万字纹边框+飞白笔触，科技风自带渐变背景+网格+glow halo+四角刻度。单张 slide 即可当品牌海报。触发词：做PPT、生成PPT、PPT、Apple发布会、苹果玻璃风、liquid glass、原研哉、水墨、国风、赛博朋克、梵高、达芬奇、莫兰迪、孟菲斯、包豪斯、韦斯安德森、小红书时尚、复古胶片、Vercel风。
version: 5.0.1
aliases:
  - 火一五PPT技能
  - 火一五演示稿技能
  - PPT生成
  - AppleKeynote风格
  - Apple发布会PPT
  - 苹果风格PPT
  - 苹果玻璃风
  - LiquidGlassPPT
  - macOS26风格
  - iOS26风格
  - 原研哉PPT
  - 无印良品风
  - MUJI风格
  - 水墨PPT
  - 中国水墨
  - 国风PPT
  - 故宫风
  - 中国风PPT
  - 赛博朋克绚彩PPT
  - 银翼杀手风
  - 梵高PPT
  - 油画PPT
  - 达芬奇PPT
  - 文艺复兴风
  - 小红书时尚PPT
  - 小红书博主PPT
  - 奶油博主PPT
  - 复古胶片PPT
  - 莫兰迪PPT
  - 高级灰PPT
  - 孟菲斯PPT
  - 包豪斯PPT
  - 韦斯安德森PPT
  - 对称美学PPT
  - 乔布斯风格PPT
  - 科技风PPT
  - 霓虹PPT
  - 极简科技PPT
  - VercelPPT
  - LinearPPT
  - SaaSPPT
  - AI发布会PPT
  - 品牌海报
dependencies:
  python-packages:
    - python-pptx
    - Pillow
---

# 火一五 PPT 技能 v3.2

> Design tokens + 11 页面模板 + **21 套生产级审美方案** — 青岛火一五信息科技有限公司

---

## 〇、v4.0 完整能力（v3.3-v4.0 累加）— 媲美 Gamma + 独有差异化

### 核心 CLI 矩阵

| 版本 | 脚本 | 能力 | 对标 Gamma |
|---|---|---|---|
| v3.3 | `anti_slop_audit.py` `wcag_audit.py` `charts.py` `pptx_critique.py` | 反 AI Slop 15 红线 + WCAG AA + 真数据图 + 4 档自评 | 我们独有 |
| v3.4 | `prompt_to_deck.py` | 自然语言 prompt → JSON deck（Claude API + cache） | Gamma 60 秒生成 |
| v3.5 | `smart_layouts.py` | timeline / pyramid / funnel / steps 4 种 PNG | Gamma Smart Layouts |
| v3.6 | `ai_image.py` | Unsplash + Pexels + Placeholder 3 provider | Gamma Imagine |
| v3.7 | `brand_init.py` | Logo → 主色提取 → brand-pack.json | Gamma brand kit |
| v3.8 | `web_export.py` `url_import.py` | scroll-snap HTML 发布 + URL 抓内容转 deck | Gamma publish/import |
| v3.9 | `remix.py` | 受众/语言/语气改写（6 audiences × 7 langs × 5 tones） | Gamma Remix |
| v4.0 | `auto_critique.py` | 一键 quick/deep/full 评审 + Markdown 报告 + PNG 截图 | 我们独有 |

### 一键工作流（推荐）

```bash
export ANTHROPIC_API_KEY='sk-ant-...'

# 1. prompt → deck
python3 scripts/prompt_to_deck.py "做一份 8 分钟产品发布演讲" \
    --output /tmp/d.json --build /tmp/d.pptx

# 2. 改受众
python3 scripts/remix.py /tmp/d.json --audience board \
    --output /tmp/board.json --build /tmp/board.pptx

# 3. 发布为网站
python3 scripts/web_export.py /tmp/d.json --output /tmp/site.html

# 4. 自动评审
python3 scripts/auto_critique.py --deck /tmp/d.json --mode full \
    --output-dir /tmp/critique/
```

### 不输 Gamma 的独有优势

- **本地运行 + 数据隐私**（合同 / 财报不上传 SaaS）
- **CJK 一等公民**（朱砂印章 / 飞白 / 国风元素，Gamma 永远做不到）
- **21 套真审美方案**（玻璃 / 水墨 / 国风 / 梵高 / 包豪斯 / 韦斯安德森，Gamma 偏新企业风千篇一律）
- **15 条反 AI Slop 红线机器化校验** + WCAG 2.2 AA 自动审计（Gamma 没系统）
- **零 vendor lock-in**（输出 PPTX / HTML 永远是自己的）

---

## 〇、v4.1 智能动画引擎 + v4.2 PPTX 编辑（对标 ChatPPT 核心差异化）

### v4.1 `pptx_animate.py` — 给现有 .pptx 加智能转场

```bash
python3 scripts/pptx_animate.py /tmp/d.pptx --style apple-keynote \
    --deck-json /tmp/d.json --output /tmp/animated.pptx
```

4 种风格预设（OOXML `<p:transition>` 直接注入）：
- `apple-keynote` — push + section wipe + quote fade
- `minimal-fade` — 全 slide fade，克制
- `dynamic-slide` — cover + push 活泼
- `cinematic` — cover + fade 电影感

按 slide type 智能选转场（hero_cover→cover 类 / section_divider→wipe / quote_card→fade / 默认 push）。**对标 ChatPPT "全网唯一智能动画引擎"，但本地实现，零云端依赖**。

### v4.2 `pptx_edit.py` — 加载现有 .pptx → AI 改写 → 输出

```bash
# 一条龙 AI 改写
python3 scripts/pptx_edit.py rewrite /input.pptx \
    --instruction "把所有标题改简洁，加 Apple 发布会的克制感" \
    --output /improved.pptx

# 提取 → 人工编辑 → 写回（不依赖 LLM）
python3 scripts/pptx_edit.py extract /input.pptx --output /tmp/edit.json
# (人工改 /tmp/edit.json 的 paragraphs[].text)
python3 scripts/pptx_edit.py apply /input.pptx --edits /tmp/edit.json \
    --output /improved.pptx
```

工作原理：python-pptx run-level 替换文字，**保留所有 formatting（字体 / 颜色 / 字号 / 段落对齐）**。对标 ChatPPT Office 插件模式，但走命令行 + OpenClaw 调用，更适合企业批量处理。

实测：6 张 slide deck → extract 30 paragraphs → 改 1 段 → apply → 再 extract 验证改动落实 ✓

---

## 〇、v4.3 演讲稿 + 文本辅写 + v4.4 多源输入（对标 ChatPPT）

### v4.3 `speaker_notes.py` — 自动生成讲解词写入 .pptx 备注层

```bash
python3 scripts/speaker_notes.py /tmp/d.pptx --tone conversational \
    --seconds-per-slide 60 --output /tmp/d-with-notes.pptx
```

5 种语气：`formal` / `conversational`（默认）/ `passionate` / `storytelling` / `professor`。120 字/分钟换算字数（60s = ~120 字）。一次 Claude API 批量生成全 deck 演讲稿，写入 .pptx notes 层，演示模式可看到。

### v4.3 `slide_polish.py` — 10 种局部文案改写模式

```bash
# 改一张 slide
python3 scripts/slide_polish.py /tmp/d.json --slide 3 --mode refine \
    --output /tmp/d-polished.json --build /tmp/d-polished.pptx

# 只改所有 slide 的标题
python3 scripts/slide_polish.py /tmp/d.json --field title --mode shorten -o /tmp/x.json
```

10 模式（`--list-modes` 看全表）：
- 语言改写：`refine` / `shorten` / `expand` / `rewrite`
- 加内容：`add-data` / `add-quote` / `add-joke`
- 修辞强化：`emphasize` / `metaphor` / `elevate`

### v4.4 多源输入：docx / xmind / pdf

```bash
# Word 文档 → deck
python3 scripts/docx_import.py report.docx --output /tmp/d.json --build /tmp/d.pptx

# XMind 思维导图 → deck（中心主题→封面，一级分支→章节，二级→列表项）
python3 scripts/xmind_import.py mindmap.xmind --output /tmp/d.json

# PDF → deck（PyMuPDF 优先，fallback pypdf）
python3 scripts/pdf_import.py whitepaper.pdf --output /tmp/d.json
```

实测：
- docx 抽 20260506会议章程.docx → 2396 字符 ✓
- pdf 抽 v7.8.5 demo 合同 → 151 字符 ✓
- xmind 解析 .xmind ZIP（content.json + content.xml 两种格式都支持）

`--print-extracted` 不调 LLM 验证抽取流程。

---

## 〇、v5.0 完整能力矩阵（v3.3 → v5.0 累加，对标 Gamma + ChatPPT）

### 18 个 CLI 脚本 — 媲美 Gamma + ChatPPT + 独有差异化

| 类别 | 脚本 | 能力 | 对标 |
|---|---|---|---|
| **🆕 v5.0 LLM provider** | `llm_provider.py` | 6 backend 抽象（anthropic/openai/deepseek/qwen/doubao/openclaw） | 国内合规 |
| **生成入口** | `prompt_to_deck.py` | 自然语言 → JSON deck（cache 90% token 省） | Gamma |
| | `url_import.py` | URL → deck | Gamma |
| | `docx_import.py` | Word → deck | ChatPPT |
| | `xmind_import.py` | XMind → deck（新老格式都支持） | ChatPPT |
| | `pdf_import.py` | PDF → deck（PyMuPDF 优先 / pypdf fallback） | ChatPPT |
| **设计 + 视觉** | `smart_layouts.py` | timeline / pyramid / funnel / steps 4 种 | Gamma Smart Layouts |
| | `ai_image.py` | Unsplash / Pexels / Placeholder 3 provider | Gamma Imagine |
| | `charts.py` | matplotlib bar/line/pie/area 真数据图 | Gamma |
| | `brand_init.py` | logo → 主色 → brand-pack.json | Gamma brand kit |
| **改写工具** | `remix.py` | 6 audiences × 7 langs × 5 tones | Gamma Remix |
| | `slide_polish.py` | 10 模式 polish（refine/shorten/add-data/...） | ChatPPT 文本辅写 |
| | `pptx_edit.py` | 加载现有 pptx → AI 改写 → 输出（保留 formatting） | ChatPPT Office 插件 |
| | `speaker_notes.py` | 5 种语气演讲稿写入 .pptx notes 层 | ChatPPT 演讲稿 |
| **效果增强** | `pptx_animate.py` | 4 种动画风格（OOXML transition 注入） | ChatPPT 动画引擎 |
| **导出** | `web_export.py` | scroll-snap HTML 浏览体验 | Gamma publish |
| | `image_export.py` | 长图 / 九宫格 / 横排走廊 | ChatPPT 公众号 |
| | `video_export.py` | MP4 + BGM 淡出 | ChatPPT 视频号 |
| **审计** | `anti_slop_audit.py` | 15 红线机器化校验 | **独有** |
| | `wcag_audit.py` | WCAG 2.2 AA 对比度 | **独有** |
| | `pptx_critique.py` `auto_critique.py` | 4 档审美档位 + 6 维评审 | **独有** |

### 一键完整工作流

```bash
# Provider 任选其一（v5.0 支持 6 种）
export PPT_LLM_PROVIDER=anthropic    # 或 openai / deepseek / qwen / doubao / openclaw
export ANTHROPIC_API_KEY='sk-ant-...'  # 或对应 provider 的 env key

# 多源输入 → JSON
python3 scripts/prompt_to_deck.py "做一份发布会演讲" -o /tmp/d.json
# 或 docx_import / xmind_import / pdf_import / url_import

# 改写优化 → JSON
python3 scripts/slide_polish.py /tmp/d.json --mode shorten -o /tmp/d2.json
python3 scripts/remix.py /tmp/d.json --audience board --lang en -o /tmp/board-en.json

# 出 PPTX
python3 scripts/create_pptx_combined.py --spec /tmp/d.json --pack apple-light -o /tmp/d.pptx

# 加动画 + 演讲稿
python3 scripts/pptx_animate.py /tmp/d.pptx --style apple-keynote -o /tmp/d-a.pptx
python3 scripts/speaker_notes.py /tmp/d-a.pptx --tone passionate -o /tmp/d-final.pptx

# 多形态导出
python3 scripts/web_export.py /tmp/d.json -o /tmp/site.html
python3 scripts/image_export.py /tmp/d-final.pptx --layout vertical -o /tmp/longpic.jpg
python3 scripts/video_export.py /tmp/d-final.pptx --bgm m.mp3 -o /tmp/d.mp4

# 自动评审
python3 scripts/auto_critique.py --deck /tmp/d.json --mode full -o /tmp/critique/
```

### 永远的独有护城河（vs Gamma + ChatPPT）

- **本地运行 + 数据隐私**（合同/财报不上传 SaaS）
- **CJK 一等公民**（朱砂印章 / 飞白 / 国风 / 中文字体 fallback）
- **21 套真审美方案**（玻璃 / 水墨 / 国风 / 梵高 / 包豪斯 / 韦斯安德森）
- **15 条反 AI Slop 红线机器化** + WCAG 2.2 AA 自检
- **6 维 4 档审美评审** + 自动 PNG 截图 + Markdown 报告
- **6 LLM provider 灵活切换**（国内合规场景必备）
- **零 vendor lock-in** — 输出 PPTX/HTML/MP4/JPG 永远是自己的

---

## 〇、v3.3 设计能力栈集成（媲美 claude design）

参照 `huo15-openclaw-frontend-design` v4.7 / `huo15-openclaw-design-critique` v2.0，把 PPT 也带入 4 档审美档位识别（AI-Slop / Junior / Senior / Master）。

### 4 个新增 CLI

```bash
# 1. 反 AI Slop 红线自检（15 条机器化校验，参照 frontend-design）
python3 scripts/anti_slop_audit.py                # 全部 21 套 pack
python3 scripts/anti_slop_audit.py apple-light   # 单 pack 详情
python3 scripts/anti_slop_audit.py --json --fail-on-violation  # CI 模式

# 2. WCAG 2.2 AA 文字对比度自检（每对 fg/bg ratio ≥ 4.5）
python3 scripts/wcag_audit.py
python3 scripts/wcag_audit.py apple-keynote

# 3. matplotlib 真数据图表（替代 CSS 假产品图，反 AI Slop R5）
python3 scripts/charts.py bar --pack apple-light \
    --title "营收增长" --xlabel "季度" --ylabel "营收（万元）" \
    --data "Q1=120,Q2=180,Q3=240,Q4=320" \
    --output ./chart.png
# 支持 bar / hbar / line / pie / scatter / area；中文字体自动 fallback
# 也可以 Python 直接用：from charts import render_chart

# 4. 设计自评（综合 anti-slop + wcag，给 4 档定位 + Keep/Fix/Quick Wins）
python3 scripts/pptx_critique.py --pack apple-light --deep
python3 scripts/pptx_critique.py --all          # 21 套 pack 综合排名
```

### v3.3 21 套 pack 自评结果

| 档位 | 数量 | pack |
|---|---|---|
| 🏆 Master (≥90) | 19 | apple-keynote / apple-light / liquid-glass / muji / ink-wash / guofeng / tech-neon / tech-minimal / cyberpunk-vivid / van-gogh / da-vinci / xhs-fashion / memphis / bauhaus / wes-anderson / xiaohongshu-vintage / jobs-dark / xiaohongshu / xiaohongshu-portrait |
| ✅ Senior (75-89) | 2 | morandi (80) / xiaohongshu-creator (78.2) — 流派必然的低对比度，仅适合极简静态展示 |
| ⚠️  Junior / ❌ AI-Slop | 0 | （v3.3 修了 4 个 pack 的 Inter 字体 + tech-minimal 紫色 accent，全员脱离低档） |

### 反 AI Slop 15 条红线（机器化校验摘要）

| # | 禁用项 | 校验方式 |
|---|---|---|
| 1 | Inter / Roboto / Arial / system-ui 字体 | display_font / body_font 字段比对禁用列表 |
| 2 | 紫色调 accent（H ∈ [240°, 300°]，S>40%） | hex → HSL 换算判定 |
| 3 | emoji 当图标 | 字段含 emoji codepoint 范围 |
| 4 | border-radius 默认 12 / 16px | card_radius pt 值检测 |
| 6 | #121212 暗黑 + 紫主题 | bg + accent 联动 |
| 8 | iOS 系统色直接套用（#007AFF 等） | accent 黑名单匹配 |
| 10 | backdrop-blur 玻璃形态滥用 | glass / frosted 必须 explicit 命名 |
| 11 | AI 渐变模糊背景（紫粉蓝青） | conic-gradient 紫粉关键词 |

### 与 4 件套设计能力栈联动

| 能力 | 来源 skill | PPT 怎么用 |
|---|---|---|
| 6 维深度评审 | `huo15-openclaw-design-critique` v2.0 | 导出 slide 为 PNG → 跑 design-critique → 拿对标差距 |
| 8 流派 design tokens | `huo15-openclaw-frontend-design` v4.7 | 复用 6 大美学方向（Bold-Minimal / Editorial / Brutalist 等） |
| 多方向并行对比 | `huo15-openclaw-design-director` v3.0 | 一题三方向：选 3 个不同流派 pack 各出一份 PPT |
| 品牌资产 5 步 | `huo15-openclaw-brand-protocol` v1.0 | 写 PPT 前先 Ask/Search/Verify 品牌官方定位 + 注入 Theme |

---

## 一、核心理念

v2.x 是「色卡游戏」——只改 primary/accent 两个颜色就叫一个新风格。v3.0 重写成真正的**设计系统**：

```
StylePack = Palette + Typography + Spacing + Elevation + Decoration + Canvas
```

每一层都是独立的 tokens，单一风格对应一整组 tokens。例如「Apple 发布会」不只是「黑底」，而是：

- **Palette**：纯黑 `#000000` 底 + 4 级灰阶文字 + Apple 蓝 `#0A84FF`
- **Typography**：SF Pro Display + hero 160pt + 负字距 -3% + 行高 0.95
- **Spacing**：8pt grid + hero 页左右留白 1.2"
- **Elevation**：完全 flat，无阴影
- **Decoration**：居中对齐、英文全大写、不显示页脚

v3.1 在 Decoration 层追加了**六件套科技装饰**，每个 pack 都能独立开关：

| 装饰 | 作用 |
|----|----|
| `gradient_bg` | 背景渐变（取代纯色），给 slide 加深度 |
| `accent_gradient` | hero/section/stat 大字做渐变文字（Keynote/PowerPoint 端显示，Impress 回落纯色） |
| `grid_overlay` / `dot_grid` | 细线网格或点阵背景层，赛博 / Vercel 的视觉招牌 |
| `glow_accent` | 强调色大字周围叠多层半透明椭圆模拟辉光 |
| `corner_marks` | 四角 L 型取景框刻度 |
| `dev_badge` | 左下等宽字体版本戳（`BUILD · 2026.4.24` / `v2026 · BUILD 1337`） |

科技风由此而来——每张 slide 都能直接当品牌海报/社媒头图使用。

---

## 二、6 套审美方案

| pack key | 风格 | 适用场景 |
|---------|------|---------|
| `apple-keynote`（别名 `apple`, `苹果`, `发布会`） | Apple 发布会暗场 | 新品发布、融资路演、重磅主题 |
| `apple-light`（别名 `苹果白`, `苹果官网`） | Apple.com 白场 | 产品介绍页、功能说明、官网风 |
| `xiaohongshu-creator`（别名 `博主`, `博主风`, `生活博主`, `奶油博主`） | 小红书博主（奶油生活系） | 博主笔记、种草分享、温度叙事 |
| `xiaohongshu-vintage`（别名 `复古`, `胶片`, `复古胶片`） | 小红书博主（复古胶片） | 旅行手记、文艺向、生活美学 |
| `tech-neon`（别名 `tech`, `neon`, `科技`, `科技风`, `霓虹`, `赛博`, `赛博朋克`, `cyberpunk`） | **科技霓虹（赛博黑蓝）** | **AI 产品发布、黑客马拉松、技术 roadshow** |
| `tech-minimal`（别名 `vercel`, `linear`, `saas`, `极简科技`, `暗黑极简`） | **科技极简（Vercel/Linear 风）** | **SaaS 产品主页、DevTool 推销、基础设施介绍** |

### 2.1 apple-keynote —— 真·发布会

- **配色**：纯黑 `#000000`（不是深蓝！）+ 白灰文字 + Apple 品牌蓝
- **字体**：SF Pro Display + SF Pro Text
- **hero 字号**：**160pt**（是 v2 的 2.5 倍，带自动 fit 避免 CJK 溢出）
- **装饰**：完全居中、英文小字全大写（INTRODUCING / SCALE）、不显示页脚
- **big_stat 字号**：280pt — "2B" 一张页的视觉锚点

### 2.2 apple-light —— 产品页白场

- **配色**：纯白 + Apple.com 的卡片灰 `#F5F5F7` + 链接蓝 `#0071E3`
- **字体**：SF Pro Display
- **hero 字号**：120pt
- **卡片**：无描边，圆角 0.18"，靠填色区分
- **装饰**：居中对齐、英文不全大写

### 2.3 xiaohongshu-creator —— 奶油生活博主

- **配色**：奶油 `#FBF7F0` 底 + 焦糖咖 `#3E2E1F` 主文字 + 鼠尾草绿 `#9FAE8B` 点缀
- **字体**：**Noto Serif SC**（衬线！）+ PingFang SC 正文
- **hero 字号**：72pt + 正字距 +2%（衬线字撑开）
- **装饰**：左对齐、标题左侧竖条 accent bar、圆角 0.22" 卡片 + 微阴影
- **特色**：文字不用纯黑而用焦糖咖色，配 sage green accent 做博主的温度

### 2.4 xiaohongshu-vintage —— 复古胶片

- **配色**：复古米 `#F2EAD9` + 深栗咖 `#4A3526` 文字 + 雾霾蓝 `#A8B8C6` accent
- **字体**：Noto Serif SC（标题和正文都衬线，强化胶片感）
- **hero 字号**：64pt + 更松字距 +3% + 高行高 1.2
- **装饰**：封面顶/底装饰横线、卡片直角 0.08" 有描边（胶片边框感）

### 2.5 tech-neon —— 科技霓虹（赛博黑蓝）🆕

- **配色**：深蓝黑 `#050510` 底 + 冷灰蓝文字 + 电青 `#00D9FF` 主 accent + 电紫 `#7C3AED` 辅 accent
- **字体**：Inter（SF Pro 兜底）+ **JetBrains Mono** 做 caption/metadata
- **hero 字号**：144pt + 左对齐 + 负字距 -2.5%
- **装饰**：**全系六件套全开**——对角微渐变背景 + 细线网格 + 四角 L 型刻度 + hero/stat 辉光 halo + 左下 `BUILD · 日期` dev badge + 等宽小字 metadata
- **accent_gradient**：`#00D9FF → #7C3AED`（电青→电紫），PowerPoint/Keynote 下 hero 大字显示渐变
- **big_stat 字号**：260pt + 辉光叠加——"42ms" 这种数字直接发光
- **场景**：AI 发布会、基础设施产品、赛博朋克叙事、黑客马拉松

### 2.6 tech-minimal —— 科技极简（Vercel/Linear 风）🆕

- **配色**：近黑 `#0A0A0F` 底 + 暖白文字 + 电紫 `#8B5CF6` 单色 accent
- **字体**：Inter + JetBrains Mono
- **hero 字号**：120pt + semibold（不过粗）+ 左对齐
- **装饰**：**点阵背景（不是网格）** + subtle halo + 左下 `V2026 · BUILD XXXX` 等宽版本戳 + 无四角刻度（更克制）
- **卡片**：细描边 `#1F1F28` + 轻量圆角 0.1"——Vercel/Linear 文档感
- **场景**：SaaS 产品主页、DevTool 推销、企业级软件 landing page、B 端销售 pitch

---

## 三、11 个页面模板

| template key（type） | 用途 | 别名 |
|----|----|----|
| `hero_cover` | 封面大字页（eyebrow + title + subtitle + footnote） | `cover` |
| `section_divider` | 分章大字页（编号 + 章节标题 + 副标） | `section` |
| `big_stat` | 单数字大字页（Apple "2B" 招牌页） | `stat`, `big_number` |
| `kpi_triple` | 3 宫格 KPI 卡（数字 auto-fit 避免 `99.97%` 溢出） | `kpi`, `kpi_card` |
| `quote_card` | 引用金句卡（大引号 + 引文 + 作者） | `quote` |
| `content_list` | 编号/要点列表 | `list` |
| `compare_columns` | 左右对比（before/after, 方案 A/B） | `compare`, `vs`, `before_after` |
| `product_shot` | 产品摄影页（大图 + 侧栏叙事） | `product`, `image`, `gallery` |
| `timeline` | 时间线（横向多节点） | `story` |
| `call_to_action` | 封底行动号召（大字 + CTA + 联系方式） | `cta`, `end`, `thanks`, `contact` |
| `code_block` 🆕 | 代码块展示页（等宽字体 + 行号 + macOS 圆点 + filename tab + 关键词上色） | `code` |

所有模板自动：
- 按 `StylePack` 的 tokens 绘图 — 换 pack 整套风格变
- **自动 fit 大字号** — hero/section/big_stat/kpi/cta 的大字按宽度约束自动缩放，避免 CJK 长文本溢出换行
- 按 `decoration` 切换布局 — 居中/左对齐/accent bar/装饰线 都由 pack 控制
- 科技风 pack 下，`hero_cover` / `section_divider` / `big_stat` 会自动叠加 glow halo + dev badge + accent gradient（Keynote/PowerPoint 渲染端）
- 支持 6 个 v3 pack + 3 个 v2.x legacy pack 全兼容

---

## 四、JSON deck 规约

```json
{
  "year": "2026",
  "slides": [
    { "type": "hero_cover",
      "eyebrow": "INTRODUCING",
      "title": "M4 Ultra.",
      "subtitle": "地球上最强的芯片。",
      "footnote": "Apple · Cupertino · 2026" },

    { "type": "section_divider",
      "number": "01",
      "title": "Performance",
      "subtitle": "性能" },

    { "type": "big_stat",
      "caption": "CPU PERFORMANCE",
      "value": "2x",
      "unit": "比 M3 Ultra 快",
      "footnote": "基于实际应用工作负载",
      "accent": true },

    { "type": "kpi_triple",
      "title": "重要数字",
      "en_sub": "Key Metrics",
      "items": [
        { "value": "192", "label": "GB 统一内存", "caption": "整张内存池共享" },
        { "value": "80B",  "label": "晶体管",      "caption": "3nm 工艺" },
        { "value": "4TB/s","label": "内存带宽",    "caption": "AI 推理飞起" }
      ] },

    { "type": "quote_card",
      "quote": "One more thing…",
      "author": "Tim Cook",
      "role": "Apple CEO" },

    { "type": "content_list",
      "title": "我们做了什么",
      "en_sub": "What We Did",
      "numbered": true,
      "items": [
        { "label": "重构设计系统", "desc": "把审美分解成 tokens" },
        { "label": "10 个语义模板", "desc": "hero / section / stat / ..." }
      ] },

    { "type": "compare_columns",
      "title": "升级对比",
      "en_sub": "Before vs After",
      "emphasize": "right",
      "left":  { "label": "BEFORE", "title": "色卡游戏", "items": ["..."] },
      "right": { "label": "AFTER",  "title": "审美方案", "items": ["..."] } },

    { "type": "product_shot",
      "title": "产品页",
      "kicker": "NEW",
      "subtitle": "Apple.com 风的大图 + 侧栏叙事",
      "bullets": ["图占大块面积", "文字简洁克制"],
      "image": "/tmp/shot.png",
      "layout": "right" },

    { "type": "timeline",
      "title": "产品演进",
      "en_sub": "Timeline",
      "events": [
        { "time": "2024", "label": "v1.0", "desc": "乔布斯暗蓝" },
        { "time": "2026", "label": "v3.0", "desc": "tokens + 4 pack" }
      ] },

    { "type": "code_block",
      "title": "Quickstart",
      "en_sub": "5 LINES OF CODE",
      "filename": "app.py",
      "language": "python",
      "code": "from synapse import Client\n\nclient = Client(api_key=\"sk-...\")\nresp = client.chat(model=\"synapse-ultra\", messages=[{\"role\": \"user\", \"content\": \"Hi\"}])\nprint(resp.content)",
      "highlight_lines": [4],
      "caption": "pip install synapse-ai · 官方 Python SDK" },

    { "type": "call_to_action",
      "title": "Thank You.",
      "subtitle": "一起做有设计感的幻灯片",
      "cta": "hello@huo15.com",
      "footnote": "火一五 · openclaw-ppt v3.1" }
  ]
}
```

### code_block 字段

- `filename`：文件名标签（如 `app.py`）
- `language`：语言提示，仅用于 UI 显示（`python` / `shell` / `ts` / `go` / ...）
- `code`：原始代码字符串（`\n` 分行，保留缩进，自动用不换行空格还原）
- `highlight_lines`：要高亮的行号数组（1-based），会在该行涂一层 accent_soft
- `caption`：代码块下方小字说明

---

## 五、命令行

```bash
# 列出所有 pack
python3 scripts/create-pptx.py --list-packs

# 列出所有 template
python3 scripts/create-pptx.py --list-templates

# 1. 按 JSON 生成完整 deck（推荐）
python3 scripts/create-pptx.py \
  --pack apple-keynote \
  --spec ./deck.json \
  --output /tmp/deck.pptx

# 2. 快速试样封面
python3 scripts/create-pptx.py \
  --pack 博主风 \
  --cover "关于做幻灯片这件小事|写给刚入行的小伙伴" \
  --year 2026 \
  --output /tmp/cover.pptx

# 3. 老的 --style 兼容（等价于 --pack）
python3 scripts/create-pptx.py --style jobs-dark --spec deck.json -o out.pptx
```

公司名解析顺序：`--company` > `~/.huo15/company-info.json` > `青岛火一五信息科技有限公司`（默认）。

---

## 六、示例 decks

`examples/decks/` 提供 6 份对应 6 套 pack 的完整样例：

| 文件 | pack | 讲什么 |
|----|----|----|
| `apple-keynote-launch.json` | `apple-keynote` | Apple "M4 Ultra" 发布会风 6 页 |
| `apple-light-product.json`  | `apple-light`   | OpenClaw Enhance 产品介绍 5 页 |
| `xhs-creator-vlog.json`     | `xiaohongshu-creator` | 博主笔记「关于做幻灯片这件小事」5 页 |
| `xhs-vintage-travel.json`   | `xiaohongshu-vintage` | 青岛老城旅行手记 6 页 |
| `tech-neon-ai-launch.json` 🆕 | `tech-neon` | AI 模型发布会 "Synapse AI" 10 页（含 code_block） |
| `tech-minimal-saas.json` 🆕 | `tech-minimal` | Vercel 风 SaaS 产品 pitch 7 页（含 shell 部署 code_block） |

对应的渲染预览放在 `examples/previews/*.png`（共 39 张）。科技风 deck 的任意单张都可以直接导出当品牌海报或 LinkedIn/小红书头图使用。

---

## 七、触发词

- 做 PPT / 生成 PPT / 制作 PPT / 写 PPT
- Apple 发布会 / 发布会风 / 苹果风格 / 官网风
- 小红书博主 / 博主风 PPT / 生活博主 / 奶油风
- 复古胶片 / 胶片风 / 复古 PPT / 文艺风
- **科技风 / 霓虹 / 赛博 / 赛博朋克 / cyberpunk / AI 发布会**
- **极简科技 / Vercel / Linear / SaaS / DevTool pitch / 品牌海报**
- 封面 / 分章页 / 大字页 / KPI / 对比页 / 时间线 / **代码块** / 封底
- 第 X 页 / 继续 / 加一页

---

## 八、选 pack 指南

| 想要的效果 | 选 |
|----|----|
| 发布会大字 / 新品宣发 / 投融资路演 | `apple-keynote` |
| 产品介绍页 / 官网风 / 功能说明 | `apple-light` |
| 博主笔记 / 种草分享 / 温度叙事 | `xiaohongshu-creator` |
| 旅行手记 / 文艺向 / 生活美学 | `xiaohongshu-vintage` |
| **AI/大模型发布会 · 赛博科技海报 · 黑客马拉松 · 技术 roadshow** | **`tech-neon`** |
| **SaaS 主页 · DevTool pitch · B 端企业软件 landing · Vercel/Linear 质感** | **`tech-minimal`** |
| 稳妥正式汇报（兼容 v1.x） | `jobs-dark` |
| 小红书品牌红 Feed 帖（兼容 v2.x） | `xiaohongshu` / `xiaohongshu-portrait` |

**科技风两兄弟的区别**：

- `tech-neon` = **品牌海报级**装饰全开（渐变背景 + 网格 + 四角刻度 + glow halo + dev badge + 等宽 metadata），电青/电紫双 accent，适合**对外宣发**
- `tech-minimal` = **产品官网级**克制装饰（点阵 + 微光 + 左下版本戳），单色紫 accent，适合**对内汇报/产品主页**

---

## 九、技术细节

- **CJK 防溢出**：`pptx_toolkit.fit_text` 自动测宽 + 字号自适应
- **玻璃风**：七彩光球 + magnitude 卡片，需 `--pack liquid-glass`
- **水墨/国风**：朱砂方印 / 万字纹边框 / 飞白笔触，自动注入
- **科技风**：渐变背景 + 网格 + glow halo + 四角刻度
- **页码**：自动注入，无需写在 deck JSON
- **footer 控制**：`show_footer=False` 关闭（apple-keynote 默认关）

## 9.1 Design tokens 层次

```
StylePack
├── Canvas       画布尺寸（默认 13.33×7.5" 16:9）
├── Palette      3 级背景 + 4 级文字 + accent + accent_soft + border/divider
├── Typography   display/body/mono 三字体 stack + 6 级字号阶梯 + 字重 + 字距 + 行高
├── Spacing      8pt grid — gutter/stack_sm/md/lg/xl + margin_x/margin_x_hero
├── Elevation    card_radius + stroke + 假阴影（python-pptx 无真阴影）
└── Decoration   cover 对齐、accent bar、tag_style、stat_hero_size、image_treatment
                 ▼ v3.1 新增六件套科技装饰字段：
                 ├── gradient_bg: (from, to, angle)   对角线性渐变铺满底板
                 ├── accent_gradient: (from, to)      大字文字渐变（PowerPoint/Keynote 端）
                 ├── grid_overlay / grid_*            细线网格层（色/间距/粗细可调）
                 ├── dot_grid / dot_*                 点阵背景层（替代 grid）
                 ├── glow_accent / glow_strength      accent 大字辉光 halo
                 ├── corner_marks / corner_*          四角 L 型取景框刻度
                 ├── dev_badge / dev_badge_template   左下等宽版本戳（{year}/{date}/{build}）
                 ├── mono_font / mono_fallbacks       JetBrains Mono / Menlo / Monaco stack
                 └── scanline / scanline_color        水平扫描线（CRT 怀旧）
```

### 9.2 字距（tracking/letter-spacing）

python-pptx 官方 API 不支持字距。v3.0 在 `templates/helpers.py::_set_run_spacing` 里用 OOXML XML 注入 `<a:rPr spc="N">`，单位是 1/100 pt。hero 大字用 -3% em（收紧），衬线字用 +2% em（展开）。

### 9.3 Auto-fit 大字号

hero/section/big_stat/cta 的文本在 `fit_font_size(text, width, base_size)` 里自动缩放，防止 CJK 长文本换行撞副标题。宽度估算按 CJK 1.1em / 大写 0.75em / 小写 0.62em / 标点 0.38em，留 12% 安全余量。

### 9.4 假阴影

`xhs-creator` 开启 `use_fake_shadow=True`，在卡片下方偏移 0.06" 画一个比卡片色深的色块模拟阴影。python-pptx 没有真阴影 API。

### 9.5 与 v2.x 兼容

- `--style` 参数保留，等价于 `--pack`
- legacy pack（`jobs-dark`, `xiaohongshu`, `xiaohongshu-portrait`）仍可用
- JSON 字段 `en_subtitle` 自动映射到 `en_sub`，`sub` 自动映射到 `subtitle`
- slide type `cover/section/list/quote/end` 仍能跑，走 templates 注册表的别名

### 9.6 科技风装饰实现（v3.1）

六件套装饰都通过 OOXML XML 直接注入实现（python-pptx 的 dataclass API 覆盖不全）。核心函数在 `templates/helpers.py`：

| 函数 | 实现 |
|----|----|
| `add_gradient_rect` | 先画矩形，再把 `p:spPr` 下的 `a:solidFill` 替换成 `a:gradFill`（双色 stop + 方向角） |
| `apply_text_gradient` | 给 run 的 `a:rPr` 注入 `a:gradFill`（覆盖 `a:solidFill`），实现渐变文字 |
| `add_glow_halo` | 在大字周围叠 N 层椭圆，每层递减 alpha 值（通过 `a:srgbClr/a:alpha`），模拟发光 |
| `_draw_grid_overlay` | 按 `grid_spacing` 铺横竖细矩形 —— 纯色矩形比 line shape 更稳（LibreOffice 渲染一致） |
| `_draw_dot_grid` | 按 `dot_spacing` 铺 OVAL，中性色 + 小尺寸 —— Vercel/Linear 招牌 |
| `_draw_corner_marks` | 四角各画 2 个 L 型方块，拼出取景框 |
| `add_dev_badge` | 左下固定位置 mono textbox，`{year}/{date}/{build}/{n}` 模板插值 |

**已知限制**：

- `apply_text_gradient` 只在 PowerPoint/Keynote 下可见；LibreOffice/Impress 渲染会回落成 solid（因为 Impress 不支持文字 gradFill）——生成 PDF 预览时 hero 大字看上去是单色 accent，但实际 pptx 打开在 mac Keynote/Windows PowerPoint 下会显示渐变。
- `glow_accent` 的 halo 用多层半透明椭圆模拟，不是 PowerPoint 真正的 glow effect（python-pptx 没暴露 effect API）。视觉效果在 PDF/PNG 预览下接近真 glow。
- 装饰层都是画在背景之上、文本之下（`new_slide` 里按顺序绘制），不会遮挡正文。

---

## 十、版本历史

详细 changelog 见 git log。当前主要里程碑：
- **v3.3.x（最新）** — 设计能力栈集成：反 AI Slop 自检 / WCAG 2.2 AA 对比度审计 / matplotlib 真数据图表 / 集成 design-critique
- **v3.2.x** — 21 套生产级审美方案（玻璃 / 水墨 / 国风 / 梵高 / 莫兰迪 / 孟菲斯 / 包豪斯 / 韦斯安德森等）
- **v3.1.x** — 科技双套（赛博霓虹 + Vercel/Linear 极简）+ 11 个页面模板
- **v3.0.x** — 4 套基础（Apple 发布会 + Apple.com + 小红书博主 + 复古胶片）
- **v2.x** — 小红书品牌风 + 竖版 9:16
- **v1.x** — Jobs 暗蓝默认风格

