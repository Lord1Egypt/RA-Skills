# pdf2md-universal：PDF 转 Markdown 通用转换器

把任意 PDF 变成 AI 友好的 Markdown，省 3 到 10 倍的 token，成本省 10 到 30 倍。

直接发 PDF 给多模态 AI 读，每一页都要当图片识别，一张高清页就要一千多 token。几百页的研报就是几十万 token，价格是文本的好几倍。先转成 Markdown，同样的内容只剩文本 token，又快又便宜。

## 适合谁用

- 常把研报、财报、论文、电子书丢给 ChatGPT / Claude 分析的人
- 被"上传 300 页 PDF 结果对话飞快烧 token"吓到过的 AI 重度用户
- 要把 PDF 转成 Markdown 存档、建知识库、喂 RAG 管线的开发者

## 快速开始

```bash
# 安装依赖（任一 python3 环境即可）
pip install pdfplumber pypdfium2 pillow
# macOS 系统需装 poppler 提供 pdftotext：brew install poppler

# 转换一个 PDF
python3 scripts/pdf2md.py 研报.pdf

# 先算账，不转换：看能省多少 token
python3 scripts/pdf2md.py 研报.pdf --token-estimate

# 扫描版 PDF 强制 OCR（可选，需要配置视觉模型 adapter）
python3 scripts/pdf2md.py 扫描件.pdf --ocr force --bailian-adapter /path/to/adapter.py
```

转换完会打印一份对比报告：直接读 PDF 要多少 token，转成 Markdown 要多少，省了多少倍。

## 文件说明

| 文件 | 作用 |
|------|------|
| `scripts/pdf2md.py` | 核心转换脚本，三层策略全在里面 |
| `SKILL.md` | 给 AI 用的技能说明，Agent 可以直接调用这个流程 |
| `references/` | 详细文档（可选） |

## 三层转换策略

1. **文本型 PDF**：pdftotext 免费抽取，pdfplumber 还原标题层级，零成本。
2. **扫描型 PDF**：自动检测（每页字符不足 300 判为扫描件），渲染成图后走 OCR 兜底。
3. **估算模式**：`--token-estimate` 只算账不转换，先看省多少再决定。

扫描型 OCR 默认找 `BAILIAN_ADAPTER` 环境变量或 `--bailian-adapter` 指定的 adapter，也可以用 tesseract 替代。

## 推荐流程

1. 拿到 PDF 先跑 `--token-estimate`，给用户看 token 对比
2. 文本型直接转，扫描型自动 OCR
3. 输出对比报告 + 生成的 .md 文件
4. 把 .md 喂给 AI 或存档，享受省 token 的快感

---

# pdf2md-universal: PDF → Markdown universal converter

Turn any PDF into AI-friendly Markdown. Save 3-10x on tokens, 10-30x on cost.

Feeding a PDF directly to a multimodal AI treats every page as an image — a high-res page can cost 1,000+ tokens. A 300-page report becomes hundreds of thousands of tokens. Converting to Markdown first keeps only text tokens: faster and far cheaper.

## Who it's for

- Anyone who regularly feeds reports, financial statements, papers, or ebooks into ChatGPT / Claude
- Heavy AI users burned by the "uploaded a 300-page PDF, blew through my token budget" experience
- Developers archiving PDFs as Markdown, building knowledge bases, or feeding RAG pipelines

## Quick start

```bash
# Install deps (any python3 works)
pip install pdfplumber pypdfium2 pillow
# macOS needs poppler for pdftotext: brew install poppler

# Convert a PDF
python3 scripts/pdf2md.py report.pdf

# Estimate first, don't convert: see the token savings
python3 scripts/pdf2md.py report.pdf --token-estimate

# Force OCR on a scanned PDF (optional, needs a vision-model adapter)
python3 scripts/pdf2md.py scanned.pdf --ocr force --bailian-adapter /path/to/adapter.py
```

After conversion it prints a comparison report: tokens to read the PDF directly vs. as Markdown, and the savings multiple.

## Files

| File | Purpose |
|------|---------|
| `scripts/pdf2md.py` | Core converter, all three strategies inside |
| `SKILL.md` | Agent-facing skill spec — an AI can call this workflow directly |
| `references/` | Optional detailed docs |

## Three-layer strategy

1. **Text-based PDF**: free extraction via pdftotext, heading levels restored with pdfplumber — zero cost.
2. **Scanned PDF**: auto-detected (page with fewer than 300 chars), rendered to images and run through OCR as fallback.
3. **Estimate mode**: `--token-estimate` shows the cost comparison without converting.

Scanned-PDF OCR looks for the `BAILIAN_ADAPTER` env var or a `--bailian-adapter` path, with tesseract as an alternative.

## Recommended workflow

1. Run `--token-estimate` first so users see the token comparison
2. Convert text-based PDFs directly; scanned ones auto-OCR
3. Output the comparison report + the generated .md file
4. Feed the .md to an AI or archive it — enjoy the savings
