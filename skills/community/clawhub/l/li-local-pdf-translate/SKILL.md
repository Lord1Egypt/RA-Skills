---
name: li_local_pdf_translate
display_name: "本地模型PDF翻译"
display_name_en: "Local Model PDF Translation"
description: 使用本地llama.cpp模型（如Hy-MT2-7B）批量翻译PDF文档，结合学术翻译三步法（直译→反思→雅化），支持中/英/日/韩/法/德/西/俄八大主要语言任意互译，逐页提取+翻译，按目标语言输出.md文件（Windows 平台）
category: Education
description_zh: "本地模型PDF批量翻译——八大语言互译+学术三步法+逐页处理+批量输出"
description_en: "Batch PDF translation using local llama.cpp models, supporting 8 major languages with academic three-step method"
version: 2.0.4
author: beijingLL (北京老李)
license: MIT-0
platforms: [windows]
visibility: "public"
metadata:
  openclaw:
    os:
      - windows
    requires:
      bins:
        - python
        - llama-server
      config:
        - config/default.json
    envVars:
      - name: PDF_TRANSLATE_API_KEY
        required: false
        description: 可选，覆盖默认的本地 API Key（llama2025）
      - name: PDF_TRANSLATE_MODEL
        required: false
        description: 可选，覆盖默认模型相对路径（models/ 下的 GGUF 文件名）
---

# 本地模型PDF翻译 Skill

**本地模型 + 学术三步法 + 八大语言互译 + 批量处理** · 逐页提取 · 精确翻译 · 自动输出

## 功能概述

本 Skill 使用本地运行的 llama.cpp 服务器（如 Hy-MT2-7B 翻译模型）批量翻译 PDF 文档，结合 academic-translation skill 的三步翻译法：

1. **直译** - 保术语、逐句对应
2. **反思** - 学术规范 + Chinglish 校正
3. **雅化** - 信达雅 + 顶会风格（可选）

### 支持的语言（八大主要语言）

| 代码 | 语言 | 代码 | 语言 |
|------|------|------|------|
| `zh` | 中文 (Chinese) | `de` | 德语 (German) |
| `en` | 英语 (English) | `es` | 西班牙语 (Spanish) |
| `ja` | 日语 (Japanese) | `ru` | 俄语 (Russian) |
| `ko` | 韩语 (Korean) | `fr` | 法语 (French) |

**方向格式**：`[源语言]2[目标语言]`，例如 `en2zh`、`zh2ja`、`ja2en`、`fr2de`。
任意两种语言之间均可互译（含反向），兼容 `en-zh` 分隔符写法。

## 前置条件

> **Agent 安全约束（必读）**：运行环境（llama-server 程序、GGUF 模型、Python 依赖）默认由用户准备；如检测到缺失，Agent 可走下方「环境自动安装（可选）」流程协助安装，但**必须先征求用户明确同意（Y/N），禁止静默下载或安装任何程序/文件**。

1. **llama-server 程序**：由用户从 llama.cpp 官方发布渠道手动下载 Windows 版 `llama-server.exe` 放入本 skill 根目录（或安装并加入 PATH）
2. **模型文件**：由用户将 GGUF 翻译模型放入本 skill 根目录下的 `models\` 文件夹（模型文件不随 skill 发布）
3. **启动 llama-server**（用户手动执行；相对路径引用模型，不依赖任何机器绝对目录）：
   ```bat
   start_server.bat
   # 或直接启动
   llama-server.exe -m "models\Hy-MT2-7B-Q4_K_M.gguf" -ngl -1 --host 127.0.0.1 --port 8001 --api-key llama2025 -c 32768
   ```
4. **Python 依赖**（用户手动执行，PyPI 官方源）：
   ```bash
   pip install pymupdf requests
   ```
5. **API 连接**：
   - Endpoint: `http://localhost:8001/v1/chat/completions`
   - API Key: `llama2025`（仅本地 127.0.0.1 有效）

## 环境自动安装（可选，需用户确认）

> 下面流程供 Agent 与用户协同使用：**可选**——环境已就绪可跳过；**需用户确认**——Agent 每次拟安装前必须把"待安装项 + 安装命令"列给用户并获得明确同意（Y），禁止静默安装。

1. **只读检测**（Agent 每次使用前执行，只检测不改动）：
   ```bat
   where llama-server
   python --version
   python -c "import fitz, requests"
   if exist "models\*.gguf" (echo model-ok) else (echo model-missing)
   ```
