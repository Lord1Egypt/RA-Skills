# INSTRUCTIONS (fill in all fields, do not skip any)

## Research Direction
> {{research_direction}}

## Scoring Criteria
Score each paper 0–10 on relevance to the research direction above:
- 9–10: directly solves a core problem in the direction
- 7–8: highly relevant
- 5–6: tangentially related
- <5: not relevant

## Analysis Requirements (IMPORTANT: write in Chinese)
For each selected paper, extract ONLY from `full_abstract`:
- motivation: 论文解决了什么问题？为什么重要？（2-3句话，用中文）
- core_innovation: 核心贡献是什么？与现有工作有何不同？（2-3句话，用中文）
- Do NOT fabricate details. Only use what is in the abstract.

## Output Steps
1. Write selected papers to `data/selected_papers.json`:
   ```json
   {
     "date": "{{date}}",
     "papers": [
       {
         "paper_id": "2603.12345",
         "title": "...",
         "authors": ["..."],
         "arxiv_url": "https://arxiv.org/abs/2603.12345",
         "pdf_url": "https://arxiv.org/pdf/2603.12345",
         "relevance_score": 9,
         "posted_date": "2026-03-30",
         "full_abstract": "...",
         "motivation": "...",
         "core_innovation": "..."
       }
     ]
   }
   ```
2. Run: `python3 scripts/paper_lark_report.py --save-selected "{{date}}" "data/selected_papers.json"`
3. Run: `python3 scripts/paper_lark_report.py --register-doc "<doc_id>" "<doc_url>" "<title>"`
4. Create Feishu wiki doc at feishu_root using `feishu-create-doc` skill, title: `📰 Research Daily {{date}}`
5. Fill the document content using the template below.

---

# 科研日报 | {{date}}

<callout emoji="📡" background-color="light-blue">
**paper-lark-report** | 研究方向：{{research_direction}}
</callout>

---

## 今日概览

| 统计项 | 数值 |
|--------|------|
| 📅 日期 | {{date}} |
| 📚 候选论文 | {{total_papers}} 篇 |
| ✨ 精选论文 | {{selected_papers}} 篇 |

---

{% for paper in papers %}

## {{ forloop.counter }}. {{ paper.title }}

{% if paper.relevance_score >= 8 %}
<callout emoji="⭐" background-color="light-green">
**相关性：{{paper.relevance_score}}/10** — 高度相关
</callout>
{% elif paper.relevance_score >= 6 %}
<callout emoji="📎" background-color="light-yellow">
**相关性：{{paper.relevance_score}}/10** — 相关
</callout>
{% endif %}

| 字段 | 内容 |
|------|------|
| **arXiv ID** | `{{ paper.paper_id }}` |
| **发布日期** | {{ paper.posted_date }} |
| **作者** | {{ paper.authors }} |
| **链接** | [arXiv]({{ paper.arxiv_url }}) · [PDF]({{ paper.pdf_url }}) |

### 【摘要】
{{ paper.full_abstract }}

### 【研究动机】
{{ paper.motivation }}

### 【核心创新】
{{ paper.core_innovation }}

---
{% endfor %}

<callout emoji="📌" background-color="pale-gray">
**数据来源**：arXiv

*本报告由 AI 自动生成，分析基于论文摘要，未补充额外信息。*
</callout>
