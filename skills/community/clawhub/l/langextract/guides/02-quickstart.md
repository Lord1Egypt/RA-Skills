# 快速开始

## 适用场景

- 从文本中提取自定义结构化信息
- 编写高质量的 Few-shot 示例
- 过滤结果并生成可视化报告

---

## 核心概念

LangExtract 的工作流程：

1. **定义提取规则**：用自然语言描述要提取什么（`prompt_description`）
2. **提供示例**：给出 1-3 个高质量示例（`examples`），驱动模型行为
3. **运行提取**：调用 `lx.extract()`，模型返回结构化提取结果
4. **过滤定位结果**：只保留有源文本定位的结果（`char_interval != None`）
5. **可视化审查**：生成 HTML 文件，在原文中高亮显示提取结果

---

## 基础提取：角色与情感

```python
import langextract as lx
import textwrap

# 1. 定义提取规则
prompt = textwrap.dedent("""\
    Extract characters, emotions, and relationships in order of appearance.
    Use exact text for extractions. Do not paraphrase or overlap entities.
    Provide meaningful attributes for each entity to add context.""")

# 2. 提供示例（示例中的 extraction_text 必须逐字出现在示例文本中）
examples = [
    lx.data.ExampleData(
        text="ROMEO. But soft! What light through yonder window breaks? Juliet is the sun.",
        extractions=[
            lx.data.Extraction(
                extraction_class="character",
                extraction_text="ROMEO",
                attributes={"emotional_state": "wonder"}
            ),
            lx.data.Extraction(
                extraction_class="emotion",
                extraction_text="But soft!",
                attributes={"feeling": "gentle awe"}
            ),
        ]
    )
]

# 3. 运行提取
input_text = "Lady Juliet gazed longingly at the stars, her heart aching for Romeo"
result = lx.extract(
    text_or_documents=input_text,
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-2.5-flash",
)

# 4. 只保留有源文本定位的结果（过滤掉 LLM 幻觉）
grounded = [e for e in result.extractions if e.char_interval]
print(f"定位到 {len(grounded)} 个实体（共 {len(result.extractions)} 个）")
for e in grounded:
    print(f"  [{e.extraction_class}] '{e.extraction_text}' at {e.char_interval}")
```

---

## 医疗文本提取

```python
import langextract as lx

prompt = """Extract medications, dosages, and conditions from clinical notes.
Use exact text. Do not overlap entities. Extract in order of appearance."""

examples = [
    lx.data.ExampleData(
        text="Patient was prescribed metformin 500mg twice daily for type 2 diabetes.",
        extractions=[
            lx.data.Extraction(
                extraction_class="medication",
                extraction_text="metformin 500mg",
                attributes={"dosage": "500mg", "frequency": "twice daily"}
            ),
            lx.data.Extraction(
                extraction_class="condition",
                extraction_text="type 2 diabetes",
                attributes={"type": "chronic"}
            ),
        ]
    )
]

clinical_note = """
John, 54M, presents with uncontrolled hypertension.
BP 160/95. Started on lisinopril 10mg daily.
Also noted: elevated HbA1c at 8.2%, considering metformin 500mg.
"""

result = lx.extract(
    text_or_documents=clinical_note,
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-2.5-flash",
)

for e in result.extractions:
    if e.char_interval:
        print(f"{e.extraction_class}: {e.extraction_text}")
        print(f"  属性: {e.attributes}")
        print(f"  位置: 字符 {e.char_interval}")
```

---

## 保存结果为 JSONL

```python
# 保存到文件（支持后续可视化和审查）
lx.io.save_annotated_documents(
    [result],
    output_name="extraction_results.jsonl",
    output_dir="."
)

# 加载已保存的结果
loaded = lx.io.load_annotated_documents("extraction_results.jsonl")
print(f"加载了 {len(loaded)} 个文档的提取结果")
```

---

## 生成交互式 HTML 可视化

```python
# 从 JSONL 文件生成可视化
html_content = lx.visualize("extraction_results.jsonl")

# 保存为独立 HTML 文件
with open("visualization.html", "w") as f:
    if hasattr(html_content, 'data'):
        f.write(html_content.data)   # Jupyter/Colab 环境
    else:
        f.write(html_content)         # 普通 Python 环境

print("可视化已保存到 visualization.html")
# 用浏览器打开即可查看交互式高亮界面
```

---

## 处理 URL 文档

LangExtract 可以直接处理在线文档 URL：

```python
result = lx.extract(
    # 直接传入 URL，自动下载和处理
    text_or_documents="https://www.gutenberg.org/files/1513/1513-0.txt",
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-2.5-flash",
    # 大文档自动分块并行处理
)
```

---

## 理解 Prompt 对齐警告

LangExtract 会在以下情况发出警告：

```
⚠️ Prompt alignment warning: extraction_text not found in example text
```

这意味着示例中的 `extraction_text` 未逐字出现在示例的 `text` 中。**最佳实践**：示例的 `extraction_text` 必须是示例 `text` 的精确子字符串，不能改写或概括。

---

## 完成确认检查清单

- [ ] `lx.extract()` 成功返回 `result.extractions` 非空列表
- [ ] 过滤 `char_interval != None` 后保留有效结果
- [ ] JSONL 文件已保存
- [ ] HTML 可视化文件生成，浏览器打开可看到高亮

---

## 下一步

- [高级用法](03-advanced-usage.md) — 长文档处理、Ollama 本地模型、自定义提取类
