# Web Slide — 网页端 Slide（PPT）生成 Skill

通过对话驱动，自动生成可在浏览器中直接打开的交互式 HTML Slide（PPT）。无需安装任何软件，生成即可演示。

## 效果预览

**渐变深色主题 · 标题页** — 全屏沉浸式开场

![标题页](https://raw.githubusercontent.com/balancegsr/office/main/web-slide/assets/headline.png)

**数据图表 · 动态交互** — Chart.js 翻页时自动播放入场动画，支持 hover 查看数据

![动态交互图表](https://raw.githubusercontent.com/balancegsr/office/main/web-slide/assets/Animation_interaction_chart.png)

**卡片布局 · 多项并列** — 自动适配列数，玻璃质感面板

![卡片归类](https://raw.githubusercontent.com/balancegsr/office/main/web-slide/assets/Card_Classification.png)

**大数字布局 · 数据冲击** — 核心数据一眼抓住注意力

![重点内容](https://raw.githubusercontent.com/balancegsr/office/main/web-slide/assets/major_content.png)

**主题可视化选择器** — 浏览器内预览所有主题，点选即用

![主题选择器](https://raw.githubusercontent.com/balancegsr/office/main/web-slide/assets/Slide_style_selector.png)

## 核心能力

- **对话驱动**：提供素材或描述需求，Agent 自动完成内容结构化、布局选择、风格匹配和 HTML 生成
- **14 种布局**：标题页、内容页、双栏、卡片、大数字、引用、图片、图表、时间线、对比、金字塔等，根据内容自动选择
- **16 套主题**：Pure / Warm / Cyber / Data / Azure / Glass / Frost / Gradient 八种风格 × 浅色/深色，支持浏览器内可视化预览后选择
- **数据可视化**：SVG 图表、Chart.js、ECharts 三种方案，Agent 根据数据特征自动选择，翻页时动画精准触发
- **入场动画**：CSS 基础动画 + 可选 GSAP 高级动画（数字滚动、打字机、路径动画等）
- **完整交互**：键盘（← → Space / Home / End）、鼠标滚轮、触控板、触控滑动翻页，右侧圆点导航（可点击跳转，超过 12 页自动切换为数字显示），右上角全屏按钮（F 键 / ESC 退出）
- **单文件交付**：生成的 HTML 自包含所有样式和脚本，浏览器直接打开即可演示

## 使用方式

安装后在对话中提及 Slide（PPT）/ 演示文稿相关需求，Skill 自动触发。

**快速开始**

```
帮我做一个关于 AI 发展趋势的 Slide（PPT）
```

Agent 会引导你补充内容、确定结构和风格，然后生成完整的 HTML Slide。

**提供素材**

```
我有一份产品介绍文档，帮我做成 Slide（PPT）
（粘贴或附上文档内容）
```

**指定风格**

```
用深色极简风格，做一个技术分享的 Slide（PPT）
```

也支持提供参考物让 Agent 提取风格：.pptx 文件、网页链接、图片截图、PDF 文件。

## 预设主题

| 主题 | 标识 | 调性 | 适用场景 |
|------|------|------|---------|
| Pure Light | `pure-light` | 极致简约、纯净白底 | 产品发布、科技展示、设计提案 |
| Pure Dark | `pure-dark` | 深邃黑底、银白文字 | 产品发布会、科技演讲、高端展示 |
| Warm Light | `warm-light` | 暖调学院、奶油白底 | AI/科研汇报、品牌故事、温暖叙事 |
| Warm Dark | `warm-dark` | 深邃暖调、琥珀强调 | AI 研究分享、深度演讲、沉浸叙事 |
| Cyber Light | `cyber-light` | 科技蓝紫、现代感 | AI/SaaS 产品介绍、技术方案、创业路演 |
| Cyber Dark | `cyber-dark` | 赛博霓虹、未来感 | AI 产品发布、黑客松、极客风格 |
| Data Light | `data-light` | 数据学院、青绿强调 | 数据分析报告、研究成果、趋势分析 |
| Data Dark | `data-dark` | 数据仪表盘、夜间 | 仪表盘展示、实时数据、趋势演讲 |
| Azure Light | `azure-light` | 蓝调科技、专业 | 企业汇报、科技产品发布、ToB 方案 |
| Azure Dark | `azure-dark` | 蓝调深邃、沉稳 | 企业年会、产品发布会、夜间演示 |
| Glass Light | `glass-light` | 液态玻璃、通透光感 | 科技前沿、产品发布、创意展示 |
| Glass Dark | `glass-dark` | 液态玻璃暗色、深邃通透 | 科技发布会、沉浸式展示、夜间演示 |
| Frost Light | `frost-light` | 磨砂玻璃、清冷克制 | SaaS 产品、数据平台、专业工具 |
| Frost Dark | `frost-dark` | 磨砂玻璃暗色、沉稳专业 | 控制面板、技术架构、暗色办公 |
| Gradient Light | `gradient-light` | 渐变潮流、活力冲击 | 创意提案、营销发布、年轻品牌 |
| Gradient Dark | `gradient-dark` | 渐变暗色、霓虹未来 | 音乐/游戏/潮牌发布、视觉冲击型演讲 |

## 安装

将 `web-slide/` 文件夹复制到 Agent 软件的 Skills 目录下即可。不同软件的约定路径可能不同，常见示例：

| Agent 软件 | Skills 目录 |
|-----------|------------|
| OpenClaw | `.claw/skills/` |
| Claude Code | `.claude/skills/` |
| Antigravity | `.antigravity/skills/` |
| CodeBuddy | `.codebuddy/skills/` |

> 以上为常见路径，具体请以各软件官方文档为准。部分 Agent 软件也支持在设置页面直接导入。

## 分享与演示

生成的 HTML 文件可以直接发送给任何人，对方用浏览器打开即可查看完整的交互式 Slide（PPT）。本地演示时，按 F 或点击右上角按钮即可进入全屏。

## 扩展

**新增主题**：在 `references/themes/` 下创建 CSS 文件（参考现有主题的变量结构），然后在 `references/guidelines.md` 的主题注册表中添加一行描述。无需修改其他文件。

**新增布局**：在 `references/layouts/` 下创建 HTML 模板，然后在 `references/guidelines.md` 的布局注册表中添加一行描述。

## 注意事项

- 生成的 HTML 无需安装任何软件即可打开；如果 Slide 中包含数据图表或高级动画，演示时需要联网加载 CDN 资源
- 本 Skill 生成 HTML 格式，不提供 .pptx 导出。如需 .pptx 格式请使用专门的 pptx 生成工具

## 版本

- **v1.0.0** — 初始发布
  - 14 种布局 + 16 套主题（8 风格 × 浅色/深色，含液态玻璃/磨砂玻璃/渐变）
  - 对话引导式创建流程
  - SVG / Chart.js / ECharts 数据可视化，翻页时动画自动触发
  - CSS + GSAP 动画系统
  - 主题可视化选择（浏览器预览 + 对话选择双路径）
  - 完整演示交互（多方式翻页 / 全屏 / 圆点导航）
  - 跨 Agent 软件兼容
