# INSTRUCTIONS

## Input Data
Papers are saved in `data/weekly_papers.json` (aggregated from Mon–Fri daily logs).

## Analysis Requirements
- Group papers by research theme or technical approach.
- Identify complementary, contrasting, and extending relationships across papers.
- Extract shared themes or trends from all papers' motivation + core_innovation.
- Do NOT fabricate details. Only use content from the papers.

## Output Steps
1. Create Feishu wiki doc at feishu_root using `feishu-create-doc` skill.
   Title: `📊 Research Weekly {{year}}-W{{week_num}}`
2. Fill the document using the template below.

---

# 科研周报 | {{year}}-W{{week_num}}

<callout emoji="📊" background-color="light-blue">
**周期**：{{start_date}} 至 {{end_date}} | 研究方向：{{research_direction}}
</callout>

---

## 本周期概览

| 统计项 | 数值 |
|--------|------|
| 📅 覆盖天数 | {{days_covered}} 天 |
| 📚 论文总数 | {{total_papers}} 篇 |
| 📈 日均论文 | {{daily_avg}} 篇 |

---

{% if daily_stats %}
### 各日论文分布

| 日期 | 论文数 |
|------|--------|
{% for day in daily_stats %}
| {{ day.date }} | {{ day.count }} |
{% endfor %}
{% endif %}

---

## 本周期论文

{% for paper in all_papers %}

### {{ forloop.counter }}. {{ paper.title }}

<callout emoji="⭐" background-color="light-green">
**相关性：{{paper.relevance_score}}/10**
</callout>

| 字段 | 内容 |
|------|------|
| **日期** | {{ paper.posted_date }} |
| **作者** | {{ paper.authors }} |
| **链接** | [arXiv]({{ paper.arxiv_url }}) |

**研究动机**：{{ paper.motivation }}

**核心创新**：{{ paper.core_innovation }}

---
{% endfor %}

## 跨论文横向比较

### 研究方向关联
> 本周期论文中，哪些在解决相似问题？哪些采用了相似的技术路线？

{{ cross_paper_analysis }}

### 共同主题
> 从所有论文的摘要和核心创新中，提炼出的共同主题或趋势。

{{ shared_themes }}

---

<callout emoji="📌" background-color="pale-gray">
**数据来源**：本周每日日报归档

*本报告由 AI 自动生成，分析基于论文摘要和每日日报，未补充额外信息。*
</callout>
