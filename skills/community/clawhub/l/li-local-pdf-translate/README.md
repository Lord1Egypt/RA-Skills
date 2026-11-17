# 多国语言本地 PDF 翻译 Skill 说明

> 本地 llama.cpp 模型 · 学术三步法 · **八国语言任意互译** · 批量处理

本 Skill 通过本地运行的翻译模型（如 `Hy-MT2-7B`）批量翻译 **PDF / Markdown / TXT** 文档。默认仅连接本机 llama-server（`http://localhost:8001`），文档文本默认只发给该本地端点；**若用户在配置中将 `api_url` 指向远程服务，文档文本将发送至该地址，请自行确认目标端点可信**。

---

## 一、支持的语言（八大主要语言）

| 代码 | 语言 | 代码 | 语言 |
|:----:|:----:|:----:|:----:|
| `zh` | 中文 (Chinese) | `de` | 德语 (German) |
| `en` | 英语 (English) | `es` | 西班牙语 (Spanish) |
| `ja` | 日语 (Japanese) | `ru` | 俄语 (Russian) |
| `ko` | 韩语 (Korean) | `fr` | 法语 (French) |

**方向格式**：`[源语言]2[目标语言]`，例如：

- `en2zh`：英语 → 中文（默认方向）
- `zh2ja`：中文 → 日语
- `ja2en`：日语 → 英语
- `fr2de`：法语 → 德语
- `ru2zh`：俄语 → 中文
- `ko2fr`：韩语 → 法语
- ……

**八语两两组合共 64 种方向（含同语）全部支持**，任意双向互译，无需逐个配置。兼容 `en-zh`（连字符）写法，也兼容 `zh-CN` 等变体的前两位识别。

查看支持的语言清单：

```bash
python scripts/config.py show
```

---

## 二、文件结构

```
li_local_pdf_translate/
├── SKILL.md                      # Skill 定义（供 Agent 读取）
├── README.md                     # 本说明文档
├── config/
│   ├── default.json             # 默认配置（模型、API 等）
│   └── user.json                # 用户配置（可选，优先级更高）
└── scripts/
    ├── config.py                # 配置管理与八语定义（LANGUAGES 表）
    ├── extract_pdf.py           # PDF 文本逐页提取（pymupdf）
    ├── translate_api.py         # 本地模型翻译封装（语言化提示词）
    ├── batch_translate.py       # 批量翻译主程序（单文件/目录）
    ├── auto_translate.py        # 单 Agent 顺序自动翻译
    └── multi_agent_translate.py # 多 Agent 并行翻译（2-4 并发）
```

---

## 三、安装与前置条件

> 以下环境准备步骤请在终端手动完成（亦可让 AI 协助，见下方「Agent 协助安装」）；模型文件放置在 `models/` 目录。
> 环境缺失时，Agent 可代为下载/安装，但**必须先列明"待安装项 + 安装命令"并征得您明确同意（Y）后才执行**；禁止静默安装，禁止静默下载任意模型。

```bash
# 1. 安装 Python 依赖（PyPI 官方源，手动执行）
pip install pymupdf requests

# 2. 模型文件：放入本 skill 根目录下的 models/ 文件夹

# 3. 在 skill 根目录启动本地翻译模型（Windows，相对路径，端口 8001）
start_server.bat
```

### Agent 协助安装（可选，需用户确认）

> 若您希望由 AI（opencode / codex / Hermes Agent / OpenClaw 等）代为准备环境，Agent 须按以下流程，**先征求您明确同意再执行**：

1. **只读检测**（只检测、不改动）：
   ```bat
   where llama-server
   python --version
   python -c "import fitz, requests"
   if exist "models\*.gguf" (echo model-ok) else (echo model-missing)
   ```
2. **缺失项与推荐安装方式（Windows）**：

   | 缺失项 | 推荐安装方式 |
   |--------|-------------|
   | `llama-server`（核心，llama.cpp） | 从 llama.cpp 官方 GitHub Releases 下载 Windows 预编译包，解压放入 skill 根目录（或 `winget` 安装并加入 PATH） |
   | `pymupdf` / `requests` | `pip install pymupdf requests`（PyPI 官方源） |
   | GGUF 翻译模型（**可选**，通常数 GB） | 用户自备放入 `models\`；默认**不自动下载**，仅在用户明确指定来源并要求时 Agent 方可代下载 |

3. **执行规则**：Agent 先输出检测结果与安装计划并提问"是否执行？（Y/N）"；得到 Y 后逐条执行，路径一律相对 skill 根目录；任一步失败立即停下并给备选方案，不静默重试/绕过；完成后重新检测，仍缺失则中止并说明。
4. 安装完成后由 `start_server.bat` 启动 llama-server（相对路径、端口 8001），再运行 `python scripts/batch_translate.py --check` 验证连通。

> 注意：模型需能处理目标语言。`Hy-MT2-7B` 对中/英/日的支持最好；跨小语种组合建议使用更大或对应语种的模型，并配合 `--depth full`。

---

## 四、快速开始

```bash
# 0. 查看配置与支持语言（重要！八语切换先看这里）
python scripts/config.py show

