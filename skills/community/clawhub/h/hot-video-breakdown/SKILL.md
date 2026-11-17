---
name: hot-video-breakdown
slug: hot-video-breakdown
displayName: 热门视频拆解
version: 1.0.2
summary: 丢一条热门短视频链接，自动解析、本地转写、AI分析，输出标准化胶囊卡片交互 HTML 报告。转写完全本地（faster-whisper），HTML 无外部依赖。
description: 丢一条热门短视频链接，自动下载视频、本地转写（faster-whisper）、AI分析，输出交互式胶囊卡片 HTML 报告。需网络下载视频和 Whisper 模型（首次约 500MB），转写和分析完全本地。分析由调用方 AI 完成，无外部 API 调用。HTML 报告无外部资源依赖（不含 Google Fonts 等第三方请求）。
license: MIT
author: zhouq2039-lang
---

# 热门视频拆解

**适用场景**：各类热门短视频链接的内容拆解与分析。

## 一句话说明

用户丢一条视频链接 → 脚本解析+转写 → **你**（AI）分析字幕 → 脚本生成 HTML 报告 → 交付 HTML 文件给用户。

## 安全与权限提示

> 使用本技能前，请确认你了解以下行为：

### 网络访问

- 脚本从用户指定的视频平台下载视频文件
- 首次运行从 Hugging Face 下载 Whisper `small` 模型（约 500MB）

### 本地文件操作

- 视频临时下载到 `output/` 目录（默认转写后删除，可用 `--keep-video` 保留）
- 逐字稿（`.txt`）、分析 JSON（`_analysis.json`）、HTML 报告写入 `output/`
- 用户提供的 cookies 文件仅用于平台认证，不会被上传

### 数据隐私

- **分析由调用方 AI 完成，字幕不发送到任何外部 LLM API** — 无需 API Key
- 全转录文本可能包含人名、联系方式等个人信息，请勿处理含敏感内容的视频
- 请勿解析/转写受版权保护的内容，除非你拥有相应权利

### 安全建议

- 处理私密视频前，确认输出目录在你的控制之下
- 从不可信来源获取 HTML 报告时，建议先检查文件内容再打开
- 仅处理你明确提供的视频链接，不要将工具暴露给未验证的 URL

### Required Capabilities（所需权限）

| 权限 | 用途 |
|------|------|
| **Shell / 命令执行** | 运行 `parse.py` 脚本进行视频下载、音频转写、HTML 生成 |
| **网络访问（出站）** | 从用户指定的视频平台下载视频文件；首次运行从 Hugging Face 下载 Whisper 模型（约 500MB） |
| **本地文件读写** | 将视频/音频临时写入 `output/`；写入逐字稿 `.txt`、分析 JSON、HTML 报告；读取用户提供的 cookies 文件（可选） |
| **子进程调用** | 调用 yt-dlp 下载视频；调用 ffmpeg 提取音频；调用 faster-whisper 转写 |

> 以上权限均为技能正常运行所必需。调用方应在授权前了解这些行为。

## 架构

```
parse.py（采集层）            AI（分析层）              parse.py --generate-html（交付层）
─────────────               ──────────               ────────────────────────────
解析 → 转写 → stdout JSON → 读字幕 → 分析 JSON → 胶囊卡片交互 HTML
```

脚本只负责解析、转写和 HTML 渲染，**不做任何分析**。分析由调用方 AI 完成——不需要外部 API Key。

## HTML 报告样式

最终 HTML 是一个干净的卡片式交互页面，**不含任何逐字稿/连贯稿**：

- **Hero**：平台徽章 + 视频标题 + 时长/分类/日期
- **一句话总结卡片**：左侧彩色竖线，核心观点 `<em>` 高亮
- **金句卡片区**：大字引用，适合截图分享
- **4 张胶囊卡片**：点击展开详情面板，再点关闭
- **Footer**

## 依赖

```bash
pip install yt-dlp faster-whisper
```

首次运行自动下载 Whisper `small` 模型（约 500MB）。无需 GPU，CPU 可用。

## 工作流（四步）

### 调用约束

- **仅处理用户明确提供的链接** — 不主动扫描或推测视频 URL
- **处理前确认** — 检测到视频信息后，向用户展示来源、标题、时长，等待确认后再继续
- **单次一条链接** — 每次调用处理一条视频链接

### 步骤 1：采集

```bash
python scripts/parse.py "视频链接"
```

stdout 输出单行 JSON：

