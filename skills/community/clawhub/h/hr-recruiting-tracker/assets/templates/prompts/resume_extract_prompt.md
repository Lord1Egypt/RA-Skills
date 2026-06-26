# 简历字段提取提示词

在 `scripts/resume_extract.py` 生成简历包之后使用此提示词。

输入文件：
- `resume.md`：模型的主要来源
- `candidate_draft.json`：基于正则表达式的确定性提示
- `extraction_report.json`：解析器、质量和警告信息

任务：
从 `resume.md` 中提取结构化候选人资料。

规则：
- 不要编造候选人事实。
- 缺失字段使用 `null`。
- 对学校、公司、技能、项目和工作年限等重要字段保留原始证据片段。
- 如果提取报告显示 `quality: fallback`，为 HR 添加审核警告。
- 如果简历看起来是扫描件或内容不完整，建议使用 Docling OCR 重新处理。
- PDF 文本层可能把中文词拆成空格。对姓名、学校、专业、公司和项目名称，先恢复明显的中文词空格，例如 `长 沙 学 院` → `长沙学院`、`计 算 机科学与技 术` → `计算机科学与技术`。
- 教育经历必须拆分为独立字段：学校只填学校名，专业只填专业名，学历只填学历，日期只填日期；不要把整段教育经历塞进 `school` 或 `major`。

输出 JSON。此结果用于 HR 审核和补充，不会被 `upload_to_smartsheet.py` 自动写入；候选人入库仍以 `candidate_draft.json` 和 `extraction_report.json` 为确定性输入。

```json
{
  "schema_version": "candidate-review/v0.1",
  "identity": {
    "name": null
  },
  "contact": {
    "phone": null,
    "email": null
  },
  "job_intent": {
    "target_role": null,
    "employment_type": null,
    "availability": null,
    "evidence": null
  },
  "education": [
    {
      "school": null,
      "degree": null,
      "major": null,
      "start_date": null,
      "end_date": null,
      "evidence": null
    }
  ],
  "work_experience": [
    {
      "company": null,
      "title": null,
      "start_date": null,
      "end_date": null,
      "responsibilities": [],
      "evidence": null
    }
  ],
  "projects": [
    {
      "name": null,
      "role": null,
      "description": null,
      "skills": [],
      "evidence": null
    }
  ],
  "skills": [],
  "summary": null,
  "missing_fields": [],
  "ambiguous_fields": [],
  "review_warnings": []
}
```
