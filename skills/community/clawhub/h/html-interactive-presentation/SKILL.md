---
name: html-interactive-presentation
description: 把一篇 Markdown 文章，变成点击驱动的 16:9 交互式理解界面 HTML，含 MiniMax CLI 多模态配图 + 口播配音。流程：原文 → 口播稿 + outline → Checkpoint 5 件事 → Vite+React+TS 网页 → MiniMax 合成图片 → MiniMax 合成音频 → build 产出。
---

# HTML Interactive Presentation

把一篇 Markdown 文章（技术博客、产品文档、知识笔记），变成**可交互、可播放的 16:9 理解界面**。产出一个 Vite + React + TS 项目，带：

- 分章分步的点击导航
- 多模态配图（MiniMax CLI 生成）
- 逐段口播音频（MiniMax TTS 合成）
- 自动播放、手动翻页、带声翻页三种模式
- 可选 Architecture Blueprint / Paper Press / Monochrome 等多种主题

## 适用场景

- 技术文章想做成可播放的交互文档
- 学习笔记想加点"视频感"
- 产品文档想让人愿意读完
- 跟原有的静态 HTML 版本做效果对比

## 兼容 Agent

| Agent | 状态 |
|-------|------|
| Claude Code | ✅ |
| OpenClaw | ✅ |
| Hermes | ✅ |
| Cursor | ✅ |
| Codex CLI | ✅ |
| 任何支持 SKILL.md 的 Agent | ✅ |

---

## 工作流总览

```
Phase 1   内容准备
   1.1  识别用户输入（原文 markdown / 已有 script）
   1.2  一次产出 script.md + outline.md
   ▼
[Checkpoint Plan]     5 件事一次对齐：稿子 / outline / 主题 / 素材 / 开发模式
   ▼
Phase 2   网页开发（16:9 点击驱动）
   2.1  从模板脚手架（可选主题）
   2.2  第 1 章 = 主线程 + 完整版（强制验收）
   2.3  第 2~N 章（逐章 / 顺序 / 并行）
   ▼
Phase 3   多模态生产
   3.1  用 mmx image 生成配图
   3.2  用 npm run extract-narrations + mmx speech synthesize 合成口播
   ▼
Phase 4   build 产出
   4.1  vite build
   4.2  输出 dist/ 目录，可部署为静态页面
```

工作目录约定：

```
my-project/
├── article.md            # 用户给的原始文章
├── script.md             # 口播稿（B 站风格）
├── outline.md            # 开发计划
└── presentation/         # Vite + React + TS 项目（脚手架产出）
    ├── src/
    │   ├── chapters/     # 每章独立目录
    │   ├── components/   # 舞台 / 进度条 / 模式切换
    │   ├── hooks/        # useStepper / useAutoMode / useAudioPlayer
    │   ├── registry/     # chapters.ts 注册
    │   └── styles/       # 主题 tokens
    ├── public/
    │   ├── img/          # MiniMax 生成的配图
    │   └── audio/        # MiniMax 合成的口播
    └── dist/             # 最终静态 HTML 产出
```

---

## Phase 1 —— 内容准备

### 1.1 识别用户输入

| 用户给的东西 | 该做的 |
|---|---|
| 原始 markdown 文章 | 一次产出 `script.md` + `outline.md`（1.2） |
| 已有口播稿 / 视频脚本 | 落盘为 `script.md`，一次产出 `outline.md` |
| 已有《The Unreasonable Effectiveness of HTML》风格文章 | 参考 SCRIPT-STYLE.md 做转写 |

### 1.2 一次产出 script.md + outline.md

**script.md 规则（B 站风口播稿）：**
- 信息保留度 ≥ 60%（字数对比）
- 口语化、短句（≤ 20 字）、第二人称
- 开头 3 秒钩子
- 数字翻译成感受
- 不用首先/其次/最后结构词
- 不用"说白了/本质上/底层逻辑"等 AI 味模板
- 不堆排比
- 末尾具体 CTA

**outline.md 结构**：

```markdown
# Video Outline

> **主题**：`blueprint`
> **总时长**：约 X 分
> **章节数**：N 章 / M 步

## 1. <chapter-id> — 标题（S steps · ~Ts）

**信息池**（回 article.md 抽细节）：
- 数字/引用/案例...

**开发计划**：
- step 1 (~Ts) — 屏幕内容描述
- step 2 (~Ts) — ...

口播节选：
> ...
```

**outline 原则**：
- 每章 3~8 步，每章 30~60s
- outline 不写动画（留给章节开发时自由设计）
- 每章首段必须有「信息池」block

---

## Checkpoint Plan —— 5 件事一次对齐

产出 script.md + outline.md 后必须停。一次确认：

1. **稿子**要不要改？
2. **开发计划**章节切分 / step 数合理吗？
3. **选哪个主题？** 内置主题：
   - `blueprint`（蓝图 / 深藏青色 + 青色 / 工程气质）
   - `paper-press`（亮色印刷 / 暖色奶油底 / 杂志风）
   - `monochrome-print`（黑白印刷 / 高对比 / 学术）
   - `terminal-green`（终端绿 / 黑客风 / 技术演示）
   - `midnight-press`（午夜印刷 / 深色 / 奢华）
   - `chalk-garden`（粉笔花园 / 柔和 / 自然）
   - 其它见 theme 清单