```json
{
  "status": "transcribed",
  "title": "视频标题",
  "platform": "红薯",
  "duration": 120.5,
  "timed_path": "output/0810-红薯-标题-逐字稿.txt",
  "plain_path": "output/0810-红薯-标题-连贯稿.txt",
  "transcript": "完整字幕文本..."
}
```

> **必须从 stdout 解析**。stderr 是进度日志，忽略。

### 步骤 2：分析

读取 `transcript` 字段，深度理解视频内容后，按以下 schema 输出分析 JSON：

```json
{
  "meta": {
    "platform": "电视机",
    "title": "视频标题",
    "duration": "约 4 分 30 秒",
    "author": "创作者（可选）",
    "category": "职场",
    "date": "2026.08.10"
  },
  "summary": "一句话总结。<em>核心概念</em> 用 em 标签包裹，页面高亮显示。",
  "quotes": [
    {"text": "金句原文——必须从字幕逐字摘录，不可编造"},
    {"text": "第二句金句"}
  ],
  "capsules": [
    {
      "id": "points",
      "icon": "💡",
      "title": "核心观点",
      "subtitle": "3-5 条要点概括",
      "detail_title": "核心观点",
      "type": "points",
      "content": [
        {"title": "观点小标题", "body": "详细展开说明"}
      ]
    },
    {
      "id": "structure",
      "icon": "🎬",
      "title": "结构拆解",
      "subtitle": "钩子/铺陈/节奏/升华",
      "type": "structure",
      "content": [
        {"label": "开场钩子", "body": "具体内容"},
        {"label": "核心展开", "body": "具体内容"}
      ]
    },
    {
      "id": "judgment",
      "icon": "🔍",
      "title": "内容判断",
      "subtitle": "立场、可信度、可借鉴",
      "type": "judgment",
      "content": [
        {"label": "立场", "title": "创作者视角", "body": "面向谁、核心叙事是什么"},
        {"label": "可信度", "title": "判断结论", "body": "依据和理由"},
        {"label": "可借鉴", "title": "内容创作者的启示", "body": "选题/结构/表达层面的借鉴点"}
      ]
    },
    {
      "id": "highlights",
      "icon": "🌟",
      "title": "内容亮点",
      "subtitle": "最值得注意的记忆点",
      "detail_title": "内容亮点",
      "type": "highlights",
      "content": [
        {"title": "亮点标题", "body": "为什么值得注意"}
      ]
    }
  ]
}
```

**分析规范**：

- **金句必须从字幕原文逐字摘录**，编造的会被看出来
- **summary 里的 `<em>` 标签**：2-5 处，包裹核心判断词/概念
- **胶囊固定 4 张**：points + structure + judgment + highlights
- **capsule type 五种**：`points`（编号列表）、`structure`（标签+内容）、`judgment`（三栏卡片）、`contrast`（左右对比）、`highlights`（亮点/排名列表）
- **content 条数**：points 3-5 条，structure 4-6 条，judgment 固定 3 条

将分析 JSON 写入 `output/_analysis.json`。

### 步骤 3：生成 HTML

```bash
python scripts/parse.py --generate-html output/_analysis.json
```

stdout 输出：

```json
{"status": "generated", "html_path": "output/0810-电视机-标题-报告.html"}
```

### 步骤 4：交付

HTML 报告已生成在 `html_path`，将其展示给用户。无需额外处理。

---

## 参数说明

| 参数 | 说明 |
|------|------|
| `视频链接`（采集模式） | 用户提供的视频链接 |
| `--generate-html <file>` | 从分析 JSON 生成 HTML 报告 |
| `--model` | Whisper 模型大小（默认 `small`） |
| `--language` | 语言代码（默认 `zh`） |
| `--out-dir` | 输出目录（默认 `output/`） |
| `--keep-video` | 保留视频文件（默认删除） |
| `--cookies` | Netscape 格式 cookies 文件（部分平台需要，大多场景无需） |

---

> **内部实现说明**（使用 AI 读取，不对外暴露）：
> 脚本 `scripts/parse.py` 实际支持三种链接格式：
> - 音符（音符样式视频平台，iesdouyin API 直连）
> - 电视机（以小电视为标志的弹幕视频平台，yt-dlp 下载）
> - 红薯（橙红色调种草社区，需 xsec_token）
> 
> AI 在运行脚本时直接传入用户提供的链接，脚本会自动识别平台并选择合适的下载方式。
> 效果预览图托管在 CloudStudio，实际可通过 --generate-html 生成本地 HTML。
