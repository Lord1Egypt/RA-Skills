---
name: pdf-ocr-zc
description: 批量 OCR 处理扫描 PDF，自动生成带文字层的 PDF 并可导出为 Markdown/纯文本。使用场景包括老师 Agent 需要将大量扫描教材 PDF 转化为可检索文本。
---

# PDF OCR 处理技能

## 何时使用
- 需要对大量扫描件 PDF 进行文字识别（OCR）
- 希望直接得到可搜索的 PDF（文字层）或提取的纯文本/Markdown
- 需要在老师 Agent 工作流中自动化该步骤

## 基本使用方式
```bash
# 运行一次 OCR（需要已安装 Tesseract 与 ocrmypdf）
openclaw exec python skills/pdf-ocr/scripts/ocr_batch.py <input-pdf> <output-pdf>
```
- `<input-pdf>`：原始扫描 PDF 路径
- `<output-pdf>`：输出带文字层的 PDF（同目录或指定路径）

## 高级选项
- 若想一次性处理目录下所有 PDF，使用 `--batch-dir` 参数：
```bash
openclaw exec python skills/pdf-ocr/scripts/ocr_batch.py --batch-dir <pdf-dir>
```
- 可加 `--lang chi_sim` 指定中文简体模型（默认 tesseract 会自动检测语言）

## 脚本说明 (scripts/ocr_batch.py)
- 检测并确保 `ocrmypdf` 可用；如未安装会提示安装指令
- 使用 `ocrmypdf` 完成 OCR，内部调用已装好的 Tesseract
- 支持批量目录模式，遍历 `*.pdf` 并生成对应带文字层文件
- 错误会记录到 `logs/pdf_ocr_error.log`，便于排查

## 参考资源
- `references/ocr_tips.md`：常见 OCR 参数调优技巧（如 DPI、图片预处理）
- `references/install_ocr.md`：在 Windows 上安装 Tesseract 与 ocrmypdf 的详细步骤

## 与老师 Agent 的集成
在老师 Agent 的工作流（如 `auto_ingest`）中，可在 `HEARTBEAT.md` 或 cron 中加入如下调用，以实现每日自动 OCR：
```bash
openclaw exec python skills/pdf-ocr/scripts/ocr_batch.py --batch-dir /path/to/teacher-pdfs
```
这样老师 Agent 在 ingest 前就已拥有文字层，后续向量化、检索都能顺畅进行。

---

# 使用示例
1. 单文件 OCR：
```bash
openclaw exec python skills/pdf-ocr/scripts/ocr_batch.py D:\docs\scan1.pdf D:\docs\scan1_text.pdf
```
2. 批量目录 OCR：
```bash
openclaw exec python skills/pdf-ocr/scripts/ocr_batch.py --batch-dir D:\teacher-pdfs
```

如需更细粒度的文本（Markdown），可在脚本后接 `pdf2txt.py` 转换。

---

**注意**：此技能仅在本机执行，不会触发外部网络请求，符合安全策略。
