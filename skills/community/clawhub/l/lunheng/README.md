# ⚖️ 论衡 (Lunheng) — AI 裁判文书写作助手

> **AI-powered judgment drafting assistant** — Syllogistic reasoning (大前提 → 小前提 → 结论), 74+ cause-of-action templates, law citation validation, and quality scoring.
>
> **AI 裁判文书写作助手** — 三段论逻辑推演，74+ 种案由模板，法条引用核查，质量评分。

---

## 为什么要用论衡？

Writing a judgment requires **rigorous legal reasoning**: identify the right law (大前提), match it to the facts (小前提), and reach a just conclusion (结论). Most AI tools generate fluent text but skip the logic.

**Lunheng is different:**
- **Explicit syllogistic reasoning** — Every phrase is traced back to a legal rule
- **74+ cause-of-action templates** — From civil loan disputes to criminal sentencing
- **Law citation validation** — Automatically flags repealed/outdated laws
- **Quality scoring** — 6-dimension evaluation (reasoning, citation, structure, etc.)
- **Class case retrieval** — Learn from 700+ award-winning judgments

---

## Quick Start / 快速开始

### Prerequisites / 前置要求

```bash
python3 >= 3.10
pip install --break-system-packages rapidfuzz pdfplumber
```

### Setup / 配置

```bash
# 1. Set your LLM API key (any OpenAI-compatible provider)
export LH_LLM_API_KEY="sk-your-key-here"
export LH_LLM_BASE_URL="https://api.deepseek.com"
export LH_LLM_MODEL="deepseek-chat"

# 2. Set optional IMA knowledge base (Chinese users only)
# export LH_IMA_API_KEY="***"
```

### Run / 运行

```bash
# Draft a judgment from case facts
python3 -m scripts pipeline draft \
  --input "原告张三诉被告李四民间借贷纠纷一案，李四向张三借款10万元，约定月利率1%，到期未还。"

# Check law references
python3 -m scripts law-check \
  --input "根据《民法典》第六百六十七条，借款人应按约定期限还款。"

# Search the 形与神 reference corpus
python3 -m scripts shape-spirit cause 民间借贷纠纷 civil
```

### Example / 示例

```python
from scripts.pipeline import run_pipeline

result = run_pipeline(
    case_text="原告张三诉被告李四民间借贷纠纷一案。2023年5月，李四向张三借款10万元...",
    cause="民间借贷纠纷",
)

print(result["formatted"])       # Full judgment text
print(result["law_check"])       # Law citation report
print(result["quality_check"])   # Quality score
```

---

## Features / 功能一览

| Module | Command | Description |
|--------|---------|-------------|
| **Pipeline** | `python3 -m scripts pipeline` | End-to-end draft → review → score |
| **Law Check** | `python3 -m scripts law-check` | 3-layer validation (local + LLM + NPC) |
| **Quality Check** | `python3 -m scripts quality-check` | 6-dimension scoring |
| **Enhanced Parser** | `python3 -m scripts parse` | LLM + Regex hybrid fact extraction |
| **Case Search** | `python3 -m scripts consistency` | IMA + local case retrieval |
| **Fee Calculator** | `python3 -m scripts fee-calc` | Court fee estimation |
| **Reasoning Enhancer** | (via pipeline) | Auto-improve reasoning quality |
| **Sentencing Calc** | (via pipeline) | Criminal sentencing recommendations |

## Architecture / 架构

```
案情输入 → 要素解析 → 多源检索 → 三段论生成 → 质量评分 → 自动增强 → 输出
   │          │           │           │           │          │
parser    retriever    assembler    scorer    enhancer   formatter
```

11 modular `refs/` knowledge files dynamically loaded:

| File | Purpose |
|------|---------|
| `refs/procedural_knowledge.md` | Judge's reasoning process |
| `refs/kb_cases.md` | Reference cases |
| `refs/kb_laws.md` | Legal references |
| `refs/kb_writing.md` | Writing techniques |
| `refs/formatting_standard.md` | Format specs |
| `refs/knowledge_router.md` | Knowledge routing |

## Data / 数据

Data is **not included** in the repository. Download separately:

| Dataset | Size | Source |
|---------|------|--------|
| 形与神 paradigm library | 904 KB | 4 volumes, 146 cases |
| Award-winning judgments | 88 KB | 700+ public judgments |
| PDF chunks (templates) | 182 MB | Element-based templates |
| PDF pages (scans) | 49 MB | Original book scans |

## Configuration / 配置

All settings via environment variables (see `.env.example`):

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LH_LLM_API_KEY` | ✅ | — | LLM API key (OpenAI-compatible) |
| `LH_LLM_BASE_URL` | ❌ | `https://api.openai.com/v1` | API base URL |
| `LH_LLM_MODEL` | ❌ | `gpt-4o-mini` | Model name |
| `LH_IMA_API_KEY` | ❌ | — | IMA knowledge base key |
| `LH_IMA_CLIENT_ID` | ❌ | — | IMA client ID |

## License / 许可证

Apache 2.0 — see [LICENSE](LICENSE).

## Disclaimer / 免责声明

This tool assists in drafting legal documents. **All output must be reviewed by a qualified legal professional.** The authors assume no liability for misuse or incorrect outcomes.

本工具辅助起草法律文书。**所有输出须经合格法律专业人士审阅。** 作者不对误用或不正确结果承担任何责任。
