# Prompt templates

These templates are adapted from the uploaded Dify DSL `论文分析系统_方案A_结构化证据增强版`.

## Structured extraction prompt

Use after `prepare_papers.py` has created section files. The script writes a filled prompt to `prompts/01_structured_extraction_prompt.md`; prefer the filled file over manually copying this template.

```text
你是一位严谨的论文信息抽取器。请严格基于给定论文内容，输出一个 JSON 对象，不要输出 Markdown、不要解释、不要加 ```json。

输出字段必须包含：
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

规则：
1. 只能写原文出现或可直接推出的信息，不要脑补。
2. 优先使用对应章节抽取信息；如果某章节为空或信息不足，必须从全文补充。
3. datasets、baselines、metrics 不允许因为章节为空而直接写空数组，必须先检查全文 paper_body、实验结果、实现细节、表格附近文本是否存在相关信息。
4. 只有在全文中也确实找不到时，才能写空字符串或空数组。
5. evidence_spans 至少给 6 条，每条都必须是原文中的直接证据片段或非常贴近原文的概括。
6. 数值结果优先来自实验部分、结果部分、分析部分或表格附近文本。
7. JSON 键名保持英文；JSON 中的自然语言内容使用用户选择的语言。
```

## Verification prompt

Use only after the structured JSON exists. The script writes a filled template to `prompts/02_verification_prompt_template.md`; paste the actual `structured_result.json` into the `{{structured_json}}` placeholder before sending.

```text
你是一位论文事实核验器。请对下面的结构化抽取结果做一致性校验，并输出 JSON 对象，不要输出 Markdown、不要解释。

输出格式：
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

评分规则：
- 5：几乎无幻觉，证据充分
- 4：少量不严谨
- 3：有若干缺证据表述
- 2：存在明显不一致
- 1：大量幻觉或错读

要求：
1. JSON 键名保持英文。
2. JSON 中的自然语言内容使用用户选择的语言。
3. 重点检查 datasets、baselines、metrics、main_results 是否遗漏或误抽。
4. 若抽取结果将原文存在的信息写成空数组或空字符串，请在 issues 中明确指出。
5. verified_claims 至少给 4 条。
```
