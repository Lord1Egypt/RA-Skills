---
name: news-research-summary
description: Researches news and factual information on the web, then produces a cited, deduplicated summary tailored to constraints (topic, time range, region, sources, language, length, and angle). Use when the user asks to “检索资讯/搜集资料/查新闻/整理资料/做信息汇总/竞品动态/行业动态/政策解读/舆情摘要/日报周报” or requests a summary with sources/links.
---

# News Research & Summary

## Quick start (do this every time)

1. Clarify requirements from the user prompt; if missing, assume sensible defaults:
   - Topic + scope, time window, region/language, target audience, desired length, and what counts as “可信来源”.
   - Default time window: last 7 days unless user specifies otherwise.
   - Default output language: match the user’s language.
2. Create a search plan (3–8 queries) that covers:
   - Primary keywords + synonyms + entities (people/orgs/products).
   - Time constraint using the current year.
   - “official / announcement / press release / regulator / filing” variants when relevant.
3. Use web search to collect sources, prioritizing:
   - Primary sources (official sites, regulators, standards bodies, court docs, academic publishers).
   - Reputable secondary sources (major newsrooms, established trade press).
4. Triangulate:
   - For every key claim, confirm with ≥2 independent sources when possible.
   - If only 1 source exists, label it explicitly as “single-source”.
5. Deduplicate:
   - Merge rewrites of the same story; keep the earliest/most primary source as the lead citation.
6. Summarize with citations:
   - Every bullet that contains a factual claim must include at least one source link.
   - Use markdown links; avoid bare URLs.

## Output format (always use this template)

```markdown
## 结论摘要（<= 120 字）
<高密度结论；点出最重要的 1–3 个变化>

## 关键要点
- **要点 1**：<一句话>（[来源A](...), [来源B](...)）
- **要点 2**：<一句话>（[来源](...)）
- **要点 3**：<一句话>（[来源](...)）

## 详情（按主题/时间线）
### <主题或日期>
- <事实 + 影响/背景>（[来源](...)）

## 影响评估（可选）
- **对谁有影响**：<受影响对象>
- **可能的下一步**：<推演，标注为推测/判断，不当作事实>

## 来源清单
1. <来源标题> — <机构/媒体>（YYYY-MM-DD）[链接](...)
2. ...

## 检索说明（简短）
- **时间范围**：<用户指定或默认>
- **检索关键词**：<3–8 条>
- **筛选标准**：<例如：官方优先/英文优先/地区限制等>
```

## Quality & safety rules

- Do not invent sources or quotes.
- If dates/numbers conflict across sources, report the discrepancy and cite both.
- Separate fact vs analysis:
  - Facts: must be cited.
  - Analysis/judgment: label clearly as “分析/判断/推测”.
- Prefer direct citations to the original document over aggregator reposts.

## When requirements are underspecified (default behavior)

- If the user says “按要求检索资讯并总结” but provides no constraints:
  - Ask up to 3 targeted questions **only if** needed to avoid wrong scope.
  - Otherwise proceed with defaults (last 7 days, global, bilingual query set, 8–12 sources).

## Additional resources

- For search query patterns, source credibility heuristics, and citation practices, read [reference.md](reference.md).
- For example prompts and ideal outputs, read [examples.md](examples.md).