4. **素材**用 MiniMax CLI 生成配图，还是用户提供？
5. **开发模式**：A) 逐章确认（推荐）B) 顺序开发 C) 并行开发

---

## Phase 2 —— 网页开发

### 2.1 脚手架

```bash
bash <skill-path>/scripts/scaffold.sh ./presentation --theme=<selected-theme>
```

脚手架产出 Vite + React + TS 项目，含：
- 16:9 固定舞台（1920×1080）
- 全局 step 计数器
- 隐形进度条 + 三种播放模式
- 音频流水线（extract-narrations + synthesize-audio）

### 2.2 章节开发

每章一个独立目录 `src/chapters/<NN>-<chapter-id>/`，包含：
- `<Chapter>.tsx` — React 组件，每个 step 返回一屏内容
- `<Chapter>.css` — 章节样式（CSS 类前缀如 `.co-` / `.wh-`）
- `narrations.ts` — 口播文本数组，长度 = step 数

**视觉原则**：
- 每章至少 1~2 处 CSS / SVG / Canvas 视觉演示
- 列表项逐步揭示（1 项 = 1 step）
- 颜色字体走主题 token，禁硬编码
- 缺素材用 placeholder，不用 fake
- 动画时长 ≤ 口播时长

**代码红线**：
- 不用 setTimeout / setInterval 驱动动画
- 交互元素加 `data-no-advance`
- 每章独立 CSS 前缀，不跨章 import
- narrations.length === 最大 step + 1

### 2.3 更新注册

编辑 `src/registry/chapters.ts`，按顺序注册所有章节。

### 2.4 bump STORAGE_KEY

改完 chapters.ts 后 bump `useStepper.ts` 中的 STORAGE_KEY。

---

## Phase 3 —— 多模态生产

> **没有 MiniMax API 怎么办？** 图片和音频各自有降级路径，见下方"降级方案"。

### 3.1 配图

```bash
cd presentation
mmx image "<描述>" && mv image_001.jpg public/img/<name>.jpg
```

建议配图：
- 冷开场背景（技术蓝图风格）
- 信息密度对比图
- 三优势概念图
- 每章特色配图

### 3.2 口播合成

```bash
cd presentation
npm run extract-narrations    # 扫 narrations.ts → audio-segments.json
bash scripts/synthesize-audio.sh  # mmx speech 逐段合成 mp3
```

输出到 `public/audio/<chapter-id>/<N>.mp3`，自动跳过已存在的文件。

---

## 降级方案（没有 MiniMax API 时）

### 配图降级

| 方案 | 做法 |
|------|------|
| **OpenAI DALL-E** | 用 `curl` 调 OpenAI image API 生成，保存到 `public/img/` |
| **Stable Diffusion** | 本地或 API 调用，输出到 `public/img/` |
| **占位符** | 章节中缺图用 placeholder 卡片（`16:9` 比例 + 文字描述），不 fake |

规则：
- 生成图片控制在 2~4 张关键配图，不要每章都生
- 核心视觉靠 CSS / SVG 动画（字号、网格、边框、虚线），配图只是氛围装饰
- 没有就承认没有，placeholder 比编造好

### 口播降级

| 方案 | 做法 | 接入成本 |
|------|------|----------|
| **OpenAI TTS** | 改 `synthesize-audio.sh` 用 `curl` 调 OpenAI TTS API | 低（替换 mmx 那一行） |
| **Edge TTS** | 用 `edge-tts` CLI（pip install edge-tts） | 低 |
| **Azure TTS** | 改脚本调 Azure Speech API | 中 |
| **ElevenLabs** | 改脚本调 ElevenLabs API | 中 |
| **跳过合成** | 不合成音频，用户只用手动翻页模式浏览 | 零 |

无需改代码 —— 替换 `synthesize-audio.sh` 中调用 `mmx speech synthesize` 那一行即可，文件输出路径不变。

### 不影响的功能

- ✅ 网页浏览（手动翻页 / 带声翻页）
- ✅ CSS / SVG / Canvas 视觉演示
- ✅ 主题切换
- ✅ 自动构建部署

---

## Phase 4 —— 构建产出

```bash
cd presentation
npx vite build
```

输出 `presentation/dist/` 为纯静态页面，可部署到任何静态托管服务。

---

## 三种播放模式

| 模式 | 行为 |
|---|---|
| **手动翻页** 🔇 | 点击 / 空格翻页，无音频 |
| **带声翻页** 🔊 | 每步播放口播，手动翻页 |
| **自动播放** ▶ | 口播自动播 + 播完自动翻页 |

用户点击右下角按钮或按 `M` 键循环切换。

---

## 相关资源

- 脚手架 `scripts/scaffold.sh`
- 音频提取脚本 `scripts/extract-narrations.ts`
- 音频合成脚本 `scripts/synthesize-audio.sh`
- 基于 [web-video-presentation](https://github.com/ConardLi/garden-skills) 技能体系
