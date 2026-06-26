---
name: html-slides
description: 为 OpenClaw 打造的网页幻灯片创建技能。将用户需求转化为精美的 HTML 演示文稿，支持从零创建和 PPT 转换两种模式。触发词：做幻灯片 / 做 PPT / 做演示 / 做 slides / 做一个网页版自我介绍 / 帮我做个路演 PPT。
---

# 🎨 HTML Slides — 网页幻灯片技能

在 OpenClaw 中创建零依赖、动画丰富的 HTML 幻灯片。

## 核心原则

1. **零依赖** — 单个 HTML 文件，CSS/JS 内联，无需 npm/框架
2. **先展示，再确认** — 生成视觉预览而非抽象选择，用户看到效果后再定
3. **独特设计** — 拒绝千篇一律的"AI 风格"，每份演示都应有定制感
4. **严格适配视口** — 每张幻灯片必须恰好填满 100vh，禁止溢出

## 工作流程（尚书省派发·六部执行）

```
用户旨意 → 皇上（你）→ 中书省（规划内容）→ 尚书省（派发）→ 兵部/工部（生成）
```

**中书省职责（内容规划）：**
- 收集用户内容（主题、页数、图片素材）
- 确定视觉风格方向（通过视觉预览选择）
- 输出结构化大纲

**兵部/工部职责（代码生成）：**
- 读取 supporting files
- 生成完整 HTML 幻灯片
- 在浏览器中打开预览

---

## 内容密度限制（每页上限）

| 类型 | 最大内容量 |
|------|-----------|
| 标题页 | 1 标题 + 1 副标题 + 可选标语 |
| 内容页 | 1 标题 + 4-6 条要点 或 1 标题 + 2 段文字 |
| 特性网格 | 1 标题 + 最多 6 张卡片（2×3 或 3×2） |
| 代码页 | 1 标题 + 8-10 行代码 |
| 引言页 | 1 条引言（最多 3 行）+ 出处 |
| 图片页 | 1 标题 + 1 张图片（最大 60vh） |

**内容超限？拆成多页，绝不堆砌。**

---

## 模式判断（Phase 0）

确认用户需求：

- **模式 A：从零创建** → 进入 Phase 1
- **模式 B：PPT 转换** → 进入 Phase 4
- **模式 C：增强现有 HTML** → 读取后增强，遵循修改规则

---

## Phase 1：内容收集（从零创建）

**一次性问完所有问题：**

1. **用途** — 路演 / 教学教程 / 大会演讲 / 内部汇报
2. **页数** — 短（5-10页）/ 中（10-20页）/ 长（20+页）
3. **内容状态** — 内容齐全 / 粗略大纲 / 只有主题
4. **内联编辑** — 是否需要生成后直接在浏览器编辑文字？（推荐选"是"）

如果用户已有内容，让其直接提供。

**图片评估（如有图片）：**
1. 列出所有图片文件
2. 逐个查看图片，判断是否可用、代表什么概念、主体颜色
3. 将图片融入大纲设计（而非"先规划再配图"）

---

## Phase 2：视觉风格选择

**核心原则：先展示，不抽象。** 大多数人选风格时说不出具体偏好，让他们看图选择。

### 风格选择路径

- **"给我看几个选项"**（推荐）→ 根据情绪词生成 3 个预览
- **"我知道我要什么"** → 直接从预设列表选

### 情绪词选择（最多选 2 个）

| 情绪 | 感觉 |
|------|------|
| 专业可信 | 专业、值得信赖 |
| 兴奋有活力 | 创新、大胆 |
| 冷静专注 | 清晰、有思考感 |
| 受启发 | 情感、有记忆点 |

### 三种风格预览

基于情绪生成 3 个单页 HTML 预览，展示字体、颜色、动画和整体美学。

**情绪 → 预设映射：**

| 情绪 | 推荐预设 |
|------|---------|
| 专业可信 | Bold Signal / Electric Studio / Dark Botanical |
| 兴奋有活力 | Creative Voltage / Neon Cyber / Split Pastel |
| 冷静专注 | Notebook Tabs / Paper & Ink / Swiss Modern |
| 受启发 | Dark Botanical / Vintage Editorial / Pastel Geometry |

预览保存在 `.slide-previews/`（style-a.html / style-b.html / style-c.html），每个约 50-100 行代码。

### 用户选择

- 选 A / 选 B / 选 C / 混搭（指定哪些元素）

---

## Phase 3：生成演示文稿