# 1. 检查模型连接
python scripts/batch_translate.py --check

# 2. 翻译单个 PDF：英语→中文（默认）
python scripts/batch_translate.py --input "paper.pdf"

# 3. 翻译单个 PDF：中文→日语，指定输出文件
python scripts/batch_translate.py --input "paper.pdf" --direction zh2ja --output "paper.ja.md"

# 4. 批量翻译目录：韩语→法语
python scripts/batch_translate.py --input-dir "E:\docs" --direction ko2fr
```

输出文件按 **目标语言代码** 命名：

```text
方向 en2zh:  paper.pdf  →  paper.zh.md
方向 zh2ja:  paper.pdf  →  paper.ja.md
方向 ja2en:  paper.pdf  →  paper.en.md
方向 en2fr:  paper.pdf  →  paper.fr.md
```

批量模式默认输出目录为 `<输入目录>_<目标语言>`（例如 `en2ja` 时为 `<输入目录>_ja`）。

---

## 五、三种执行模式

| 模式 | 命令 | 特点 |
|------|------|------|
| **直接翻译** | `batch_translate.py` | 单文件或整目录，脚本内逐页处理 |
| **单 Agent** | `auto_translate.py` | 顺序处理，低 GPU 占用，稳定优先 |
| **多 Agent** | `multi_agent_translate.py` | 2-4 并发，约 1.5-2 倍速，大批量优先 |

```bash
# 单 Agent：英→俄
python scripts/auto_translate.py --input "E:\pdfs" --direction en2ru

# 多 Agent：英→俄（4 并发）
python scripts/multi_agent_translate.py --input "E:\pdfs" --direction en2ru --agents 4
```

---

## 六、深度模式（学术三步法）

| 深度 | 流程 | 耗时倍率 | 适用 |
|------|------|:------:|------|
| `quick` | 仅直译 | 1× | 快速理解大意 |
| `standard` | 直译 + 反思（学术规范、术语一致） | 2.5× | 日常推荐（默认） |
| `full` | 直译 + 反思 + 雅化（信达雅、顶会风格） | 4× | 投稿发表、跨语种组合 |

```bash
python scripts/batch_translate.py --input "paper.pdf" --direction ja2en --depth full
```

---

## 七、参数说明

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `--input` / `-i` | path | 必填 | 输入 PDF 文件或目录 |
| `--output` / `-o` | path | 自动 | 输出文件/目录 |
| `--input-dir` / `--output-dir` | path | — | 批量模式目录 |
| `--direction` | string | `en2zh` | 方向，如 `en2zh` `zh2ja` `ja2en`，八语任意 |
| `--depth` | enum | `standard` | `quick` / `standard` / `full` |
| `--pages` | string | 全部 | 页码，如 `"1-5"` 或 `"1,3,5-7"` |
| `--agents` | int | 2 | 多 Agent 并发数（最大 4） |
| `--filter` | string | — | 单 Agent/多 Agent 的文件过滤，如 `"*.pdf"` |
| `--api-url` / `--api-key` / `--model` | string | 配置值 | 覆盖默认配置 |
| `--check` | flag | — | 仅测试连接 |
| `--config` | flag | — | 显示配置及支持语言 |

---

## 八、常见问题

| 问题 | 解决 |
|------|------|
| API 连接失败 | 检查 llama-server 是否在 skill 根目录启动、端口 8001 是否占用 |
| `Unsupported source/target language` | 方向必须为两位代码，如 `en2zh`；`config.py show` 查看支持列表 |
| `Invalid direction` | 检查格式是否含 `2` 或 `-` 分隔，如 `zh2ja` |
| 小语种翻译质量差 | 换用覆盖目标语种的模型；或 `--depth full` |
| 输出文件里出现乱码 | PDF 需有文本层且字体嵌入（含 CJK/西里尔字符集），扫描件不支持 |
| 内存不足 | 减小 `--batch-size`、降低并发、关闭其他程序 |
| 长文档翻译慢 | 单 Agent 约 50 tokens/s；大批量用多 Agent |

---

## 九、扩展更多语言

只需在 `scripts/config.py` 的 `LANGUAGES` 表中增加一项即可，无需改动其他代码：

```python
LANGUAGES = {
    ...
    "it": {"name": "意大利语", "name_en": "Italian"},
}
```

然后即可使用 `en2it`、`it2zh` 等新方向。

---

*生成质量取决于本地模型能力；八语互译为软件能力支持，实际效果请以模型覆盖语种为准。*