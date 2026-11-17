# 图片PPT Skill · 文字材料转可编辑PPT

![GitHub stars](https://img.shields.io/github/stars/helloo1568/image-ppt?style=flat-square)
![License](https://img.shields.io/github/license/helloo1568/image-ppt?style=flat-square)
![Skill](https://img.shields.io/badge/Skill-Agent-111111?style=flat-square)
![Codex](https://img.shields.io/badge/Codex-Recommended-222222?style=flat-square)
![GPT-Image 2.0](https://img.shields.io/badge/GPT--Image%202.0-Recommended-0A7CFF?style=flat-square)

> 🌏 **English version: [README.en.md](./README.en.md)**

一个适配 **Codex / Claude Code 等 Agent 环境**的 PPT 生成技能：把书籍、PDF 或任意文字材料，变成**精美且可编辑的 PPTX**，而不是一张张没法改的图片。

**推荐运行环境：Codex + GPT-Image 2.0**。Codex 负责读懂文档、编排流程、拼装文件；GPT-Image 2.0 负责绘制风格统一、文字精准的 PPT 页面。

## 为什么推荐 Codex + GPT-Image 2.0

| 环节 | 推荐工具 | 为什么 |
|------|---------|--------|
| 文档理解与流程编排 | **Codex** | 有 shell 权限，能读长文档、循环生图、自动合并/还原 PPTX，一次跑完三步流程 |
| 页面绘制 | **GPT-Image 2.0** | 像素级文字渲染、跨页风格一致、商业级排版，能精确还原模板气质 |
| PPTX 拼装 | Codex + python-pptx | 图片页按 16:9 顺序嵌入，输出可下载 .pptx |

> 本技能也兼容其他具备「文档读取 + 图像生成 + 文件输出」能力的 AI 助手（GPT、Claude、Kimi、豆包、WorkBuddy 等），按提示词中的适配说明取用即可。

## 三步工作流

```
源材料（PDF / 书籍 / 文字）
    │
    ▼
① 内容提炼 + 风格设计   读懂材料、提炼大纲，生成 4 套风格预览供选择
    │
    ▼
② 图片版 PPT 生成       按选定风格逐页绘制，合并为可下载 .pptx
    │
    ▼
③ 可编辑 PPTX 还原      逐页拆解为「复杂视觉保真 + 文字可编辑」的 PPTX
```

## 30 秒开始

直接把这段话发给有 shell 权限的 AI Agent（推荐 Codex）：

```text
帮我安装 image-ppt 技能。请把 https://github.com/helloo1568/image-ppt 克隆到本地技能目录，
安装完成后检查 SKILL.md、references/ 是否存在。装好后我说"帮我把这本书做成 PPT"就会触发它。
```

安装后直接对 Agent 说：

```text
帮我把这份 PDF 做成课堂汇报 PPT，先按提示词生成 4 套风格预览，我选一套再继续。
```

也可以试这些请求：

```text
帮我把这本书做成读书分享 PPT，配图用 GPT-Image 2.0 生成。
把这份报告做成组会汇报 PPT，参考我上传的模板风格。
图片PPT：把这份 Markdown 变成 16:9 可编辑 PPTX。
```

## 效果

- 🧠 **读懂材料**：自动提炼作者背景、全书结构、主要观点、典型案例、经典语句与现实意义
- 🎨 **四套风格预览**：生成 4 套不同配色/排版/视觉风格的缩略图，选定后再开工
- 🖼 **逐页绘制**：每页突出一个核心观点，配结构图、时间轴、人物关系图等可视化
- 📦 **可编辑 PPTX**：复杂视觉保留为高清图片，主要文字还原为 PPT 原生文本框
- 🔁 **逐页迭代**：每次还原 1-3 页，先确认一页质量再批量推进

## 适合 / 不适合

**✅ 合适**：大学课堂小组汇报 / 读书分享 / 组会文献汇报 / 项目汇报 / 比赛路演 / 课程作业

**❌ 不合适**：需要多人实时协作编辑的文档（建议直接用 Office 在线协作）、大段表格数据型汇报（图片版信息密度有限）

## 常见使用场景

| 任务 | 推荐方式 |
|------|---------|
| 一本书变成读书分享 PPT | 三步全流程，重点提炼核心观点与金句 |
| 论文 / 文献做组会汇报 | 用 Prompt 1 提炼结构，配流程图、关系图 |
| 课程作业 / 课堂展示 | 参考模板图 + 四套风格预览，快速定稿 |
| 比赛路演 / 项目汇报 | 突出结论与亮点页，控制页数与节奏 |
| 已有图片版 PPT 要改文字 | 直接用 Prompt 3 逐页还原为可编辑 PPTX |

## 平台支持

| 平台 | 状态 | 说明 |
|------|------|------|
| **Codex** | 推荐 | 完整跑通三步流程：读文档、GPT-Image 2.0 生图、python-pptx 拼装/还原 |
| Claude Code | 可用 | 文本/编排能力强；生图需接入外部图像工具 |
| GPT / ChatGPT | 可用 | 原生图像能力，直接粘贴三段提示词即可 |
| WorkBuddy | 可用 | 支持文档读取与本地工具链，按适配说明执行 |
| Kimi / 豆包 / 通义 | 部分可用 | 需自行确认其图像生成与文件输出能力 |

## 安装

### 方式一：一行命令安装（推荐）

```bash
npx skills add https://github.com/helloo1568/image-ppt --skill image-ppt
```

### 方式二：发给 AI 自动安装

> 帮我安装 `image-ppt` 这个 skill。按下面步骤做：
>
> 1. 确保本地技能目录存在（`~/.claude/skills/` 或 `~/.codex/skills/`，不存在就创建）
> 2. 执行 `git clone https://github.com/helloo1568/image-ppt.git <技能目录>/image-ppt`
> 3. 验证 `SKILL.md`、`references/prompts.md` 存在
> 4. 告诉我安装好了，之后我说"做一份 PPT"之类的话就会触发

### 方式三：手动克隆

```bash
git clone https://github.com/helloo1568/image-ppt.git ~/.claude/skills/image-ppt
# 或放入 Codex 技能目录
git clone https://github.com/helloo1568/image-ppt.git ~/.codex/skills/image-ppt
```

### 触发方式

装好后 Agent 会在对话里自动发现并调用。触发关键词：

- "帮我把这本书做成 PPT"
- "把这份 PDF 做成课堂汇报 PPT"
- "图片PPT 生成读书分享演示文稿"
- "基于这份材料做一份可编辑 PPTX"
- "image-ppt"

## 使用流程

Skill 是结构化工作流，Agent 会逐步引导：

1. **读懂材料** — 读取 PDF/文档，提炼作者背景、结构、观点、案例、金句与现实意义
2. **风格设计** — 询问是否有参考模板图，用 GPT-Image 2.0 生成 4 套风格预览
3. **用户选择** — 展示预览，等待选定一套风格
4. **逐页生成** — 按选定风格逐页绘制（封面 → 目录 → 内容页 → 总结 → 致谢）
5. **合并 PPTX** — 图片页按 16:9 顺序嵌入，输出可下载 .pptx
6. **可编辑还原** — 逐页拆解（每次 1-3 页）：复杂视觉转图片、主要文字转原生文本框
7. **对照迭代** — 渲染预览与原图对照，明显差距继续迭代
8. **交付说明** — 说明哪些是可编辑文本、哪些保留为图片、字体替代情况

详细说明见 [`SKILL.md`](./SKILL.md)，三段核心提示词见 [`references/prompts.md`](./references/prompts.md)。

## 目录结构

```
image-ppt/
├── SKILL.md              ← Skill 主文件：三步工作流与适配说明
├── README.md             ← 本文件（中文）
├── README.en.md          ← English version
├── manifest.yaml         ← 技能清单（版本、触发词、安全声明）
└── references/
    └── prompts.md        ← 三段核心提示词（可直接复制使用）
```

## 核心提示词

三段提示词直接可用，详见 [`references/prompts.md`](./references/prompts.md)：

- **Prompt 1** — 内容提炼与风格设计：读懂材料、生成 4 套风格预览
- **Prompt 2** — 图片版 PPT 生成：按选定风格逐页绘制并合并
- **Prompt 3** — 可编辑 PPTX 还原：「复杂视觉保真 + 主要文字可编辑」混合策略

## FAQ

**必须用 Codex 吗？**
不是。Codex 是推荐环境（文档读取 + GPT-Image 2.0 + python-pptx 一条龙），但三段提示词在任何能读文档、能生图的 AI 里都能用。

**必须用 GPT-Image 2.0 吗？**
不是。GPT-Image 2.0 在文字渲染和跨页一致性上表现最好；其他图像模型也能生成，把提示词里的模型名换成你用的即可。

**生成的 PPT 能直接编辑吗？**
第 2 步产出的是图片版 PPT（每页一张图，不可编辑）；第 3 步会逐页还原成可编辑 PPTX，主要文字用 PPT 原生文本框重建。

**一次能还原多少页？**
建议每次 1-3 页。拆得太多，元素拆分效果会明显下降。

**这个技能会联网或上传数据吗？**
不会。纯提示词方法论，所有执行都在你的 AI 环境中完成。

## Roadmap

- 补充更多真实案例与效果图
- 增加书籍结构图 / 时间轴 / 人物关系图的固定版式
- 提供可直接运行的 python-pptx 合并脚本
- 整理上架 ClawHub / 各平台 Skill 商店

## License

[MIT](./LICENSE) © 2026 风清云影（helloo1568）