基于 Phase 1 内容 + Phase 2 风格生成完整 HTML。

**生成前必须读取以下文件（由工部/兵部执行）：**

- [html-template.md](html-template.md) — HTML 架构和 JS 特性
- [viewport-base.css](viewport-base.css) — 强制 CSS（每个演示必须包含）
- [animation-patterns.md](animation-patterns.md) — 动画参考
- [STYLE_PRESETS.md](STYLE_PRESETS.md) — 所选风格的详细规格

**关键要求：**
- 单个自包含 HTML 文件，CSS/JS 内联
- 必须完整包含 viewport-base.css 的全部内容
- 使用 Fontshare 或 Google Fonts 字体，禁止系统字体
- 每个区块添加清晰注释 `/* === 区块名称 === */`

---

## Phase 4：PPT 转换

1. **提取内容** — 运行 `python scripts/extract-pptx.py <input.pptx> <output_dir>`
2. **用户确认** — 展示提取的幻灯片标题、内容摘要、图片数量
3. **风格选择** — 进入 Phase 2
4. **生成 HTML** — 转换为选定风格，保留所有文字、图片（从 assets/）、顺序和备注

---

## Phase 5：交付

1. **打开预览** — 使用 `start [filename].html` 在浏览器打开
2. **告知用户：**
   - 文件位置、风格名称、页数
   - 操作方式：方向键 / 空格键 / 滚动 / 滑动 / 点击导航点
   - 如何自定义：修改 `:root` CSS 变量改颜色，改字体链接换字体，`.reveal` 类改动画
   - 如启用了内联编辑：悬停左上角或按 `E` 进入编辑模式

---

## Phase 6：分享与导出（可选）

交付后询问：_"需要分享这个演示吗？可以部署到在线链接，或者导出为 PDF。"_

### 6A：部署到在线链接（Vercel）

**注意：Windows 环境需要 WSL（Linux 子系统）或手动安装 Vercel CLI。**

```powershell
# 检查 Vercel CLI
npx vercel --version

# 部署（需要先登录）
npx vercel deploy <path-to-html> --yes --prod
```

**如未登录：**
1. 访问 https://vercel.com/signup 注册账号
2. 运行 `vercel login` 登录
3. 重新运行部署命令

### 6B：导出为 PDF

```powershell
# 需要 Node.js + Playwright
bash scripts/export-pdf.sh <path-to-html> [output.pdf]
```

Windows 下可直接用 Node.js 运行 export-pdf 脚本（需要先 `npm install playwright`）。

---

## 适配 OpenClaw 的关键变化

### 1. Subagent 协作模式

| 阶段 | 执行者 |
|------|--------|
| 内容收集 + 风格确认 | 主 agent（中书省） |
| HTML 生成 | `bingbu` 或 `gongbu` subagent（兵部/工部） |
| 部署/导出 | `gongbu` subagent（工部） |

### 2. 文件位置

生成的文件保存在：
```
C:\Users\HUAWEI\.openclaw\workspace\slides\
├── presentation-YYYYMMDD-HHMMSS.html   # 生成的幻灯片
└── assets/                               # 图片素材（如果有）
```

### 3. 分享方式

- **分享链接**：部署到 Vercel 后获取 URL
- **导出 PDF**：使用 scripts/export-pdf.sh
- **发送给 ZYQ**：直接生成文件后告知路径

---

## Supporting Files

| 文件 | 用途 | 何时读取 |
|------|------|---------|
| [STYLE_PRESETS.md](STYLE_PRESETS.md) | 12 种视觉预设（颜色、字体、特征元素） | Phase 2（风格选择） |
| [viewport-base.css](viewport-base.css) | 强制响应式 CSS — 每个演示必须包含 | Phase 3（生成） |
| [html-template.md](html-template.md) | HTML 结构、JS 特性、代码质量标准 | Phase 3（生成） |
| [animation-patterns.md](animation-patterns.md) | CSS/JS 动画片段和效果-情绪对照表 | Phase 3（生成） |
| [scripts/extract-pptx.py](scripts/extract-pptx.py) | PPT 内容提取（Python） | Phase 4（转换） |
| [scripts/export-pdf.ps1](scripts/export-pdf.ps1) | 导出 PDF（Windows PowerShell） | Phase 6（分享） |
| [scripts/deploy.ps1](scripts/deploy.ps1) | 部署到 Vercel（Windows PowerShell） | Phase 6（分享） |
