---
name: pdf2md-universal
description: 通用 PDF→Markdown 转换器。当用户需要把 PDF（研报/财报/招股书/论文/电子书/扫描件）转成 Markdown 再阅读或喂给 AI、或担心直接把 PDF 发给 AI 会消耗大量 token 时使用。三层策略：文本型 PDF 用 pdftotext 免费抽取、扫描型 PDF 自动 OCR 兜底、转换后输出 token 对比报告。Triggers: PDF转Markdown, 把PDF转成md, PDF怎么省token, 扫描版PDF提取文字, convert PDF to markdown, pdf 转 md, PDF转文档.
agent_created: true
---

# PDF → Markdown 通用转换器

## Purpose

把任意 PDF 转成结构化 Markdown，核心卖点是**省 token**：直接发 PDF 给多模态 AI 读，
每页要按图像识别（约 1000+ token/页），几百页就是几十万 token；先转成 Markdown，
同样的内容只需文本 token（通常省 3-10 倍，成本省 10-30 倍）。

## When to Use

- 用户想读一个 PDF 但不想直接喂给 AI（担心 token / 成本）
- 用户要把 PDF 转成 Markdown 存档或入知识库
- 用户说"PDF 太费 token / 转成 md 会不会更省"
- 扫描版 PDF（拍照/扫描件）需要提取文字

## 依赖检查

- `pdftotext`（poppler，文本抽取，macOS: brew install poppler）
- Python 包：pdfplumber（标题还原）、pypdfium2 + Pillow（扫描件渲染）
- 扫描件 OCR 可选：百炼 CLI adapter（`BAILIAN_ADAPTER` 环境变量或 `--bailian-adapter` 指定）或 tesseract

## 核心脚本

```bash
python3 scripts/pdf2md.py INPUT.pdf [--output out.md] [--mode full|summary] [--ocr auto|force|none]
python3 scripts/pdf2md.py INPUT.pdf --token-estimate   # 只估算不转换
```

## 三层转换策略

### L1 文本型 PDF（默认，零成本）

`pdftotext -layout` 抽取文本 + pdfplumber 检测标题层级（按字号分级 H1/H2/H3），
输出结构化 Markdown。适合：研报、财报、招股书、论文、电子书。

### L2 扫描型 PDF（自动 OCR 兜底）

检测到每页有效字符不足 300（文本型特征消失）→ 自动判为扫描件，
用 pypdfium2 渲染成图 → OCR（百炼 qwen3-vl-plus 或 tesseract）转 Markdown。

OCR 不可用时降级提示，不会硬跑。

### L3 Token 预估模式（不转换只算账）

`--token-estimate` 只输出对比报告，让用户先看到"转完能省多少"，再决定转不转。

## 输出报告（每次转换都会打印）

```
══════════ PDF→Markdown 转换报告 ══════════
直接读 PDF (多模态): ~436,274 token
转 Markdown 后读取: ~128,824 token
节省: 3.4x   (token), 成本通常省 10-30x
```

**把这个报告原样转达给用户**——它是这个 skill 的价值证明。

## 参数说明

| 参数 | 默认 | 说明 |
|------|------|------|
| `--mode` | `full` | `full`=全量转换；`summary`=只保留高密度内容（待扩展） |
| `--ocr` | `auto` | `auto`=扫描型自动OCR；`force`=强制OCR；`none`=禁用OCR |
| `--output` | 同目录同名.md | 输出路径 |
| `--bailian-adapter` | 环境变量 | 百炼 adapter 路径（覆盖默认查找） |

## 使用流程

1. 确认输入 PDF 路径存在
2. 运行转换（或先跑 `--token-estimate` 给用户看成本对比）
3. 输出 token 报告 + 指向生成的 .md 文件
4. 用文件展示工具把 .md 呈现给用户
5. 如输出有扫描型降级警告，告知用户 OCR 不可用的原因

## 已知限制

- 标题检测基于字号启发式，复杂版式（多栏、图注）可能漏判或误判少量标题
- OCR 只处理前 50 页（`pages_limit`），超长扫描件需分批
- 表格还原依赖 pdftotext 排版，复杂表格可能不完美
- `summary` 模式目前等同 full，待实现
