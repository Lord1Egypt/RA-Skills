# 高级用法

## 长文档处理

对于超长文档（小说、报告、合同），LangExtract 自动分块并行处理：

```python
import langextract as lx

prompt = """Extract characters, emotions, and relationships in order of appearance.
Use exact text for extractions. Do not paraphrase or overlap entities."""

examples = [...]  # 如快速开始中定义的示例

# 直接处理长文档 URL（自动分块 + 并行）
result = lx.extract(
    text_or_documents="https://www.gutenberg.org/files/1513/1513-0.txt",
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-2.5-flash",
    # 高召回率配置（多次 Pass 检查）
    num_extra_passes=2,
)

print(f"共提取 {len(result.extractions)} 个实体")
grounded = [e for e in result.extractions if e.char_interval]
print(f"有源文本定位 {len(grounded)} 个")
```

---

## 批量处理多个文档

```python
import langextract as lx
from pathlib import Path

prompt = "Extract key findings and conclusions from research papers."
examples = [...]

# 批量处理多个文件
doc_paths = list(Path("papers/").glob("*.txt"))
results = []

for doc_path in doc_paths:
    text = doc_path.read_text()
    result = lx.extract(
        text_or_documents=text,
        prompt_description=prompt,
        examples=examples,
        model_id="gemini-2.5-flash",
    )
    results.append(result)
    print(f"处理完成: {doc_path.name}")

# 统一保存
lx.io.save_annotated_documents(
    results,
    output_name="batch_results.jsonl",
    output_dir="."
)

# 生成统一可视化
html = lx.visualize("batch_results.jsonl")
with open("batch_visualization.html", "w") as f:
    f.write(html if isinstance(html, str) else html.data)
```

---

## 使用本地 Ollama 模型（零 API 费用）

适合隐私敏感场景或本地开发：

```bash
# 先安装并启动 Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama serve

# 下载模型（选择一个）
ollama pull llama3.2          # 3.2B，较快
ollama pull mistral           # 7B，较好质量
ollama pull llama3.1:8b       # 8B，推荐质量
```

```python
import langextract as lx

# 使用 Ollama 模型
result = lx.extract(
    text_or_documents=text,
    prompt_description=prompt,
    examples=examples,
    model_id="ollama/llama3.2",  # 前缀 "ollama/" + 模型名
)
```

**注意：** 本地模型的结构化输出能力不如 Gemini，可能需要更多示例才能达到同等效果。

---

## 使用 OpenAI 模型

```python
import langextract as lx
import os

os.environ["OPENAI_API_KEY"] = "your-key"

result = lx.extract(
    text_or_documents=text,
    prompt_description=prompt,
    examples=examples,
    model_id="gpt-4o",         # GPT-4o
    # 或
    # model_id="gpt-4o-mini", # 更快更便宜
)
```

---

## 自定义多个提取类

定义复杂的多类别提取任务：

```python
import langextract as lx

prompt = """Extract the following from radiology reports:
- findings: specific abnormal findings
- anatomy: body parts mentioned
- measurements: numerical measurements with units
- recommendations: follow-up recommendations
Use exact text. Do not overlap entities."""

examples = [
    lx.data.ExampleData(
        text="Chest X-ray shows 2.3cm nodule in right lower lobe. Recommend CT scan follow-up.",
        extractions=[
            lx.data.Extraction(
                extraction_class="finding",
                extraction_text="2.3cm nodule",
                attributes={"severity": "moderate", "requires_follow_up": "true"}
            ),
            lx.data.Extraction(
                extraction_class="anatomy",
                extraction_text="right lower lobe",
                attributes={"organ": "lung"}
            ),
            lx.data.Extraction(
                extraction_class="measurement",
                extraction_text="2.3cm",
                attributes={"unit": "cm", "value": "2.3"}
            ),
            lx.data.Extraction(
                extraction_class="recommendation",
                extraction_text="CT scan follow-up",
                attributes={"urgency": "routine"}
            ),
        ]
    )
]

result = lx.extract(
    text_or_documents="Patient presents with 1.8cm mass in left upper lobe. No lymphadenopathy. Follow-up MRI recommended.",
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-2.5-pro",  # 复杂任务用 Pro
)
```

---

## 分析提取结果

```python
import langextract as lx
from collections import Counter

# 加载已保存结果
docs = lx.io.load_annotated_documents("results.jsonl")

# 统计各类别数量
all_extractions = [e for doc in docs for e in doc.extractions if e.char_interval]
class_counts = Counter(e.extraction_class for e in all_extractions)
print("提取类别分布:", dict(class_counts))

# 提取特定属性
medications = [
    {
        "text": e.extraction_text,
        "dosage": e.attributes.get("dosage", "未知"),
        "position": e.char_interval,
    }
    for doc in docs
    for e in doc.extractions
    if e.extraction_class == "medication" and e.char_interval
]
```

---

## 完成确认检查清单

- [ ] 长文档（>10K 字符）处理成功（自动分块）
- [ ] 批量处理多文档并统一保存 JSONL
- [ ] Ollama 本地模型接入成功（可选）
- [ ] 多提取类别任务输出正确

---

## 相关链接

- [故障排查](../troubleshooting.md)
- [GitHub](https://github.com/google/langextract)
- [示例集合](https://github.com/google/langextract/tree/main/examples)
