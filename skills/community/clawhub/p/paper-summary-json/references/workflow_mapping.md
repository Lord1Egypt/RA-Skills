# Dify Scheme A to OpenClaw Skill mapping

## Original Dify intent

The uploaded workflow is named `论文分析系统_方案A_结构化证据增强版`. It analyzes one or more uploaded papers and/or paper PDF URLs, extracts structured paper information, performs evidence-focused consistency verification, and exports a Markdown-to-DOCX report.

## Node mapping

| Dify node | Skill implementation |
|---|---|
| `if_empty` + `empty_error` | `prepare_papers.py` exits with `上传的文件和论文URL不能同时为空。` when no inputs are provided. |
| `split_urls` | `prepare_papers.py --urls` accepts repeated values or comma-separated URL lists. |
| `http_download` | `prepare_papers.py` downloads URLs to the batch `downloads/` directory under the Desktop output root. |
| `upload_doc_extract` / `download_doc_extract` | `prepare_papers.py` extracts text from copied local files or downloaded files. |
| `upload_clean` / `download_clean` | `prepare_papers.py` applies the same whitespace normalization and reference/bibliography trimming pattern. |
| `upload_sections` / `download_sections` | `prepare_papers.py` implements the same abstract, intro, method, experiment, conclusion, and `paper_body` section split. |
| `upload_structured` / `download_structured` | The Agent must send `prompts/01_structured_extraction_prompt.md` to the model and save JSON-only output to `generated/structured_result.json`. |
| `upload_verify` / `download_verify` | The Agent must send `prompts/02_verification_prompt_template.md` with actual structured JSON inserted and save JSON-only output to `generated/verification_result.json`. |
| `upload_render` / `download_render` | `render_report.py` aggregates structured and verification JSON into a final report. |
| `upload_docx` / `download_docx` | `render_report.py` writes `.docx`; it also writes `.md` and rendered `.html` for easier Markdown preview. |

## Output directory convention

Default runtime path:

```text
~/Desktop/paper_analysis_results/<YYYYMMDD_HHMMSS>/
```

Per-paper files are placed under:

```text
paper_XX_<filename>/
├── input/
├── text/raw_text.txt
├── text/cleaned_text.txt
├── sections/sections.json
├── prompts/01_structured_extraction_prompt.md
├── prompts/02_verification_prompt_template.md
├── generated/structured_result.json
├── generated/verification_result.json
└── report/
    ├── final_report.md
    ├── final_report.html
    └── final_report.docx
```
