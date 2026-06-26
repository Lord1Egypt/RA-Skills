---
name: langextract
description: Google 出品的 Python 库，用 LLM 从非结构化文本中提取结构化信息，每个提取结果精确对应源文本位置，支持交互式可视化，适配 Gemini/OpenAI/Ollama 等多种模型
version: 0.1.1
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: 🔍
    homepage: https://github.com/google/langextract
---

# LangExtract — LLM 驱动的结构化信息提取

LangExtract 是 Google 出品的 Python 库，利用 LLM 从临床笔记、法律文书、新闻报道等非结构化文本中提取结构化信息。其核心优势是**精确源文本定位**：每个提取结果都映射到源文本的精确字符位置，支持可视化高亮审查，适合需要可追溯性的企业级数据提取场景。只需几个示例即可定义提取任务，无需微调模型。

## 核心使用场景

- **医疗文本提取**：从临床笔记提取药物、剂量、诊断结果，含可追溯的源文本定位
- **法律文书解析**：提取合同条款、当事方信息、关键日期等结构化字段
- **文学/学术分析**：提取人物、情感、关系等实体（如 Romeo and Juliet 示例）
- **长文档批量处理**：分块并行处理大型文档，支持多次 Pass 提高召回率
- **交互式审查**：生成自包含 HTML 可视化文件，高亮显示提取结果与源文本的对应关系

## AI 辅助使用流程

1. **安装依赖** — AI 执行 `pip install langextract` 并配置 API 密钥
2. **定义提取任务** — AI 根据需求编写提取描述（prompt）和高质量示例（examples）
3. **运行提取** — AI 调用 `lx.extract()` 处理文本或文档 URL
4. **保存结果** — AI 将结果存为 JSONL 格式，便于后续分析
5. **生成可视化** — AI 调用 `lx.visualize()` 生成交互式 HTML 审查界面
6. **过滤非定位提取** — AI 过滤掉 `char_interval=None` 的结果，保留有源文本依据的提取

## 关键章节导航

- [安装指南](guides/01-installation.md) — pip 安装、API 密钥配置、Ollama 本地模型
- [快速开始](guides/02-quickstart.md) — 定义提取任务、运行提取、结果过滤、可视化
- [高级用法](guides/03-advanced-usage.md) — 长文档处理、自定义模型、医疗/法律场景
- [故障排查](troubleshooting.md) — API 认证、Prompt 对齐警告、召回率低

## AI 助手能力

使用本技能时，AI 可以：

- ✅ 安装 LangExtract 并配置 Gemini/OpenAI API 密钥
- ✅ 根据用户描述的提取需求，自动编写 `prompt_description` 和 `examples`
- ✅ 调用 `lx.extract()` 处理文本字符串或文档 URL
- ✅ 过滤非定位（`char_interval=None`）的提取结果
- ✅ 保存提取结果为 JSONL 格式
- ✅ 生成交互式 HTML 可视化文件
- ✅ 配置 Ollama 本地模型，避免 API 费用
- ✅ 使用并行处理和分块策略处理长文档

## 核心功能

- ✅ **精确源文本定位** — 每个提取结果映射到源文本的 `char_interval`（字符偏移）
- ✅ **结构化输出** — 基于 Few-shot 示例强制输出一致 Schema
- ✅ **长文档优化** — 文本分块 + 并行处理 + 多次 Pass，提高大文档召回率
- ✅ **交互式可视化** — 自包含 HTML 文件，高亮显示数千个提取结果
- ✅ **多模型支持** — Gemini（推荐）、OpenAI、Ollama 本地模型
- ✅ **域无关** — 用 Few-shot 示例适配任意领域，无需微调
- ✅ **自动对齐检测** — 检测示例与文本不匹配的情况并发出警告
- ✅ **URL 直接处理** — 可直接传入文档 URL（如 Gutenberg 文本）

## 快速示例

```python
import langextract as lx

# 定义提取任务
result = lx.extract(
    text_or_documents="John took aspirin 500mg twice daily for headache.",
    prompt_description="Extract medications and dosages.",
    examples=[
        lx.data.ExampleData(
            text="Patient was prescribed ibuprofen 400mg.",
            extractions=[
                lx.data.Extraction(
                    extraction_class="medication",
                    extraction_text="ibuprofen 400mg",
                    attributes={"dosage": "400mg"}
                )
            ]
        )
    ],
    model_id="gemini-2.5-flash",
)

# 只保留有源文本依据的结果
grounded = [e for e in result.extractions if e.char_interval]
print(grounded)

# 生成可视化
lx.io.save_annotated_documents([result], output_name="out.jsonl", output_dir=".")
html = lx.visualize("out.jsonl")
```

## 安装要求

| 依赖 | 版本要求 |
|------|---------|
| Python | >= 3.9 |
| Gemini API Key | 推荐（或 OpenAI/Ollama） |
| pip | 任意版本 |

## 项目链接

- GitHub：https://github.com/google/langextract
- PyPI：https://pypi.org/project/langextract/
- 论文 DOI：https://doi.org/10.5281/zenodo.17015089
