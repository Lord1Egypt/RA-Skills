---
name: kb_eval_repo
description: Evaluate whether a GitHub/open-source repository is useful for the user's selected Research KB context. Use for query-page tasks asking to assess a repo's relevance, usefulness, reproducibility, setup effort, risks, or whether it is worth studying; accepts Java backend research_kb_agent_task JSON with taskType kb_query or kb_eval_repo and returns query-compatible answer/citations.
---

# Skill: kb_eval_repo

## Scope

Use this skill only when the user is asking to evaluate an open-source project, usually with a GitHub URL or `owner/repo` name, and wants a judgment such as:

- 是否对我/团队有用
- 值不值得深入
- 能不能复现
- 环境怎么配
- 风险、坑、适配成本
- 和知识库已有资料是什么关系

Do not use it for normal knowledge-base lookup, paper ingestion, file ingestion, or broad literature review.

## Input

Accept the same query-page envelope used by the Java backend:

- `protocol = research_kb_agent_task`
- `taskType = kb_query` or `kb_eval_repo`
- `kbTargets[]` contains one or two repositories
- `payload.question` is the user's natural-language request
- Optional: `payload.repoUrl`, `payload.options.writeReview`

Only read repositories listed in `kbTargets`. Do not infer or access any other repository.

## Workflow

1. Validate the task JSON.
2. Extract a GitHub repo from `payload.repoUrl`, `payload.question`, or `owner/repo` text.
3. If a GitHub repo is present, fetch public metadata, README, and common dependency/config files.
4. Read relevant Markdown pages from the selected knowledge repositories.
5. Evaluate with five dimensions:
   - relevance to the selected KB context
   - reproducibility and engineering maturity
   - activity and credibility
   - adaptation cost
   - unique value compared with KB materials
6. Give exactly one verdict:
   - `值得深入`
   - `选择性参考`
   - `暂不建议`
7. Return a query-compatible JSON result with:
   - `answer`
   - `citations`
   - `usedScopes`
   - `readPages`
   - optional `generatedPage`

If `payload.options.writeReview` is not `false`, write an evaluation report to `reviews/<repo>-开源项目评估.md` in the first selected target repository and cite it.

## Evidence Rules

- Project facts must come from GitHub metadata/README/dependency files.
- Knowledge-base comparisons must come from pages actually read.
- If no repo URL/name is provided and no related KB project can be found, ask the user to provide a GitHub URL.
- If GitHub cannot be fetched, explain the failure and still use KB evidence if enough exists.
- Do not pretend the project was actually installed or run. State that reproducibility is an initial assessment based on repository materials.

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
    "usedScopes": ["personal"],
    "readPages": [],
    "mode": "repo_evaluation",
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
