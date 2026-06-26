# 安装指南

## 适用场景

- 安装 LangExtract 并配置 LLM API 密钥
- 选择使用 Gemini、OpenAI 还是本地 Ollama 模型
- 在 Jupyter/Colab 环境中使用

---

## 基础安装

> **AI 可自动执行**

```bash
pip install langextract
```

验证安装：
```python
import langextract as lx
print(lx.__version__)
```

---

## API 密钥配置

### Gemini（推荐）

LangExtract 使用 Gemini 模型的控制生成能力确保结构化输出：

```bash
# 获取 API Key：https://aistudio.google.com/app/apikey
export GOOGLE_API_KEY="your-api-key-here"

# 或写入 .env 文件（配合 python-dotenv 使用）
echo 'GOOGLE_API_KEY=your-api-key-here' >> .env
```

```python
# 在代码中加载
from dotenv import load_dotenv
load_dotenv()

import langextract as lx
# 自动读取 GOOGLE_API_KEY
```

### OpenAI

```bash
export OPENAI_API_KEY="your-openai-key"
```

```python
# 使用时指定 model_id
result = lx.extract(
    text_or_documents=text,
    prompt_description=prompt,
    examples=examples,
    model_id="gpt-4o",   # OpenAI 模型
)
```

### Ollama（本地模型，无需 API Key）

```bash
# 先安装 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 拉取模型（如 Llama3）
ollama pull llama3.2

# LangExtract 配置使用 Ollama
```

```python
result = lx.extract(
    text_or_documents=text,
    prompt_description=prompt,
    examples=examples,
    model_id="ollama/llama3.2",  # Ollama 本地模型
)
```

---

## Jupyter/Colab 安装

```bash
# 在 Notebook 中安装
!pip install langextract

# 配置 API Key（Colab）
import os
from google.colab import userdata
os.environ["GOOGLE_API_KEY"] = userdata.get("GOOGLE_API_KEY")
```

---

## 验证安装

```python
import langextract as lx
import os

# 确认 API Key 已配置
assert os.getenv("GOOGLE_API_KEY"), "请设置 GOOGLE_API_KEY 环境变量"

# 快速测试
result = lx.extract(
    text_or_documents="John took aspirin 500mg for headache.",
    prompt_description="Extract medications and dosages.",
    examples=[
        lx.data.ExampleData(
            text="Patient took ibuprofen 400mg.",
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
print(f"提取了 {len(result.extractions)} 个实体")
```

---

## 完成确认检查清单

- [ ] `pip install langextract` 成功
- [ ] `GOOGLE_API_KEY`（或其他）环境变量已设置
- [ ] 验证代码运行成功，`result.extractions` 非空

---

## 下一步

- [快速开始](02-quickstart.md) — 定义提取任务、运行提取、结果过滤、可视化
