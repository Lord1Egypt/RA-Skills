# 简历导入工作流

当用户提供简历文件，并要求让 AI 可读、提取候选人信息或准备招聘记录时，使用此参考说明。

## 目录

- 目标
- 输入
- 流程
- 解析器策略
- 质量门槛
- 隐私
- 预期回复

## 目标

将简历文件转换为适合下游招聘工作流使用的本地简历包：

```text
resume_bundle/
├── original.<ext>
├── resume.md
├── resume.raw.json
├── candidate_draft.json
├── extraction_report.json
└── manifest.json
```

## 输入

- PDF 简历
- DOCX 简历
- TXT 或 Markdown 简历

Docling 可以支持更多格式，但除非 `scripts/dependency_check.py --workflow resume-ingest` 和 `scripts/resume_extract.py` 都成功，否则不要假设未列出的格式可用。

## 流程

1. 运行依赖检查：

   ```bash
   python3 {baseDir}/scripts/dependency_check.py --workflow resume-ingest
   ```

   如果要用真实简历验证当前环境的解析能力，运行：

   ```bash
   python3 {baseDir}/scripts/dependency_check.py --workflow resume-ingest --probe-file "/path/to/resume.pdf"
   ```

2. 将简历转换为简历包：

   ```bash
   python3 {baseDir}/scripts/resume_extract.py "/path/to/resume.pdf" --out-dir "/path/to/output-bundle"
   ```

   默认 `auto` 策略只使用本地安全解析器，不主动触发外部模型下载。需要 Docling 高保真解析时，显式运行：

   ```bash
   python3 {baseDir}/scripts/resume_extract.py "/path/to/resume.pdf" --parser docling --out-dir "/path/to/output-bundle"
   ```

   需要在 `auto` 策略中优先尝试 Docling，并接受模型下载时，才使用 `--allow-model-downloads`。

3. 读取 `extraction_report.json`。

4. 如果 `status` 为 `failed`，停止并报告解析器错误。

5. 如果 `quality` 为 `fallback`，告知 HR 在写入候选人数据库前应先审核结果。

6. 将 `resume.md` 作为模型推理的主要来源。

7. 仅将 `candidate_draft.json` 用作提示。它基于正则表达式，且有意保持不完整。

8. 如果用户要求结构化候选人字段，使用 `assets/templates/prompts/resume_extract_prompt.md` 作为提取契约。

## 解析器策略

默认解析器顺序：

- PDF：pypdf 或 PyPDF2、PyMuPDF、pdftotext
- DOCX：python-docx
- TXT/Markdown：纯文本读取器

高保真增强解析器：

- Docling Python 包或 Docling CLI；仅在显式指定 `--parser docling`，或允许模型下载的场景下使用。

回退解析器：

- PyMuPDF
- pypdf 或 PyPDF2
- pdftotext
- python-docx
- 纯文本读取器

回退输出可用于阅读和草稿提取。未经 HR 审核，不要将基于回退输出得到的记录写入最终招聘系统。

注意：Docling 能启动不代表真实 PDF 转换可用。标准 PDF 管线可能需要本地已缓存的版面模型、OCR 模型或联网下载权限。

## 质量门槛

遇到以下情况时，停止并要求提供更好的输入文件：

- `resume.md` 为空。
- 大多数页面没有可读文本。
- `extraction_report.json` 显示 `status: failed`。
- 用户要求 OCR，但 Docling 不可用，或模型未缓存且不允许下载。

遇到以下情况时，可以继续，但需要附带审核警告：

- 解析器不是 Docling。
- 简历是扫描版 PDF。
- 表格或时间线看起来损坏。
- 联系方式字段缺失或不明确。

`extraction_report.json` 必须包含：

- `parser_attempts`
- `text_stats`
- `review_required`
- `review_reasons`
- `missing_or_ambiguous_fields`

## 隐私

将每个生成的简历包都视为机密招聘数据。除非 HR 明确要求且环境允许，否则不要在聊天中粘贴完整电话号码、邮箱或原始简历文本。

## 预期回复

成功提取后，回复以下内容：

- 简历包目录
- 使用的解析器
- 质量等级
- 生成的文件
- 缺失或不明确的字段
- 是否需要 HR 审核
- HR 审核原因
