---
name: kb_literature_review
description: Produce a focused literature/knowledge review using only selected Research KB contents. Use for query-page tasks asking to write a review, synthesize a topic, compare multiple papers/projects, summarize methods, identify research gaps, or produce a source-grounded thematic survey; accepts Java backend research_kb_agent_task JSON with taskType kb_query or kb_literature_review and returns query-compatible answer/citations.
---

# Skill: kb_literature_review

## Scope

Use this skill when the user wants a cross-document synthesis from the selected personal/team knowledge bases, not a single fact lookup.

Typical triggers:

- 写一篇/一份关于 X 的综述
- 梳理知识库里关于 X 的资料
- 对比几种方法/路线
- 总结主流方法、优缺点、研究缺口
- 基于知识库内容做专项报告

Do not use it for:

- simple lookup like "有没有 X"
- one document's conclusion
- open-source repository usefulness evaluation
- ingestion or source scanning

## Input

Accept the Java backend query-page envelope:

- `protocol = research_kb_agent_task`
- `taskType = kb_query` or `kb_literature_review`
- `kbTargets[]` contains one or two repositories
- `payload.question` is the user's natural-language request
- Optional: `payload.topic`, `payload.options.writeReview`

Only read repositories listed in `kbTargets`.

## Workflow

1. Validate the task JSON.
2. Determine the review topic from `payload.topic` or `payload.question`.
3. Read repository Markdown trees and collect candidate pages, excluding `source_files/`.
4. Score candidates by topic terms, title, path, headings, and content.
5. Read a focused set of relevant pages. Prefer concept/review/summary pages before low-level archive pages.
6. If fewer than two relevant pages exist, say the knowledge base is insufficient and do not fabricate a review.
7. Generate a Chinese review with:
   - scope
   - topic overview
   - method/category map
   - comparison of strengths and limitations
   - contradictions or disagreements
   - research gaps
   - implications for the selected KB context
   - source list
8. If `payload.options.writeReview` is not `false`, write the review to `reviews/<topic>-专项综述.md` in the first selected target repository and cite it.
9. Return one query-compatible JSON result.

## Evidence Rules

- Every knowledge-base fact must come from pages actually read.
- Do not fill missing areas with general knowledge unless explicitly marked as non-KB background.
- Citations must be repository-relative `.md` paths and must not point to `source_files/`.
- The answer body should be readable as a concise executive summary; detailed source list belongs in `citations[]`.

## Output

Return only one JSON object. Do not use Markdown fences.

```json
{
  "protocol": "research_kb_agent_result",
  "protocolVersion": "1.0",
  "taskId": "...",
  "taskType": "...",
  "success": true,
  "result": {
    "answer": "...",
    "citations": [],
    "usedScopes": ["personal", "team"],
    "readPages": [],
    "mode": "literature_review",
    "generatedPage": ""
  },
  "errors": []
}
```

## Helper

Prefer the bundled deterministic helper:

```bash
python3 scripts/run_task.py --stdin
python3 scripts/run_task.py --task-json <path>
```