2. **缺失项与推荐安装方式（Windows）**：

   | 缺失项 | 推荐安装方式 |
   |--------|-------------|
   | `llama-server`（核心，llama.cpp） | 从 llama.cpp 官方 GitHub Releases 下载 Windows 预编译包，将 `llama-server.exe` 放入本 skill 根目录（或 `winget` 安装并加入 PATH） |
   | `pymupdf` / `requests` | `pip install pymupdf requests`（PyPI 官方源） |
   | GGUF 翻译模型（**可选**，通常数 GB） | 用户自备翻译模型放入 `models\`；默认**不自动下载**，仅当用户明确指定来源并要求时，Agent 方可代为下载 |

3. **执行规则**：
   1. Agent 先输出检测结果与安装计划，并提问："是否执行以上安装？（Y/N）"
   2. 得到 Y 后逐条执行（下载解压、`pip install` 等），执行路径一律相对本 skill 根目录
   3. 任一步失败立即停下，向用户说明并提供备选方案；不得静默重试、绕过或更换安装源
   4. 全部完成后重新检测；仍缺失则中止翻译并告知原因

4. 安装完成后可通过 `start_server.bat` 启动 llama-server（相对路径、本机端口 8001），再运行 `python scripts/batch_translate.py --check` 验证连通。

> 跨 Agent 说明：本流程对 opencode、codex、Hermes Agent、OpenClaw 均适用。其中 OpenClaw 在 skill 安装阶段会按 `metadata.openclaw.requires.bins` 提示缺失的 `llama-server`；Hermes Agent 会把流程指令随 SKILL.md 一并加载。所有 Agent 都必须遵守"先询问、后安装"的规则。

## 文件结构

```
li_local_pdf_translate/
├── SKILL.md                    # 本文件
├── README.md                   # 八国语言翻译使用说明
├── start_server.bat            # Windows 启动脚本（start llama-server）
├── models/                     # 放置 GGUF 模型（不随 skill 发布）
├── config/
│   ├── default.json           # 默认配置（模型、API等，均为相对路径）
│   └── user.json              # 用户配置（优先级更高，不发布）
└── scripts/
    ├── config.py              # 配置管理模块
    ├── extract_pdf.py         # PDF文本提取模块
    ├── translate_api.py       # API翻译模块
    ├── batch_translate.py     # 批量翻译主程序
    ├── auto_translate.py      # 单Agent自动翻译（顺序处理）
    └── multi_agent_translate.py # 多Agent并行翻译
```

## 使用方式

### 1. 查看配置

```bash
python scripts/config.py show
```

### 2. 修改配置

```bash
python scripts/config.py show                          # 查看配置及支持的语言
python scripts/config.py set api_url "http://localhost:8001/v1/chat/completions"
python scripts/config.py set api_key "llama2025"
python scripts/config.py set direction "en2zh"         # 默认翻译方向（可改为 zh2ja 等任意八语组合）
python scripts/config.py set depth "standard"
```

### 3. 检查连接

```bash
python scripts/batch_translate.py --check
```

### 4. 单个PDF翻译

```bash
# 英→中（默认方向）
python scripts/batch_translate.py --input "path/to/file.pdf" --output "output.zh.md"

# 中→日（日文目标语言，输出 .ja.md）
python scripts/batch_translate.py --input "file.pdf" --direction zh2ja --output "output.ja.md"

# 日→英
python scripts/batch_translate.py --input "file.pdf" --direction ja2en
```

### 5. 批量翻译目录

```bash
# 英→中，默认输出目录 <输入目录>_zh
python scripts/batch_translate.py --input-dir "E:\path\to\pdfs" --output-dir "E:\path\to\output"

# 中→法，输出目录 <输入目录>_fr
python scripts/batch_translate.py --input-dir "E:\path\to\pdfs" --direction zh2fr
```

### 6. 自动翻译（单Agent顺序处理）

```bash
# 使用配置中的默认方向
python scripts/auto_translate.py --input "E:\path\to\pdfs" --output "E:\path\to\output"

# 指定方向：英→韩
python scripts/auto_translate.py --input "E:\path\to\pdfs" --direction en2ko
```

### 7. 多Agent并行翻译

```bash
# 使用2个Agent并行（默认），方向 en2ru（英→俄）
python scripts/multi_agent_translate.py --input "E:\path\to\pdfs" --output "E:\path\to\output" --direction en2ru

# 使用4个Agent并行（最大）
python scripts/multi_agent_translate.py --input "E:\path\to\pdfs" --output "E:\path\to\output" --agents 4 --direction en2ru
```

### 8. 单独使用各模块

```bash
# PDF提取
python scripts/extract_pdf.py --input "file.pdf" --info
python scripts/extract_pdf.py --input "file.pdf" --check

