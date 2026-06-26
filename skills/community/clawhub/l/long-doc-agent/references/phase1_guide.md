# Phase 1: Planner Full Prompt Template

## Execution Steps

1. Load `F:/agent/chapters/reference_material.txt` summary (first 3000 characters) as `reference_summary`
2. Replace `{xxx}` placeholders in the template below with actual values
3. Write output to `F:/agent/chapters/plan.json`

## Prompt Template

```
You are a professional project planner. The user needs to write a 【{doc_type}】 on the topic of "{topic}".

## User-Provided Background Information
{background}

## Reference Material Summary (Priority Reference)
{reference_summary}

Please complete the following tasks:
1. Create a detailed document outline (down to H3 headings)
2. Annotate core writing points for each chapter
3. Identify RAG search keywords for each chapter (≤3 per chapter)
4. Evaluate complexity of each chapter, mark key chapters
5. Identify chapter dependencies (which chapters must be completed before others can be written)

**Chapter Dependency Rules**:
- Type 1 (no dependencies, write first): Overview, Background, Current Analysis, Technology Selection
- Type 2 (depends on Type 1): Overall Design, Detailed Function Design
- Type 3 (depends on several preceding chapters): Implementation Plan, Testing Plan, Deployment Plan
- Type 4 (can write independently or last): Training Plan, Acceptance Plan, Appendices, Conclusion

**Reference Materials Prohibition**
Actively exclude content unrelated to the topic during planning (e.g., infusion monitoring systems, etc.).

Write the following structured information to F:/agent/chapters/plan.json:
{
  "project_name": "Project Name",
  "doc_type": "Document Type",
  "chapters": [
    {
      "seq": "01",
      "title": "Chapter Title",
      "brief": "Writing Points",
      "feishu_keywords": ["k1", "k2"],
      "web_keywords": ["k1", "k2"],
      "word_count": 3000,
      "batch": "A",
      "dependencies": [],
      "status": "pending"
    }
  ]
}
```

## plan.json Field Descriptions

| Field | Description |
|-------|-------------|
| `seq` | Chapter sequence number, 2-digit string ("01", "02") |
| `title` | Chapter title |
| `brief` | Core writing points (50-100 characters) |
| `feishu_keywords` | Feishu knowledge base search keywords, max 3 |
| `web_keywords` | Web search keywords, max 3 |
| `word_count` | Target word count (body text, excluding headings) |
| `batch` | Batch label ("A"/"B"/"C", same batch can be written in parallel) |
| `dependencies` | Dependent chapter seq list, e.g. `["01", "02"]` |
| `status` | Status: `pending`/`writing`/`txt_done`/`confirmed` |

## Post-Execution Actions

```bash
# 1. Generate initial glossary (extracted from reference materials)
python integrate_report.py glossary

# 2. Save outline snapshot
python integrate_report.py save-outline

# 3. Display outline to user for confirmation
```
