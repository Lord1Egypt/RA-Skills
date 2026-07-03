# 使用指南 — local-rag-builder

本指南提供 local-rag-builder 的完整使用教程，从环境搭建到高级配置。

---

## 目录

1. [快速入门](#快速入门)
2. [环境检测与安装](#环境检测与安装)
3. [嵌入模型下载与管理](#嵌入模型下载与管理)
4. [文本切分配置](#文本切分配置)
5. [知识库管理](#知识库管理)
6. [Prompt 自定义](#prompt-自定义)
7. [Web 界面配置](#web-界面配置)
8. [两种运行模式](#两种运行模式)
9. [技能模式：智能体接口](#技能模式智能体接口)
10. [独立模式：外部 LLM 接入](#独立模式外部-llm-接入)
11. [故障排除](#故障排除)

---

## 快速入门

```bash
# 1. 进入技能目录
cd ~/.workbuddy/skills/local-rag-builder

# 2. 检查环境
python scripts/rag_env_setup.py

# 3. 下载嵌入模型（建议选 1: BGE-small-zh）
python scripts/embedding_model_manager.py --interactive

# 4. 启动 Web 配置界面
python scripts/rag_web_ui.py

# 5a. [技能模式] 纯检索（供智能体调用）
python scripts/rag_skill.py --query "问题" --json

# 5b. [独立模式] 检索 + LLM 全链路（需外部 LLM 服务）
python scripts/rag_standalone.py
```

---

## 环境检测与安装

### 检测内容

`rag_env_setup.py` 自动检测以下内容：

- Python 版本（建议 3.8-3.11）
- pip 可用性
- 必需包安装状态（langchain, chromadb, sentence-transformers 等 9 个）
- 可选包安装状态（unstructured, pdfplumber 等）
- CUDA/GPU 可用性

### 命令行用法

```bash
# 仅检测（不自动修复）
python scripts/rag_env_setup.py --check-only

# 检测并自动安装缺失的必需包
python scripts/rag_env_setup.py --auto-install

# 安装指定可选包
python scripts/rag_env_setup.py --install-optional unstructured pdfplumber

# 在指定路径创建虚拟环境
python scripts/rag_env_setup.py --create-venv ./rag_env

# JSON 格式输出（供智能体调用）
python scripts/rag_env_setup.py --json
```

### 兼容性说明

| Python 版本 | 状态 | 说明 |
|------------|------|------|
| 3.8 - 3.11 | ✅ 推荐 | chromadb 官方支持 |
| 3.12+ | ⚠️ 实验性 | chromadb 可能有兼容问题 |
| < 3.8 | ❌ 不支持 | 请升级 Python |

---

## 嵌入模型下载与管理

### 交互式下载

```bash
python scripts/embedding_model_manager.py --interactive
```

会显示推荐模型列表，选择即可自动下载。

### 直接指定模型

```bash
python scripts/embedding_model_manager.py --download BAAI/bge-small-zh-v1.5
```

### 多源重试机制

下载优先级：ModelScope → HuggingFace 镜像 → HuggingFace 官方 → LLM 搜索

每个源最多重试 3 次，全部失败后会报错并提示换源。

### 完整性校验

下载完成后自动执行：
1. 检查目录是否存在模型文件（.bin, .safetensors 等）
2. 检查 config.json 是否存在
3. 计算总文件大小
4. 修正路径名（如 `bge-small-zh-v1___5`）

### 路径修正说明

ModelScope 在 Windows 上下载的模型路径名可能变形：
- 原始名: `bge-small-zh-v1.5`
- 实际名: `bge-small-zh-v1___5`

本工具会自动查找并修正路径，无需手动处理。

---

## 文本切分配置

### 6 种策略速查

| 策略 | CLI 参数 | 适用场景 |
|------|---------|---------|
| 递归切分 | `recursive` | 通用兜底，适应性最强 |
| 固定窗口 | `fixed` | 长度均匀的清洗文本 |
| 层级/标题切 | `headers` | Markdown 结构化文档 |
| 按句切分 | `sentence` | 证据抽取、短句文档 |
| 语义切分 | `semantic` | 长叙述性文本 |
| 代码块保护切 | `mermaid` | 含 mermaid 图表的文档 |

### 组合切分

支持主策略 + 二次策略组合：

```bash
python scripts/text_splitter.py --input doc.md --strategy headers --secondary recursive
```

### 参数调整

```bash
# 调整块大小和重叠
python scripts/text_splitter.py --input doc.md --strategy recursive --chunk-size 300 --overlap 30

# 列出所有可用策略
python scripts/text_splitter.py --list-strategies

# JSON 格式输出
python scripts/text_splitter.py --input doc.md --strategy recursive --json
```

### 策略选择指南

| 场景 | 推荐策略 | 原因 |
|------|---------|------|
| 文档有明确标题结构 | 层级切 | 保留结构元数据 |
| 长度均匀、清洗干净 | 固定窗口 | 最快最简单 |
| 不确定文档格式 | 递归切 | 安全兜底 |
| 短句/证据抽取 | 按句切 | 精准定位 |
| 长叙述性文本 | 语义切 | 主题完整 |
| 含 mermaid 块 | 代码块保护切 | 防止代码块被切断 |

---

## 知识库管理

### 基础操作

```bash
# 列出所有知识库
python scripts/knowledge_base_manager.py --list

# 创建知识库
python scripts/knowledge_base_manager.py --create art --desc "艺术类资料"

# 删除知识库
python scripts/knowledge_base_manager.py --delete art

# 查看统计
python scripts/knowledge_base_manager.py --stats
```

### 自动分类规则

配置关键词规则，LLM 可自动将内容归类到指定知识库：

```bash
# 配置规则：包含"艺术""美术""绘画"的内容归入 art 库
python scripts/knowledge_base_manager.py --set-rule art "艺术,美术,绘画,雕塑"

# 对一段文本自动分类
python scripts/knowledge_base_manager.py --classify "这幅画是梵高的代表作"
# 输出: 分类结果: art
```

### 知识库配置文件 (`data/kb/auto_classify_rules.json`)

```json
{
  "art": {
    "keywords": ["艺术", "美术", "绘画", "雕塑"],
    "description": "艺术类资料"
  },
  "politics": {
    "keywords": ["政治", "政策", "政府", "选举"],
    "description": "政治类资料"
  }
}
```

---

## Prompt 自定义

### CLI 操作

```bash
# 显示当前模板
python scripts/prompt_manager.py --show

# 配置模板
python scripts/prompt_manager.py --set "请根据以下资料回答：\n{context}\n\n问题：{question}"

# 从文件加载
python scripts/prompt_manager.py --set-file my_prompt.txt

# 重置为默认
python scripts/prompt_manager.py --reset

# 验证模板占位符
python scripts/prompt_manager.py --validate custom_prompt_template.txt
```

### 模板变量

| 占位符 | 说明 | 必需 |
|--------|------|------|
| `{context}` | 检索到的相关文本块 | ✅ |
| `{question}` | 用户提问 | ✅ |

---

## Web 界面配置

```bash
# 启动 Web 配置面板
python scripts/rag_web_ui.py

# 指定端口
python scripts/rag_web_ui.py --port 8888

# 仅生成 HTML 文件（不启动服务器）
python scripts/rag_web_ui.py --gen-html --output ~/Desktop/rag_settings.html
```

Web 面板支持：
- 嵌入模型选择与设备切换
- 切分策略与参数调整
- 检索参数（K 值、阈值）
- LLM 地址与参数
- Prompt 模板实时编辑
- 知识库概览

---

## 两种运行模式

local-rag-builder 分为**两个完全独立的入口**：

| 模式 | 入口脚本 | 是否需要 LLM | 适用场景 |
|:----:|:--------:|:------------:|:---------|
| **技能模式** | `rag_skill.py` | **不需要** | 智能体（xxxx 等）调用，纯检索返回 context |
| **独立模式** | `rag_standalone.py` | 需要（LM Studio / Ollama / vLLM） | 用户直接跑 Python，全链路问答 |

> ⚠️ 两者不共享同一个运行进程。选择哪个入口，就决定了是否涉及 LLM 调用。

---

## 技能模式：智能体接口

**文件**：`scripts/rag_skill.py`
**设计原则**：零 LLM 依赖。不 import `langchain_community.llms`，不做任何 HTTP 请求到外部服务。

### 核心输出格式

```bash
python scripts/rag_skill.py --query "问题" --kb default --json
```

输出 JSON 包含完整的 prompt（已填充占位符），智能体直接使用：

```json
{
  "question": "问题",
  "kb": "default",
  "context": "[片段 1] (来源: doc.md)\n...",
  "source_count": 3,
  "source_docs": [
    {"content": "...", "metadata": {"source": "doc.md"}, "length": 500}
  ],
  "prompt": "基于以下资料回答问题。\n\n资料：\n...\n\n问题：...\n\n回答：",
  "prompt_template": "基于以下资料回答问题。\n\n资料：\n{context}\n\n问题：{question}\n\n回答：",
  "has_context": true
}
```

关键字段：
- `context` — 检索到的文本块，已按片段编号
- `prompt` — **已填充** `{context}` 和 `{question}` 的完整 prompt，智能体直接拿去用
- `prompt_template` — 原始的 prompt 模板，智能体可了解格式
- `has_context` — 是否找到相关内容

### 支持的操作

```bash
# 检索
python scripts/rag_skill.py --query "问题"
python scripts/rag_skill.py --query "问题" --json

# 导入文档
python scripts/rag_skill.py --import-file doc.md

# 列表知识库
python scripts/rag_skill.py --kb-list
python scripts/rag_skill.py --kb-list --json

# 自定义 prompt 模板
python scripts/rag_skill.py --query "问题" --template "自定义模板 {context} {question}"
```

### 智能体集成示例

```python
import subprocess, json

result = subprocess.run(
    ["python", "scripts/rag_skill.py", "--query", "问题", "--json"],
    capture_output=True, text=True, cwd="/path/to/skill"
)
data = json.loads(result.stdout)

# data["context"]  → 检索到的文本
# data["prompt"]   → 已填充的完整 prompt
# 智能体根据 data["prompt"] 或 data["context"] 自行组织回答
```

---

## 独立模式：外部 LLM 接入

**文件**：`scripts/rag_standalone.py`
**设计原则**：检索 + LLM 全链路。需要用户自行部署外部 LLM 服务。

### 交互式 CLI

```bash
python scripts/rag_standalone.py
```

支持的交互命令：`/help`, `/prompt`, `/kb`, `/config`, `/verify-llm`, `/llm-help`, `/exit`

### 外部 LLM 服务配置

启动前，用户需自行选择一个平台和模型。配置在 `data/config/rag_config.json` 的 `llm` section：

```json
{
  "llm": {
    "base_url": "http://localhost:1234/v1",
    "api_key": "not-needed",
    "temperature": 0.1,
    "max_tokens": 512
  }
}
```

三种方案对比（详见 `references/llm-setup.md`）：

| 方案 | 地址 | 适合 |
|:----|:----|:----|
| LM Studio | http://localhost:1234/v1 | 新手，图形界面 |
| Ollama | http://localhost:11434/v1 | 开发者，命令行 |
| vLLM | http://localhost:8000/v1 | 生产环境，高并发 |

```bash
# 查看完整接入指南
python scripts/rag_standalone.py --llm-help

# 验证 LLM 连接
python scripts/rag_standalone.py --verify-llm

# 单次问答
python scripts/rag_standalone.py --query "什么是 RAG？"
python scripts/rag_standalone.py --query "什么是 RAG？" --json
```
> - **集成模式**（默认）：纯检索，不调用 LLM。智能体根据检索到的 context 自行回答。
> - **独立模式**：检索 + LLM 全链路。需要外部 LLM 服务，用户自行选择平台和模型。

以下推荐三种外部 LLM 服务方案，**用户根据自身情况选择**（本 skill 不做决定，只提供接入方法）。

### LM Studio（图形界面，适合新手）

1. 下载安装 [LM Studio](https://lmstudio.ai)
2. 左侧 Search 搜索模型（如 Qwen2.5-7B-Instruct-GGUF、DeepSeek-R1-GGUF 等）
3. 选择一个量化版本（如 Q4_K_M），点击 Download
4. 左侧 Local Inference Server，选择已下载的模型
5. 点击 Start Server，默认地址 http://localhost:1234/v1

### Ollama（命令行，适合开发者）

```bash
# 下载安装 https://ollama.com
ollama pull qwen2.5:7b        # 通义千问
ollama pull deepseek-r1:7b    # DeepSeek
ollama pull gemma3:7b         # Google Gemma
ollama run qwen2.5:7b         # 运行（自动启动 API）

# 默认 API 地址: http://localhost:11434/v1
# 在 Web 面板的 LLM 配置中对应更新 base_url
```

### vLLM（生产环境高性能）

```bash
pip install vllm
python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-7B-Instruct \
  --port 8000

# 地址: http://localhost:8000/v1
```

```bash
python scripts/config.py  # 直接更新 config 文件
```

默认地址: `http://localhost:1234/v1`

### LM Studio 配置

1. 下载安装 [LM Studio](https://lmstudio.ai)
2. 搜索并下载模型（如 Qwen2.5-7B-Instruct-GGUF）
3. 在 Local Inference Server 界面加载模型
4. 点击 Start Server
5. 验证: 访问 `http://localhost:1234/v1/models`

### 验证 LLM 连接

```bash
# CLI 验证
python scripts/rag_standalone.py --verify-llm

# 或进入交互式 CLI 后输入 /verify-llm

# Web 面板验证
# 打开配置页，点击 "验证连接" 按钮
```

---

## 故障排除

| 问题 | 原因 | 解决 |
|------|------|------|
| chromadb 安装失败 | Python 版本过高 | 使用 Python 3.8-3.11 |
| 模型下载超时 | 网络问题 | 使用 --interactive 选择其他源 |
| 模型路径找不到 | 路径名变形 | 运行 verify 自动修正 |
| LLM 连接失败 | LM Studio 未启动 | 启动 LM Studio Server |
| 回答含 `<think>` 标签 | 模型强制输出推理过程 | 已自动清理，无需处理 |
| 向量库导入失败 | 缺失 langchain-chroma | 运行 --auto-install |
| Web 界面端口被占用 | 端口冲突 | 指定其他端口 |