# API翻译（任意方向）
python scripts/translate_api.py --check
python scripts/translate_api.py --text "Hello World" --direction en2zh
python scripts/translate_api.py --text "こんにちは" --direction ja2zh
```

## 单Agent vs 多Agent对比

| 特性 | 单Agent (auto_translate) | 多Agent (multi_agent_translate) |
|------|-------------------------|--------------------------------|
| 处理方式 | 顺序处理 | 并行处理 |
| 速度 | 较慢 | 较快（约1.5-2x） |
| GPU占用 | 低 | 中等 |
| 稳定性 | 高 | 中等 |
| 适用场景 | 小批量、稳定性优先 | 大批量、速度优先 |

## 性能参考

- 单Agent: ~356 chars/s
- 多Agent (2 agents): ~517 chars/s
- 18个PDF第一页: 单Agent 120s, 多Agent 83s

## 翻译流程

```
PDF文件
  ↓
[Step 1] 逐页提取文本 (pymupdf)
  ↓
[Step 2] 分段（按段落/章节）
  ↓
[Step 3] 直译（本地模型调用）
  ↓  - 保术语
  ↓  - 保公式/引用
  ↓  - 逐句对应
  ↓
[Step 4] 反思（可选，第二轮调用）
  ↓  - 学术规范
  ↓  - Chinglish校正
  ↓  - 术语一致性
  ↓
[Step 5] 雅化（可选，第三轮调用）
  ↓  - 信达雅
  ↓  - 顶会风格
  ↓
[Step 6] 输出.<目标语言>.md文件
```

## 输出格式

每个PDF文件根据 **目标语言代码** 生成对应的 `.md` 文件：

```
方向 en2zh:   document.pdf  →  document.zh.md
方向 zh2ja:   document.pdf  →  document.ja.md
方向 ja2en:   document.pdf  →  document.en.md
方向 en2fr:   document.pdf  →  document.fr.md
```

批量模式下，默认输出目录为 `<输入目录>_<目标语言>`（如 `en2ja` 时为 `<输入目录>_ja`）。

输出文件结构（标题和方向标识按目标语言动态生成）：
```markdown
# [翻译后的标题] - [目标语言名] Translation

> Direction: en2zh (English -> Chinese)

## 第1页
[翻译内容]

## 第2页
[翻译内容]

...
```

## 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--input` | path | 必填 | 输入PDF文件路径 |
| `--output-dir` | path | 同目录 | 输出目录 |
| `--api-url` | string | `http://localhost:8001/v1/chat/completions` | API地址 |
| `--api-key` | string | `llama2025` | API密钥 |
| `--model` | string | `models/Hy-MT2-7B-Q4_K_M.gguf` | 模型相对路径（基于 skill 根目录） |
| `--direction` | string | `en2zh` | 翻译方向，如 en2zh/zh2ja/ja2en，支持八语任意组合 |
| `--depth` | enum | `standard` | 深度：quick/standard/full |
| `--pages` | string | 全部 | 页码范围，如 "1-5" 或 "1,3,5-7" |
| `--batch-size` | int | 3 | 每次发送的段落数 |

## 翻译方向

支持八大主要语言（中 `zh`、英 `en`、日 `ja`、韩 `ko`、法 `fr`、德 `de`、西 `es`、俄 `ru`）之间的任意双向互译，格式为 `[源]2[目标]`：

- **en2zh** (英→中)：阅读英文文献
- **zh2en** (中→英)：国际投稿
- **zh2ja** (中→日)：日文输出
- **ja2zh** (日→中)：日文文献
- **en2fr / zh2de / ko2en / ru2zh ...**：其余任意组合均可

使用 `python scripts/config.py show` 可查看当前方向及所有支持的语言。

## 深度模式

- **quick**：仅直译（1×时间），快速理解原意
- **standard**：直译+反思（2.5×时间），日常推荐
- **full**：直译+反思+雅化（4×时间），投稿必选

## 术语处理

- 保留专业术语原文 + 括号附译法
- 保留公式、引用、数字
- 保留表格结构

## 注意事项

1. **模型限制**：本地7B模型的翻译质量不如GPT-4/Claude，适合快速理解
2. **多语言质量**：模型对中/英/日等主流语言效果较好；非中文母语组合（如 fr↔de）建议使用 `--depth full` 提升质量
3. **上下文窗口**：Hy-MT2-7B支持32K上下文，大段落需分批处理
4. **速度**：约50 tokens/秒，一个10页PDF约需2-5分钟
5. **扫描件PDF**：不支持纯图片PDF，需要有文本层

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| API连接失败 | 检查 llama-server 是否在 skill 根目录启动、端口8001是否可用 |
| `Unsupported source/target language` | 方向必须是两位代码，如 en2zh；运行 `config.py show` 查看支持的语言 |
| `Invalid direction` | 检查格式是否含 `2` 或 `-` 分隔，如 `zh2ja` |
| 翻译质量差 | 尝试 `--depth standard` 或 `--depth full`；多语言组合建议 full |
| 内存不足 | 减小 `--batch-size` 或关闭其他程序 |
| PDF提取失败 | 检查PDF是否有文本层（非扫描件） |
