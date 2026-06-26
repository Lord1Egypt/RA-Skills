# 故障排查

## 安装问题

---

### 问题 1：安装后 `import langextract` 失败

**难度：** 低

**症状：** `ModuleNotFoundError: No module named 'langextract'`

**解决方案：**
```bash
# 确认在正确的虚拟环境中
which python
pip show langextract

# 重新安装
pip install --upgrade langextract

# 如果使用 conda，确认已激活
conda activate your-env
pip install langextract
```

---

### 问题 2：API 密钥认证失败

**难度：** 低

**症状：** `google.api_core.exceptions.InvalidArgument: API key not valid` 或 `AuthenticationError: 401`

**排查步骤：**
```bash
echo $GOOGLE_API_KEY  # 确认不为空
# 期望输出：AIza... 或类似格式
```

**解决方案：**
```bash
# 重新设置环境变量
export GOOGLE_API_KEY="your-key-here"

# 验证 Gemini API 可访问
python -c "
import google.generativeai as genai
import os
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel('gemini-2.5-flash')
response = model.generate_content('Hello')
print('API 正常:', response.text[:50])
"
```

---

## 使用问题

---

### 问题 3：`extractions` 返回空列表

**难度：** 中

**症状：** `result.extractions` 为 `[]`，或所有提取结果的 `char_interval` 均为 `None`

**常见原因：**
- `examples` 中的 `extraction_text` 不是 `text` 的精确子字符串（概率 50%）
- `prompt_description` 描述不够清晰（概率 30%）
- 输入文本太短（概率 20%）

**解决方案：**
```python
# 诊断：打印所有提取结果（包括未定位的）
for e in result.extractions:
    grounded = "✅" if e.char_interval else "❌ 未定位"
    print(f"{grounded} [{e.extraction_class}] '{e.extraction_text}'")

# 检查示例对齐
example = lx.data.ExampleData(
    text="Patient took ibuprofen 400mg.",
    extractions=[
        lx.data.Extraction(
            extraction_class="medication",
            # ✅ 正确：逐字出现在 text 中
            extraction_text="ibuprofen 400mg",
            # ❌ 错误：这是改写，不在原文中
            # extraction_text="ibuprofen medication 400mg dose",
            attributes={}
        )
    ]
)
```

---

### 问题 4：Prompt 对齐警告（`Prompt alignment warning`）

**难度：** 低

**症状：** 控制台打印 `⚠️ Prompt alignment warning: extraction_text not found in example text`

**说明：** 这不是错误，而是提示示例质量不佳。`extraction_text` 必须是示例 `text` 的精确子字符串。

**解决方案：**
```python
# 错误示例（改写/概括）
lx.data.Extraction(
    extraction_class="emotion",
    extraction_text="grief and sorrow",    # ❌ 这是改写
    # 而原文是 "deep sadness"
)

# 正确示例（精确原文）
lx.data.Extraction(
    extraction_class="emotion",
    extraction_text="deep sadness",        # ✅ 逐字出现在原文中
)
```

---

### 问题 5：提取召回率低（漏掉了很多实体）

**难度：** 中

**症状：** 明显的实体没有被提取到

**解决方案：**
```python
# 增加多次 Pass（提高召回率，但增加 API 成本）
result = lx.extract(
    text_or_documents=text,
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-2.5-flash",
    num_extra_passes=2,  # 额外 2 次检查
)

# 或使用更强的模型
result = lx.extract(
    text_or_documents=text,
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-2.5-pro",  # Pro 比 Flash 召回率更高
)

# 改进 prompt_description，更明确地描述要提取什么
prompt = """Extract ALL medications mentioned, including:
- Drug names with dosages
- Over-the-counter drugs
- Supplements and vitamins
List in order of appearance. Use exact text."""
```

---

### 问题 6：长文档处理超时或 API 限流

**难度：** 中

**症状：** `ResourceExhausted: 429 Too Many Requests` 或处理长文档时挂起

**解决方案：**
```python
# 使用更小的分块
result = lx.extract(
    text_or_documents=long_text,
    prompt_description=prompt,
    examples=examples,
    model_id="gemini-2.5-flash",
    chunk_size=2000,          # 减小分块大小（字符）
    chunk_overlap=200,         # 分块重叠，避免边界漏提
)
```

对于 Tier 1 免费 API，建议升级到 Tier 2 配额或在请求间加入延迟：
- 免费配额：15 RPM（每分钟请求数）
- Tier 2：根据项目配额，通常 1000+ RPM

---

## 网络/环境问题

---

### 问题 7：Ollama 模型返回结构错误

**难度：** 中

**症状：** 使用 Ollama 时提取结果 schema 不正确，或返回纯文本

**解决方案：**
```python
# Ollama 对结构化输出支持较弱，建议：
# 1. 使用更大的本地模型
result = lx.extract(
    model_id="ollama/llama3.1:8b",   # 8B 比 3.2B 更好
)

# 2. 提供更多示例（3-5 个，而不是 1 个）
examples = [
    example1,   # 多个不同的示例帮助本地模型理解 schema
    example2,
    example3,
]

# 3. 最终建议：对精度要求高的场景，优先使用 Gemini
```

---

### 问题 8：可视化 HTML 文件无法显示高亮

**难度：** 低

**症状：** 生成的 `visualization.html` 打开后没有高亮，或显示空白

**排查：**
```python
# 确认 JSONL 文件非空
import json
with open("results.jsonl") as f:
    lines = f.readlines()
print(f"文档数量: {len(lines)}")

# 确认有 grounded 的提取结果
docs = lx.io.load_annotated_documents("results.jsonl")
grounded_count = sum(
    1 for doc in docs
    for e in doc.extractions
    if e.char_interval
)
print(f"有定位的提取数量: {grounded_count}")
```

如果 `grounded_count == 0`，需要先解决提取定位问题（见问题 3）。

---

## 通用诊断

```python
import langextract as lx
import os

# 快速诊断
print("langextract 版本:", lx.__version__)
print("GOOGLE_API_KEY 已设置:", bool(os.getenv("GOOGLE_API_KEY")))

# 最小可运行示例
result = lx.extract(
    text_or_documents="Romeo loves Juliet.",
    prompt_description="Extract characters and relationships.",
    examples=[
        lx.data.ExampleData(
            text="Alice likes Bob.",
            extractions=[
                lx.data.Extraction(
                    extraction_class="character",
                    extraction_text="Alice",
                    attributes={}
                )
            ]
        )
    ],
    model_id="gemini-2.5-flash",
)
grounded = [e for e in result.extractions if e.char_interval]
print(f"提取成功: {len(grounded)} 个有定位实体")
```

**GitHub Issues：** https://github.com/google/langextract/issues
