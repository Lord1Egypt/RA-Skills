---
name: paper-analysis-evidence
description: structured academic paper analysis from local paper files or paper urls, adapted from a dify scheme a workflow. use when the user asks to analyze pdf/docx/text/html academic papers, extract title/task/background/problem/method/datasets/baselines/metrics/results/ablations/limitations/contributions, cite evidence spans, verify consistency against the original paper, or export paper analysis reports. supports chinese or english outputs and saves downloaded inputs, intermediate files, generated json, markdown, html, and docx reports under the ubuntu desktop.
---

# Paper Analysis Evidence

## Purpose

Run the Scheme A evidence-enhanced paper analysis workflow: prepare paper inputs, split the paper into key sections, generate structured extraction JSON, verify the extraction against the original text, and render final reports.

This skill is based on the uploaded Dify workflow `论文分析系统_方案A_结构化证据增强版`.

## Runtime file policy

Always save runtime downloads and generated outputs under the Ubuntu desktop unless the user explicitly requests another location:

```bash
~/Desktop/paper_analysis_results/<YYYYMMDD_HHMMSS>/
```

Do not modify the original local paper file. Copy it into the work directory before extraction. Download URL inputs into the same batch work directory.

## Inputs

Accept:

- `language`: `中文` or `英文`; default to `中文` when unspecified.
- `paper_files`: one or more local paper files, preferably PDF, DOCX, TXT, MD, or HTML.
- `paper_urls`: one or more PDF/direct paper URLs, comma-separated or repeated.

If both local files and URLs are empty, stop with this message:

```text
上传的文件和论文URL不能同时为空。
```

## Workflow

### 1. Prepare inputs and sections

Run:

```bash
python scripts/prepare_papers.py --language 中文 --files /path/to/paper.pdf --urls "https://example.com/paper.pdf"
```

Use only the relevant arguments. For URL-only runs, omit `--files`; for local-only runs, omit `--urls`.

The script creates `manifest.json` and one work directory per paper. It performs:

1. local file copy or URL download,
2. raw text extraction,
3. text cleaning,
4. section splitting into abstract, intro, method, experiment, conclusion, and `paper_body`,
5. prompt file generation.

### 2. Generate structured extraction JSON

For each paper in `manifest.json`, read:

```text
prompts/01_structured_extraction_prompt.md
```

Send that prompt to the model. Save the model response exactly as JSON-only content to:

```text
generated/structured_result.json
```

Required JSON fields:

```json
{
  "title": "",
  "task": "",
  "background": "",
  "problem_statement": "",
  "method_name": "",
  "method_core": "",
  "datasets": [],
  "baselines": [],
  "metrics": [],
  "main_results": [
    {"dataset": "", "metric": "", "value": "", "baseline": "", "improvement": ""}
  ],
  "ablations": [],
  "limitations": [],
  "claims": [],
  "contributions": [],
  "evidence_spans": [
    {"field": "", "claim": "", "evidence": ""}
  ]
}
```

Extraction rules:

- Only use information present in, or directly inferable from, the paper.
- Prefer corresponding sections, but fall back to the full `paper_body` when a section is empty or insufficient.
- Do not leave `datasets`, `baselines`, or `metrics` empty just because the experiment section is weak; first check `paper_body`, result text, implementation details, and table-neighboring text.
- Use empty strings or arrays only when the full paper text truly lacks the information.
- Provide at least 6 evidence spans. Each evidence span must be a direct quote or a very close paraphrase from the source text.
- Prioritize numeric results from experiment, results, analysis, implementation details, or table-neighboring text.
- Keep JSON keys in English. Natural-language values must use the selected output language.

### 3. Run consistency verification

Open:

```text
prompts/02_verification_prompt_template.md
```

Replace `{{structured_json}}` with the actual content of `generated/structured_result.json`. Send the complete verification prompt to the model and save JSON-only output to:

```text
generated/verification_result.json
```

Required verification JSON:

```json
{
  "overall_score": 0,
  "hallucination_risk": "low/medium/high",
  "issues": [
    {"field": "", "problem": "", "severity": "low/medium/high"}
  ],
  "verified_claims": [
    {"claim": "", "status": "supported/weak/unsupported", "evidence": ""}
  ],
  "final_verdict": ""
}
```

Verification rules:

- Score 5: nearly no hallucination, strong evidence.
- Score 4: minor imprecision.
- Score 3: several claims lack evidence.
- Score 2: clear inconsistency exists.
- Score 1: substantial hallucination or misreading.
- Focus on omitted or incorrect datasets, baselines, metrics, and main results.
- If the structured extraction uses an empty array/string for information that exists in the original paper, explicitly list that in `issues`.
- Provide at least 4 verified claims.

### 4. Render reports

After `structured_result.json` and `verification_result.json` are saved for every paper, run:

```bash
python scripts/render_report.py --manifest ~/Desktop/paper_analysis_results/<YYYYMMDD_HHMMSS>/manifest.json
```

Outputs per paper:

```text
report/final_report.md
report/final_report.html
report/final_report.docx
```

The `.md` file preserves editable Markdown source. The `.html` file is the rendered visual version. The `.docx` file is the Word-compatible report.

## Report structure

Chinese report sections:

1. 论文题目
2. 任务与问题
3. 方法概述
4. 实验要素：数据集、基线方法、评价指标
5. 主要结果
6. 贡献提炼
7. 消融与局限性
8. 证据片段
9. 一致性校验：总评分、幻觉风险、最终结论、已核验结论、发现的问题

English report sections mirror the same structure as `Paper Analysis`.

## References

- Use `references/prompt_templates.md` when prompt details are needed.
- Use `references/workflow_mapping.md` when checking how the Dify nodes map to this skill.
- `references/dify_scheme_a_source.yml` preserves the uploaded Dify DSL source for auditability.
